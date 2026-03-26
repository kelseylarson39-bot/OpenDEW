"""
CryptoEdge — free-API income generator
Income streams:
  1. Exchange affiliate links  (Binance ~$15-50/referral, Coinbase $10/referral)
  2. Premium subscription tier via Stripe (add STRIPE_KEY to monetize)
  3. Optional ad slot in dashboard HTML

Run:  python3 app.py
"""
import json
import time
import threading
from flask import Flask, jsonify, render_template, request

from arbitrage import scan_top_coins
from signals import generate_signals

app = Flask(__name__)

# ── Simple in-memory cache so the free API rate limit isn't hit on every page load
_cache: dict = {
    "signals": {"data": [], "ts": 0},
    "arbitrage": {"data": [], "ts": 0},
}
CACHE_TTL = 300  # seconds


def _cached(key: str, fetch_fn, *args, **kwargs):
    entry = _cache[key]
    if time.time() - entry["ts"] > CACHE_TTL:
        entry["data"] = fetch_fn(*args, **kwargs)
        entry["ts"] = time.time()
    return entry["data"]


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/signals")
def api_signals():
    limit = min(int(request.args.get("limit", 10)), 20)
    data = _cached("signals", generate_signals, limit)
    return jsonify(data)


@app.route("/api/arbitrage")
def api_arbitrage():
    limit = min(int(request.args.get("coins", 8)), 15)
    spread = float(request.args.get("min_spread", 0.5))
    data = _cached("arbitrage", scan_top_coins, limit, spread)
    return jsonify(data)


@app.route("/api/status")
def api_status():
    return jsonify({
        "signals_cached_at": _cache["signals"]["ts"],
        "arbitrage_cached_at": _cache["arbitrage"]["ts"],
        "cache_ttl_sec": CACHE_TTL,
    })


def _background_refresh():
    """Pre-warm cache every CACHE_TTL seconds so users get fast responses."""
    while True:
        time.sleep(CACHE_TTL)
        try:
            _cache["signals"]["data"] = generate_signals(10)
            _cache["signals"]["ts"] = time.time()
            _cache["arbitrage"]["data"] = scan_top_coins(8, 0.5)
            _cache["arbitrage"]["ts"] = time.time()
        except Exception:
            pass


if __name__ == "__main__":
    t = threading.Thread(target=_background_refresh, daemon=True)
    t.start()
    app.run(host="0.0.0.0", port=5000, debug=False)
