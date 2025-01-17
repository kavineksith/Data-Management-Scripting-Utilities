#!/usr/bin/env python3

class FileProcessingError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class CharacterFrequencyCounter:
    def __init__(self, filename):
        self.filename = filename

    def count_character_frequency(self):
        try:
            with open(self.filename) as f:
                characters = {}
                for line in f:
                    for char in line:
                        characters[char] = characters.get(char, 0) + 1
        except FileNotFoundError:
            raise FileProcessingError(f"File not found: {self.filename}. Please check file path and name.")
        except PermissionError:
            raise FileProcessingError(f"Permission denied: Unable to open {self.filename}.")
        except OSError as e:
            raise FileProcessingError(f"Error opening file {self.filename}: {e}")
        except Exception as e:
            raise FileProcessingError(f"An unexpected error occurred: {e}")
        
        return characters

def main():
    try:
        if len(sys.argv) != 2:
            print('Usage:\n\tpython character_frequency.py <file_path>')
            sys.exit(1)

        filename = sys.argv[1]
        
        frequency_counter = CharacterFrequencyCounter(filename)
        character_frequency = frequency_counter.count_character_frequency()

        if character_frequency is None:
            print(f"Failed to process file: {filename}")
        else:
            print("Character frequency:")
            for char, count in character_frequency.items():
                print(f"{char}: {count}")

    except FileProcessingError as fpe:
        print(f"Error during file processing: {fpe}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    import sys
    main()
    sys.exit(0)
