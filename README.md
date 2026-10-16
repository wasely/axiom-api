# axiom-api

**From [BLIX](https://blixvip.com) · [Explore the Solana trading terminal →](https://blixvip.com)**

**Inspect Solana wallet activity from Python.**

![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-3776AB?style=flat-square&logo=python&logoColor=white) ![Dependencies: standard library](https://img.shields.io/badge/dependencies-standard_library-334155?style=flat-square) ![Mode: read only](https://img.shields.io/badge/mode-read_only-0F766E?style=flat-square)

A small, read-only companion for Axiom Trade users who want to inspect a known public wallet address through Solana JSON-RPC.

[Quick start](#quick-start) · [Examples](docs/examples.md) · [Python usage](#use-from-python) · [FAQ](#frequently-asked-questions)

Independent, unofficial companion tool. This is **not an Axiom Trade API client** and does not connect to Axiom accounts, execute orders, discover wallets by username, or calculate trading P&L. It calls Solana JSON-RPC directly. Not affiliated with Axiom Trade or Axiom.co.

## Quick start

Requires Python 3.11 or newer and Git. Uses only the Python standard library; no pip install or API key is required for the public RPC endpoint.

```sh
git clone https://github.com/wasely/axiom-api.git
cd axiom-api
python activity.py Vote111111111111111111111111111111111111111 --limit 5
```

The included addresses are public program/mint examples, not personal wallets. Replace them with the addresses you want to inspect.

## At a glance

| Task | Command |
| --- | --- |
| Inspect recent activity | `python activity.py ADDRESS --limit 20` |
| Fetch an older page | `python activity.py ADDRESS --before SIGNATURE` |
| Import into a script | `from activity import activity` |

Replace uppercase placeholders with actual addresses or signatures.

## Example output

Illustrative response, shortened from a devnet read. The signature is a placeholder; actual signatures and slots vary.

```json
{
  "address": "Vote111111111111111111111111111111111111111",
  "transactions": [
    {
      "signature": "<transaction signature>",
      "slot": 511552880,
      "blockTime": 1792116001,
      "confirmationStatus": "finalized",
      "err": null,
      "memo": null
    }
  ]
}
```

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

## Frequently asked questions

### Is this an official Axiom API or SDK?

No. It is an independent tool for reading public Solana activity. It does not call Axiom Trade endpoints and is unrelated to the Axiom.co observability API.

### Do I need an Axiom API key?

No. This tool uses a Solana RPC endpoint. Public endpoints require no key; a private RPC provider may require one in its URL.

### Does this identify trades or show profit and loss?

No. It lists transactions that reference the supplied address. Decoding swaps, attributing trades, and computing P&L require additional data and logic.

## Related tools

| Repository | Use it for |
| --- | --- |
| [axiom-api](https://github.com/wasely/axiom-api) | Recent Solana wallet transaction signatures |
| [fomo-api](https://github.com/wasely/fomo-api) | Native SOL balance snapshots for a watchlist |
| [solana-api](https://github.com/wasely/solana-api) | RPC health, balances, and token supply |

Each project is an independent, read-only tool. Axiom and Fomo accounts are not connected.

## References

- [Solana getSignaturesForAddress](https://solana.com/docs/rpc/http/getsignaturesforaddress)
- [Official Axiom Trade documentation](https://docs.axiom.trade/)
