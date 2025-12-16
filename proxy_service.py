# proxy_service.py
# Supports authenticated proxy rotation
# Stable for Selenium + Requests

import random
import logging
import requests

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# ================= CONFIG =================
# FORMAT: username:password@ip:port
PROXY_POOL = [
    # EXAMPLE (replace with your real proxies)
    # "rbzrukmm:jbmoof8iyzub@142.111.48.253:7030",

    # You can add multiple proxies here
]

TEST_URL = "https://ipv4.webshare.io/"
REQUEST_TIMEOUT = 10

# ================= INTERNAL =================
_current_proxy = None


def _parse_proxy(proxy_str: str):
    """
    Parses user:pass@ip:port
    """
    creds, address = proxy_str.split("@")
    username, password = creds.split(":")
    host, port = address.split(":")
    return username, password, host, port


# ================= PUBLIC API =================

def get_next_proxy():
    """
    Returns a random proxy from pool (string)
    """
    global _current_proxy

    if not PROXY_POOL:
        logging.warning("⚠ Proxy pool empty")
        return None

    _current_proxy = random.choice(PROXY_POOL)
    logging.info(f"🔄 Selected proxy: {_current_proxy}")
    return _current_proxy


def get_requests_proxy(proxy_str=None):
    """
    Returns proxy dict usable in requests
    """
    if not proxy_str:
        proxy_str = _current_proxy

    if not proxy_str:
        return None

    return {
        "http": f"http://{proxy_str}",
        "https": f"http://{proxy_str}"
    }


def test_proxy(proxy_str):
    """
    Tests proxy using requests only (SAFE)
    """
    try:
        proxies = get_requests_proxy(proxy_str)
        r = requests.get(TEST_URL, proxies=proxies, timeout=REQUEST_TIMEOUT)
        if r.status_code == 200:
            logging.info(f"✅ Proxy working: {proxy_str}")
            return True
    except Exception as e:
        logging.warning(f"❌ Proxy failed: {proxy_str} | {e}")
    return False


def get_working_proxy():
    """
    Rotates until a working proxy is found
    """
    random.shuffle(PROXY_POOL)

    for proxy in PROXY_POOL:
        if test_proxy(proxy):
            return proxy

    logging.error("⛔ No working proxy found")
    return None
