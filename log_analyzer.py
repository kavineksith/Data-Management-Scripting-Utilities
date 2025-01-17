from pathlib import Path
import sys
import re

class LogFileException(Exception):
    def __init__(self, message):
        # Initialize the custom exception with a message
        self.message = message
        super().__init__(self.message)

class LogAnalyzer:
    def __init__(self, log_file):
        # Initialize the LogAnalyzer with the log file path
        self.log_file = log_file

    def search_log_data(self, log_level):
        try:
            # Define regex patterns for each log level
            level_patterns = {
                'ERROR': r'ERROR',
                'INFO': r'INFO',
                'WARN': r'WARN'
            }
            
            # Get the regex pattern for the specified log level
            log_level_pattern = level_patterns.get(log_level.upper(), '')
            if not log_level_pattern:
                raise ValueError(f"Unsupported log level: {log_level}")

            analyzed_log_data = []
            # Open the log file for reading
            with open(f'./{self.log_file}.log', mode='r', encoding='UTF-8') as file:
                for line in file:
                    # Check if the line matches the log level pattern
                    if re.search(log_level_pattern, line):
                        # Prepare search patterns by escaping special characters
                        search_patterns = [re.escape(word.lower()) for word in log_level.split()]
                        # Check if all search patterns are present in the line
                        if all(re.search(pattern, line.lower()) for pattern in search_patterns):
                            analyzed_log_data.append(line)
            return analyzed_log_data
        except PermissionError:
            raise LogFileException(f"Can't open {self.log_file}. Please check file permissions.")
        except FileNotFoundError:
            raise LogFileException(f"Can't find {self.log_file}. Please check file path and name.")
        except KeyboardInterrupt:
            # Handle keyboard interrupt gracefully
            print("Process interrupted by the user.")
            sys.exit(1)
        except Exception as e:
            # Handle any other exceptions
            raise LogFileException(f"An error occurred: {e}")

    def export_filtered_log_data(self, filtered_log_data, export_file):
        try:
            # Open the export file for appending data
            with open(f'./{export_file}.log', 'a', encoding='UTF-8') as file:
                for log_data in filtered_log_data:
                    file.write(log_data)
        except PermissionError:
            raise LogFileException(f"Can't open {export_file}. Please check file permissions.")
        except FileExistsError:
            raise LogFileException(f"Can't create {export_file}. {export_file} already exists.")
        except FileNotFoundError:
            raise LogFileException(f"Can't find {export_file}. Please check file path and name.")
        except KeyboardInterrupt:
            # Handle keyboard interrupt gracefully
            print("Process interrupted by the user.")
            sys.exit(1)
        except Exception as e:
            # Handle any other exceptions
            raise LogFileException(f"An error occurred: {e}")

def user_input_sanitization(user_parameters):
    # Convert user input to lowercase and strip any leading/trailing whitespace
    return user_parameters.lower().strip()

def main():
    # Ensure the correct number of command-line arguments are provided
    if len(sys.argv) != 4:
        print('Example:\n\tpython log_analyzer.py log_level log_file export_file')
        sys.exit(1)

    log_level_paramter, log_file, export_file = sys.argv[1:]
    # Sanitize input parameters
    # search_text = user_input_sanitization(search_parameter)
    log_level = user_input_sanitization(log_level_paramter).upper()

    # Validate log level
    if log_level not in ['ERROR', 'INFO', 'WARN']:
        print('Operation terminated...!!')
        sys.exit(1)

    try:
        # Create an instance of LogAnalyzer with the provided log file
        analyzer = LogAnalyzer(Path(log_file))
        # Search log data based on parameters and log level
        filtered_output = analyzer.search_log_data(log_level)
        # Export the filtered log data to the specified file
        analyzer.export_filtered_log_data(filtered_output, Path(export_file))
        print(f"Filtered log data exported to {export_file}.log successfully.")
    except LogFileException as lfe:
        # Print custom error messages for log file exceptions
        print(f"Error: {lfe.message}")
    except KeyboardInterrupt:
        # Handle keyboard interrupt gracefully
        print("Process interrupted by the user.")
    except Exception as e:
        # Print generic error messages for any other exceptions
        print(f'An error occurred: {e}')

if __name__ == "__main__":
    # Run the main function if this script is executed
    main()
    sys.exit(0)
