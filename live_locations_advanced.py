#!/usr/bin/env python3
"""
Advanced Live Location Tracker
Enhanced GPS location tracking with weather, traffic, routes, and shareable links.
"""

import time
import random
import threading
from datetime import datetime, timedelta
import json
import os
from math import radians, cos, sin, sqrt, atan2
import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser
import urllib.parse
import base64
from io import BytesIO

class AdvancedLocationTracker:
    def __init__(self):
        """Initialize the Advanced Location Tracker."""
        self.is_tracking = False
        self.current_location = None
        self.location_history = []
        self.tracking_interval = 1.0
        self.log_file = "advanced_locations_log.txt"
        self.route_mode = False
        self.weather_enabled = True
        self.traffic_enabled = True
        self.social_sharing = False
        
        # Extended sample locations with more data
        self.sample_locations = [
            {"name": "New York", "lat": 40.7128, "lon": -74.0060, "country": "USA", "timezone": "EST", "population": "8.4M"},
            {"name": "London", "lat": 51.5074, "lon": -0.1278, "country": "UK", "timezone": "GMT", "population": "8.9M"},
            {"name": "Tokyo", "lat": 35.6762, "lon": 139.6503, "country": "Japan", "timezone": "JST", "population": "13.9M"},
            {"name": "Paris", "lat": 48.8566, "lon": 2.3522, "country": "France", "timezone": "CET", "population": "2.2M"},
            {"name": "Sydney", "lat": -33.8688, "lon": 151.2093, "country": "Australia", "timezone": "AEST", "population": "5.3M"},
            {"name": "Moscow", "lat": 55.7558, "lon": 37.6176, "country": "Russia", "timezone": "MSK", "population": "12.5M"},
            {"name": "Beijing", "lat": 39.9042, "lon": 116.4074, "country": "China", "timezone": "CST", "population": "21.5M"},
            {"name": "Dubai", "lat": 25.2048, "lon": 55.2708, "country": "UAE", "timezone": "GST", "population": "3.3M"},
            {"name": "Singapore", "lat": 1.3521, "lon": 103.8198, "country": "Singapore", "timezone": "SGT", "population": "5.7M"},
            {"name": "Mumbai", "lat": 19.0760, "lon": 72.8777, "country": "India", "timezone": "IST", "population": "20.4M"},
            {"name": "São Paulo", "lat": -23.5505, "lon": -46.6333, "country": "Brazil", "timezone": "BRT", "population": "12.3M"},
            {"name": "Cairo", "lat": 30.0444, "lon": 31.2357, "country": "Egypt", "timezone": "EET", "population": "9.5M"},
            {"name": "Seoul", "lat": 37.5665, "lon": 126.9780, "country": "South Korea", "timezone": "KST", "population": "9.7M"},
            {"name": "Mexico City", "lat": 19.4326, "lon": -99.1332, "country": "Mexico", "timezone": "CST", "population": "9.2M"},
            {"name": "Istanbul", "lat": 41.0082, "lon": 28.9784, "country": "Turkey", "timezone": "TRT", "population": "15.5M"}
        ]
        
        # Weather conditions
        self.weather_conditions = ["Sunny", "Cloudy", "Rainy", "Snowy", "Foggy", "Stormy", "Clear", "Partly Cloudy"]
        
        # Traffic conditions
        self.traffic_conditions = ["Light", "Moderate", "Heavy", "Congested", "Clear", "Slow", "Standstill"]
        
        print("📍 Advanced Location Tracker Initialized")
        print("=" * 60)
    
    def get_current_location(self):
        """Get current GPS location with enhanced data."""
        location = random.choice(self.sample_locations)
        
        # Add variation for realistic movement
        lat_variation = random.uniform(-0.001, 0.001)
        lon_variation = random.uniform(-0.001, 0.001)
        
        # Enhanced location data
        current_location = {
            "name": location["name"],
            "lat": location["lat"] + lat_variation,
            "lon": location["lon"] + lon_variation,
            "country": location["country"],
            "timezone": location["timezone"],
            "population": location["population"],
            "timestamp": datetime.now().isoformat(),
            "accuracy": random.uniform(3, 15),
            "speed": random.uniform(0, 80),
            "heading": random.uniform(0, 360),
            "altitude": random.uniform(0, 2000),
            "weather": random.choice(self.weather_conditions),
            "temperature": random.uniform(-10, 40),
            "humidity": random.uniform(30, 90),
            "traffic": random.choice(self.traffic_conditions),
            "battery_level": random.uniform(20, 100),
            "signal_strength": random.uniform(1, 5),
            "network_type": random.choice(["4G", "5G", "WiFi", "3G"]),
            "estimated_arrival": None,
            "route_distance": 0,
            "route_duration": 0
        }
        
        return current_location
    
    def calculate_distance(self, lat1, lon1, lat2, lon2):
        """Calculate distance between GPS coordinates."""
        R = 6371
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        return R * c
    
    def get_weather_info(self, location):
        """Get weather information for location."""
        weather_info = {
            "condition": location["weather"],
            "temperature": f"{location['temperature']:.1f}°C",
            "humidity": f"{location['humidity']:.0f}%",
            "feels_like": f"{location['temperature'] + random.uniform(-5, 5):.1f}°C",
            "wind_speed": f"{random.uniform(0, 30):.1f} km/h",
            "visibility": f"{random.uniform(5, 20):.1f} km",
            "uv_index": random.randint(0, 10)
        }
        return weather_info
    
    def get_traffic_info(self, location):
        """Get traffic information for location."""
        traffic_info = {
            "condition": location["traffic"],
            "delay_minutes": random.randint(0, 45),
            "average_speed": f"{random.uniform(10, 80):.0f} km/h",
            "congestion_level": random.randint(1, 10),
            "incidents": random.randint(0, 3),
            "road_conditions": random.choice(["Good", "Fair", "Poor", "Excellent"])
        }
        return traffic_info
    
    def get_route_info(self, start_location, end_location):
        """Calculate route information."""
        distance = self.calculate_distance(
            start_location["lat"], start_location["lon"],
            end_location["lat"], end_location["lon"]
        )
        
        # Estimate travel time based on traffic and speed
        avg_speed = random.uniform(30, 80)
        duration_hours = distance / avg_speed
        duration_minutes = duration_hours * 60
        
        route_info = {
            "distance": f"{distance:.1f} km",
            "duration": f"{duration_minutes:.0f} min",
            "avg_speed": f"{avg_speed:.0f} km/h",
            "fuel_consumption": f"{distance * 0.08:.1f} L",
            "co2_emission": f"{distance * 0.2:.1f} kg",
            "tolls": random.randint(0, 3),
            "rest_stops": random.randint(0, 2)
        }
        return route_info
    
    def get_location_details(self, location):
        """Get comprehensive location information."""
        details = {
            "basic_info": {
                "city": location["name"],
                "country": location["country"],
                "coordinates": f"{location['lat']:.6f}, {location['lon']:.6f}",
                "timezone": location["timezone"],
                "population": location["population"]
            },
            "gps_info": {
                "accuracy": f"{location['accuracy']:.1f}m",
                "speed": f"{location['speed']:.1f} km/h",
                "heading": f"{location['heading']:.1f}°",
                "altitude": f"{location['altitude']:.0f}m"
            },
            "weather": self.get_weather_info(location),
            "traffic": self.get_traffic_info(location),
            "device_info": {
                "battery": f"{location['battery_level']:.0f}%",
                "signal": f"{location['signal_strength']:.0f}/5",
                "network": location["network_type"],
                "timestamp": location["timestamp"]
            }
        }
        return details
    
    def generate_shareable_links(self, location):
        """Generate various shareable links for the location."""
        lat, lon = location["lat"], location["lon"]
        city_name = location["name"]
        country = location["country"]
        
        # Create location description
        location_desc = f"{city_name}, {country}"
        
        # Generate different types of shareable links
        links = {
            "google_maps": f"https://www.google.com/maps?q={lat},{lon}",
            "apple_maps": f"https://maps.apple.com/?q={lat},{lon}",
            "waze": f"https://waze.com/ul?ll={lat},{lon}&navigate=yes",
            "bing_maps": f"https://www.bing.com/maps?cp={lat}~{lon}&lvl=15",
            "openstreetmap": f"https://www.openstreetmap.org/?mlat={lat}&mlon={lon}&zoom=15",
            "whatsapp": f"https://wa.me/?text=📍 I'm at {location_desc} ({lat:.6f}, {lon:.6f})",
            "telegram": f"https://t.me/share/url?url={urllib.parse.quote(f'https://maps.google.com/?q={lat},{lon}')}&text=📍 I'm at {location_desc}",
            "twitter": f"https://twitter.com/intent/tweet?text=📍 I'm at {location_desc} ({lat:.6f}, {lon:.6f})&url={urllib.parse.quote(f'https://maps.google.com/?q={lat},{lon}')}",
            "facebook": f"https://www.facebook.com/sharer/sharer.php?u={urllib.parse.quote(f'https://maps.google.com/?q={lat},{lon}')}",
            "linkedin": f"https://www.linkedin.com/sharing/share-offsite/?url={urllib.parse.quote(f'https://maps.google.com/?q={lat},{lon}')}",
            "email": f"mailto:?subject=📍 My Location&body=📍 I'm at {location_desc} ({lat:.6f}, {lon:.6f})%0A%0AView on Google Maps: https://maps.google.com/?q={lat},{lon}",
            "sms": f"sms:?body=📍 I'm at {location_desc} ({lat:.6f}, {lon:.6f})",
            "qr_code_data": f"https://maps.google.com/?q={lat},{lon}",
            "deep_link": f"geo:{lat},{lon}?q={urllib.parse.quote(location_desc)}",
            "custom_share": f"📍 I'm at {location_desc} ({lat:.6f}, {lon:.6f})%0A%0A🌤️ Weather: {location['weather']} | 🌡️ {location['temperature']:.1f}°C%0A🚦 Traffic: {location['traffic']} | 🚗 {location['speed']:.1f} km/h%0A%0A🗺️ View on Google Maps: https://maps.google.com/?q={lat},{lon}"
        }
        
        return links
    
    def start_tracking(self):
        """Start advanced location tracking."""
        print("🚀 Starting advanced location tracking...")
        self.is_tracking = True
        
        tracking_thread = threading.Thread(target=self.tracking_loop)
        tracking_thread.daemon = True
        tracking_thread.start()
        
        return tracking_thread
    
    def tracking_loop(self):
        """Enhanced tracking loop with additional features."""
        while self.is_tracking:
            try:
                location = self.get_current_location()
                self.current_location = location
                self.location_history.append(location)
                
                if len(self.location_history) > 100:
                    self.location_history = self.location_history[-100:]
                
                self.log_location(location)
                time.sleep(self.tracking_interval)
                
            except Exception as e:
                print(f"❌ Tracking error: {e}")
                time.sleep(1)
    
    def stop_tracking(self):
        """Stop location tracking."""
        self.is_tracking = False
        print("🛑 Advanced location tracking stopped")
    
    def log_location(self, location):
        """Log enhanced location data."""
        log_entry = {
            "timestamp": location["timestamp"],
            "location": location["name"],
            "coordinates": f"{location['lat']:.6f}, {location['lon']:.6f}",
            "weather": location["weather"],
            "temperature": location["temperature"],
            "traffic": location["traffic"],
            "speed": location["speed"],
            "battery": location["battery_level"]
        }
        
        with open(self.log_file, "a") as f:
            f.write(json.dumps(log_entry) + "\n")
    
    def get_location_history(self, limit=10):
        """Get recent location history."""
        return self.location_history[-limit:] if self.location_history else []
    
    def get_distance_traveled(self):
        """Calculate total distance traveled."""
        if len(self.location_history) < 2:
            return 0
        
        total_distance = 0
        for i in range(1, len(self.location_history)):
            prev = self.location_history[i-1]
            curr = self.location_history[i]
            distance = self.calculate_distance(
                prev["lat"], prev["lon"],
                curr["lat"], curr["lon"]
            )
            total_distance += distance
        
        return total_distance
    
    def get_current_status(self):
        """Get comprehensive tracking status."""
        status = {
            "tracking_active": self.is_tracking,
            "current_location": self.current_location["name"] if self.current_location else "Unknown",
            "total_locations": len(self.location_history),
            "distance_traveled": f"{self.get_distance_traveled():.2f} km",
            "tracking_interval": f"{self.tracking_interval}s",
            "weather_enabled": self.weather_enabled,
            "traffic_enabled": self.traffic_enabled,
            "route_mode": self.route_mode,
            "social_sharing": self.social_sharing
        }
        return status

class AdvancedLocationGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("📍 Advanced Location Tracker")
        self.root.geometry("1200x900")
        self.root.configure(bg='#1a1a1a')
        
        self.tracker = AdvancedLocationTracker()
        self.tracking_thread = None
        self.is_tracking = False
        
        self.setup_gui()
    
    def setup_gui(self):
        """Setup the advanced GUI interface."""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="📍 Advanced Location Tracker", 
                               font=("Arial", 18, "bold"))
        title_label.grid(row=0, column=0, columnspan=4, pady=(0, 20))
        
        # Control Panel
        control_frame = ttk.LabelFrame(main_frame, text="Advanced Controls", padding="10")
        control_frame.grid(row=1, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Control Buttons
        button_frame = ttk.Frame(control_frame)
        button_frame.grid(row=0, column=0, columnspan=4, pady=(0, 10))
        
        self.start_button = ttk.Button(button_frame, text="🚀 Start Tracking", 
                                      command=self.start_tracking)
        self.start_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.stop_button = ttk.Button(button_frame, text="🛑 Stop Tracking", 
                                     command=self.stop_tracking, state="disabled")
        self.stop_button.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(button_frame, text="📊 Status", command=self.show_status).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="📜 History", command=self.show_history).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="🗺️ Map", command=self.open_map).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="🔗 Share Links", command=self.show_share_links).pack(side=tk.LEFT)
        
        # Feature toggles
        toggle_frame = ttk.Frame(control_frame)
        toggle_frame.grid(row=1, column=0, columnspan=4, pady=(10, 0))
        
        self.weather_var = tk.BooleanVar(value=True)
        self.traffic_var = tk.BooleanVar(value=True)
        self.route_var = tk.BooleanVar(value=False)
        self.social_var = tk.BooleanVar(value=False)
        
        ttk.Checkbutton(toggle_frame, text="🌤️ Weather", variable=self.weather_var).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Checkbutton(toggle_frame, text="🚦 Traffic", variable=self.traffic_var).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Checkbutton(toggle_frame, text="🗺️ Route Mode", variable=self.route_var).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Checkbutton(toggle_frame, text="📤 Social Sharing", variable=self.social_var).pack(side=tk.LEFT)
        
        # Location Display
        location_frame = ttk.LabelFrame(main_frame, text="Current Location", padding="10")
        location_frame.grid(row=2, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=(0, 10))
        location_frame.columnconfigure(1, weight=1)
        
        # Location info labels
        self.location_labels = {}
        location_info = [
            ("city", "🌍 City:"),
            ("country", "🏳️ Country:"),
            ("coordinates", "📍 Coordinates:"),
            ("timezone", "⏰ Timezone:"),
            ("population", "👥 Population:"),
            ("accuracy", "🎯 Accuracy:"),
            ("speed", "🚗 Speed:"),
            ("heading", "🧭 Heading:"),
            ("altitude", "⛰️ Altitude:")
        ]
        
        for i, (key, label) in enumerate(location_info):
            row = i // 2
            col = (i % 2) * 2
            ttk.Label(location_frame, text=label).grid(row=row, column=col, sticky=tk.W, pady=2)
            self.location_labels[key] = ttk.Label(location_frame, text="--", font=("Arial", 10, "bold"))
            self.location_labels[key].grid(row=row, column=col+1, sticky=tk.W, padx=(10, 0), pady=2)
        
        # Weather and Traffic Display
        info_frame = ttk.Frame(main_frame)
        info_frame.grid(row=3, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=(0, 10))
        info_frame.columnconfigure(0, weight=1)
        info_frame.columnconfigure(1, weight=1)
        
        # Weather Frame
        weather_frame = ttk.LabelFrame(info_frame, text="🌤️ Weather Information", padding="10")
        weather_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        
        self.weather_labels = {}
        weather_info = [
            ("condition", "Condition:"),
            ("temperature", "Temperature:"),
            ("humidity", "Humidity:"),
            ("feels_like", "Feels Like:"),
            ("wind_speed", "Wind Speed:"),
            ("visibility", "Visibility:")
        ]
        
        for i, (key, label) in enumerate(weather_info):
            ttk.Label(weather_frame, text=label).grid(row=i, column=0, sticky=tk.W, pady=1)
            self.weather_labels[key] = ttk.Label(weather_frame, text="--", font=("Arial", 9))
            self.weather_labels[key].grid(row=i, column=1, sticky=tk.W, padx=(5, 0), pady=1)
        
        # Traffic Frame
        traffic_frame = ttk.LabelFrame(info_frame, text="🚦 Traffic Information", padding="10")
        traffic_frame.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(5, 0))
        
        self.traffic_labels = {}
        traffic_info = [
            ("condition", "Condition:"),
            ("delay_minutes", "Delay:"),
            ("average_speed", "Avg Speed:"),
            ("congestion_level", "Congestion:"),
            ("incidents", "Incidents:"),
            ("road_conditions", "Road Condition:")
        ]
        
        for i, (key, label) in enumerate(traffic_info):
            ttk.Label(traffic_frame, text=label).grid(row=i, column=0, sticky=tk.W, pady=1)
            self.traffic_labels[key] = ttk.Label(traffic_frame, text="--", font=("Arial", 9))
            self.traffic_labels[key].grid(row=i, column=1, sticky=tk.W, padx=(5, 0), pady=1)
        
        # Device Info Frame
        device_frame = ttk.LabelFrame(main_frame, text="📱 Device Information", padding="10")
        device_frame.grid(row=4, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=(0, 10))
        device_frame.columnconfigure(1, weight=1)
        
        self.device_labels = {}
        device_info = [
            ("battery", "🔋 Battery:"),
            ("signal", "📶 Signal:"),
            ("network", "🌐 Network:"),
            ("timestamp", "⏰ Last Update:")
        ]
        
        for i, (key, label) in enumerate(device_info):
            ttk.Label(device_frame, text=label).grid(row=i, column=0, sticky=tk.W, pady=2)
            self.device_labels[key] = ttk.Label(device_frame, text="--", font=("Arial", 10, "bold"))
            self.device_labels[key].grid(row=i, column=1, sticky=tk.W, padx=(10, 0), pady=2)
        
        # Status Display
        status_frame = ttk.LabelFrame(main_frame, text="📊 Tracking Status", padding="10")
        status_frame.grid(row=5, column=0, columnspan=4, sticky=(tk.W, tk.E, tk.N, tk.S))
        status_frame.columnconfigure(0, weight=1)
        status_frame.rowconfigure(0, weight=1)
        
        self.status_text = tk.Text(status_frame, height=8, width=80, bg='#2a2a2a', fg='#00ff00')
        status_scrollbar = ttk.Scrollbar(status_frame, orient="vertical", command=self.status_text.yview)
        self.status_text.configure(yscrollcommand=status_scrollbar.set)
        
        self.status_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        status_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        self.update_location_display()
    
    def start_tracking(self):
        """Start the tracking process."""
        if not self.is_tracking:
            self.is_tracking = True
            self.start_button.config(state="disabled")
            self.stop_button.config(state="normal")
            
            # Update tracker settings
            self.tracker.weather_enabled = self.weather_var.get()
            self.tracker.traffic_enabled = self.traffic_var.get()
            self.tracker.route_mode = self.route_var.get()
            self.tracker.social_sharing = self.social_var.get()
            
            # Start tracking thread
            self.tracking_thread = threading.Thread(target=self.tracking_loop)
            self.tracking_thread.daemon = True
            self.tracking_thread.start()
            
            self.log_message("🚀 Advanced location tracking started")
            self.update_location_display()
    
    def stop_tracking(self):
        """Stop the tracking process."""
        if self.is_tracking:
            self.is_tracking = False
            self.tracker.stop_tracking()
            self.start_button.config(state="normal")
            self.stop_button.config(state="disabled")
            
            self.log_message("🛑 Advanced location tracking stopped")
            self.update_location_display()
    
    def tracking_loop(self):
        """Main tracking loop."""
        while self.is_tracking:
            try:
                location = self.tracker.get_current_location()
                self.tracker.current_location = location
                self.tracker.location_history.append(location)
                
                if len(self.tracker.location_history) > 100:
                    self.tracker.location_history = self.tracker.location_history[-100:]
                
                self.tracker.log_location(location)
                
                # Update GUI
                self.root.after(0, self.update_location_display)
                
                time.sleep(2)
                
            except Exception as e:
                self.root.after(0, self.log_message, f"Error: {str(e)}")
                time.sleep(1)
    
    def update_location_display(self):
        """Update all location displays."""
        if self.tracker.current_location:
            location = self.tracker.current_location
            details = self.tracker.get_location_details(location)
            
            # Update basic location info
            for key, label in self.location_labels.items():
                if key in details["basic_info"]:
                    label.config(text=details["basic_info"][key])
                elif key in details["gps_info"]:
                    label.config(text=details["gps_info"][key])
            
            # Update weather info
            if self.tracker.weather_enabled:
                for key, label in self.weather_labels.items():
                    if key in details["weather"]:
                        label.config(text=details["weather"][key])
            
            # Update traffic info
            if self.tracker.traffic_enabled:
                for key, label in self.traffic_labels.items():
                    if key in details["traffic"]:
                        label.config(text=details["traffic"][key])
            
            # Update device info
            for key, label in self.device_labels.items():
                if key in details["device_info"]:
                    label.config(text=details["device_info"][key])
        
        # Update status
        status = self.tracker.get_current_status()
        status_display = f"📊 ADVANCED TRACKING STATUS\n"
        status_display += f"{'='*40}\n"
        status_display += f"Active: {status['tracking_active']}\n"
        status_display += f"Current: {status['current_location']}\n"
        status_display += f"Total: {status['total_locations']}\n"
        status_display += f"Distance: {status['distance_traveled']}\n"
        status_display += f"Weather: {'ON' if status['weather_enabled'] else 'OFF'}\n"
        status_display += f"Traffic: {'ON' if status['traffic_enabled'] else 'OFF'}\n"
        status_display += f"Route Mode: {'ON' if status['route_mode'] else 'OFF'}\n"
        status_display += f"Social Sharing: {'ON' if status['social_sharing'] else 'OFF'}"
        
        self.status_text.delete(1.0, tk.END)
        self.status_text.insert(tk.END, status_display)
    
    def show_status(self):
        """Show detailed tracking status."""
        status = self.tracker.get_current_status()
        
        status_window = tk.Toplevel(self.root)
        status_window.title("Advanced Tracking Status")
        status_window.geometry("500x400")
        
        status_text = tk.Text(status_window, bg='#2a2a2a', fg='#ffffff')
        status_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        status_display = "📊 ADVANCED TRACKING STATUS\n"
        status_display += "=" * 40 + "\n\n"
        
        for key, value in status.items():
            status_display += f"{key.replace('_', ' ').title()}: {value}\n"
        
        if self.tracker.current_location:
            location = self.tracker.current_location
            status_display += f"\n📍 CURRENT LOCATION:\n"
            status_display += f"City: {location['name']}\n"
            status_display += f"Country: {location['country']}\n"
            status_display += f"Coordinates: {location['lat']:.6f}, {location['lon']:.6f}\n"
            status_display += f"Weather: {location['weather']}\n"
            status_display += f"Temperature: {location['temperature']:.1f}°C\n"
            status_display += f"Traffic: {location['traffic']}\n"
            status_display += f"Speed: {location['speed']:.1f} km/h\n"
            status_display += f"Battery: {location['battery_level']:.0f}%\n"
        
        status_text.insert(tk.END, status_display)
        status_text.config(state=tk.DISABLED)
    
    def show_history(self):
        """Show location history."""
        history = self.tracker.get_location_history(20)
        
        history_window = tk.Toplevel(self.root)
        history_window.title("Advanced Location History")
        history_window.geometry("700x500")
        
        history_text = tk.Text(history_window, bg='#2a2a2a', fg='#00ff00')
        history_scrollbar = ttk.Scrollbar(history_window, orient="vertical", command=history_text.yview)
        history_text.configure(yscrollcommand=history_scrollbar.set)
        
        history_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        history_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        history_display = "📜 ADVANCED LOCATION HISTORY\n"
        history_display += "=" * 60 + "\n\n"
        
        for i, location in enumerate(reversed(history), 1):
            history_display += f"{i:2d}. {location['name']}, {location['country']}\n"
            history_display += f"    📍 {location['lat']:.6f}, {location['lon']:.6f}\n"
            history_display += f"    🌤️ {location['weather']} | 🌡️ {location['temperature']:.1f}°C\n"
            history_display += f"    🚦 {location['traffic']} | 🚗 {location['speed']:.1f} km/h\n"
            history_display += f"    🔋 {location['battery_level']:.0f}% | 📶 {location['signal_strength']:.0f}/5\n"
            history_display += f"    ⏰ {location['timestamp']}\n"
            history_display += "-" * 50 + "\n"
        
        history_text.insert(tk.END, history_display)
        history_text.config(state=tk.DISABLED)
    
    def open_map(self):
        """Open location in web map."""
        if self.tracker.current_location:
            location = self.tracker.current_location
            url = f"https://www.google.com/maps?q={location['lat']},{location['lon']}"
            webbrowser.open(url)
            self.log_message("🗺️ Opening location in web map")
        else:
            messagebox.showinfo("Map", "No current location available")
    
    def show_share_links(self):
        """Show comprehensive shareable links window."""
        if not self.tracker.current_location:
            messagebox.showinfo("Share Links", "No current location available")
            return
        
        location = self.tracker.current_location
        links = self.tracker.generate_shareable_links(location)
        
        # Create share links window
        share_window = tk.Toplevel(self.root)
        share_window.title("🔗 Shareable Location Links")
        share_window.geometry("800x600")
        
        # Main frame
        main_frame = ttk.Frame(share_window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="🔗 Shareable Location Links", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Location info
        location_info = ttk.LabelFrame(main_frame, text="📍 Current Location", padding="10")
        location_info.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(location_info, text=f"🌍 {location['name']}, {location['country']}", 
                 font=("Arial", 12, "bold")).pack()
        ttk.Label(location_info, text=f"📍 {location['lat']:.6f}, {location['lon']:.6f}").pack()
        ttk.Label(location_info, text=f"🌤️ {location['weather']} | 🌡️ {location['temperature']:.1f}°C").pack()
        
        # Create notebook for different categories
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Maps tab
        maps_frame = ttk.Frame(notebook)
        notebook.add(maps_frame, text="🗺️ Maps")
        
        maps_links = [
            ("Google Maps", links["google_maps"], "🌐"),
            ("Apple Maps", links["apple_maps"], "🍎"),
            ("Waze", links["waze"], "🚗"),
            ("Bing Maps", links["bing_maps"], "🔍"),
            ("OpenStreetMap", links["openstreetmap"], "🗺️")
        ]
        
        for name, url, icon in maps_links:
            frame = ttk.Frame(maps_frame)
            frame.pack(fill=tk.X, pady=2)
            ttk.Label(frame, text=f"{icon} {name}").pack(side=tk.LEFT)
            ttk.Button(frame, text="🔗 Open", 
                      command=lambda u=url: webbrowser.open(u)).pack(side=tk.RIGHT)
            ttk.Button(frame, text="📋 Copy", 
                      command=lambda u=url: self.copy_to_clipboard(u)).pack(side=tk.RIGHT, padx=(0, 5))
        
        # Social Media tab
        social_frame = ttk.Frame(notebook)
        notebook.add(social_frame, text="📱 Social")
        
        social_links = [
            ("WhatsApp", links["whatsapp"], "💬"),
            ("Telegram", links["telegram"], "📱"),
            ("Twitter", links["twitter"], "🐦"),
            ("Facebook", links["facebook"], "📘"),
            ("LinkedIn", links["linkedin"], "💼")
        ]
        
        for name, url, icon in social_links:
            frame = ttk.Frame(social_frame)
            frame.pack(fill=tk.X, pady=2)
            ttk.Label(frame, text=f"{icon} {name}").pack(side=tk.LEFT)
            ttk.Button(frame, text="🔗 Open", 
                      command=lambda u=url: webbrowser.open(u)).pack(side=tk.RIGHT)
            ttk.Button(frame, text="📋 Copy", 
                      command=lambda u=url: self.copy_to_clipboard(u)).pack(side=tk.RIGHT, padx=(0, 5))
        
        # Communication tab
        comm_frame = ttk.Frame(notebook)
        notebook.add(comm_frame, text="📧 Communication")
        
        comm_links = [
            ("Email", links["email"], "📧"),
            ("SMS", links["sms"], "💬"),
            ("Deep Link", links["deep_link"], "🔗")
        ]
        
        for name, url, icon in comm_links:
            frame = ttk.Frame(comm_frame)
            frame.pack(fill=tk.X, pady=2)
            ttk.Label(frame, text=f"{icon} {name}").pack(side=tk.LEFT)
            ttk.Button(frame, text="🔗 Open", 
                      command=lambda u=url: webbrowser.open(u)).pack(side=tk.RIGHT)
            ttk.Button(frame, text="📋 Copy", 
                      command=lambda u=url: self.copy_to_clipboard(u)).pack(side=tk.RIGHT, padx=(0, 5))
        
        # Custom Share tab
        custom_frame = ttk.Frame(notebook)
        notebook.add(custom_frame, text="📤 Custom")
        
        # Custom share text
        custom_text = ttk.Text(custom_frame, height=8, width=70)
        custom_text.pack(pady=10)
        custom_text.insert(tk.END, links["custom_share"])
        
        # Buttons for custom share
        custom_buttons = ttk.Frame(custom_frame)
        custom_buttons.pack(pady=10)
        
        ttk.Button(custom_buttons, text="📋 Copy Text", 
                  command=lambda: self.copy_to_clipboard(custom_text.get(1.0, tk.END).strip())).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(custom_buttons, text="🔗 Copy Google Maps Link", 
                  command=lambda: self.copy_to_clipboard(links["google_maps"])).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(custom_buttons, text="📱 Copy QR Code Data", 
                  command=lambda: self.copy_to_clipboard(links["qr_code_data"])).pack(side=tk.LEFT)
        
        # Quick actions frame
        quick_frame = ttk.LabelFrame(main_frame, text="⚡ Quick Actions", padding="10")
        quick_frame.pack(fill=tk.X, pady=(20, 0))
        
        quick_buttons = ttk.Frame(quick_frame)
        quick_buttons.pack()
        
        ttk.Button(quick_buttons, text="🗺️ Open Google Maps", 
                  command=lambda: webbrowser.open(links["google_maps"])).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(quick_buttons, text="💬 Share on WhatsApp", 
                  command=lambda: webbrowser.open(links["whatsapp"])).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(quick_buttons, text="📱 Share on Telegram", 
                  command=lambda: webbrowser.open(links["telegram"])).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(quick_buttons, text="📧 Send Email", 
                  command=lambda: webbrowser.open(links["email"])).pack(side=tk.LEFT)
        
        self.log_message("🔗 Shareable links window opened")
    
    def copy_to_clipboard(self, text):
        """Copy text to clipboard."""
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.log_message("📋 Link copied to clipboard")
        messagebox.showinfo("Copy", "Link copied to clipboard!")
    
    def share_location(self):
        """Share current location."""
        if self.tracker.current_location:
            location = self.tracker.current_location
            share_text = f"📍 I'm at {location['name']}, {location['country']} ({location['lat']:.6f}, {location['lon']:.6f})"
            self.root.clipboard_clear()
            self.root.clipboard_append(share_text)
            self.log_message("📤 Location copied to clipboard")
            messagebox.showinfo("Share", "Location copied to clipboard!")
        else:
            messagebox.showinfo("Share", "No current location available")
    
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
    """Main function to run the advanced GUI."""
    root = tk.Tk()
    app = AdvancedLocationGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
