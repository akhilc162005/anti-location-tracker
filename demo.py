#!/usr/bin/env python3
"""
Anti GPS System Demo
Interactive demonstration of GPS signal detection and privacy protection.
"""

import time
import random
from datetime import datetime
from anti_gps import AntiGPSSystem

def demo_gps_detection():
    """Demonstrate GPS signal detection capabilities."""
    print("🔍 GPS Signal Detection Demo")
    print("=" * 50)
    
    anti_gps = AntiGPSSystem()
    
    print("Scanning for GPS signals...")
    for i in range(5):
        signals = anti_gps.detect_gps_signals()
        
        if signals:
            print(f"\n📡 Scan {i+1}: {len(signals)} signals detected")
            for signal in signals:
                print(f"  ⚠️  {signal['frequency']}: {signal['strength']:.2f} strength")
            
            threat_level = anti_gps.analyze_threat_level(signals)
            print(f"  🚨 Threat Level: {threat_level.upper()}")
        else:
            print(f"📡 Scan {i+1}: No signals detected")
        
        time.sleep(1)
    
    print("\n✅ GPS Detection Demo Complete")

def demo_location_spoofing():
    """Demonstrate location spoofing capabilities."""
    print("\n📍 Location Spoofing Demo")
    print("=" * 50)
    
    anti_gps = AntiGPSSystem()
    
    print("Generating fake locations...")
    for i in range(3):
        spoof_result = anti_gps.location_spoofing()
        location = spoof_result['spoofed_location']
        
        print(f"🎭 Spoof {i+1}: {location['name']}")
        print(f"  📍 Coordinates: {location['lat']:.4f}, {location['lon']:.4f}")
        print(f"  ⏰ Timestamp: {spoof_result['timestamp']}")
        
        time.sleep(0.5)
    
    print("\n✅ Location Spoofing Demo Complete")

def demo_signal_jamming():
    """Demonstrate signal jamming capabilities."""
    print("\n📡 Signal Jamming Demo")
    print("=" * 50)
    
    anti_gps = AntiGPSSystem()
    
    # Create sample signals
    sample_signals = [
        {"frequency": "L1", "strength": 0.8, "quality": 0.9},
        {"frequency": "L2", "strength": 0.6, "quality": 0.8},
        {"frequency": "L5", "strength": 0.7, "quality": 0.85}
    ]
    
    print("Jamming detected GPS signals...")
    jamming_results = anti_gps.signal_jamming(sample_signals)
    
    for result in jamming_results:
        status = "✅" if result["success"] else "❌"
        print(f"{status} {result['frequency']}: {result['jamming_power']:.2f} power")
    
    print("\n✅ Signal Jamming Demo Complete")

def demo_frequency_hopping():
    """Demonstrate frequency hopping capabilities."""
    print("\n🔄 Frequency Hopping Demo")
    print("=" * 50)
    
    anti_gps = AntiGPSSystem()
    
    print("Activating frequency hopping patterns...")
    for i in range(3):
        hopping_result = anti_gps.frequency_hopping()
        
        print(f"🔄 Pattern {i+1}:")
        print(f"  📡 Frequencies: {len(hopping_result['pattern'])} bands")
        print(f"  ⏱️  Interval: {hopping_result['interval']:.2f}s")
        print(f"  🎯 Method: {hopping_result['method']}")
        
        time.sleep(0.5)
    
    print("\n✅ Frequency Hopping Demo Complete")

def demo_encryption():
    """Demonstrate data encryption capabilities."""
    print("\n🔐 Data Encryption Demo")
    print("=" * 50)
    
    anti_gps = AntiGPSSystem()
    
    print("Encrypting location data...")
    for i in range(3):
        encrypt_result = anti_gps.encrypt_location_data()
        
        print(f"🔐 Encryption {i+1}:")
        print(f"  🔑 Key: {encrypt_result['encryption_key'][:16]}...")
        print(f"  🛡️  Algorithm: {encrypt_result['algorithm']}")
        print(f"  ⏰ Timestamp: {encrypt_result['timestamp']}")
        
        time.sleep(0.5)
    
    print("\n✅ Data Encryption Demo Complete")

def demo_protection_levels():
    """Demonstrate different protection levels."""
    print("\n🛡️ Protection Levels Demo")
    print("=" * 50)
    
    anti_gps = AntiGPSSystem()
    
    protection_levels = ["low", "medium", "high", "maximum"]
    
    for level in protection_levels:
        print(f"\n🛡️ Testing {level.upper()} protection...")
        anti_gps.set_protection_level(level)
        
        methods = anti_gps.protection_methods[level]
        print(f"  📋 Methods: {', '.join(methods)}")
        
        # Simulate threat
        sample_signals = [{"frequency": "L1", "strength": 0.8, "quality": 0.9}]
        
        if level in ["high", "maximum"]:
            anti_gps.apply_protection(sample_signals)
        else:
            anti_gps.apply_basic_protection(sample_signals)
        
        time.sleep(1)
    
    print("\n✅ Protection Levels Demo Complete")

def demo_threat_assessment():
    """Demonstrate threat assessment capabilities."""
    print("\n🚨 Threat Assessment Demo")
    print("=" * 50)
    
    anti_gps = AntiGPSSystem()
    
    # Test different threat scenarios
    threat_scenarios = [
        {"name": "No Threat", "signals": []},
        {"name": "Low Threat", "signals": [{"strength": 0.3, "quality": 0.6}]},
        {"name": "Medium Threat", "signals": [{"strength": 0.7, "quality": 0.8}]},
        {"name": "High Threat", "signals": [{"strength": 0.9, "quality": 0.9}]},
        {"name": "Critical Threat", "signals": [{"strength": 1.0, "quality": 0.95}]}
    ]
    
    for scenario in threat_scenarios:
        print(f"\n🚨 Testing: {scenario['name']}")
        
        threat_level = anti_gps.analyze_threat_level(scenario['signals'])
        print(f"  📊 Threat Level: {threat_level.upper()}")
        
        if threat_level in ["high", "critical"]:
            print("  🛡️ Applying maximum protection...")
        elif threat_level == "medium":
            print("  🛡️ Applying basic protection...")
        else:
            print("  ✅ No protection needed")
        
        time.sleep(0.5)
    
    print("\n✅ Threat Assessment Demo Complete")

def interactive_demo():
    """Interactive demo with user input."""
    print("\n🎮 Interactive Anti GPS Demo")
    print("=" * 50)
    
    anti_gps = AntiGPSSystem()
    
    print("Choose a demo option:")
    print("1. 🔍 GPS Signal Detection")
    print("2. 📍 Location Spoofing")
    print("3. 📡 Signal Jamming")
    print("4. 🔄 Frequency Hopping")
    print("5. 🔐 Data Encryption")
    print("6. 🛡️ Protection Levels")
    print("7. 🚨 Threat Assessment")
    print("8. 🎯 Full System Demo")
    print("9. ❌ Exit")
    
    while True:
        try:
            choice = input("\nEnter your choice (1-9): ").strip()
            
            if choice == "1":
                demo_gps_detection()
            elif choice == "2":
                demo_location_spoofing()
            elif choice == "3":
                demo_signal_jamming()
            elif choice == "4":
                demo_frequency_hopping()
            elif choice == "5":
                demo_encryption()
            elif choice == "6":
                demo_protection_levels()
            elif choice == "7":
                demo_threat_assessment()
            elif choice == "8":
                full_system_demo()
            elif choice == "9":
                print("👋 Thanks for trying the Anti GPS System!")
                break
            else:
                print("❌ Invalid choice. Please enter 1-9.")
                
        except KeyboardInterrupt:
            print("\n👋 Demo interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

def full_system_demo():
    """Run a complete system demonstration."""
    print("\n🎯 Full Anti GPS System Demo")
    print("=" * 50)
    
    anti_gps = AntiGPSSystem()
    
    print("🚀 Starting comprehensive system demo...")
    
    # Set high protection
    anti_gps.set_protection_level("high")
    anti_gps.set_detection_mode("active")
    
    print("🛡️ Protection Level: HIGH")
    print("🔍 Detection Mode: ACTIVE")
    
    # Simulate continuous monitoring
    for i in range(5):
        print(f"\n📡 Scan {i+1}/5...")
        
        # Detect signals
        signals = anti_gps.detect_gps_signals()
        
        if signals:
            threat_level = anti_gps.analyze_threat_level(signals)
            print(f"🚨 Threat Level: {threat_level.upper()}")
            
            # Apply protection
            if threat_level in ["high", "critical"]:
                anti_gps.apply_protection(signals)
            elif threat_level == "medium":
                anti_gps.apply_basic_protection(signals)
        else:
            print("✅ No threats detected")
        
        time.sleep(1)
    
    # Show final status
    status = anti_gps.get_status()
    print(f"\n📊 Final System Status:")
    for key, value in status.items():
        print(f"  {key.replace('_', ' ').title()}: {value}")
    
    print("\n✅ Full System Demo Complete")

def main():
    """Main demo function."""
    print("🛡️ ANTI GPS SYSTEM DEMO")
    print("=" * 50)
    print("GPS Signal Detection and Privacy Protection")
    print("=" * 50)
    
    print("\nThis demo showcases the Anti GPS System capabilities:")
    print("• GPS signal detection and analysis")
    print("• Location spoofing and privacy protection")
    print("• Signal jamming and interference")
    print("• Frequency hopping and evasion")
    print("• Data encryption and security")
    print("• Threat assessment and response")
    
    print("\n⚠️  LEGAL DISCLAIMER:")
    print("This is for educational purposes only.")
    print("GPS jamming may be illegal in many jurisdictions.")
    print("Use responsibly and in compliance with local laws.")
    
    # Run interactive demo
    interactive_demo()

if __name__ == "__main__":
    main()
