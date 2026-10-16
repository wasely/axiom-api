# axiom-api — Solana wallet activity for Axiom Trade users

Read recent on-chain transaction signatures for a public Solana wallet. Useful when inspecting a wallet address you already know from Axiom Trade.

Independent, unofficial companion tool. This is **not an Axiom Trade API client** and does not connect to Axiom accounts, execute orders, discover wallets by username, or calculate trading P&L. It calls Solana JSON-RPC directly. Not affiliated with Axiom Trade or Axiom.co.

## Quick start

Requires Python 3.11 or newer and Git. Uses only the Python standard library; no pip install or API key is required for the public RPC endpoint.

```sh
git clone https://github.com/wasely/axiom-api.git
cd axiom-api
python activity.py Vote111111111111111111111111111111111111111 --limit 5
```

The included addresses are public program/mint examples, not personal wallets. Replace them with the addresses you want to inspect.

## What it does

- JSON output with signatures, slots, timestamps, confirmation status, and transaction errors.
- `--limit` accepts 1–100 results; `--before SIGNATURE` fetches an older page.
- Failed transactions and null timestamps remain visible.

## Choose a cluster or RPC provider

Defaults to Solana mainnet at `https://api.mainnet-beta.solana.com`.
Use `SOLANA_RPC_URL` for devnet or your own provider.

PowerShell:

```powershell
$env:SOLANA_RPC_URL = "https://api.devnet.solana.com"
```

macOS / Linux:

```sh
export SOLANA_RPC_URL="https://api.devnet.solana.com"
```

Run the quick-start commands after setting the variable. Devnet and mainnet have separate data. Public endpoints may return HTTP 403 or 429; wait before retrying or configure your own RPC provider. Requests time out after 15 seconds. The tool does not automatically retry.

Provider URLs can contain API keys. Keep them in your local environment, not in commits. These scripts do not load `.env` files automatically. They never need a seed phrase or private key.

## Use from Python

Run from this repository directory:

```python
from activity import activity

result = activity("Vote111111111111111111111111111111111111111", limit=5)
print(result["transactions"])
```

## Limits

Transactions are newest first. A signature means the address was referenced by a transaction; it does not prove the wallet made a trade. Token-account activity may require querying the token account separately. This tool does not decode swaps or identify buys and sells.

Reads use confirmed commitment, so recent data can change. Address validation checks base58 and decoded length; it does not prove an account exists. The transport reports HTTP, network, JSON, and JSON-RPC errors without echoing provider response text or URLs.

## Tests

```sh
python -m unittest discover -v
```

Ten offline tests cover the tool's behavior, address validation, exact balance formatting, malformed JSON-RPC responses, and HTTP/network errors. Live read-only examples were also checked against Solana devnet on 2026-10-15. Live results change and are not part of the offline test suite.

## References

- [Solana getSignaturesForAddress](https://solana.com/docs/rpc/http/getsignaturesforaddress)
- [Official Axiom Trade documentation](https://docs.axiom.trade/)
