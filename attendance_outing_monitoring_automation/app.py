# app.py

import sys
from datetime import datetime

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QPushButton, QLabel, QTabWidget, QMessageBox
)
from PyQt6.QtCore import Qt

from modules.qr_scanner import scan_qr_code
from modules.csv_handler import ensure_csv_files, add_in_record, process_out_record

ensure_csv_files()


class App(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Trinetra - Smart Attendance & Outing Monitoring")
        self.setGeometry(400, 200, 520, 420)

        self.load_styles()
        self.init_ui()

    # ---------------------------------
    # Load QSS Style
    # ---------------------------------
    def load_styles(self):

        try:
            with open("assets/style.qss", "r") as f:
                self.setStyleSheet(f.read())
        except:
            print("Style file not found")

    # ---------------------------------
    # UI Setup
    # ---------------------------------
    def init_ui(self):

        central = QWidget()
        layout = QVBoxLayout()

        title = QLabel("Trinetra - Smart Monitoring")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(title)

        self.tabs = QTabWidget()

        self.attendance_tab = QWidget()
        self.outing_tab = QWidget()

        self.tabs.addTab(self.attendance_tab, "Attendance")
        self.tabs.addTab(self.outing_tab, "Outing")

        self.init_attendance_tab()
        self.init_outing_tab()

        layout.addWidget(self.tabs)

        self.last_scan_label = QLabel("Last Scan: None")
        self.last_scan_label.setObjectName("lastScanLabel")
        self.last_scan_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(self.last_scan_label)

        central.setLayout(layout)
        self.setCentralWidget(central)

    # ---------------------------------
    # Attendance Tab
    # ---------------------------------
    def init_attendance_tab(self):

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(30)

        in_btn = QPushButton("Mark IN")
        in_btn.setObjectName("inButton")
        in_btn.setFixedWidth(220)
        in_btn.setFixedHeight(60)
        in_btn.clicked.connect(lambda: self.handle_in("Attendance"))

        out_btn = QPushButton("Mark OUT")
        out_btn.setObjectName("outButton")
        out_btn.setFixedWidth(220)
        out_btn.setFixedHeight(60)
        out_btn.clicked.connect(lambda: self.handle_out("Attendance"))

        layout.addWidget(in_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(out_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        self.attendance_tab.setLayout(layout)

    # ---------------------------------
    # Outing Tab
    # ---------------------------------
    def init_outing_tab(self):

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(30)

        out_btn = QPushButton("Start Outing")
        out_btn.setObjectName("outButton")
        out_btn.setFixedWidth(220)
        out_btn.setFixedHeight(60)
        out_btn.clicked.connect(lambda: self.handle_out("Outing"))

        in_btn = QPushButton("Return (IN)")
        in_btn.setObjectName("inButton")
        in_btn.setFixedWidth(220)
        in_btn.setFixedHeight(60)
        in_btn.clicked.connect(lambda: self.handle_in("Outing"))

        layout.addWidget(out_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(in_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        self.outing_tab.setLayout(layout)

    # ---------------------------------
    # Update Last Scan
    # ---------------------------------
    def update_last_scan(self, enrollment):

        time_now = datetime.now().strftime("%H:%M:%S")

        self.last_scan_label.setText(
            f"Last Scan: {enrollment}    |    Time: {time_now}"
        )

    # ---------------------------------
    # IN HANDLER
    # ---------------------------------
    def handle_in(self, section):

        enrollment = scan_qr_code()

        if not enrollment:
            QMessageBox.warning(self, "Cancelled", "Scan cancelled or no QR detected.")
            return

        self.update_last_scan(enrollment)

        status, time_now = add_in_record(section.lower(), enrollment)

        if status == "success":

            QMessageBox.information(
                self,
                "IN Successful",
                f"{enrollment} marked IN at {time_now}"
            )

        elif status == "duplicate":

            QMessageBox.warning(
                self,
                "Duplicate Entry",
                f"{enrollment} is already marked IN."
            )

        elif status == "fraud":

            QMessageBox.critical(
                self,
                "Fraud Alert",
                f"{enrollment} attempted IN without OUT in {section}."
            )

    # ---------------------------------
    # OUT HANDLER
    # ---------------------------------
    def handle_out(self, section):

        enrollment = scan_qr_code()

        if not enrollment:
            QMessageBox.warning(self, "Cancelled", "Scan cancelled or no QR detected.")
            return

        self.update_last_scan(enrollment)

        status, start_time, end_time = process_out_record(section.lower(), enrollment)

        if status == "success":

            if section.lower() == "outing":

                QMessageBox.information(
                    self,
                    "OUT Successful",
                    f"{enrollment} started outing at {start_time}"
                )

            else:

                QMessageBox.information(
                    self,
                    "OUT Successful",
                    f"{enrollment} checked OUT.\nStart: {start_time}\nEnd: {end_time}"
                )

        elif status == "duplicate":

            QMessageBox.warning(
                self,
                "Duplicate Entry",
                f"{enrollment} already marked OUT."
            )

        elif status == "fraud":

            QMessageBox.critical(
                self,
                "Fraud Alert",
                f"{enrollment} attempted OUT without IN in {section}."
            )


# ---------------------------------
# RUN APP
# ---------------------------------

if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = App()
    window.show()

    sys.exit(app.exec())










# # app.py

# import tkinter as tk
# from tkinter import ttk, messagebox
# from datetime import datetime

# from modules.qr_scanner import scan_qr_code
# from modules.csv_handler import ensure_csv_files, add_in_record, process_out_record

# ensure_csv_files()


# # ---------------------------------
# # Update Last Scan Display
# # ---------------------------------
# def update_last_scan(enrollment):

#     time_now = datetime.now().strftime("%H:%M:%S")

#     last_scan_var.set(
#         f"Last Scan: {enrollment}    |    Time: {time_now}"
#     )


# # ---------------------------------
# # IN HANDLER
# # ---------------------------------
# def handle_in(section):

#     enrollment = scan_qr_code()

#     if not enrollment:
#         messagebox.showwarning("Cancelled", "Scan cancelled or no QR detected.")
#         return

#     update_last_scan(enrollment)

#     status, time_now = add_in_record(section.lower(), enrollment)

#     if status == "success":

#         messagebox.showinfo(
#             "IN Successful",
#             f"{enrollment} marked IN at {time_now}"
#         )

#     elif status == "duplicate":

#         messagebox.showwarning(
#             "Duplicate Entry",
#             f"{enrollment} is already marked IN."
#         )

#     elif status == "fraud":

#         messagebox.showerror(
#             "Fraud Alert",
#             f"{enrollment} attempted IN without OUT in {section}."
#         )


# # ---------------------------------
# # OUT HANDLER
# # ---------------------------------
# def handle_out(section):

#     enrollment = scan_qr_code()

#     if not enrollment:
#         messagebox.showwarning("Cancelled", "Scan cancelled or no QR detected.")
#         return

#     update_last_scan(enrollment)

#     status, start_time, end_time = process_out_record(section.lower(), enrollment)

#     if status == "success":

#         if section.lower() == "outing":

#             messagebox.showinfo(
#                 "OUT Successful",
#                 f"{enrollment} started outing at {start_time}"
#             )

#         else:

#             messagebox.showinfo(
#                 "OUT Successful",
#                 f"{enrollment} checked OUT.\nStart: {start_time}\nEnd: {end_time}"
#             )

#     elif status == "duplicate":

#         messagebox.showwarning(
#             "Duplicate Entry",
#             f"{enrollment} already marked OUT."
#         )

#     elif status == "fraud":

#         messagebox.showerror(
#             "Fraud Alert",
#             f"{enrollment} attempted OUT without IN in {section}."
#         )


# # ---------------------------------
# # GUI
# # ---------------------------------

# root = tk.Tk()
# root.title("Trinetra - Smart Attendance & Outing Monitoring")
# root.geometry("500x380")
# # root.configure(bg="#E65100")
# root.configure(bg="#0B3D0B")

# tab_control = ttk.Notebook(root)


# # ================================
# # Attendance Tab
# # ================================

# attendance_tab = ttk.Frame(tab_control)
# tab_control.add(attendance_tab, text="Attendance")

# attendance_in_btn = tk.Button(
#     attendance_tab,
#     text="IN",
#     font=("Helvetica", 14, "bold"),
#     bg="#1E5D1E",
#     fg="white",
#     activebackground="#2E7D2E",
#     bd=0,
#     padx=20,
#     pady=10,
#     cursor="hand2",
#     command=lambda: handle_in("Attendance")
# )

# attendance_in_btn.pack(pady=20)


# attendance_out_btn = tk.Button(
#     attendance_tab,
#     text="OUT",
#     font=("Helvetica", 14, "bold"),
#     bg="#B22222",
#     fg="white",
#     activebackground="#CD3333",
#     bd=0,
#     padx=20,
#     pady=10,
#     cursor="hand2",
#     command=lambda: handle_out("Attendance")
# )

# attendance_out_btn.pack(pady=20)


# # ================================
# # Outing Tab
# # ================================

# outing_tab = ttk.Frame(tab_control)
# tab_control.add(outing_tab, text="Outing")

# outing_out_btn = tk.Button(
#     outing_tab,
#     text="OUT",
#     font=("Helvetica", 14, "bold"),
#     bg="#B22222",
#     fg="white",
#     activebackground="#CD3333",
#     bd=0,
#     padx=25,
#     pady=12,
#     cursor="hand2",
#     command=lambda: handle_out("Outing")
# )

# outing_out_btn.pack(pady=25)


# outing_in_btn = tk.Button(
#     outing_tab,
#     text="IN",
#     font=("Helvetica", 14, "bold"),
#     bg="#1E5D1E",
#     fg="white",
#     activebackground="#2E7D2E",
#     bd=0,
#     padx=25,
#     pady=12,
#     cursor="hand2",
#     command=lambda: handle_in("Outing")
# )

# outing_in_btn.pack(pady=20)


# tab_control.pack(expand=1, fill="both")


# # =================================
# # LAST SCAN DISPLAY
# # =================================

# last_scan_var = tk.StringVar()
# last_scan_var.set("Last Scan: None")

# last_scan_label = tk.Label(
#     root,
#     textvariable=last_scan_var,
#     font=("Helvetica", 12, "bold"),
#     bg="#0B3D0B",
#     fg="white",
#     pady=10
# )

# last_scan_label.pack()


# root.mainloop()