import io
import json
import unittest
from unittest.mock import patch
from urllib.error import HTTPError, URLError
from rpc import RpcError, rpc, validate_address, sol

ADDRESS = "11111111111111111111111111111111"

class RpcTests(unittest.TestCase):
    def test_preserves_integer_precision_and_formats_sol(self):
        self.assertEqual(sol(1234567891), "1.234567891")
        self.assertEqual(sol(1), "0.000000001")

    def test_validates_decoded_address_length(self):
        self.assertEqual(validate_address(ADDRESS), ADDRESS)
        for value in ("0" * 32, "1" * 31, "1" * 33, ""):
            with self.assertRaises(ValueError):
                validate_address(value)

    @patch("rpc.urlopen")
    def test_sends_json_rpc_and_reads_result(self, request):
        request.return_value.__enter__.return_value = io.BytesIO(
            b'{"jsonrpc":"2.0","id":1,"result":{"value":42}}')
        self.assertEqual(rpc("getBalance", [ADDRESS]), {"value": 42})
        sent = request.call_args.args[0]
        self.assertEqual(json.loads(sent.data)["params"], [ADDRESS])
        self.assertEqual(request.call_args.kwargs["timeout"], 15)

    @patch("rpc.urlopen")
    def test_surfaces_rpc_errors_without_echoing_provider_secrets(self, request):
        request.return_value.__enter__.return_value = io.BytesIO(
            b'{"jsonrpc":"2.0","id":1,"error":{"code":-32602,"message":"secret"}}')
        with self.assertRaisesRegex(RpcError, "RPC error -32602") as error:
            rpc("getBalance")
        self.assertNotIn("secret", str(error.exception))

    @patch("rpc.urlopen")
    def test_rejects_malformed_responses(self, request):
        for payload in (b"html", b"[]", b'{"result":1}', b'{"jsonrpc":"2.0","id":2,"result":1}'):
            request.return_value.__enter__.return_value = io.BytesIO(payload)
            with self.assertRaises(RpcError):
                rpc("getBalance")

    @patch("rpc.urlopen")
    def test_http_and_network_failures_are_actionable(self, request):
        request.side_effect = HTTPError("https://example.com?secret=abc", 429, "rate limit", {}, None)
        with self.assertRaisesRegex(RpcError, "429") as error:
            rpc("getBalance")
        self.assertNotIn("abc", str(error.exception))
        request.side_effect = URLError("secret=abc")
        with self.assertRaisesRegex(RpcError, "network"):
            rpc("getBalance")

    def test_rejects_non_http_endpoint(self):
        with self.assertRaises(ValueError):
            rpc("getBalance", endpoint="file:///tmp/test")

from activity import activity

class ActivityTests(unittest.TestCase):
    @patch("activity.rpc")
    def test_keeps_failed_and_pending_transactions(self, request):
        rows = [{"signature":"test","err":{"InstructionError":[0,"failed"]},"blockTime":None}]
        request.return_value = rows
        result = activity(ADDRESS, limit=5, before="cursor")
        self.assertEqual(result["transactions"], rows)
        self.assertEqual(request.call_args.args[1][1]["before"], "cursor")

    @patch("activity.rpc")
    def test_rejects_invalid_limits_before_network(self, request):
        for limit in (0, 101):
            with self.assertRaises(ValueError):
                activity(ADDRESS, limit=limit)
        request.assert_not_called()

    @patch("activity.rpc", return_value=[])
    def test_empty_history(self, request):
        self.assertEqual(activity(ADDRESS)["transactions"], [])

if __name__ == "__main__":
    unittest.main()
