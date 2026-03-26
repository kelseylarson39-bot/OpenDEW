"""
Crypto arbitrage detection using CoinGecko's free API.
No API key required. Rate limit: 10-50 calls/min on free tier.
"""
import requests
import time
from dataclasses import dataclass
from typing import Optional

COINGECKO_BASE = "https://api.coingecko.com/api/v3"

SUPPORTED_EXCHANGES = [
    "binance", "coinbase", "kraken", "bitfinex",
    "huobi", "okex", "bybit", "gate", "kucoin"
]

# Affiliate referral links — each referral earns $10–50+
AFFILIATE_LINKS = {
    "binance":  "https://www.binance.com/en/register?ref=YOUR_REF_ID",
    "coinbase": "https://coinbase.com/join/YOUR_REF_ID",
    "kraken":   "https://www.kraken.com/sign-up?referral=YOUR_REF_ID",
    "bybit":    "https://www.bybit.com/invite?ref=YOUR_REF_ID",
    "kucoin":   "https://www.kucoin.com/r/YOUR_REF_ID",
    "gate":     "https://www.gate.io/ref/YOUR_REF_ID",
    "okex":     "https://www.okx.com/join/YOUR_REF_ID",
}


@dataclass
class ArbitrageOp:
    coin: str
    coin_id: str
    buy_exchange: str
    sell_exchange: str
    buy_price: float
    sell_price: float
    spread_pct: float
    estimated_profit_100: float  # profit per $100 traded

    def to_dict(self):
        return {
            "coin": self.coin,
            "coin_id": self.coin_id,
            "buy_exchange": self.buy_exchange,
            "sell_exchange": self.sell_exchange,
            "buy_price": self.buy_price,
            "sell_price": self.sell_price,
            "spread_pct": round(self.spread_pct, 3),
            "estimated_profit_100": round(self.estimated_profit_100, 2),
            "buy_link": AFFILIATE_LINKS.get(self.buy_exchange, "#"),
            "sell_link": AFFILIATE_LINKS.get(self.sell_exchange, "#"),
        }


def get_coin_tickers(coin_id: str) -> Optional[dict]:
    """Fetch per-exchange ticker data for a coin from CoinGecko."""
    try:
        url = f"{COINGECKO_BASE}/coins/{coin_id}/tickers"
        r = requests.get(url, timeout=10, params={"include_exchange_logo": "false"})
        r.raise_for_status()
        return r.json()
    except Exception:
        return None


def get_top_coins(limit: int = 20) -> list[dict]:
    """Return top coins by market cap."""
    try:
        url = f"{COINGECKO_BASE}/coins/markets"
        params = {
            "vs_currency": "usd",
            "order": "market_cap_desc",
            "per_page": limit,
            "page": 1,
            "sparkline": "false",
        }
        r = requests.get(url, timeout=10, params=params)
        r.raise_for_status()
        return r.json()
    except Exception:
        return []


def find_arbitrage(coin_id: str, coin_symbol: str, min_spread_pct: float = 0.5) -> list[ArbitrageOp]:
    """
    Find arbitrage opportunities for a coin across exchanges.
    Typical exchange fees: 0.1% maker + 0.1% taker = ~0.2% round-trip.
    Only surfaces ops with spread > min_spread_pct to clear fees.
    """
    data = get_coin_tickers(coin_id)
    if not data:
        return []

    prices: dict[str, float] = {}
    for ticker in data.get("tickers", []):
        exchange = ticker.get("market", {}).get("identifier", "").lower()
        target = ticker.get("target", "").upper()
        # Only USD/USDT/USDC pairs for clean comparisons
        if target not in ("USD", "USDT", "USDC"):
            continue
        if exchange not in SUPPORTED_EXCHANGES:
            continue
        price = ticker.get("last")
        if price and price > 0:
            if exchange not in prices or prices[exchange] > price:
                prices[exchange] = float(price)

    if len(prices) < 2:
        return []

    ops = []
    exchanges = list(prices.keys())
    for i in range(len(exchanges)):
        for j in range(len(exchanges)):
            if i == j:
                continue
            buy_ex = exchanges[i]
            sell_ex = exchanges[j]
            buy_price = prices[buy_ex]
            sell_price = prices[sell_ex]
            spread_pct = ((sell_price - buy_price) / buy_price) * 100
            if spread_pct >= min_spread_pct:
                profit = (spread_pct / 100) * 100  # per $100 traded
                ops.append(ArbitrageOp(
                    coin=coin_symbol.upper(),
                    coin_id=coin_id,
                    buy_exchange=buy_ex,
                    sell_exchange=sell_ex,
                    buy_price=buy_price,
                    sell_price=sell_price,
                    spread_pct=spread_pct,
                    estimated_profit_100=profit,
                ))

    ops.sort(key=lambda x: x.spread_pct, reverse=True)
    return ops


def scan_top_coins(limit: int = 10, min_spread_pct: float = 0.5) -> list[dict]:
    """Scan top N coins and return all arbitrage opportunities found."""
    coins = get_top_coins(limit)
    all_ops = []
    for coin in coins:
        coin_id = coin["id"]
        coin_symbol = coin["symbol"]
        ops = find_arbitrage(coin_id, coin_symbol, min_spread_pct)
        all_ops.extend([op.to_dict() for op in ops])
        time.sleep(1.2)  # respect CoinGecko free-tier rate limit
    all_ops.sort(key=lambda x: x["spread_pct"], reverse=True)
    return all_ops
