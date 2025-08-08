#!/usr/bin/env python3
"""
Live Location Tracker
Real-time GPS location tracking and display system.
"""

import time
import random
import threading
from datetime import datetime
import json
import os
from math import radians, cos, sin, sqrt, atan2

class LiveLocationTracker:
    def __init__(self):
        """Initialize the Live Location Tracker."""
        self.is_tracking = False
        self.current_location = None
        self.location_history = []
        self.tracking_interval = 1.0  # seconds
        self.log_file = "live_locations_log.txt"
        
        # Sample locations for demonstration
        self.sample_locations = [
            {"name": "New York", "lat": 40.7128, "lon": -74.0060, "country": "USA"},
            {"name": "London", "lat": 51.5074, "lon": -0.1278, "country": "UK"},
            {"name": "Tokyo", "lat": 35.6762, "lon": 139.6503, "country": "Japan"},
            {"name": "Paris", "lat": 48.8566, "lon": 2.3522, "country": "France"},
            {"name": "Sydney", "lat": -33.8688, "lon": 151.2093, "country": "Australia"},
            {"name": "Moscow", "lat": 55.7558, "lon": 37.6176, "country": "Russia"},
            {"name": "Beijing", "lat": 39.9042, "lon": 116.4074, "country": "China"},
            {"name": "Dubai", "lat": 25.2048, "lon": 55.2708, "country": "UAE"},
            {"name": "Singapore", "lat": 1.3521, "lon": 103.8198, "country": "Singapore"},
            {"name": "Mumbai", "lat": 19.0760, "lon": 72.8777, "country": "India"}
        ]
        
        print("📍 Live Location Tracker Initialized")
        print("=" * 50)
    
    def get_current_location(self):
        """Get current GPS location (simulated)."""
        # Simulate GPS location acquisition
        location = random.choice(self.sample_locations)
        
        # Add some random variation to simulate movement
        lat_variation = random.uniform(-0.001, 0.001)
        lon_variation = random.uniform(-0.001, 0.001)
        
        current_location = {
            "name": location["name"],
            "lat": location["lat"] + lat_variation,
            "lon": location["lon"] + lon_variation,
            "country": location["country"],
            "timestamp": datetime.now().isoformat(),
            "accuracy": random.uniform(5, 20),  # meters
            "speed": random.uniform(0, 50),  # km/h
            "heading": random.uniform(0, 360),  # degrees
            "altitude": random.uniform(0, 1000)  # meters
        }
        
        return current_location
    
    def calculate_distance(self, lat1, lon1, lat2, lon2):
        """Calculate distance between two GPS coordinates in kilometers."""
        R = 6371  # Earth's radius in kilometers
        
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        distance = R * c
        
        return distance
    
    def get_location_info(self, location):
        """Get detailed information about a location."""
        info = {
            "coordinates": f"{location['lat']:.6f}, {location['lon']:.6f}",
            "city": location["name"],
            "country": location["country"],
            "accuracy": f"{location['accuracy']:.1f}m",
            "speed": f"{location['speed']:.1f} km/h",
            "heading": f"{location['heading']:.1f}°",
            "altitude": f"{location['altitude']:.0f}m",
            "timestamp": location["timestamp"]
        }
        return info
    
    def start_tracking(self):
        """Start live location tracking."""
        print("🚀 Starting live location tracking...")
        self.is_tracking = True
        
        # Start tracking in a separate thread
        tracking_thread = threading.Thread(target=self.tracking_loop)
        tracking_thread.daemon = True
        tracking_thread.start()
        
        return tracking_thread
    
    def tracking_loop(self):
        """Main tracking loop."""
        while self.is_tracking:
            try:
                # Get current location
                location = self.get_current_location()
                self.current_location = location
                self.location_history.append(location)
                
                # Keep only last 100 locations
                if len(self.location_history) > 100:
                    self.location_history = self.location_history[-100:]
                
                # Log location
                self.log_location(location)
                
                # Wait before next update
                time.sleep(self.tracking_interval)
                
            except Exception as e:
                print(f"❌ Tracking error: {e}")
                time.sleep(1)
    
    def stop_tracking(self):
        """Stop live location tracking."""
        self.is_tracking = False
        print("🛑 Location tracking stopped")
    
    def log_location(self, location):
        """Log location data."""
        log_entry = {
            "timestamp": location["timestamp"],
            "location": location["name"],
            "coordinates": f"{location['lat']:.6f}, {location['lon']:.6f}",
            "speed": location["speed"],
            "accuracy": location["accuracy"]
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
        """Get current tracking status."""
        status = {
            "tracking_active": self.is_tracking,
            "current_location": self.current_location["name"] if self.current_location else "Unknown",
            "total_locations": len(self.location_history),
            "distance_traveled": f"{self.get_distance_traveled():.2f} km",
            "tracking_interval": f"{self.tracking_interval}s"
        }
        return status

def display_live_location():
    """Display live location information."""
    tracker = LiveLocationTracker()
    
    print("📍 LIVE LOCATION TRACKER")
    print("=" * 50)
    print("Real-time GPS location tracking")
    print("=" * 50)
    
    # Start tracking
    tracker.start_tracking()
    
    try:
        while True:
            if tracker.current_location:
                location = tracker.current_location
                info = tracker.get_location_info(location)
                
                # Clear screen (works on most terminals)
                os.system('cls' if os.name == 'nt' else 'clear')
                
                print("📍 LIVE LOCATION TRACKER")
                print("=" * 50)
                print(f"🌍 Location: {info['city']}, {info['country']}")
                print(f"📍 Coordinates: {info['coordinates']}")
                print(f"🎯 Accuracy: {info['accuracy']}")
                print(f"🚗 Speed: {info['speed']}")
                print(f"🧭 Heading: {info['heading']}")
                print(f"⛰️  Altitude: {info['altitude']}")
                print(f"⏰ Time: {info['timestamp']}")
                print("=" * 50)
                
                # Show recent history
                history = tracker.get_location_history(5)
                if history:
                    print("📜 Recent Locations:")
                    for i, loc in enumerate(history[-5:], 1):
                        print(f"  {i}. {loc['name']} ({loc['lat']:.4f}, {loc['lon']:.4f})")
                
                # Show status
                status = tracker.get_current_status()
                print(f"\n📊 Status: Tracking Active | Total: {status['total_locations']} | Distance: {status['distance_traveled']}")
                
            time.sleep(2)
            
    except KeyboardInterrupt:
        print("\n🛑 Stopping live location tracking...")
        tracker.stop_tracking()
        
        # Show final summary
        print("\n📊 TRACKING SUMMARY")
        print("=" * 30)
        status = tracker.get_current_status()
        for key, value in status.items():
            print(f"{key.replace('_', ' ').title()}: {value}")

def main():
    """Main function to run live location tracking."""
    display_live_location()

if __name__ == "__main__":
    main()
