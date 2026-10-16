"""Read recent Solana address activity without signing transactions."""
import argparse
import json
from rpc import RpcError, rpc, validate_address


def activity(address, limit=20, before=None):
    validate_address(address)
    if not 1 <= limit <= 100:
        raise ValueError("Limit must be between 1 and 100.")
    options = {"commitment": "confirmed", "limit": limit}
    if before:
        options["before"] = before
    return {"address": address,
            "transactions": rpc("getSignaturesForAddress", [address, options])}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("address", help="Public Solana wallet address")
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--before", help="Transaction signature for the next page")
    args = parser.parse_args()
    try:
        print(json.dumps(activity(args.address, args.limit, args.before), indent=2))
    except (ValueError, RpcError) as exc:
        parser.exit(1, f"Error: {exc}\n")


if __name__ == "__main__":
    main()
