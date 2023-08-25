import unittest
from server.core.command_parser import CommandParser


class TestCommandParser(unittest.TestCase):

    def test_valid_commands(self):
        """Tests parsing valid commands."""
        parser = CommandParser()

        # Testing BEGIN command
        action, params, transaction_id = parser.parse_command("BEGIN")
        self.assertEqual(action, "BEGIN")
        self.assertEqual(params, {})
        self.assertIsNone(transaction_id)

        # Testing START command
        action, params, transaction_id = parser.parse_command("START")
        self.assertEqual(action, "START")
        self.assertEqual(params, {})
        self.assertIsNone(transaction_id)

        # Testing PUT command
        action, params, transaction_id = parser.parse_command("PUT key1 value1")
        self.assertEqual(action, "PUT")
        self.assertEqual(params, {'key': 'key1', 'value': 'value1'})
        self.assertIsNone(transaction_id)

        # Testing GET command
        action, params, transaction_id = parser.parse_command("GET key1")
        self.assertEqual(action, "GET")
        self.assertEqual(params, {'key': 'key1'})
        self.assertIsNone(transaction_id)

        # Testing DEL command
        action, params, transaction_id = parser.parse_command("DEL key1")
        self.assertEqual(action, "DEL")
        self.assertEqual(params, {'key': 'key1'})
        self.assertIsNone(transaction_id)

        # Testing COMMIT command
        action, params, transaction_id = parser.parse_command("COMMIT")
        self.assertEqual(action, "COMMIT")
        self.assertEqual(params, {})
        self.assertIsNone(transaction_id)

        # Testing ROLLBACK command
        action, params, transaction_id = parser.parse_command("ROLLBACK")
        self.assertEqual(action, "ROLLBACK")
        self.assertEqual(params, {})
        self.assertIsNone(transaction_id)

    def test_invalid_commands(self):
        """Tests parsing invalid commands."""
        parser = CommandParser()

        with self.assertRaises(ValueError):
            parser.parse_command("")

        with self.assertRaises(ValueError):
            parser.parse_command("INVALID_COMMAND")

        with self.assertRaises(ValueError):
            parser.parse_command("PUT key1")

        with self.assertRaises(ValueError):
            parser.parse_command("GET")


if __name__ == "__main__":
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
