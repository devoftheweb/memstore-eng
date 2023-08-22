import unittest
from server.command_parser import CommandParser


class TestCommandParser(unittest.TestCase):

    def test_valid_commands(self):
        """Tests parsing valid commands."""
        parser = CommandParser()

        # Testing START command
        action, params = parser.parse_command("START")
        self.assertEqual(action, "START")
        self.assertEqual(params, {})

        # Testing PUT command
        action, params = parser.parse_command("PUT key1 value1")
        self.assertEqual(action, "PUT")
        self.assertEqual(params, {'key': 'key1', 'value': 'value1'})

        # Testing GET command
        action, params = parser.parse_command("GET key1")
        self.assertEqual(action, "GET")
        self.assertEqual(params, {'key': 'key1'})

        # Testing DEL command
        action, params = parser.parse_command("DEL key1")
        self.assertEqual(action, "DEL")
        self.assertEqual(params, {'key': 'key1'})

        # Testing COMMIT command
        action, params = parser.parse_command("COMMIT")
        self.assertEqual(action, "COMMIT")
        self.assertEqual(params, {})

        # Testing ROLLBACK command
        action, params = parser.parse_command("ROLLBACK")
        self.assertEqual(action, "ROLLBACK")
        self.assertEqual(params, {})

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
