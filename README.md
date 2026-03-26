# CryptoEdge — Free-API Income Generator

Live crypto arbitrage monitor and momentum signal dashboard.
**Zero API costs.** Income from exchange affiliate referrals.

## How the money works

| Stream | Rate | Effort |
|---|---|---|
| Exchange affiliate (Binance) | $15–50 / referral | Add your ref ID |
| Exchange affiliate (Coinbase) | $10 / referral | Add your ref ID |
| Exchange affiliate (KuCoin/Bybit) | $10–30 / referral | Add your ref ID |
| Premium signals subscription | $9–29/mo (add Stripe) | ~1 day of dev |

## Setup

```bash
pip install -r requirements.txt
python3 app.py
# → http://localhost:5000
```

## Monetize

1. Sign up as an affiliate on each exchange (free):
   - Binance: https://www.binance.com/en/activity/referral
   - Coinbase: https://www.coinbase.com/affiliates
   - KuCoin: https://www.kucoin.com/affiliate
   - Bybit: https://affiliate.bybit.com

2. Replace every `YOUR_REF_ID` in `arbitrage.py` and `signals.py` with your IDs.

3. Deploy (free tiers available):
   - Railway.app (free hobby tier)
   - Render.com (free tier)
   - Fly.io (free tier)

4. Drive traffic — Reddit (r/CryptoCurrency), Twitter/X, SEO for "crypto arbitrage tool".

## APIs used (all free, no key required)

- **CoinGecko** `/coins/markets` — prices, market cap, % changes
- **CoinGecko** `/coins/{id}/tickers` — per-exchange prices for arbitrage
- **CoinGecko** `/coins/{id}/market_chart` — historical prices for RSI

Free tier: ~10–50 calls/min. The app caches results for 5 minutes.

## Add Stripe subscriptions (optional)

```bash
pip install stripe
# Set STRIPE_KEY env var, add /subscribe route in app.py
# Gate /api/arbitrage behind session check
```
