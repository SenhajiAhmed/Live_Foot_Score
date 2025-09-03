"""
Theme Manager Module
Handles theme switching and updates all UI components when theme changes.
"""

import tkinter as tk


class ThemeManager:
    """Manages theme switching and component updates."""
    
    def __init__(self, design_system):
        self.design_system = design_system
        self.components = set()  # Using set to avoid duplicate components
        self.design_system.register_theme_change_callback(self._on_theme_changed)
    
    def register_component(self, component):
        """Register a component to receive theme updates"""
        if hasattr(component, 'update_theme'):
            self.components.add(component)
    
    def unregister_component(self, component):
        """Unregister a component from theme updates"""
        if component in self.components:
            self.components.remove(component)
    
    def switch_theme(self, theme):
        """Switch theme and update all registered components"""
        if theme not in ['light', 'dark']:
            return False
            
        if theme != self.design_system.current_theme:
            self.design_system.current_theme = theme
            return True
        return False
    
    def _on_theme_changed(self):
        """Internal handler for theme change events"""
        self.update_all_components()
    
    def update_all_components(self):
        """Update all registered components with current theme"""
        for component in list(self.components):  # Create a copy to allow modification during iteration
            try:
                if hasattr(component, 'update_theme'):
                    component.update_theme(self.design_system)
            except Exception as e:
                print(f"Error updating component theme: {e}")
    
    def get_current_theme(self):
        """Get current theme"""
        return self.design_system.current_theme
    
    def is_dark_theme(self):
        """Check if current theme is dark"""
        return self.design_system.current_theme == 'dark'
