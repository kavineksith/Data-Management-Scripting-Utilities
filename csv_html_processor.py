#!/usr/bin/env python3

import sys
import csv
import os

class CSVProcessor:
    def __init__(self, csv_file):
        self.csv_file = csv_file
        self.data = []

    def process_csv(self):
        """Turn the contents of the CSV file into a list of lists"""
        try:
            with open(self.csv_file, "r", newline='') as datafile:
                csv_reader = csv.reader(datafile)
                self.data = list(csv_reader)
        except FileNotFoundError as e:
            self._exit_with_error(f"{self.csv_file} not found")
        except PermissionError as e:
            self._exit_with_error(f"Permission denied for {self.csv_file}")
        except Exception as e:
            self._exit_with_error(f"Error occurred while processing CSV: {e}")

    def get_title(self):
        """Extracts the title from the CSV filename"""
        return os.path.splitext(os.path.basename(self.csv_file))[0].replace("_", " ").title()

    @staticmethod
    def _exit_with_error(message):
        """Prints an error message and exits the program"""
        print(f"Error: {message}")
        sys.exit(1)


class HTMLGenerator:
    @staticmethod
    def generate_html(title, data):
        """Turns a list of lists into an HTML table"""
        try:
            # HTML Headers
            html_content = """
<html>
<head>
<style>
table {
  width: 25%;
  font-family: Arial, sans-serif;
  border-collapse: collapse;
}

tr:nth-child(odd) {
  background-color: #dddddd;
}

td, th {
  border: 1px solid #dddddd;
  text-align: left;
  padding: 8px;
}
</style>
</head>
<body>
"""

            # Add the header part with the given title
            html_content += f"<h2>{title}</h2><table>"

            # Add each row in data as a row in the table
            for i, row in enumerate(data):
                html_content += "<tr>"
                for column in row:
                    if i == 0:
                        html_content += f"<th>{column}</th>"
                    else:
                        html_content += f"<td>{column}</td>"
                html_content += "</tr>"

            html_content += "</table></body></html>"
            return html_content
        except Exception as e:
            HTMLGenerator._exit_with_error(f"Error occurred while generating HTML: {e}")

    @staticmethod
    def _exit_with_error(message):
        """Prints an error message and exits the program"""
        print(f"Error: {message}")
        sys.exit(1)


class FileWriter:
    @staticmethod
    def write_html(html_string, html_file):
        """Writes the HTML string to a file"""
        try:
            # Making a note of whether the html file we're writing exists or not
            if os.path.exists(html_file):
                print(f"{html_file} already exists. Overwriting...")

            with open(html_file, "w") as htmlfile:
                htmlfile.write(html_string)
            print(f"Table successfully written to {html_file}")
        except PermissionError as e:
            FileWriter._exit_with_error(f"Permission denied for {html_file}")
        except FileExistsError as e:
            FileWriter._exit_with_error(f"{html_file} already exists")
        except Exception as e:
            FileWriter._exit_with_error(f"Error occurred while writing HTML file: {e}")

    @staticmethod
    def _exit_with_error(message):
        """Prints an error message and exits the program"""
        print(f"Error: {message}")
        sys.exit(1)


def main():
    """Verifies the arguments and then orchestrates the processing"""
    try:
        # Check that command-line arguments are included
        if len(sys.argv) != 3:
            raise ValueError("Usage: python script.py <input_csv_file> <output_html_file>")
        
        # Retrieve command-line arguments
        csv_file = sys.argv[1]
        html_file = sys.argv[2]
        
        # Check that file extensions are included
        if not csv_file.endswith(".csv"):
            raise ValueError('Error: Input file must have ".csv" extension!')
        
        if not html_file.endswith(".html"):
            raise ValueError('Error: Output file must have ".html" extension!')
        
        # Check that the csv file exists
        if not os.path.exists(csv_file):
            raise FileNotFoundError(f"{csv_file} does not exist")
        
        # Initialize and process the CSV data
        csv_processor = CSVProcessor(csv_file)
        csv_processor.process_csv()
        data = csv_processor.data
        title = csv_processor.get_title()
        
        # Generate HTML content
        html_content = HTMLGenerator.generate_html(title, data)
        
        # Write HTML content to file
        FileWriter.write_html(html_content, html_file)

    except ValueError as ve:
        print(f"Error: {ve}")
        sys.exit(1)
    except FileNotFoundError as fnfe:
        print(f"Error: {fnfe}")
        sys.exit(1)
    except PermissionError as pe:
        print(f"Error: {pe}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
