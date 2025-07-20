import tkinter as tk
from tkinter import messagebox
import subprocess
import os
import signal

# Global variable to store subprocess reference
detection_process = None

def start_detection():
    global detection_process
    if detection_process is None:
        detection_process = subprocess.Popen(["python", "app.py"])
        status_label.config(text="Detection: ON", fg="green")
        start_btn.config(state="disabled")
        stop_btn.config(state="normal")
    else:
        messagebox.showinfo("Already Running", "Drowsiness detection is already running.")

def stop_detection():
    global detection_process
    if detection_process:
        detection_process.terminate()
        detection_process = None
        status_label.config(text="Detection: OFF", fg="red")
        start_btn.config(state="normal")
        stop_btn.config(state="disabled")

# GUI Setup
root = tk.Tk()
root.title("Driver Drowsiness Detector")
root.geometry("400x250")
root.resizable(False, False)

tk.Label(root, text="🛡️ Drowsiness Detection System", font=("Arial", 16, "bold")).pack(pady=15)

status_label = tk.Label(root, text="Detection: OFF", font=("Arial", 14), fg="red")
status_label.pack(pady=10)

# Buttons
start_btn = tk.Button(root, text="▶️ Start Detection", font=("Arial", 12), width=20, command=start_detection)
start_btn.pack(pady=5)

stop_btn = tk.Button(root, text="⏹ Stop Detection", font=("Arial", 12), width=20, command=stop_detection, state="disabled")
stop_btn.pack(pady=5)

# Exit clean-up
def on_close():
    if detection_process:
        detection_process.terminate()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()
