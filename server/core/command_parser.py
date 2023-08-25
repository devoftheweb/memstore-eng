from typing import Any, Dict, Tuple, Optional

class CommandParser:
    def parse_command(self, command_str: str) -> Tuple[str, Dict[str, Any], Optional[int]]:
        """Parses a command string and returns the corresponding action and parameters.

        Args:
            command_str (str): The command string to parse.

        Returns:
            Tuple[str, Dict[str, Any]]: A tuple containing the action and parameters.

        Raises:
            ValueError: If the command is invalid.
        """
        parts = command_str.strip().split()
        if not parts:
            raise ValueError("Empty command")

        action = parts[0].upper()
        params = {}
        transaction_id = None
        if len(parts) >= 3 and parts[-1].isdigit():
            transaction_id = int(parts[-1])
            parts = parts[:-1]

        if action == "PUT":
            if len(parts) != 3:
                raise ValueError("PUT command requires two parameters: key and value")
            params['key'] = parts[1]
            params['value'] = parts[2]

        elif action == "GET" or action == "DEL":
            if len(parts) != 2:
                raise ValueError(f"{action} command requires one parameter: key")
            params['key'] = parts[1]

        elif action == "BEGIN":
            if len(parts) != 1:
                raise ValueError("BEGIN command takes no parameters")

        elif action not in ("START", "COMMIT", "ROLLBACK"):
            raise ValueError("Invalid command")

        return action, params, transaction_id
