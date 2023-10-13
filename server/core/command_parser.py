from typing import Any, Dict, Tuple, Optional


class CommandParser:
    def parse_command(self, command_str: str) -> Tuple[str, Dict[str, Any], Optional[int]]:
        """
        Parses a command string and returns the corresponding action and parameters.

        Args:
            command_str (str): The command string to parse.

        Returns:
            Tuple[str, Dict[str, Any], Optional[int]]: A tuple containing the action, parameters, and optional transaction ID.

        Raises:
            ValueError: If the command is invalid.
        """

        # Split the command string into parts
        parts = command_str.strip().split()

        # If the command string is empty, raise an error
        if not parts:
            raise ValueError("Empty command")

        # Convert action part to upper case for uniformity
        action = parts[0].upper()
        # Initialize parameters and transaction ID
        params = {}
        transaction_id = None

        # Check for an optional transaction ID at the end of the command
        if len(parts) >= 3 and parts[-1].isdigit():
            transaction_id = int(parts[-1])
            parts = parts[:-1]

        # PUT command
        if action == "PUT":
            if len(parts) != 3:
                raise ValueError("PUT command requires two parameters: key and value")
            params['key'] = parts[1]
            params['value'] = parts[2]

        # GET and DEL commands
        elif action == "GET" or action == "DEL":
            if len(parts) != 2:
                raise ValueError(f"{action} command requires one parameter: key")
            params['key'] = parts[1]

        # BEGIN command
        elif action == "BEGIN":
            if len(parts) != 1:
                raise ValueError("BEGIN command takes no parameters")

        # SHOWALL command
        elif action == "SHOWALL":
            if len(parts) != 1:
                raise ValueError("SHOWALL command takes no parameters")

        # COMMITALL command
        elif action == "COMMITALL":
            if len(parts) != 1:
                raise ValueError("COMMIT ALL command takes no parameters")

        # COMMIT and ROLLBACK commands
        elif action in ("COMMIT", "ROLLBACK"):
            if len(parts) != 2 or not parts[1].isdigit():
                raise ValueError(f"{action} command requires a transaction ID")
            transaction_id = int(parts[1])

        # invalid commands
        else:
            raise ValueError("Invalid command")

        return action, params, transaction_id
