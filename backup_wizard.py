#!/usr/bin/env python3

from multiprocessing import Pool
import multiprocessing
import subprocess
import os

class ProcessExecutionError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class DataSyncManager:
    def __init__(self, source_dir, dest_dir):
        self.source_dir = source_dir
        self.dest_dir = dest_dir

    def sync_data(self):
        try:
            subprocess.call(["rsync", "-arq", self.source_dir, self.dest_dir])
        except subprocess.CalledProcessError as e:
            raise ProcessExecutionError(f"Rsync process failed: {e}")
        except PermissionError:
            raise ProcessExecutionError("Permission denied: Unable to execute rsync command.")
        except FileNotFoundError:
            raise ProcessExecutionError("rsync command not found. Please ensure it is installed.")
        except KeyboardInterrupt:
            raise ProcessExecutionError("Process interrupted by user.")
        except Exception as e:
            raise ProcessExecutionError(f"An error occurred during rsync operation: {e}")

def main():
    try:
        home_path = os.path.expanduser('~')
        source_dir = os.path.join(home_path, "data", "prod")
        dest_dir = os.path.join(home_path, "data", "prod_backup")

        data_sync_manager = DataSyncManager(source_dir, dest_dir)
        
        pool = Pool(multiprocessing.cpu_count())
        pool.apply(data_sync_manager.sync_data)

        pool.close()
        pool.join()

        print("Data synchronization completed successfully.")
    except ProcessExecutionError as pee:
        print(f"Error during data synchronization: {pee}")
        exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        exit(1)

if __name__ == "__main__":
    main()
    exit(0)
