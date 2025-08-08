#!/usr/bin/env python3
"""
Enhanced Shareable Links Generator
Advanced GPS location sharing with analytics, export, and additional platforms.
"""

import urllib.parse
import webbrowser
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
from datetime import datetime

class EnhancedShareableLinksGenerator:
    def __init__(self):
        """Initialize the enhanced shareable links generator."""
        # Professional color scheme
        self.colors = {
            "primary": "#2563eb",      # Blue
            "secondary": "#64748b",     # Slate
            "success": "#059669",       # Green
            "warning": "#d97706",       # Orange
            "danger": "#dc2626",        # Red
            "dark": "#1e293b",          # Dark slate
            "light": "#f8fafc",         # Light gray
            "white": "#ffffff",         # White
            "accent": "#7c3aed",        # Purple
            "gradient_start": "#3b82f6", # Blue gradient
            "gradient_end": "#1d4ed8"   # Darker blue
        }
        
        # Analytics tracking
        self.analytics = {"clicks": 0, "shares": 0, "copies": 0}
    
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
            "here_maps": f"https://wego.here.com/location?map=lat,{lat},lon,{lon}",
            
            # Social Media
            "whatsapp": f"https://wa.me/?text=📍 I'm at {location_desc} ({lat:.6f}, {lon:.6f})",
            "telegram": f"https://t.me/share/url?url={urllib.parse.quote(f'https://maps.google.com/?q={lat},{lon}')}&text=📍 I'm at {location_desc}",
            "twitter": f"https://twitter.com/intent/tweet?text=📍 I'm at {location_desc} ({lat:.6f}, {lon:.6f})&url={urllib.parse.quote(f'https://maps.google.com/?q={lat},{lon}')}",
            "facebook": f"https://www.facebook.com/sharer/sharer.php?u={urllib.parse.quote(f'https://maps.google.com/?q={lat},{lon}')}",
            "linkedin": f"https://www.linkedin.com/sharing/share-offsite/?url={urllib.parse.quote(f'https://maps.google.com/?q={lat},{lon}')}",
            "instagram": f"https://www.instagram.com/?url={urllib.parse.quote(f'https://maps.google.com/?q={lat},{lon}')}",
            "discord": f"https://discord.com/channels/@me?content=📍 I'm at {location_desc} ({lat:.6f}, {lon:.6f})",
            
            # Communication
            "email": f"mailto:?subject=📍 My Location&body=📍 I'm at {location_desc} ({lat:.6f}, {lon:.6f})%0A%0AView on Google Maps: https://maps.google.com/?q={lat},{lon}",
            "sms": f"sms:?body=📍 I'm at {location_desc} ({lat:.6f}, {lon:.6f})",
            "deep_link": f"geo:{lat},{lon}?q={urllib.parse.quote(location_desc)}",
            "skype": f"skype:?chat&topic=📍 I'm at {location_desc}",
            
            # Custom Formats
            "qr_code_data": f"https://maps.google.com/?q={lat},{lon}",
            "custom_share": f"📍 I'm at {location_desc} ({lat:.6f}, {lon:.6f})%0A%0A🌤️ Weather: {weather} | 🌡️ {temperature:.1f}°C%0A🚦 Traffic: {traffic} | 🚗 {speed:.1f} km/h%0A%0A🗺️ View on Google Maps: https://maps.google.com/?q={lat},{lon}",
            "short_text": f"📍 {location_desc} ({lat:.6f}, {lon:.6f})",
            "detailed_text": f"📍 Location: {location_desc}%0A🌤️ Weather: {weather} | 🌡️ {temperature:.1f}°C%0A🚦 Traffic: {traffic} | 🚗 {speed:.1f} km/h%0A🗺️ Maps: https://maps.google.com/?q={lat},{lon}",
            "rich_text": f"<h3>📍 My Location</h3><p><strong>{location_desc}</strong></p><p>Coordinates: {lat:.6f}, {lon:.6f}</p><p>Weather: {weather} | Temperature: {temperature:.1f}°C</p><p>Traffic: {traffic} | Speed: {speed:.1f} km/h</p><p><a href='https://maps.google.com/?q={lat},{lon}'>View on Google Maps</a></p>"
        }
        
        return links
    
    def export_data(self, location_data, links, format_type="json"):
        """Export location and links data."""
        export_data = {
            "timestamp": datetime.now().isoformat(),
            "location": location_data,
            "links": links,
            "analytics": self.analytics
        }
        
        if format_type == "json":
            return json.dumps(export_data, indent=2)
        elif format_type == "csv":
            csv_data = "Platform,URL\n"
            for platform, url in links.items():
                csv_data += f"{platform},{url}\n"
            return csv_data
        elif format_type == "txt":
            txt_data = f"Location: {location_data['name']}, {location_data['country']}\n"
            txt_data += f"Coordinates: {location_data['lat']:.6f}, {location_data['lon']:.6f}\n"
            txt_data += f"Weather: {location_data.get('weather', 'Unknown')}\n"
            txt_data += f"Temperature: {location_data.get('temperature', 0):.1f}°C\n\n"
            txt_data += "Shareable Links:\n"
            for platform, url in links.items():
                txt_data += f"{platform}: {url}\n"
            return txt_data
        
        return export_data
    
    def open_link(self, url):
        """Open a link in the default browser."""
        try:
            webbrowser.open(url)
            self.analytics["clicks"] += 1
            return True
        except Exception as e:
            print(f"Error opening link: {e}")
            return False
    
    def copy_to_clipboard(self, text, root):
        """Copy text to clipboard."""
        try:
            root.clipboard_clear()
            root.clipboard_append(text)
            self.analytics["copies"] += 1
            return True
        except Exception as e:
            print(f"Error copying to clipboard: {e}")
            return False

class EnhancedShareableLinksGUI:
    def __init__(self, root, location_data):
        self.root = root
        self.location_data = location_data
        self.generator = EnhancedShareableLinksGenerator()
        self.links = self.generator.generate_links(location_data)
        self.colors = self.generator.colors
        
        self.setup_gui()
        self.apply_styles()
    
    def setup_gui(self):
        """Setup the enhanced shareable links GUI."""
        # Main window setup
        self.root.title("🔗 Enhanced Location Sharing Pro")
        self.root.geometry("1200x900")
        self.root.configure(bg=self.colors["dark"])
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # Main frame with gradient effect
        main_frame = tk.Frame(self.root, bg=self.colors["dark"])
        main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Header with gradient effect
        header_frame = tk.Frame(main_frame, bg=self.colors["gradient_start"], height=80)
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        header_frame.grid_propagate(False)
        
        # Title with modern styling
        title_label = tk.Label(header_frame, 
                              text="🔗 Enhanced Location Sharing Pro",
                              font=("Segoe UI", 24, "bold"),
                              fg=self.colors["white"],
                              bg=self.colors["gradient_start"])
        title_label.pack(expand=True)
        
        # Location info card
        self.create_location_card(main_frame)
        
        # Create notebook for different categories
        notebook = ttk.Notebook(main_frame)
        notebook.grid(row=2, column=0, sticky="nsew", pady=(20, 0))
        
        # Maps tab
        self.create_maps_tab(notebook)
        
        # Social Media tab
        self.create_social_tab(notebook)
        
        # Communication tab
        self.create_communication_tab(notebook)
        
        # Custom tab
        self.create_custom_tab(notebook)
        
        # Analytics tab
        self.create_analytics_tab(notebook)
        
        # Quick actions
        self.create_quick_actions(main_frame)
    
    def create_location_card(self, parent):
        """Create a professional location info card."""
        card_frame = tk.Frame(parent, bg=self.colors["white"], relief="raised", bd=2)
        card_frame.grid(row=1, column=0, sticky="ew", pady=(0, 20))
        
        # Card header
        header_label = tk.Label(card_frame, 
                               text="📍 Current Location",
                               font=("Segoe UI", 16, "bold"),
                               fg=self.colors["dark"],
                               bg=self.colors["white"])
        header_label.pack(pady=(15, 10))
        
        # Location details
        location = self.location_data
        
        # City and country
        city_label = tk.Label(card_frame,
                             text=f"🌍 {location['name']}, {location['country']}",
                             font=("Segoe UI", 14, "bold"),
                             fg=self.colors["primary"],
                             bg=self.colors["white"])
        city_label.pack(pady=2)
        
        # Coordinates
        coords_label = tk.Label(card_frame,
                               text=f"📍 {location['lat']:.6f}, {location['lon']:.6f}",
                               font=("Segoe UI", 12),
                               fg=self.colors["secondary"],
                               bg=self.colors["white"])
        coords_label.pack(pady=2)
        
        # Weather and traffic info
        weather_frame = tk.Frame(card_frame, bg=self.colors["white"])
        weather_frame.pack(pady=10)
        
        weather_label = tk.Label(weather_frame,
                                text=f"🌤️ {location.get('weather', 'Unknown')} | 🌡️ {location.get('temperature', 0):.1f}°C",
                                font=("Segoe UI", 11),
                                fg=self.colors["success"],
                                bg=self.colors["white"])
        weather_label.pack(side=tk.LEFT, padx=(0, 20))
        
        traffic_label = tk.Label(weather_frame,
                                text=f"🚦 {location.get('traffic', 'Unknown')} | 🚗 {location.get('speed', 0):.1f} km/h",
                                font=("Segoe UI", 11),
                                fg=self.colors["warning"],
                                bg=self.colors["white"])
        traffic_label.pack(side=tk.LEFT)
        
        # Bottom padding
        tk.Label(card_frame, bg=self.colors["white"]).pack(pady=15)
    
    def create_maps_tab(self, notebook):
        """Create the maps tab with professional styling."""
        maps_frame = tk.Frame(notebook, bg=self.colors["light"])
        notebook.add(maps_frame, text="🗺️ Maps")
        
        # Tab header
        header_label = tk.Label(maps_frame,
                               text="🗺️ Map Services",
                               font=("Segoe UI", 16, "bold"),
                               fg=self.colors["dark"],
                               bg=self.colors["light"])
        header_label.pack(pady=(20, 15))
        
        maps_links = [
            ("Google Maps", self.links["google_maps"], "🌐", self.colors["primary"]),
            ("Apple Maps", self.links["apple_maps"], "🍎", self.colors["secondary"]),
            ("Waze", self.links["waze"], "🚗", self.colors["accent"]),
            ("Bing Maps", self.links["bing_maps"], "🔍", self.colors["warning"]),
            ("OpenStreetMap", self.links["openstreetmap"], "🗺️", self.colors["success"]),
            ("Here Maps", self.links["here_maps"], "📍", "#00D4AA")
        ]
        
        for name, url, icon, color in maps_links:
            self.create_link_card(maps_frame, name, url, icon, color)
    
    def create_social_tab(self, notebook):
        """Create the social media tab."""
        social_frame = tk.Frame(notebook, bg=self.colors["light"])
        notebook.add(social_frame, text="📱 Social")
        
        # Tab header
        header_label = tk.Label(social_frame,
                               text="📱 Social Media",
                               font=("Segoe UI", 16, "bold"),
                               fg=self.colors["dark"],
                               bg=self.colors["light"])
        header_label.pack(pady=(20, 15))
        
        social_links = [
            ("WhatsApp", self.links["whatsapp"], "💬", "#25D366"),
            ("Telegram", self.links["telegram"], "📱", "#0088cc"),
            ("Twitter", self.links["twitter"], "🐦", "#1DA1F2"),
            ("Facebook", self.links["facebook"], "📘", "#1877F2"),
            ("LinkedIn", self.links["linkedin"], "💼", "#0A66C2"),
            ("Instagram", self.links["instagram"], "📷", "#E4405F"),
            ("Discord", self.links["discord"], "🎮", "#5865F2")
        ]
        
        for name, url, icon, color in social_links:
            self.create_link_card(social_frame, name, url, icon, color)
    
    def create_communication_tab(self, notebook):
        """Create the communication tab."""
        comm_frame = tk.Frame(notebook, bg=self.colors["light"])
        notebook.add(comm_frame, text="📧 Communication")
        
        # Tab header
        header_label = tk.Label(comm_frame,
                               text="📧 Communication Tools",
                               font=("Segoe UI", 16, "bold"),
                               fg=self.colors["dark"],
                               bg=self.colors["light"])
        header_label.pack(pady=(20, 15))
        
        comm_links = [
            ("Email", self.links["email"], "📧", self.colors["primary"]),
            ("SMS", self.links["sms"], "💬", self.colors["success"]),
            ("Deep Link", self.links["deep_link"], "🔗", self.colors["accent"]),
            ("Skype", self.links["skype"], "📞", "#00AFF0")
        ]
        
        for name, url, icon, color in comm_links:
            self.create_link_card(comm_frame, name, url, icon, color)
    
    def create_custom_tab(self, notebook):
        """Create the custom sharing tab."""
        custom_frame = tk.Frame(notebook, bg=self.colors["light"])
        notebook.add(custom_frame, text="📤 Custom")
        
        # Tab header
        header_label = tk.Label(custom_frame,
                               text="📤 Custom Sharing",
                               font=("Segoe UI", 16, "bold"),
                               fg=self.colors["dark"],
                               bg=self.colors["light"])
        header_label.pack(pady=(20, 15))
        
        # Custom share text area
        text_frame = tk.Frame(custom_frame, bg=self.colors["white"], relief="solid", bd=1)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        custom_text = tk.Text(text_frame, 
                             height=8, 
                             width=70,
                             font=("Consolas", 10),
                             bg=self.colors["white"],
                             fg=self.colors["dark"],
                             relief="flat",
                             padx=10,
                             pady=10)
        custom_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        custom_text.insert(tk.END, self.links["custom_share"])
        
        # Buttons for custom share
        custom_buttons = tk.Frame(custom_frame, bg=self.colors["light"])
        custom_buttons.pack(pady=15)
        
        self.create_professional_button(custom_buttons, "📋 Copy Text", 
                                      lambda: self.copy_text(custom_text.get(1.0, tk.END).strip()),
                                      self.colors["primary"])
        
        self.create_professional_button(custom_buttons, "🔗 Copy Google Maps Link", 
                                      lambda: self.copy_link(self.links["google_maps"]),
                                      self.colors["success"])
        
        self.create_professional_button(custom_buttons, "📱 Copy QR Code Data", 
                                      lambda: self.copy_link(self.links["qr_code_data"]),
                                      self.colors["accent"])
        
        # Additional custom formats
        formats_frame = tk.LabelFrame(custom_frame, text="📝 Custom Formats", 
                                     font=("Segoe UI", 12, "bold"),
                                     bg=self.colors["light"],
                                     fg=self.colors["dark"])
        formats_frame.pack(fill=tk.X, padx=20, pady=10)
        
        formats_buttons = tk.Frame(formats_frame, bg=self.colors["light"])
        formats_buttons.pack(pady=10)
        
        self.create_professional_button(formats_buttons, "📋 Short Text", 
                                      lambda: self.copy_text(self.links["short_text"]),
                                      self.colors["primary"])
        
        self.create_professional_button(formats_buttons, "📋 Detailed Text", 
                                      lambda: self.copy_text(self.links["detailed_text"]),
                                      self.colors["success"])
        
        self.create_professional_button(formats_buttons, "📋 Rich Text", 
                                      lambda: self.copy_text(self.links["rich_text"]),
                                      self.colors["accent"])
    
    def create_analytics_tab(self, notebook):
        """Create the analytics tab."""
        analytics_frame = tk.Frame(notebook, bg=self.colors["light"])
        notebook.add(analytics_frame, text="📊 Analytics")
        
        # Tab header
        header_label = tk.Label(analytics_frame,
                               text="📊 Sharing Analytics",
                               font=("Segoe UI", 16, "bold"),
                               fg=self.colors["dark"],
                               bg=self.colors["light"])
        header_label.pack(pady=(20, 15))
        
        # Analytics cards
        analytics_cards = tk.Frame(analytics_frame, bg=self.colors["light"])
        analytics_cards.pack(fill=tk.X, padx=20)
        
        # Clicks card
        clicks_card = tk.Frame(analytics_cards, bg=self.colors["white"], relief="solid", bd=1)
        clicks_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=10)
        
        tk.Label(clicks_card, text="🔗 Link Clicks", font=("Segoe UI", 12, "bold"),
                bg=self.colors["white"], fg=self.colors["primary"]).pack(pady=10)
        
        clicks_label = tk.Label(clicks_card, text=str(self.generator.analytics["clicks"]),
                               font=("Segoe UI", 24, "bold"),
                               bg=self.colors["white"], fg=self.colors["primary"])
        clicks_label.pack(pady=10)
        
        # Shares card
        shares_card = tk.Frame(analytics_cards, bg=self.colors["white"], relief="solid", bd=1)
        shares_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=10)
        
        tk.Label(shares_card, text="📤 Shares", font=("Segoe UI", 12, "bold"),
                bg=self.colors["white"], fg=self.colors["success"]).pack(pady=10)
        
        shares_label = tk.Label(shares_card, text=str(self.generator.analytics["shares"]),
                               font=("Segoe UI", 24, "bold"),
                               bg=self.colors["white"], fg=self.colors["success"])
        shares_label.pack(pady=10)
        
        # Copies card
        copies_card = tk.Frame(analytics_cards, bg=self.colors["white"], relief="solid", bd=1)
        copies_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=10)
        
        tk.Label(copies_card, text="📋 Copies", font=("Segoe UI", 12, "bold"),
                bg=self.colors["white"], fg=self.colors["warning"]).pack(pady=10)
        
        copies_label = tk.Label(copies_card, text=str(self.generator.analytics["copies"]),
                               font=("Segoe UI", 24, "bold"),
                               bg=self.colors["white"], fg=self.colors["warning"])
        copies_label.pack(pady=10)
        
        # Export buttons
        export_frame = tk.Frame(analytics_frame, bg=self.colors["light"])
        export_frame.pack(pady=20)
        
        self.create_professional_button(export_frame, "📊 Export JSON", 
                                      lambda: self.export_data("json"),
                                      self.colors["primary"])
        
        self.create_professional_button(export_frame, "📊 Export CSV", 
                                      lambda: self.export_data("csv"),
                                      self.colors["success"])
        
        self.create_professional_button(export_frame, "📊 Export TXT", 
                                      lambda: self.export_data("txt"),
                                      self.colors["accent"])
    
    def create_link_card(self, parent, name, url, icon, color):
        """Create a professional link card."""
        card_frame = tk.Frame(parent, 
                             bg=self.colors["white"], 
                             relief="solid", 
                             bd=1)
        card_frame.pack(fill=tk.X, padx=20, pady=5)
        
        # Card content
        content_frame = tk.Frame(card_frame, bg=self.colors["white"])
        content_frame.pack(fill=tk.X, padx=15, pady=10)
        
        # Icon and name
        icon_label = tk.Label(content_frame,
                             text=icon,
                             font=("Segoe UI", 16),
                             bg=self.colors["white"])
        icon_label.pack(side=tk.LEFT)
        
        name_label = tk.Label(content_frame,
                             text=name,
                             font=("Segoe UI", 12, "bold"),
                             fg=self.colors["dark"],
                             bg=self.colors["white"])
        name_label.pack(side=tk.LEFT, padx=(10, 0))
        
        # Buttons
        button_frame = tk.Frame(content_frame, bg=self.colors["white"])
        button_frame.pack(side=tk.RIGHT)
        
        self.create_professional_button(button_frame, "🔗 Open", 
                                      lambda: self.open_link(url),
                                      color)
        
        self.create_professional_button(button_frame, "📋 Copy", 
                                      lambda: self.copy_link(url),
                                      self.colors["secondary"])
    
    def create_professional_button(self, parent, text, command, color):
        """Create a professional styled button."""
        button = tk.Button(parent,
                          text=text,
                          command=command,
                          font=("Segoe UI", 10, "bold"),
                          fg=self.colors["white"],
                          bg=color,
                          relief="flat",
                          padx=15,
                          pady=5,
                          cursor="hand2")
        button.pack(side=tk.LEFT, padx=(0, 5))
        
        # Hover effects
        button.bind("<Enter>", lambda e: button.configure(bg=self.lighten_color(color)))
        button.bind("<Leave>", lambda e: button.configure(bg=color))
        
        return button
    
    def lighten_color(self, color):
        """Lighten a color for hover effects."""
        # Simple color lightening for hover effect
        if color.startswith("#"):
            r = int(color[1:3], 16)
            g = int(color[3:5], 16)
            b = int(color[5:7], 16)
            r = min(255, r + 30)
            g = min(255, g + 30)
            b = min(255, b + 30)
            return f"#{r:02x}{g:02x}{b:02x}"
        return color
    
    def create_quick_actions(self, parent):
        """Create professional quick action buttons."""
        quick_frame = tk.Frame(parent, bg=self.colors["dark"])
        quick_frame.grid(row=3, column=0, sticky="ew", pady=(20, 0))
        
        # Quick actions header
        header_label = tk.Label(quick_frame,
                               text="⚡ Quick Actions",
                               font=("Segoe UI", 14, "bold"),
                               fg=self.colors["white"],
                               bg=self.colors["dark"])
        header_label.pack(pady=(0, 15))
        
        # Quick action buttons
        actions_frame = tk.Frame(quick_frame, bg=self.colors["dark"])
        actions_frame.pack()
        
        quick_actions = [
            ("🗺️ Open Google Maps", self.links["google_maps"], self.colors["primary"]),
            ("💬 Share on WhatsApp", self.links["whatsapp"], "#25D366"),
            ("📱 Share on Telegram", self.links["telegram"], "#0088cc"),
            ("📧 Send Email", self.links["email"], self.colors["success"])
        ]
        
        for text, url, color in quick_actions:
            self.create_professional_button(actions_frame, text, 
                                          lambda u=url: self.open_link(u), color)
    
    def apply_styles(self):
        """Apply professional styles to the application."""
        # Configure ttk styles
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure notebook style
        style.configure('TNotebook', 
                       background=self.colors["light"],
                       borderwidth=0)
        style.configure('TNotebook.Tab', 
                       padding=[20, 10],
                       font=('Segoe UI', 10, 'bold'))
        style.map('TNotebook.Tab',
                 background=[('selected', self.colors["primary"]),
                           ('active', self.colors["secondary"])],
                 foreground=[('selected', self.colors["white"]),
                           ('active', self.colors["white"])])
    
    def export_data(self, format_type):
        """Export data in the specified format."""
        export_content = self.generator.export_data(self.location_data, self.links, format_type)
        
        # Get file extension
        extensions = {"json": ".json", "csv": ".csv", "txt": ".txt"}
        extension = extensions.get(format_type, ".txt")
        
        # Ask user for save location
        filename = filedialog.asksaveasfilename(
            defaultextension=extension,
            filetypes=[(f"{format_type.upper()} files", f"*{extension}")],
            title=f"Export {format_type.upper()} Data"
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(export_content)
                messagebox.showinfo("✅ Export Successful", f"Data exported to {filename}")
            except Exception as e:
                messagebox.showerror("❌ Export Failed", f"Failed to export data: {str(e)}")
    
    def open_link(self, url):
        """Open a link in the browser with professional feedback."""
        if self.generator.open_link(url):
            self.show_success_message("Link opened in browser!")
        else:
            self.show_error_message("Failed to open link")
    
    def copy_link(self, url):
        """Copy a link to clipboard with professional feedback."""
        if self.generator.copy_to_clipboard(url, self.root):
            self.show_success_message("Link copied to clipboard!")
        else:
            self.show_error_message("Failed to copy link")
    
    def copy_text(self, text):
        """Copy text to clipboard with professional feedback."""
        if self.generator.copy_to_clipboard(text, self.root):
            self.show_success_message("Text copied to clipboard!")
        else:
            self.show_error_message("Failed to copy text")
    
    def show_success_message(self, message):
        """Show a professional success message."""
        messagebox.showinfo("✅ Success", message)
    
    def show_error_message(self, message):
        """Show a professional error message."""
        messagebox.showerror("❌ Error", message)

def demo_enhanced_shareable_links():
    """Demo function to test enhanced shareable links."""
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
    app = EnhancedShareableLinksGUI(root, sample_location)
    root.mainloop()

if __name__ == "__main__":
    demo_enhanced_shareable_links()
