#!/usr/bin/env python3
"""
Live Location Tracker GUI
Graphical interface for real-time GPS location tracking.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import json
from datetime import datetime
from live_locations import LiveLocationTracker

class LiveLocationGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("📍 Live Location Tracker")
        self.root.geometry("900x700")
        self.root.configure(bg='#1a1a1a')
        
        # Initialize the location tracker
        self.tracker = LiveLocationTracker()
        self.tracking_thread = None
        self.is_tracking = False
        
        # Create GUI elements
        self.setup_gui()
        
    def setup_gui(self):
        """Setup the GUI interface."""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="📍 Live Location Tracker", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Control Panel
        control_frame = ttk.LabelFrame(main_frame, text="Control Panel", padding="10")
        control_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Control Buttons
        button_frame = ttk.Frame(control_frame)
        button_frame.grid(row=0, column=0, columnspan=2, pady=(0, 10))
        
        self.start_button = ttk.Button(button_frame, text="🚀 Start Tracking", 
                                      command=self.start_tracking)
        self.start_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.stop_button = ttk.Button(button_frame, text="🛑 Stop Tracking", 
                                     command=self.stop_tracking, state="disabled")
        self.stop_button.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(button_frame, text="📊 Status", command=self.show_status).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="📜 History", command=self.show_history).pack(side=tk.LEFT)
        
        # Current Location Display
        location_frame = ttk.LabelFrame(main_frame, text="Current Location", padding="10")
        location_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        location_frame.columnconfigure(0, weight=1)
        
        # Location info labels
        self.location_labels = {}
        location_info = [
            ("city", "🌍 City:"),
            ("country", "🏳️ Country:"),
            ("coordinates", "📍 Coordinates:"),
            ("accuracy", "🎯 Accuracy:"),
            ("speed", "🚗 Speed:"),
            ("heading", "🧭 Heading:"),
            ("altitude", "⛰️ Altitude:"),
            ("timestamp", "⏰ Time:")
        ]
        
        for i, (key, label) in enumerate(location_info):
            ttk.Label(location_frame, text=label).grid(row=i, column=0, sticky=tk.W, pady=2)
            self.location_labels[key] = ttk.Label(location_frame, text="--", font=("Arial", 10, "bold"))
            self.location_labels[key].grid(row=i, column=1, sticky=tk.W, padx=(10, 0), pady=2)
        
        # Map-like Display
        map_frame = ttk.LabelFrame(main_frame, text="Location Map", padding="10")
        map_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        map_frame.columnconfigure(0, weight=1)
        map_frame.rowconfigure(0, weight=1)
        
        # Map canvas
        self.map_canvas = tk.Canvas(map_frame, bg='#2a2a2a', height=300, width=800)
        map_scrollbar = ttk.Scrollbar(map_frame, orient="vertical", command=self.map_canvas.yview)
        self.map_canvas.configure(yscrollcommand=map_scrollbar.set)
        
        self.map_canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        map_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Status Display
        status_frame = ttk.LabelFrame(main_frame, text="Tracking Status", padding="10")
        status_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))
        status_frame.columnconfigure(0, weight=1)
        status_frame.rowconfigure(0, weight=1)
        
        # Status text area
        self.status_text = tk.Text(status_frame, height=8, width=80, bg='#2a2a2a', fg='#00ff00')
        status_scrollbar = ttk.Scrollbar(status_frame, orient="vertical", command=self.status_text.yview)
        self.status_text.configure(yscrollcommand=status_scrollbar.set)
        
        self.status_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        status_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Initialize display
        self.update_location_display()
        
    def start_tracking(self):
        """Start the tracking process."""
        if not self.is_tracking:
            self.is_tracking = True
            self.start_button.config(state="disabled")
            self.stop_button.config(state="normal")
            
            # Start tracking in a separate thread
            self.tracking_thread = threading.Thread(target=self.tracking_loop)
            self.tracking_thread.daemon = True
            self.tracking_thread.start()
            
            self.log_message("🚀 Live location tracking started")
            self.update_location_display()
            
    def stop_tracking(self):
        """Stop the tracking process."""
        if self.is_tracking:
            self.is_tracking = False
            self.tracker.stop_tracking()
            self.start_button.config(state="normal")
            self.stop_button.config(state="disabled")
            
            self.log_message("🛑 Live location tracking stopped")
            self.update_location_display()
            
    def tracking_loop(self):
        """Main tracking loop."""
        while self.is_tracking:
            try:
                # Get current location
                location = self.tracker.get_current_location()
                self.tracker.current_location = location
                self.tracker.location_history.append(location)
                
                # Keep only last 100 locations
                if len(self.tracker.location_history) > 100:
                    self.tracker.location_history = self.tracker.location_history[-100:]
                
                # Log location
                self.tracker.log_location(location)
                
                # Update GUI
                self.root.after(0, self.update_location_display)
                self.root.after(0, self.update_map_display)
                
                # Wait before next update
                time.sleep(2)
                
            except Exception as e:
                self.root.after(0, self.log_message, f"Error: {str(e)}")
                time.sleep(1)
                
    def update_location_display(self):
        """Update the location display."""
        if self.tracker.current_location:
            location = self.tracker.current_location
            info = self.tracker.get_location_info(location)
            
            # Update labels
            for key, label in self.location_labels.items():
                if key in info:
                    label.config(text=info[key])
        
        # Update status
        status = self.tracker.get_current_status()
        status_display = f"📊 Tracking Status:\n"
        status_display += f"Active: {status['tracking_active']}\n"
        status_display += f"Current: {status['current_location']}\n"
        status_display += f"Total: {status['total_locations']}\n"
        status_display += f"Distance: {status['distance_traveled']}\n"
        status_display += f"Interval: {status['tracking_interval']}"
        
        self.status_text.delete(1.0, tk.END)
        self.status_text.insert(tk.END, status_display)
        
    def update_map_display(self):
        """Update the map-like display."""
        self.map_canvas.delete("all")
        
        if not self.tracker.location_history:
            return
        
        # Create a simple map visualization
        canvas_width = 800
        canvas_height = 300
        margin = 50
        
        # Draw grid
        for i in range(0, canvas_width, 50):
            self.map_canvas.create_line(i, 0, i, canvas_height, fill='#444444', width=1)
        for i in range(0, canvas_height, 50):
            self.map_canvas.create_line(0, i, canvas_width, i, fill='#444444', width=1)
        
        # Plot recent locations
        recent_locations = self.tracker.get_location_history(10)
        if len(recent_locations) > 1:
            # Create path
            points = []
            for i, location in enumerate(recent_locations):
                x = margin + (i * (canvas_width - 2 * margin) / (len(recent_locations) - 1))
                y = margin + (location['lat'] % 90) * (canvas_height - 2 * margin) / 90
                points.extend([x, y])
                
                # Draw location point
                color = '#ff0000' if i == len(recent_locations) - 1 else '#00ff00'
                size = 8 if i == len(recent_locations) - 1 else 4
                self.map_canvas.create_oval(x-size, y-size, x+size, y+size, 
                                          fill=color, outline='white')
                
                # Add location label
                self.map_canvas.create_text(x, y-15, text=location['name'][:8], 
                                          fill='white', font=('Arial', 8))
            
            # Draw path line
            if len(points) >= 4:
                self.map_canvas.create_line(points, fill='#00ffff', width=2, smooth=True)
        
        # Add map title
        self.map_canvas.create_text(canvas_width//2, 20, text="Live Location Map", 
                                  fill='white', font=('Arial', 12, 'bold'))
        
    def show_status(self):
        """Show detailed tracking status."""
        status = self.tracker.get_current_status()
        
        status_window = tk.Toplevel(self.root)
        status_window.title("Tracking Status")
        status_window.geometry("400x300")
        
        status_text = tk.Text(status_window, bg='#2a2a2a', fg='#ffffff')
        status_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        status_display = "📊 TRACKING STATUS\n"
        status_display += "=" * 30 + "\n\n"
        
        for key, value in status.items():
            status_display += f"{key.replace('_', ' ').title()}: {value}\n"
        
        if self.tracker.current_location:
            location = self.tracker.current_location
            status_display += f"\n📍 CURRENT LOCATION:\n"
            status_display += f"City: {location['name']}\n"
            status_display += f"Country: {location['country']}\n"
            status_display += f"Coordinates: {location['lat']:.6f}, {location['lon']:.6f}\n"
            status_display += f"Speed: {location['speed']:.1f} km/h\n"
            status_display += f"Accuracy: {location['accuracy']:.1f}m\n"
        
        status_text.insert(tk.END, status_display)
        status_text.config(state=tk.DISABLED)
        
    def show_history(self):
        """Show location history."""
        history = self.tracker.get_location_history(20)
        
        history_window = tk.Toplevel(self.root)
        history_window.title("Location History")
        history_window.geometry("600x400")
        
        history_text = tk.Text(history_window, bg='#2a2a2a', fg='#00ff00')
        history_scrollbar = ttk.Scrollbar(history_window, orient="vertical", command=history_text.yview)
        history_text.configure(yscrollcommand=history_scrollbar.set)
        
        history_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        history_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        history_display = "📜 LOCATION HISTORY\n"
        history_display += "=" * 50 + "\n\n"
        
        for i, location in enumerate(reversed(history), 1):
            history_display += f"{i:2d}. {location['name']}, {location['country']}\n"
            history_display += f"    📍 {location['lat']:.6f}, {location['lon']:.6f}\n"
            history_display += f"    🚗 Speed: {location['speed']:.1f} km/h\n"
            history_display += f"    ⏰ {location['timestamp']}\n"
            history_display += "-" * 40 + "\n"
        
        history_text.insert(tk.END, history_display)
        history_text.config(state=tk.DISABLED)
        
    def log_message(self, message):
        """Add a message to the log."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        self.status_text.insert(tk.END, log_entry)
        self.status_text.see(tk.END)
        
        # Keep only last 50 lines
        lines = self.status_text.get(1.0, tk.END).split('\n')
        if len(lines) > 50:
            self.status_text.delete(1.0, tk.END)
            self.status_text.insert(tk.END, '\n'.join(lines[-50:]))

def main():
    """Main function to run the GUI."""
    root = tk.Tk()
    app = LiveLocationGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
