# Read Solana wallet transaction history

Use a known public wallet address. The Vote program address below is a repeatable example, not a trader wallet.

## Read the latest page

```sh
python activity.py Vote111111111111111111111111111111111111111 --limit 5
```

The `transactions` list is newest first. `err: null` means the transaction did not report an execution error. A null `blockTime` means the RPC did not provide a timestamp.

## Fetch older results

Copy the final entry's actual `signature` into `--before`:

```sh
python activity.py ADDRESS --limit 20 --before SIGNATURE
```

`ADDRESS` and `SIGNATURE` are placeholders. Pagination uses an exclusive cursor. Stop when the returned list is empty. Providers can have different historical coverage.

## Save JSON

```sh
python activity.py ADDRESS --limit 20 > activity.local.json
```

A failed command exits nonzero; do not treat an empty output file as an empty history. `*.local.json` files are ignored by Git.

## Interpret carefully

An address can appear in a transaction without initiating it. SPL token activity may reference a token account rather than the wallet itself. This script does not retrieve transaction details or decode swaps.

[Back to README](../README.md)
