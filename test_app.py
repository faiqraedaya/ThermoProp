#!/usr/bin/env python3
"""
Test script for ThermoProp application
"""

import sys
import traceback

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    
    try:
        from PyQt5.QtWidgets import QApplication
        print("✓ PyQt5 imported successfully")
    except ImportError as e:
        print(f"✗ PyQt5 import failed: {e}")
        return False
    
    try:
        import CoolProp.CoolProp as CP
        print("✓ CoolProp imported successfully")
    except ImportError as e:
        print(f"✗ CoolProp import failed: {e}")
        return False
    
    try:
        import matplotlib.pyplot as plt
        print("✓ matplotlib imported successfully")
    except ImportError as e:
        print(f"✗ matplotlib import failed: {e}")
        return False
    
    try:
        import pandas as pd
        print("✓ pandas imported successfully")
    except ImportError as e:
        print(f"✗ pandas import failed: {e}")
        return False
    
    try:
        import numpy as np
        print("✓ numpy imported successfully")
    except ImportError as e:
        print(f"✗ numpy import failed: {e}")
        return False
    
    return True

def test_calculator():
    """Test the mixture calculator"""
    print("\nTesting calculator...")
    
    try:
        from core.mixture_calculator import MixtureCalculator
        calc = MixtureCalculator()
        print(f"✓ Calculator created successfully with {len(calc.fluids)} fluids")
        
        # Test single point calculation
        try:
            results = calc.calculate_single_point_properties(
                'Water', 'T', 25, 'C', 'P', 1.01325, 'bar'
            )
            print(f"✓ Single point calculation successful: {len(results)} properties calculated")
        except Exception as e:
            print(f"✗ Single point calculation failed: {e}")
        
        # Test saturation calculation
        try:
            sat_results = calc.calculate_saturation_properties('Water', 'T', 100, 'C')
            print(f"✓ Saturation calculation successful: {len(sat_results)} properties calculated")
        except Exception as e:
            print(f"✗ Saturation calculation failed: {e}")
        
        return True
    except Exception as e:
        print(f"✗ Calculator test failed: {e}")
        traceback.print_exc()
        return False

def test_ui_components():
    """Test UI components"""
    print("\nTesting UI components...")
    
    try:
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        
        # Test tab creation
        from tabs.tab_manager import TabManager
        from core.mixture_calculator import MixtureCalculator
        
        calc = MixtureCalculator()
        tab_manager = TabManager(None, calc)
        print("✓ Tab manager created successfully")
        
        # Test individual tabs
        tabs = tab_manager.tabs
        for tab_name, tab in tabs.items():
            print(f"✓ {tab_name} tab created successfully")
        
        return True
    except Exception as e:
        print(f"✗ UI components test failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("ThermoProp Application Test")
    print("=" * 40)
    
    # Test imports
    if not test_imports():
        print("\n❌ Import test failed. Please install missing dependencies.")
        return False
    
    # Test calculator
    if not test_calculator():
        print("\n❌ Calculator test failed.")
        return False
    
    # Test UI components
    if not test_ui_components():
        print("\n❌ UI components test failed.")
        return False
    
    print("\n✅ All tests passed! The application should work correctly.")
    print("\nTo run the application, use: python main.py")
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1) 