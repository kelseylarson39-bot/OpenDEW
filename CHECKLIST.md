# CryptoEdge Launch Checklist

## 1. Get Affiliate IDs (free, ~10 min each)

Search each exchange name + "affiliate program" in your browser.
Sign up, then copy your referral/ref ID.

- [ ] Binance — search: "Binance affiliate program"
- [ ] Coinbase — search: "Coinbase affiliate program"
- [ ] KuCoin — search: "KuCoin affiliate program"
- [ ] Bybit — search: "Bybit affiliate program"
- [ ] Gate.io — search: "Gate.io affiliate program"

## 2. Add Your IDs to the Code

Open `arbitrage.py` and `signals.py`, replace every `YOUR_REF_ID` with your actual ID.

Example in `arbitrage.py`:
```python
# Before
"binance": "https://www.binance.com/en/register?ref=YOUR_REF_ID",

# After
"binance": "https://www.binance.com/en/register?ref=ABC123XYZ",
```

There are 7 occurrences total across both files.

## 3. Deploy (free)

Pick one hosting platform, search its name to find the signup page:

- **Railway** — search: "Railway app deploy Python"
- **Render** — search: "Render deploy Python Flask"
- **Fly.io** — search: "Fly.io deploy Python"

All support free tiers. Run command on the platform: `python3 app.py`

## 4. Drive Traffic

- Post your live URL in crypto subreddits (e.g. r/CryptoCurrency)
- Share in crypto Discord servers
- Post on Twitter/X with hashtags like #crypto #arbitrage

## 5. Optional: Add Paid Subscriptions

Run this when ready:
```bash
pip install stripe
```
Then ask Claude to add a Stripe subscription gate to `/api/arbitrage`.

---

## Income Potential

| Action | Estimated Earnings |
|---|---|
| 1 Binance referral | $15–50 |
| 1 Coinbase referral | $10 |
| 1 KuCoin/Bybit referral | $10–30 |
| 100 visitors/day × 2% conversion | $20–100/day |
