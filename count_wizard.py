import csv
import json
import sys

class DataProcessingError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class EmployeeDataProcessor:
    def __init__(self, source_file, dest_file):
        self.source_file = source_file
        self.dest_file = dest_file

    def read_employee_data(self):
        try:
            csv.register_dialect('empDialect', skipinitialspace=True, strict=True)
            with open(self.source_file) as csvfile:
                employee_file = csv.DictReader(csvfile, dialect='empDialect')
                employee_list = [data for data in employee_file]
            return employee_list
        except PermissionError:
            raise DataProcessingError(f"Permission denied: Unable to open {self.source_file}. Please check file permissions.")
        except FileNotFoundError:
            raise DataProcessingError(f"File not found: {self.source_file}. Please check file path and name.")
        except KeyboardInterrupt:
            raise DataProcessingError("Process interrupted by user.")
        except Exception as e:
            raise DataProcessingError(f"An error occurred while reading employee data: {e}")

    def process_employee_data(self, employee_list):
        try:
            department_list = [employee_data['Department'] for employee_data in employee_list]
            department_data = {department_name: department_list.count(department_name) for department_name in set(department_list)}
            return department_data
        except KeyboardInterrupt:
            raise DataProcessingError("Process interrupted by user.")
        except Exception as e:
            raise DataProcessingError(f"An error occurred while processing employee data: {e}")

    def save_to_json(self, result):
        try:
            with open(self.dest_file, 'w', encoding='utf-8') as json_file:
                json.dump(result, json_file, indent=4, ensure_ascii=False)
        except PermissionError:
            raise DataProcessingError(f"Permission denied: Unable to create {self.dest_file}. Please check file permissions.")
        except FileExistsError:
            raise DataProcessingError(f"File already exists: {self.dest_file}. Cannot overwrite existing file.")
        except FileNotFoundError:
            raise DataProcessingError(f"File not found: {self.dest_file}. Please check file path and name.")
        except KeyboardInterrupt:
            raise DataProcessingError("Process interrupted by user.")
        except Exception as e:
            raise DataProcessingError(f"An error occurred while saving data to JSON: {e}")

def main():
    try:
        if len(sys.argv) != 3:
            print('Example:\n\tpython data_processor.py ./data.csv ./report.json')
            sys.exit(1)

        data_file, save_file = sys.argv[1:]
        
        data_processor = EmployeeDataProcessor(data_file, save_file)
        employee_list = data_processor.read_employee_data()
        employee_dict = data_processor.process_employee_data(employee_list)
        
        data_processor.save_to_json(employee_dict)

        print(f'Expected Output:\n{json.dumps(employee_dict, indent=4)}')

    except KeyboardInterrupt:
        print('Process interrupted by user.')
        sys.exit(1)
    except DataProcessingError as dpe:
        print(f'Error: {dpe}')
        sys.exit(1)
    except Exception as e:
        print(f'An unexpected error occurred: {e}')
        sys.exit(1)

if __name__ == "__main__":
    main()
    sys.exit(0)
