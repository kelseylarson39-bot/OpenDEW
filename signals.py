"""
Simple momentum & RSI signals using CoinGecko's free market chart endpoint.
No API key required.
"""
import requests
from dataclasses import dataclass

COINGECKO_BASE = "https://api.coingecko.com/api/v3"


@dataclass
class Signal:
    coin: str
    coin_id: str
    price: float
    change_24h: float
    change_7d: float
    rsi_14: float
    signal: str   # BUY / SELL / HOLD
    reason: str
    affiliate_link: str

    def to_dict(self):
        return self.__dict__


def _rsi(prices: list[float], period: int = 14) -> float:
    if len(prices) < period + 1:
        return 50.0
    gains, losses = [], []
    for i in range(1, period + 1):
        delta = prices[-i] - prices[-(i + 1)]
        (gains if delta > 0 else losses).append(abs(delta))
    avg_gain = sum(gains) / period if gains else 0
    avg_loss = sum(losses) / period if losses else 0
    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))


def get_ohlc(coin_id: str, days: int = 30) -> list[float]:
    """Return daily closing prices for a coin."""
    try:
        url = f"{COINGECKO_BASE}/coins/{coin_id}/market_chart"
        r = requests.get(url, timeout=10, params={
            "vs_currency": "usd",
            "days": days,
            "interval": "daily",
        })
        r.raise_for_status()
        data = r.json()
        return [p[1] for p in data.get("prices", [])]
    except Exception:
        return []


def get_market_overview(limit: int = 15) -> list[dict]:
    """Return top coins with price, 24h/7d change and volume."""
    try:
        url = f"{COINGECKO_BASE}/coins/markets"
        r = requests.get(url, timeout=10, params={
            "vs_currency": "usd",
            "order": "market_cap_desc",
            "per_page": limit,
            "page": 1,
            "sparkline": "false",
            "price_change_percentage": "24h,7d",
        })
        r.raise_for_status()
        return r.json()
    except Exception:
        return []


AFFILIATE_LINKS = {
    "bitcoin":   "https://www.coinbase.com/join/YOUR_REF_ID",
    "ethereum":  "https://www.coinbase.com/join/YOUR_REF_ID",
    "default":   "https://www.binance.com/en/register?ref=YOUR_REF_ID",
}


def generate_signals(limit: int = 10) -> list[dict]:
    """Generate BUY/SELL/HOLD signals for top coins."""
    coins = get_market_overview(limit)
    results = []
    for coin in coins:
        coin_id = coin["id"]
        prices = get_ohlc(coin_id, days=20)
        rsi = _rsi(prices) if prices else 50.0
        price = coin.get("current_price", 0)
        change_24h = coin.get("price_change_percentage_24h") or 0
        change_7d = coin.get("price_change_percentage_7d_in_currency") or 0

        if rsi < 30 and change_24h < -3:
            signal, reason = "BUY", f"RSI oversold ({rsi:.1f}) + 24h dip ({change_24h:.1f}%)"
        elif rsi > 70 and change_24h > 5:
            signal, reason = "SELL", f"RSI overbought ({rsi:.1f}) + 24h surge ({change_24h:.1f}%)"
        elif change_7d > 15 and rsi < 60:
            signal, reason = "BUY", f"Strong 7d momentum ({change_7d:.1f}%) with room to run"
        elif change_7d < -20 and rsi > 40:
            signal, reason = "SELL", f"Weak 7d trend ({change_7d:.1f}%)"
        else:
            signal, reason = "HOLD", f"No clear edge (RSI {rsi:.1f})"

        link = AFFILIATE_LINKS.get(coin_id, AFFILIATE_LINKS["default"])
        results.append(Signal(
            coin=coin["symbol"].upper(),
            coin_id=coin_id,
            price=price,
            change_24h=round(change_24h, 2),
            change_7d=round(change_7d, 2),
            rsi_14=round(rsi, 1),
            signal=signal,
            reason=reason,
            affiliate_link=link,
        ).to_dict())

    return results
