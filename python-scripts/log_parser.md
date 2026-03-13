# Linux Log Parser (Python)

## Overview
This script parses Linux authentication logs and extracts structured fields using regular expressions.

```python
import re
import pandas as pd

# Open and read the log file
with open("Linux_2k.log", "r") as file:
    lines = file.readlines()

# Define the log pattern
log_pattern = r"(?P<date>[A-Za-z]{3} \d{1,2} \d{2}:\d{2}:\d{2}) (?P<host>\S+) (?P<service>\w+)\((?P<module>\w+)\)\[(?P<pid>\d+)\]: (?P<message>.+)"
logs = [re.match(log_pattern, line).groupdict() for line in lines if re.match(log_pattern, line)]

# Convert to DataFrame for analysis
log_df = pd.DataFrame(logs)
print("Parsed Logs:\n", log_df.head())

# Count authentication failures
log_df[log_df["message"].str.contains("failure")]

#Find most attacked IP
log_df["message"].value_counts()

#Filter ssh logs
log_df[log_df["service"] == "sshd"]
