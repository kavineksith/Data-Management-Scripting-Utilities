import csv
import sys

class DataProcessingError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class DataHandler:
    def __init__(self, filename):
        self.filename = filename
        self.data_dict = {}

    def load_data(self):
        try:
            with open(self.filename) as csvfile:
                lines = csv.reader(csvfile, delimiter=',')
                for row in lines:
                    name = str(row[0].lower())
                    self.data_dict[name] = row[1]
        except PermissionError:
            raise DataProcessingError(f"Permission denied: Unable to open {self.filename}. Please check file permissions.")
        except FileNotFoundError:
            raise DataProcessingError(f"File not found: {self.filename}. Please check file path and name.")
        except Exception as e:
            raise DataProcessingError(f"An error occurred while loading data: {e}")

    def find_data_entry(self, first_name, last_name):
        try:
            fullname = f'{first_name} {last_name}'
            if fullname.lower() in self.data_dict:
                return self.data_dict[fullname.lower()]
            else:
                return None
        except KeyboardInterrupt:
            raise DataProcessingError("Process interrupted by the user.")
        except Exception as e:
            raise DataProcessingError(f"An error occurred while finding data: {e}")

def main():
    if len(sys.argv) != 4:
        print('Example:\n\tpython data_processor.py ./data.csv \'first_name\' \'last_name\'')
        sys.exit(1)

    data_source_file, first_name, last_name = sys.argv[1:]
    
    try:
        data_handler = DataHandler(data_source_file)
        data_handler.load_data()
        data_entry = data_handler.find_data_entry(first_name, last_name)
        
        if data_entry:
            print(f"Data entry found: {data_entry}")
        else:
            print("No data entry found")
    except DataProcessingError as dpe:
        print(f"Error: {dpe}")
    except KeyboardInterrupt:
        print("Process interrupted by the user.")
    except Exception as e:
        print(f'An error occurred: {e}')

if __name__ == "__main__":
    main()
    sys.exit(0)
