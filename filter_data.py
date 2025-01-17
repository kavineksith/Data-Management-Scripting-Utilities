import csv
import datetime
import sys

class DateRangeException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class DateRangeValidator:
    def __init__(self, start_date_str, end_date_str):
        self.start_date = self._parse_date(start_date_str)
        self.end_date = self._parse_date(end_date_str)

    def _parse_date(self, date_str):
        try:
            year, month, day = map(int, date_str.strip().split('-'))
            return datetime.datetime(year, month, day)
        except ValueError:
            raise DateRangeException(f"Invalid date format: {date_str}. Please use YYYY-MM-DD.")

    def get_date_range(self):
        if self.start_date > self.end_date:
            raise DateRangeException("Start date cannot be after end date.")
        return self.start_date, self.end_date

class EmployeeDataProcessor:
    def __init__(self, source_file):
        self.source_file = source_file

    def get_employee_data(self):
        try:
            with open(self.source_file, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                data_list = list(reader)
                return data_list
        except PermissionError:
            raise DateRangeException(f"Can't open {self.source_file}. Please check file permissions.")
        except FileNotFoundError:
            raise DateRangeException(f"Can't find {self.source_file}. Please check file path and name.")

    def list_newer_employees(self, start_date, end_date):
        data = self.get_employee_data()
        data.sort(key=lambda x: datetime.datetime.strptime(x[3], '%Y-%m-%d'))

        current_date = start_date
        while current_date <= end_date:
            current_date, employees = self.get_same_or_newer(data, current_date, end_date)
            if current_date <= end_date:
                print(f"Started on {current_date.strftime('%b %d, %Y')}: {employees}")
                current_date += datetime.timedelta(days=1)

    def get_same_or_newer(self, data, start_date, end_date):
        min_date = end_date
        min_date_employees = []

        for column in data:
            if column[3] == 'Start Date':  # Skip header column
                continue
            
            column_date = datetime.datetime.strptime(column[3], '%Y-%m-%d')

            if column_date < start_date:
                continue

            if column_date < min_date:
                min_date = column_date
                min_date_employees = []

            if column_date == min_date:
                min_date_employees.append(f"{column[0]} {column[1]}")

        return min_date, min_date_employees

def main():
    if len(sys.argv) != 4:
        print('Example:\n\tpython filter_data.py ./data.csv \'start_date\' \'end_date\'')
        sys.exit(1)

    source_file, start_day, end_day = sys.argv[1:]

    try:
        date_validator = DateRangeValidator(start_day, end_day)
        start_date, end_date = date_validator.get_date_range()

        processor = EmployeeDataProcessor(source_file)
        processor.list_newer_employees(start_date, end_date)

    except DateRangeException as dre:
        print(f"Error: {dre}")
    except KeyboardInterrupt:
        print('Process interrupted by user.')
    except Exception as e:
        print(f'An error occurred: {e}')

if __name__ == "__main__":
    main()
    sys.exit(0)
