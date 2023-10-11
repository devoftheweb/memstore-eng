import unittest
from server.core.command_parser import CommandParser


class TestCommandParser(unittest.TestCase):

    def print_pass_message(self, cmd):
        print(f"{cmd} command - Test passed")

    def test_valid_commands(self):
        """Tests parsing valid commands."""
        parser = CommandParser()

        test_cases = [
            {"command": "BEGIN", "expected_action": "BEGIN", "expected_params": {}, "expected_transaction_id": None},
            {"command": "PUT key1 value1", "expected_action": "PUT", "expected_params": {'key': 'key1', 'value': 'value1'}, "expected_transaction_id": None},
            {"command": "GET key1", "expected_action": "GET", "expected_params": {'key': 'key1'}, "expected_transaction_id": None},
            {"command": "DEL key1", "expected_action": "DEL", "expected_params": {'key': 'key1'}, "expected_transaction_id": None},
            {"command": "COMMIT 1", "expected_action": "COMMIT", "expected_params": {}, "expected_transaction_id": 1},
            {"command": "ROLLBACK 1", "expected_action": "ROLLBACK", "expected_params": {}, "expected_transaction_id": 1},
            {"command": "SHOWALL", "expected_action": "SHOWALL", "expected_params": {}, "expected_transaction_id": None},
            {"command": "COMMITALL", "expected_action": "COMMITALL", "expected_params": {}, "expected_transaction_id": None},
        ]

        for test_case in test_cases:
            cmd = test_case["command"]
            expected_action = test_case["expected_action"]
            expected_params = test_case["expected_params"]
            expected_transaction_id = test_case["expected_transaction_id"]

            action, params, transaction_id = parser.parse_command(cmd)

            with self.subTest(cmd=cmd):
                self.addCleanup(self.print_pass_message, expected_action)
                self.assertEqual(action, expected_action)
                self.assertEqual(params, expected_params)
                self.assertEqual(transaction_id, expected_transaction_id)

    def test_invalid_commands(self):
        """Tests parsing invalid commands."""
        parser = CommandParser()

        invalid_test_cases = [
            "",
            "INVALID_COMMAND",
            "PUT key1",
            "GET",
        ]

        for cmd in invalid_test_cases:
            with self.assertRaises(ValueError):
                parser.parse_command(cmd)


if __name__ == "__main__":
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
