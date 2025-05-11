import tkinter as tk
from tkinter import ttk
import psutil
import time
import threading

class SystemMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("System Information Monitor")
        self.root.geometry("600x400")
        
        # Labels to display system information
        self.cpu_label = ttk.Label(root, text="CPU Usage: 0%")
        self.cpu_label.pack(pady=10)
        
        self.memory_label = ttk.Label(root, text="Memory Usage: 0%")
        self.memory_label.pack(pady=10)
        
        self.disk_label = ttk.Label(root, text="Disk Usage: 0%")
        self.disk_label.pack(pady=10)
        
        self.network_label = ttk.Label(root, text="Network: Sent 0 KB | Received 0 KB")
        self.network_label.pack(pady=10)
        
        # Button to start/stop monitoring
        self.monitoring = False
        self.start_button = ttk.Button(root, text="Start Monitoring", command=self.toggle_monitoring)
        self.start_button.pack(pady=20)
        
        # Start the update loop in a separate thread
        self.thread = None
        
    def get_system_info(self):
        # CPU Usage
        cpu_usage = psutil.cpu_percent(interval=1)
        self.cpu_label.config(text=f"CPU Usage: {cpu_usage}%")
        
        # Memory Usage
        memory = psutil.virtual_memory()
        memory_usage = memory.percent
        self.memory_label.config(text=f"Memory Usage: {memory_usage}%")
        
        # Disk Usage
        disk = psutil.disk_usage('/')
        disk_usage = disk.percent
        self.disk_label.config(text=f"Disk Usage: {disk_usage}%")
        
        # Network Usage
        net_io = psutil.net_io_counters()
        sent = net_io.bytes_sent / 1024  # Convert to KB
        received = net_io.bytes_recv / 1024  # Convert to KB
        self.network_label.config(text=f"Network: Sent {sent:.2f} KB | Received {received:.2f} KB")
    
    def update_loop(self):
        while self.monitoring:
            self.get_system_info()
            time.sleep(2)  # Update every 2 seconds
    
    def toggle_monitoring(self):
        if not self.monitoring:
            self.monitoring = True
            self.start_button.config(text="Stop Monitoring")
            self.thread = threading.Thread(target=self.update_loop, daemon=True)
            self.thread.start()
        else:
            self.monitoring = False
            self.start_button.config(text="Start Monitoring")

if __name__ == "__main__":
    root = tk.Tk()
    app = SystemMonitorApp(root)
    root.mainloop()