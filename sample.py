import os
from pathlib import Path


log_file = Path("./error_log.log")

if os.path.exists(log_file):
    print("Correct")