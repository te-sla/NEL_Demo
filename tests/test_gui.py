#!/usr/bin/env python3
"""
Tests for NEL Demo GUI application.

These tests verify that the GUI initializes correctly, especially when
widgets are mocked or patched during testing.
"""

import unittest
from unittest.mock import Mock, MagicMock, patch
import tkinter as tk
import sys
from pathlib import Path

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from gui import NERDemoGUI, ToolTip


class TestNERDemoGUIInitialization(unittest.TestCase):
    """Test NERDemoGUI initialization behavior."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.root = tk.Tk()
    
    def tearDown(self):
        """Clean up after tests."""
        try:
            self.root.destroy()
        except tk.TclError:
            # Ignore errors if the window is already destroyed or not initialized
            pass
    
    @patch.object(NERDemoGUI, 'create_widgets')
    @patch.object(NERDemoGUI, 'check_models')
    def test_init_with_patched_create_widgets_no_check_models(self, mock_check_models, mock_create_widgets):
        """Test that check_models is NOT called when create_widgets doesn't set widget attributes."""
        # When create_widgets is patched and doesn't set model_combo/status_var,
        # check_models should not be called automatically
        app = NERDemoGUI(self.root)
        
        # create_widgets should have been called
        mock_create_widgets.assert_called_once()
        
        # check_models should NOT have been called because widgets weren't created
        mock_check_models.assert_not_called()
        
        # Attributes should be None (default values set before create_widgets)
        self.assertIsNone(app.model_combo)
        self.assertIsNone(app.status_var)
    
    @patch.object(NERDemoGUI, 'check_models')
    def test_init_with_real_create_widgets_calls_check_models(self, mock_check_models):
        """Test that check_models IS called when create_widgets actually creates widgets."""
        # When create_widgets runs normally and creates widgets,
        # check_models should be called automatically
        app = NERDemoGUI(self.root)
        
        # Widgets should have been created
        self.assertIsNotNone(app.model_combo)
        self.assertIsNotNone(app.status_var)
        
        # check_models should have been called because widgets were created
        mock_check_models.assert_called_once()
    
    @patch.object(NERDemoGUI, 'create_widgets')
    def test_init_sets_default_attributes_before_create_widgets(self, mock_create_widgets):
        """Test that default attributes are set before create_widgets is called."""
        # When create_widgets is patched, it won't set widgets
        # But the defaults should still be set in __init__
        
        app = NERDemoGUI(self.root)
        mock_create_widgets.assert_called_once()
        
        # The defaults should be set even though create_widgets was patched
        self.assertIsNone(app.model_combo)
        self.assertIsNone(app.status_var)
    
    def test_manual_widget_setting_allows_check_models(self):
        """Test that manually setting widgets after init allows check_models to work."""
        # When a test patches create_widgets but manually sets the widget attributes,
        # check_models should work when called manually
        
        def set_widgets_manually(gui_self):
            # Simulate what a test might do: manually set widget attributes
            gui_self.model_combo = MagicMock()
            gui_self.status_var = MagicMock()
        
        with patch.object(NERDemoGUI, 'create_widgets', set_widgets_manually):
            app = NERDemoGUI(self.root)
            
            # Widgets were set manually in the patched create_widgets
            self.assertIsNotNone(app.model_combo)
            self.assertIsNotNone(app.status_var)
            
            # Now check_models should be callable without AttributeError
            with patch('gui.Path.iterdir', return_value=[]), \
                 patch('gui.messagebox.showinfo'):
                app.check_models()  # Should not raise AttributeError


class TestToolTip(unittest.TestCase):
    """Test ToolTip behavior, especially with mocked widgets."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.root = tk.Tk()
    
    def tearDown(self):
        """Clean up after tests."""
        try:
            self.root.destroy()
        except tk.TclError:
            # Ignore errors if root window is already destroyed
            pass
    
    def test_tooltip_with_real_widget(self):
        """Test that tooltip works with a real widget."""
        label = tk.Label(self.root, text="Test")
        tooltip = ToolTip(label, "Tooltip text")
        
        # Should not raise any errors
        tooltip.show_tooltip()
        
        # Tooltip window should be created
        self.assertIsNotNone(tooltip.tooltip_window)
        
        # Clean up
        tooltip.hide_tooltip()
        self.assertIsNone(tooltip.tooltip_window)
    
    def test_tooltip_with_mocked_widget_methods(self):
        """Test that tooltip handles mocked widget methods gracefully."""
        # Create a mock widget where winfo_* methods return Mock objects
        mock_widget = MagicMock()
        mock_widget.winfo_rootx.return_value = Mock()  # Returns Mock, not int
        mock_widget.winfo_rooty.return_value = Mock()  # Returns Mock, not int
        mock_widget.winfo_height.return_value = Mock()  # Returns Mock, not int
        
        tooltip = ToolTip(mock_widget, "Tooltip text")
        
        # Should not raise TypeError when trying to add Mock + int
        # Instead, it should silently return and not create tooltip_window
        tooltip.show_tooltip()
        
        # Tooltip window should NOT be created because we caught the exception
        self.assertIsNone(tooltip.tooltip_window)
    
    def test_tooltip_with_widget_methods_raising_exception(self):
        """Test that tooltip handles exceptions from widget methods."""
        # Create a mock widget where winfo_* methods raise exceptions
        mock_widget = MagicMock()
        mock_widget.winfo_rootx.side_effect = RuntimeError("Widget not available")
        
        tooltip = ToolTip(mock_widget, "Tooltip text")
        
        # Should not raise RuntimeError
        # Instead, it should silently return and not create tooltip_window
        tooltip.show_tooltip()
        
        # Tooltip window should NOT be created because we caught the exception
        self.assertIsNone(tooltip.tooltip_window)
    
    def test_tooltip_empty_text_no_show(self):
        """Test that tooltip doesn't show when text is empty."""
        label = tk.Label(self.root, text="Test")
        tooltip = ToolTip(label, "")
        
        tooltip.show_tooltip()
        
        # Tooltip window should NOT be created for empty text
        self.assertIsNone(tooltip.tooltip_window)
    
    def test_tooltip_already_showing_no_duplicate(self):
        """Test that tooltip doesn't create duplicate windows."""
        label = tk.Label(self.root, text="Test")
        tooltip = ToolTip(label, "Tooltip text")
        
        # Show tooltip first time
        tooltip.show_tooltip()
        first_window = tooltip.tooltip_window
        self.assertIsNotNone(first_window)
        
        # Try to show again - should not create a new window
        tooltip.show_tooltip()
        self.assertIs(tooltip.tooltip_window, first_window)
        
        # Clean up
        tooltip.hide_tooltip()


class TestNERDemoGUICheckModels(unittest.TestCase):
    """Test check_models functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.root = tk.Tk()
    
    def tearDown(self):
        """Clean up after tests."""
        try:
            self.root.destroy()
        except tk.TclError:
            # Ignore errors if the root window is already destroyed
            pass
    
    @patch.object(NERDemoGUI, 'create_widgets')
    def test_check_models_requires_model_combo(self, mock_create_widgets):
        """Test that check_models raises TypeError when model_combo is None."""
        app = NERDemoGUI(self.root)
        
        # Initially, widgets are None
        self.assertIsNone(app.model_combo)
        
        # Set up mocks for Path operations
        with patch('gui.Path.exists', return_value=True), \
             patch('gui.Path.iterdir', return_value=[]), \
             patch('gui.Path.mkdir'):
            
            # This should raise TypeError because model_combo is None
            # (can't do item assignment on None)
            with self.assertRaises(TypeError):
                app.check_models()
    
    def test_check_models_works_with_widgets_set(self):
        """Test that check_models works when widgets are properly set."""
        
        def set_widgets(gui_self):
            # Manually set the required widgets
            gui_self.model_combo = MagicMock()
            gui_self.model_combo.__setitem__ = MagicMock()  # For model_combo['values'] = ...
            gui_self.status_var = MagicMock()
        
        with patch.object(NERDemoGUI, 'create_widgets', set_widgets):
            app = NERDemoGUI(self.root)
            
            # Now widgets are set
            self.assertIsNotNone(app.model_combo)
            self.assertIsNotNone(app.status_var)
            
            # Set up mocks for Path operations and messagebox
            with patch('gui.Path.exists', return_value=True), \
                 patch('gui.Path.iterdir', return_value=[]), \
                 patch('gui.Path.mkdir'), \
                 patch('gui.messagebox.showinfo'):
                
                # This should work without raising AttributeError
                app.check_models()
                
                # Verify that model_combo and status_var were accessed
                app.model_combo.__setitem__.assert_called()
                app.status_var.set.assert_called()


if __name__ == '__main__':
    unittest.main()
