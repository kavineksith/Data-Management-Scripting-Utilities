#!/usr/bin/env python3

import sys
import subprocess

class ValueProcessingError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class ValueRenamer:
    def __init__(self, file_path, orignal_value, modern_value):
        self.file_path = file_path
        self.original_value = orignal_value
        self.modern_value = modern_value

    def rename_files(self):
        try:
            with open(self.file_path) as f:
                for line in f.readlines():
                    source = line.strip()
                    destination = source.replace(self.original_value, self.modern_value)
                    subprocess.run(['mv', source, destination], check=True)
        except FileNotFoundError:
            raise ValueProcessingError(f"File not found: {self.file_path}. Please check file path and name.")
        except PermissionError:
            raise ValueProcessingError(f"Permission denied: Unable to open or modify {self.file_path}.")
        except subprocess.CalledProcessError as e:
            raise ValueProcessingError(f"Error occurred during file rename operation: {e}")
        except KeyboardInterrupt:
            raise ValueProcessingError("Process interrupted by user.")
        except Exception as e:
            raise ValueProcessingError(f"An unexpected error occurred: {e}")

def main():
    try:
        if len(sys.argv) != 2:
            print('Usage:\n\tpython file_renamer.py <file_path> current_value new_value')
            sys.exit(1)

        file_path, current_value, new_value = sys.argv[1]
        
        value_renamer = ValueRenamer(file_path, current_value, new_value)
        value_renamer.rename_files()

        print("File renaming completed successfully.")
    except ValueProcessingError as fpe:
        print(f"Error during file processing: {fpe}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
    sys.exit(0)
