#!/usr/bin/env python3
"""
GUI Launcher for Student Result Management System
Run this script to start the GUI application
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """Main launcher function"""
    try:
        # Import and run the GUI
        from GUI.app import main as gui_main
        gui_main()
    except ImportError as e:
        print(f"Error importing GUI modules: {e}")
        print("Please make sure all dependencies are installed:")
        print("pip install ttkbootstrap")
        return 1
    except Exception as e:
        print(f"Error starting GUI: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 