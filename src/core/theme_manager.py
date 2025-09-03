"""
Theme Manager Module
Handles theme switching and updates all UI components when theme changes.
"""

import tkinter as tk


class ThemeManager:
    """Manages theme switching and component updates."""
    
    def __init__(self, design_system):
        self.design_system = design_system
        self.components = []
    
    def register_component(self, component):
        """Register a component to receive theme updates"""
        if hasattr(component, 'update_theme'):
            self.components.append(component)
    
    def unregister_component(self, component):
        """Unregister a component from theme updates"""
        if component in self.components:
            self.components.remove(component)
    
    def switch_theme(self, theme):
        """Switch theme and update all registered components"""
        if self.design_system.switch_theme(theme):
            self.update_all_components()
            return True
        return False
    
    def update_all_components(self):
        """Update all registered components with new theme"""
        for component in self.components:
            try:
                component.update_theme(self.design_system)
            except Exception as e:
                print(f"Error updating component theme: {e}")
    
    def get_current_theme(self):
        """Get current theme"""
        return self.design_system.get_theme()
    
    def is_dark_theme(self):
        """Check if current theme is dark"""
        return self.design_system.is_dark_theme()
