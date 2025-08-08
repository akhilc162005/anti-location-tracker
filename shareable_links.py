#!/usr/bin/env python3
"""
Shareable Links Generator for Location Tracker
Generate various types of shareable links for GPS locations.
"""

import urllib.parse
import webbrowser
import tkinter as tk
from tkinter import ttk, messagebox

class ShareableLinksGenerator:
    def __init__(self):
        """Initialize the shareable links generator."""
        self.supported_platforms = {
            "maps": ["Google Maps", "Apple Maps", "Waze", "Bing Maps", "OpenStreetMap"],
            "social": ["WhatsApp", "Telegram", "Twitter", "Facebook", "LinkedIn"],
            "communication": ["Email", "SMS", "Deep Link"],
            "custom": ["Custom Text", "QR Code Data", "Short Link"]
        }
    
    def generate_links(self, location):
        """Generate comprehensive shareable links for a location."""
        lat, lon = location["lat"], location["lon"]
        city_name = location["name"]
        country = location["country"]
        weather = location.get("weather", "Unknown")
        temperature = location.get("temperature", 0)
        traffic = location.get("traffic", "Unknown")
        speed = location.get("speed", 0)
        
        # Create location description
        location_desc = f"{city_name}, {country}"
        
        # Generate different types of shareable links
        links = {
            # Map Services
            "google_maps": f"https://www.google.com/maps?q={lat},{lon}",
            "apple_maps": f"https://maps.apple.com/?q={lat},{lon}",
            "waze": f"https://waze.com/ul?ll={lat},{lon}&navigate=yes",
            "bing_maps": f"https://www.bing.com/maps?cp={lat}~{lon}&lvl=15",
            "openstreetmap": f"https://www.openstreetmap.org/?mlat={lat}&mlon={lon}&zoom=15",
            
            # Social Media
            "whatsapp": f"https://wa.me/?text=📍 I'm at {location_desc} ({lat:.6f}, {lon:.6f})",
            "telegram": f"https://t.me/share/url?url={urllib.parse.quote(f'https://maps.google.com/?q={lat},{lon}')}&text=📍 I'm at {location_desc}",
            "twitter": f"https://twitter.com/intent/tweet?text=📍 I'm at {location_desc} ({lat:.6f}, {lon:.6f})&url={urllib.parse.quote(f'https://maps.google.com/?q={lat},{lon}')}",
            "facebook": f"https://www.facebook.com/sharer/sharer.php?u={urllib.parse.quote(f'https://maps.google.com/?q={lat},{lon}')}",
            "linkedin": f"https://www.linkedin.com/sharing/share-offsite/?url={urllib.parse.quote(f'https://maps.google.com/?q={lat},{lon}')}",
            
            # Communication
            "email": f"mailto:?subject=📍 My Location&body=📍 I'm at {location_desc} ({lat:.6f}, {lon:.6f})%0A%0AView on Google Maps: https://maps.google.com/?q={lat},{lon}",
            "sms": f"sms:?body=📍 I'm at {location_desc} ({lat:.6f}, {lon:.6f})",
            "deep_link": f"geo:{lat},{lon}?q={urllib.parse.quote(location_desc)}",
            
            # Custom Formats
            "qr_code_data": f"https://maps.google.com/?q={lat},{lon}",
            "custom_share": f"📍 I'm at {location_desc} ({lat:.6f}, {lon:.6f})%0A%0A🌤️ Weather: {weather} | 🌡️ {temperature:.1f}°C%0A🚦 Traffic: {traffic} | 🚗 {speed:.1f} km/h%0A%0A🗺️ View on Google Maps: https://maps.google.com/?q={lat},{lon}",
            "short_text": f"📍 {location_desc} ({lat:.6f}, {lon:.6f})",
            "detailed_text": f"📍 Location: {location_desc}%0A🌤️ Weather: {weather} | 🌡️ {temperature:.1f}°C%0A🚦 Traffic: {traffic} | 🚗 {speed:.1f} km/h%0A🗺️ Maps: https://maps.google.com/?q={lat},{lon}"
        }
        
        return links
    
    def open_link(self, url):
        """Open a link in the default browser."""
        try:
            webbrowser.open(url)
            return True
        except Exception as e:
            print(f"Error opening link: {e}")
            return False
    
    def copy_to_clipboard(self, text, root):
        """Copy text to clipboard."""
        try:
            root.clipboard_clear()
            root.clipboard_append(text)
            return True
        except Exception as e:
            print(f"Error copying to clipboard: {e}")
            return False

class ShareableLinksGUI:
    def __init__(self, root, location_data):
        self.root = root
        self.location_data = location_data
        self.generator = ShareableLinksGenerator()
        self.links = self.generator.generate_links(location_data)
        
        self.setup_gui()
    
    def setup_gui(self):
        """Setup the shareable links GUI."""
        # Main window setup
        self.root.title("🔗 Shareable Location Links")
        self.root.geometry("900x700")
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="🔗 Shareable Location Links", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Location info
        location_info = ttk.LabelFrame(main_frame, text="📍 Current Location", padding="10")
        location_info.pack(fill=tk.X, pady=(0, 20))
        
        location = self.location_data
        ttk.Label(location_info, text=f"🌍 {location['name']}, {location['country']}", 
                 font=("Arial", 12, "bold")).pack()
        ttk.Label(location_info, text=f"📍 {location['lat']:.6f}, {location['lon']:.6f}").pack()
        ttk.Label(location_info, text=f"🌤️ {location.get('weather', 'Unknown')} | 🌡️ {location.get('temperature', 0):.1f}°C").pack()
        
        # Create notebook for different categories
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Maps tab
        self.create_maps_tab(notebook)
        
        # Social Media tab
        self.create_social_tab(notebook)
        
        # Communication tab
        self.create_communication_tab(notebook)
        
        # Custom tab
        self.create_custom_tab(notebook)
        
        # Quick actions
        self.create_quick_actions(main_frame)
    
    def create_maps_tab(self, notebook):
        """Create the maps tab."""
        maps_frame = ttk.Frame(notebook)
        notebook.add(maps_frame, text="🗺️ Maps")
        
        maps_links = [
            ("Google Maps", self.links["google_maps"], "🌐"),
            ("Apple Maps", self.links["apple_maps"], "🍎"),
            ("Waze", self.links["waze"], "🚗"),
            ("Bing Maps", self.links["bing_maps"], "🔍"),
            ("OpenStreetMap", self.links["openstreetmap"], "🗺️")
        ]
        
        for name, url, icon in maps_links:
            frame = ttk.Frame(maps_frame)
            frame.pack(fill=tk.X, pady=2, padx=10)
            ttk.Label(frame, text=f"{icon} {name}").pack(side=tk.LEFT)
            ttk.Button(frame, text="🔗 Open", 
                      command=lambda u=url: self.open_link(u)).pack(side=tk.RIGHT)
            ttk.Button(frame, text="📋 Copy", 
                      command=lambda u=url: self.copy_link(u)).pack(side=tk.RIGHT, padx=(0, 5))
    
    def create_social_tab(self, notebook):
        """Create the social media tab."""
        social_frame = ttk.Frame(notebook)
        notebook.add(social_frame, text="📱 Social")
        
        social_links = [
            ("WhatsApp", self.links["whatsapp"], "💬"),
            ("Telegram", self.links["telegram"], "📱"),
            ("Twitter", self.links["twitter"], "🐦"),
            ("Facebook", self.links["facebook"], "📘"),
            ("LinkedIn", self.links["linkedin"], "💼")
        ]
        
        for name, url, icon in social_links:
            frame = ttk.Frame(social_frame)
            frame.pack(fill=tk.X, pady=2, padx=10)
            ttk.Label(frame, text=f"{icon} {name}").pack(side=tk.LEFT)
            ttk.Button(frame, text="🔗 Open", 
                      command=lambda u=url: self.open_link(u)).pack(side=tk.RIGHT)
            ttk.Button(frame, text="📋 Copy", 
                      command=lambda u=url: self.copy_link(u)).pack(side=tk.RIGHT, padx=(0, 5))
    
    def create_communication_tab(self, notebook):
        """Create the communication tab."""
        comm_frame = ttk.Frame(notebook)
        notebook.add(comm_frame, text="📧 Communication")
        
        comm_links = [
            ("Email", self.links["email"], "📧"),
            ("SMS", self.links["sms"], "💬"),
            ("Deep Link", self.links["deep_link"], "🔗")
        ]
        
        for name, url, icon in comm_links:
            frame = ttk.Frame(comm_frame)
            frame.pack(fill=tk.X, pady=2, padx=10)
            ttk.Label(frame, text=f"{icon} {name}").pack(side=tk.LEFT)
            ttk.Button(frame, text="🔗 Open", 
                      command=lambda u=url: self.open_link(u)).pack(side=tk.RIGHT)
            ttk.Button(frame, text="📋 Copy", 
                      command=lambda u=url: self.copy_link(u)).pack(side=tk.RIGHT, padx=(0, 5))
    
    def create_custom_tab(self, notebook):
        """Create the custom sharing tab."""
        custom_frame = ttk.Frame(notebook)
        notebook.add(custom_frame, text="📤 Custom")
        
        # Custom share text
        custom_text = tk.Text(custom_frame, height=8, width=70)
        custom_text.pack(pady=10, padx=10)
        custom_text.insert(tk.END, self.links["custom_share"])
        
        # Buttons for custom share
        custom_buttons = ttk.Frame(custom_frame)
        custom_buttons.pack(pady=10)
        
        ttk.Button(custom_buttons, text="📋 Copy Text", 
                  command=lambda: self.copy_text(custom_text.get(1.0, tk.END).strip())).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(custom_buttons, text="🔗 Copy Google Maps Link", 
                  command=lambda: self.copy_link(self.links["google_maps"])).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(custom_buttons, text="📱 Copy QR Code Data", 
                  command=lambda: self.copy_link(self.links["qr_code_data"])).pack(side=tk.LEFT)
        
        # Additional custom formats
        formats_frame = ttk.LabelFrame(custom_frame, text="📝 Custom Formats", padding="10")
        formats_frame.pack(fill=tk.X, pady=10, padx=10)
        
        ttk.Button(formats_frame, text="📋 Short Text", 
                  command=lambda: self.copy_text(self.links["short_text"])).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(formats_frame, text="📋 Detailed Text", 
                  command=lambda: self.copy_text(self.links["detailed_text"])).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(formats_frame, text="📋 Coordinates Only", 
                  command=lambda: self.copy_text(f"{self.location_data['lat']:.6f}, {self.location_data['lon']:.6f}")).pack(side=tk.LEFT)
    
    def create_quick_actions(self, main_frame):
        """Create quick action buttons."""
        quick_frame = ttk.LabelFrame(main_frame, text="⚡ Quick Actions", padding="10")
        quick_frame.pack(fill=tk.X, pady=(20, 0))
        
        quick_buttons = ttk.Frame(quick_frame)
        quick_buttons.pack()
        
        ttk.Button(quick_buttons, text="🗺️ Open Google Maps", 
                  command=lambda: self.open_link(self.links["google_maps"])).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(quick_buttons, text="💬 Share on WhatsApp", 
                  command=lambda: self.open_link(self.links["whatsapp"])).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(quick_buttons, text="📱 Share on Telegram", 
                  command=lambda: self.open_link(self.links["telegram"])).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(quick_buttons, text="📧 Send Email", 
                  command=lambda: self.open_link(self.links["email"])).pack(side=tk.LEFT)
    
    def open_link(self, url):
        """Open a link in the browser."""
        if self.generator.open_link(url):
            messagebox.showinfo("Success", "Link opened in browser!")
        else:
            messagebox.showerror("Error", "Failed to open link")
    
    def copy_link(self, url):
        """Copy a link to clipboard."""
        if self.generator.copy_to_clipboard(url, self.root):
            messagebox.showinfo("Success", "Link copied to clipboard!")
        else:
            messagebox.showerror("Error", "Failed to copy link")
    
    def copy_text(self, text):
        """Copy text to clipboard."""
        if self.generator.copy_to_clipboard(text, self.root):
            messagebox.showinfo("Success", "Text copied to clipboard!")
        else:
            messagebox.showerror("Error", "Failed to copy text")

def demo_shareable_links():
    """Demo function to test shareable links."""
    # Sample location data
    sample_location = {
        "name": "New York",
        "lat": 40.7128,
        "lon": -74.0060,
        "country": "USA",
        "weather": "Sunny",
        "temperature": 22.5,
        "traffic": "Moderate",
        "speed": 35.2
    }
    
    root = tk.Tk()
    app = ShareableLinksGUI(root, sample_location)
    root.mainloop()

if __name__ == "__main__":
    demo_shareable_links()
