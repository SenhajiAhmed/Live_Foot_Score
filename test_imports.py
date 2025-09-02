"""
Test script to verify all modules can be imported correctly.
"""

def test_imports():
    """Test importing all modules"""
    try:
        print("Testing module imports...")
        
        # Add src to path
        import sys
        import os
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
        
        # Test core modules
        from core.design_system import DesignSystem
        print("✓ DesignSystem imported successfully")
        
        # Test UI modules
        from ui.header import Header
        print("✓ Header imported successfully")
        
        from ui.sidebar import Sidebar
        print("✓ Sidebar imported successfully")
        
        from ui.content import ContentArea
        print("✓ ContentArea imported successfully")
        
        from ui.status_bar import StatusBar
        print("✓ StatusBar imported successfully")
        
        from ui.match_display import MatchDisplay
        print("✓ MatchDisplay imported successfully")
        
        # Test data modules
        from data.data_processor import DataProcessor, MatchOrganizer
        print("✓ DataProcessor and MatchOrganizer imported successfully")
        
        print("\n🎉 All modules imported successfully!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_design_system():
    """Test design system initialization"""
    try:
        import sys
        import os
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
        from core.design_system import DesignSystem
        design = DesignSystem()
        
        # Test that colors are defined
        assert 'primary' in design.colors
        assert 'success' in design.colors
        assert 'live' in design.colors
        
        # Test that fonts are defined
        assert 'display_medium' in design.fonts
        assert 'body_medium' in design.fonts
        
        # Test that spacing is defined
        assert 'md' in design.spacing
        assert 'lg' in design.spacing
        
        print("✓ DesignSystem initialized successfully")
        return True
        
    except Exception as e:
        print(f"❌ DesignSystem test failed: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("FOOTBALL SCORES PRO - MODULE IMPORT TEST")
    print("=" * 50)
    
    success = True
    success &= test_imports()
    success &= test_design_system()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 ALL TESTS PASSED! The refactored structure is working correctly.")
    else:
        print("❌ SOME TESTS FAILED! Please check the errors above.")
    print("=" * 50)
