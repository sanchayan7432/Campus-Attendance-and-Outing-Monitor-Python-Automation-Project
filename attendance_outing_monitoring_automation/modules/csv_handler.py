# # modules/csv_handler.py
# import os
# import csv
# from datetime import datetime

# BASE_PATH = os.path.dirname(os.path.abspath(__file__))

# def ensure_csv_files():
#     """Ensure all CSV files exist"""
#     files = {
#         "attendance.csv": ["enrollment_no", "time"],
#         "outing.csv": ["enrollment_no", "time"],
#         "record.csv": ["enrollment_no", "start_time", "end_time", "section"],
#         "fraud.csv": ["enrollment_no", "time", "section", "direction"]
#     }
#     for file, headers in files.items():
#         path = os.path.join(BASE_PATH, file)
#         if not os.path.exists(path):
#             with open(path, "w", newline="") as f:
#                 writer = csv.writer(f)
#                 writer.writerow(headers)

# def add_in_record(section, enrollment_no):
#     file_path = os.path.join(BASE_PATH, f"{section}.csv")
#     time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

#     # Check duplicate
#     existing = []
#     with open(file_path, "r", newline="") as f:
#         reader = csv.DictReader(f)
#         for row in reader:
#             existing.append(row["enrollment_no"])

#     if enrollment_no in existing:
#         return False, time_now

#     # Append new IN
#     with open(file_path, "a", newline="") as f:
#         writer = csv.writer(f)
#         writer.writerow([enrollment_no, time_now])

#     return True, time_now

# def process_out_record(section, enrollment_no):
#     section_file = os.path.join(BASE_PATH, f"{section}.csv")
#     record_file = os.path.join(BASE_PATH, "record.csv")
#     fraud_file = os.path.join(BASE_PATH, "fraud.csv")

#     rows = []
#     start_time = None

#     # Read section CSV
#     with open(section_file, "r", newline="") as f:
#         reader = csv.DictReader(f)
#         for row in reader:
#             if row["enrollment_no"] == enrollment_no:
#                 start_time = row["time"]
#             else:
#                 rows.append(row)

#     if start_time:
#         # Remove from section CSV
#         with open(section_file, "w", newline="") as f:
#             writer = csv.DictWriter(f, fieldnames=["enrollment_no", "time"])
#             writer.writeheader()
#             for row in rows:
#                 writer.writerow(row)

#         end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         # Add to record.csv
#         with open(record_file, "a", newline="") as f:
#             writer = csv.writer(f)
#             writer.writerow([enrollment_no, start_time, end_time, section])

#         return True, start_time, end_time
#     else:
#         # Log fraud
#         with open(fraud_file, "a", newline="") as f:
#             writer = csv.writer(f)
#             writer.writerow([
#                 enrollment_no,
#                 datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#                 section,
#                 "OUT"
#             ])
#         return False, None, None



# modules/csv_handler.py

import os
import csv
from datetime import datetime

BASE_PATH = os.path.dirname(os.path.abspath(__file__))


def ensure_csv_files():
    """Ensure all required CSV files exist"""

    files = {
        "attendance.csv": ["enrollment_no", "time"],
        "outing.csv": ["enrollment_no", "time"],
        "record.csv": ["enrollment_no", "start_time", "end_time", "section"],
        "fraud.csv": ["enrollment_no", "time", "section", "direction"]
    }

    for file, headers in files.items():
        path = os.path.join(BASE_PATH, file)

        if not os.path.exists(path):
            with open(path, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(headers)


def current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# ---------------------------------------------------
# IN RECORD
# ---------------------------------------------------
def add_in_record(section, enrollment_no):

    file_path = os.path.join(BASE_PATH, f"{section}.csv")
    fraud_file = os.path.join(BASE_PATH, "fraud.csv")

    rows = []
    found = False
    start_time = None

    with open(file_path, "r", newline="") as f:
        reader = csv.DictReader(f)

        for row in reader:

            if section == "attendance":

                if row["enrollment_no"] == enrollment_no:
                    return "duplicate", row["time"]

                rows.append(row)

            elif section == "outing":

                if row["enrollment_no"] == enrollment_no:
                    found = True
                    start_time = row["time"]
                else:
                    rows.append(row)

    # -------------------------
    # ATTENDANCE IN
    # -------------------------
    if section == "attendance":

        time_now = current_time()

        with open(file_path, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([enrollment_no, time_now])

        return "success", time_now


    # -------------------------
    # OUTING IN (Return)
    # -------------------------
    elif section == "outing":

        if not found:

            # Fraud: IN without OUT
            with open(fraud_file, "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([
                    enrollment_no,
                    current_time(),
                    section,
                    "IN"
                ])

            return "fraud", None

        end_time = current_time()

        # Remove student from outing.csv
        with open(file_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["enrollment_no", "time"])
            writer.writeheader()

            for row in rows:
                writer.writerow(row)

        # Add to record.csv
        record_file = os.path.join(BASE_PATH, "record.csv")

        with open(record_file, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([enrollment_no, start_time, end_time, section])

        return "success", end_time


# ---------------------------------------------------
# OUT RECORD
# ---------------------------------------------------
def process_out_record(section, enrollment_no):

    file_path = os.path.join(BASE_PATH, f"{section}.csv")
    fraud_file = os.path.join(BASE_PATH, "fraud.csv")

    rows = []
    found = False
    start_time = None

    with open(file_path, "r", newline="") as f:
        reader = csv.DictReader(f)

        for row in reader:

            if row["enrollment_no"] == enrollment_no:
                found = True
                start_time = row["time"]
            else:
                rows.append(row)

    # -------------------------
    # ATTENDANCE OUT
    # -------------------------
    if section == "attendance":

        if not found:

            # Fraud: OUT without IN
            with open(fraud_file, "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([
                    enrollment_no,
                    current_time(),
                    section,
                    "OUT"
                ])

            return "fraud", None, None

        end_time = current_time()

        with open(file_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["enrollment_no", "time"])
            writer.writeheader()

            for row in rows:
                writer.writerow(row)

        record_file = os.path.join(BASE_PATH, "record.csv")

        with open(record_file, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([enrollment_no, start_time, end_time, section])

        return "success", start_time, end_time


    # -------------------------
    # OUTING OUT (Start outing)
    # -------------------------
    elif section == "outing":

        if found:
            return "duplicate", start_time, None

        start_time = current_time()

        with open(file_path, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([enrollment_no, start_time])

        return "success", start_time, None