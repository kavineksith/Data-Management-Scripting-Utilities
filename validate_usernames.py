import re

class UsernameValidationException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class UsernameValidator:
    def __init__(self, min_length=1):
        self.min_length = min_length

    def validate(self, username):
        try:
            self._check_type(username)
            self._check_length(username)
            self._check_characters(username)
            self._check_start(username)
            self._check_numeric_start(username)
            return True
        except UsernameValidationException as e:
            raise e

    def _check_type(self, username):
        if not isinstance(username, str):
            raise UsernameValidationException("Username must be a string.")

    def _check_length(self, username):
        if len(username) < self.min_length:
            raise UsernameValidationException(f"Usernames can't be shorter than {self.min_length}.")

    def _check_characters(self, username):
        if not re.match('^[a-zA-Z0-9._]*$', username):
            raise UsernameValidationException("Usernames can only use letters, numbers, dots, and underscores.")

    def _check_start(self, username):
        if username.startswith('.') or username.startswith('_'):
            raise UsernameValidationException("Usernames can't begin with dots and underscores.")

    def _check_numeric_start(self, username):
        if username[0].isdigit():
            raise UsernameValidationException("Username can't begin with a number.")

def get_an_username():
    validator = UsernameValidator(min_length=1)
    try:
        while True:
            user_name = input("What's your username? ").strip()
            if validator.validate(user_name):
                print(f"Username '{user_name}' is valid!")
                break
    except UsernameValidationException as e:
        print(f"Validation error: {e}")
    except KeyboardInterrupt:
        print("\nProcess interrupted by the user.")

if __name__ == "__main__":
    get_an_username()
