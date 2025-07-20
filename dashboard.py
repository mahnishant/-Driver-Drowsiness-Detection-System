import tkinter as tk
from tkinter import ttk
import pandas as pd
from datetime import datetime
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# CSV file
LOG_FILE = "drowsiness_log.csv"

# Main window
root = tk.Tk()
root.title("🛡️ Driver Drowsiness Monitor")
root.geometry("850x600")
root.resizable(False, False)

# Heading
title_label = tk.Label(root, text="Driver Drowsiness Dashboard", font=("Arial", 18, "bold"))
title_label.pack(pady=10)

# Info Labels
total_label = tk.Label(root, text="Total Drowsiness Alerts: --", font=("Arial", 14))
last_label = tk.Label(root, text="Last Alert: --", font=("Arial", 12))

total_label.pack()
last_label.pack()

# Table for recent events
tree = ttk.Treeview(root, columns=("Time", "Event"), show="headings", height=6)
tree.heading("Time", text="Timestamp")
tree.heading("Event", text="Event")
tree.pack(pady=10)

# Scrollbar for table
scrollbar = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.pack(side="right", fill="y")

# Frame for graph
graph_frame = tk.Frame(root)
graph_frame.pack(pady=10)

# Create matplotlib figure
fig, ax = plt.subplots(figsize=(6, 3))
canvas = FigureCanvasTkAgg(fig, master=graph_frame)
canvas.get_tk_widget().pack()

def update_dashboard():
    if os.path.exists(LOG_FILE):
        df = pd.read_csv(LOG_FILE, names=["Time", "Event"])
        df["Time"] = pd.to_datetime(df["Time"])

        # Update stats
        total_label.config(text=f"Total Drowsiness Alerts: {len(df)}")
        last_label.config(text=f"Last Alert: {df['Time'].iloc[-1].strftime('%Y-%m-%d %H:%M:%S')}")

        # Update Table
        for row in tree.get_children():
            tree.delete(row)
        for _, row in df.tail(10).iterrows():
            tree.insert("", "end", values=(row["Time"].strftime('%Y-%m-%d %H:%M:%S'), row["Event"]))

        # Update Graph - alerts per minute
        df_minute = df.groupby(df["Time"].dt.strftime('%H:%M')).count()["Event"]
        ax.clear()
        df_minute.plot(kind="bar", ax=ax, color="#ff5733")
        ax.set_title("Drowsiness Alerts per Minute")
        ax.set_ylabel("Count")
        ax.set_xlabel("Time")
        ax.tick_params(axis='x', rotation=45)
        fig.tight_layout()
        canvas.draw()

    root.after(5000, update_dashboard)  # Update every 5 seconds

# Start live updates
update_dashboard()
root.mainloop()
