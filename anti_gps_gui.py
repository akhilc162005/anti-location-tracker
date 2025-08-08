#!/usr/bin/env python3
"""
Anti GPS System GUI
A graphical interface for the Anti GPS System with real-time monitoring.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import json
from datetime import datetime
from anti_gps import AntiGPSSystem

class AntiGPSGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🛡️ Anti GPS System")
        self.root.geometry("800x600")
        self.root.configure(bg='#1a1a1a')
        
        # Initialize the anti GPS system
        self.anti_gps = AntiGPSSystem()
        self.monitoring_thread = None
        self.is_monitoring = False
        
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
        title_label = ttk.Label(main_frame, text="🛡️ Anti GPS System", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Control Panel
        control_frame = ttk.LabelFrame(main_frame, text="Control Panel", padding="10")
        control_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Protection Level
        ttk.Label(control_frame, text="Protection Level:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.protection_var = tk.StringVar(value="medium")
        protection_combo = ttk.Combobox(control_frame, textvariable=self.protection_var, 
                                       values=["low", "medium", "high", "maximum"], state="readonly")
        protection_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(5, 5), pady=5)
        protection_combo.bind("<<ComboboxSelected>>", self.on_protection_change)
        
        # Detection Mode
        ttk.Label(control_frame, text="Detection Mode:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.detection_var = tk.StringVar(value="passive")
        detection_combo = ttk.Combobox(control_frame, textvariable=self.detection_var,
                                      values=["passive", "active", "aggressive"], state="readonly")
        detection_combo.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(5, 5), pady=5)
        detection_combo.bind("<<ComboboxSelected>>", self.on_detection_change)
        
        # Control Buttons
        button_frame = ttk.Frame(control_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=(10, 0))
        
        self.start_button = ttk.Button(button_frame, text="🚀 Start Monitoring", 
                                      command=self.start_monitoring)
        self.start_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.stop_button = ttk.Button(button_frame, text="🛑 Stop Monitoring", 
                                     command=self.stop_monitoring, state="disabled")
        self.stop_button.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(button_frame, text="📊 Status", command=self.show_status).pack(side=tk.LEFT)
        
        # Status Display
        status_frame = ttk.LabelFrame(main_frame, text="Real-Time Status", padding="10")
        status_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        status_frame.columnconfigure(0, weight=1)
        status_frame.rowconfigure(0, weight=1)
        
        # Status text area
        self.status_text = tk.Text(status_frame, height=15, width=80, bg='#2a2a2a', fg='#ffffff')
        status_scrollbar = ttk.Scrollbar(status_frame, orient="vertical", command=self.status_text.yview)
        self.status_text.configure(yscrollcommand=status_scrollbar.set)
        
        self.status_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        status_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Log Display
        log_frame = ttk.LabelFrame(main_frame, text="Activity Log", padding="10")
        log_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        # Log text area
        self.log_text = tk.Text(log_frame, height=8, width=80, bg='#2a2a2a', fg='#00ff00')
        log_scrollbar = ttk.Scrollbar(log_frame, orient="vertical", command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=log_scrollbar.set)
        
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        log_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Initialize status
        self.update_status_display()
        
    def on_protection_change(self, event=None):
        """Handle protection level change."""
        level = self.protection_var.get()
        self.anti_gps.set_protection_level(level)
        self.log_message(f"Protection level changed to: {level}")
        
    def on_detection_change(self, event=None):
        """Handle detection mode change."""
        mode = self.detection_var.get()
        self.anti_gps.set_detection_mode(mode)
        self.log_message(f"Detection mode changed to: {mode}")
        
    def start_monitoring(self):
        """Start the monitoring process."""
        if not self.is_monitoring:
            self.is_monitoring = True
            self.start_button.config(state="disabled")
            self.stop_button.config(state="normal")
            
            # Start monitoring in a separate thread
            self.monitoring_thread = threading.Thread(target=self.monitoring_loop)
            self.monitoring_thread.daemon = True
            self.monitoring_thread.start()
            
            self.log_message("🚀 Monitoring started")
            self.update_status_display()
            
    def stop_monitoring(self):
        """Stop the monitoring process."""
        if self.is_monitoring:
            self.is_monitoring = False
            self.anti_gps.stop_monitoring()
            self.start_button.config(state="normal")
            self.stop_button.config(state="disabled")
            
            self.log_message("🛑 Monitoring stopped")
            self.update_status_display()
            
    def monitoring_loop(self):
        """Main monitoring loop."""
        while self.is_monitoring:
            try:
                # Detect GPS signals
                signals = self.anti_gps.detect_gps_signals()
                
                if signals:
                    threat_level = self.anti_gps.analyze_threat_level(signals)
                    
                    # Update GUI with signal information
                    self.root.after(0, self.update_signal_display, signals, threat_level)
                    
                    # Apply protection based on threat level
                    if threat_level in ["high", "critical"]:
                        self.root.after(0, self.apply_protection, signals)
                    elif threat_level == "medium":
                        self.root.after(0, self.apply_basic_protection, signals)
                
                # Log activity
                self.anti_gps.log_activity(signals)
                
                # Wait before next scan
                time.sleep(3)
                
            except Exception as e:
                self.root.after(0, self.log_message, f"Error: {str(e)}")
                time.sleep(1)
                
    def update_signal_display(self, signals, threat_level):
        """Update the signal display."""
        status = f"🔍 Signals Detected: {len(signals)}\n"
        status += f"🚨 Threat Level: {threat_level.upper()}\n"
        status += f"📡 Jamming Active: {self.anti_gps.jamming_active}\n"
        status += f"🛡️ Protection Level: {self.anti_gps.protection_level.upper()}\n"
        status += f"🔍 Detection Mode: {self.anti_gps.detection_mode.upper()}\n\n"
        
        for signal in signals:
            status += f"⚠️  {signal['frequency']}: {signal['strength']:.2f} strength\n"
        
        self.status_text.delete(1.0, tk.END)
        self.status_text.insert(tk.END, status)
        
    def apply_protection(self, signals):
        """Apply maximum protection."""
        self.log_message("🛡️ Applying maximum protection...")
        
        # Location spoofing
        spoof_result = self.anti_gps.location_spoofing()
        self.log_message(f"📍 Location spoofed to: {spoof_result['spoofed_location']['name']}")
        
        # Signal jamming
        jamming_results = self.anti_gps.signal_jamming(signals)
        for result in jamming_results:
            status = "✅" if result["success"] else "❌"
            self.log_message(f"{status} Jamming {result['frequency']}: {result['jamming_power']:.2f} power")
        
        # Frequency hopping
        hopping_result = self.anti_gps.frequency_hopping()
        self.log_message(f"🔄 Frequency hopping activated")
        
        # Encryption
        encrypt_result = self.anti_gps.encrypt_location_data()
        self.log_message(f"🔐 Location data encrypted")
        
    def apply_basic_protection(self, signals):
        """Apply basic protection."""
        self.log_message("🛡️ Applying basic protection...")
        
        # Location spoofing
        spoof_result = self.anti_gps.location_spoofing()
        self.log_message(f"📍 Location spoofed to: {spoof_result['spoofed_location']['name']}")
        
        # Signal jamming
        jamming_results = self.anti_gps.signal_jamming(signals)
        for result in jamming_results:
            status = "✅" if result["success"] else "❌"
            self.log_message(f"{status} Jamming {result['frequency']}: {result['jamming_power']:.2f} power")
            
    def show_status(self):
        """Show detailed system status."""
        status = self.anti_gps.get_status()
        
        status_window = tk.Toplevel(self.root)
        status_window.title("System Status")
        status_window.geometry("400x300")
        
        status_text = tk.Text(status_window, bg='#2a2a2a', fg='#ffffff')
        status_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        status_display = "📊 SYSTEM STATUS\n"
        status_display += "=" * 30 + "\n\n"
        
        for key, value in status.items():
            status_display += f"{key.replace('_', ' ').title()}: {value}\n"
        
        status_text.insert(tk.END, status_display)
        status_text.config(state=tk.DISABLED)
        
    def update_status_display(self):
        """Update the status display."""
        status = self.anti_gps.get_status()
        self.status_text.delete(1.0, tk.END)
        
        status_display = "📊 SYSTEM STATUS\n"
        status_display += "=" * 30 + "\n\n"
        
        for key, value in status.items():
            status_display += f"{key.replace('_', ' ').title()}: {value}\n"
        
        self.status_text.insert(tk.END, status_display)
        
    def log_message(self, message):
        """Add a message to the log."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)
        
        # Keep only last 100 lines
        lines = self.log_text.get(1.0, tk.END).split('\n')
        if len(lines) > 100:
            self.log_text.delete(1.0, tk.END)
            self.log_text.insert(tk.END, '\n'.join(lines[-100:]))

def main():
    """Main function to run the GUI."""
    root = tk.Tk()
    app = AntiGPSGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
