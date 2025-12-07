#!/usr/bin/env python3
"""
Tests for GUI module

This module provides tests for the GUI application, focusing on core functionality
without requiring actual GUI rendering or user interaction.
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch, mock_open

# Add src directory to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

# Try to import tkinter, skip all tests if not available
try:
    import tkinter as tk
    TKINTER_AVAILABLE = True
except ImportError:
    TKINTER_AVAILABLE = False
    pytestmark = pytest.mark.skip(reason="tkinter not available in headless environment")


class TestToolTip:
    """Test suite for ToolTip class."""
    
    def test_tooltip_creation(self):
        """Test that tooltip can be created."""
        # Import here to avoid tkinter initialization issues in headless environments
        try:
            from gui import ToolTip
            
            # Create a mock widget
            mock_widget = Mock()
            mock_widget.bind = Mock()
            
            # Create tooltip
            tooltip = ToolTip(mock_widget, "Test tooltip")
            
            # Verify tooltip was initialized
            assert tooltip.widget == mock_widget
            assert tooltip.text == "Test tooltip"
            assert tooltip.tooltip_window is None
            
            # Verify bindings were created
            assert mock_widget.bind.call_count == 2
            mock_widget.bind.assert_any_call("<Enter>", tooltip.show_tooltip)
            mock_widget.bind.assert_any_call("<Leave>", tooltip.hide_tooltip)
        except ImportError:
            pytest.skip("tkinter not available in headless environment")


class TestNERDemoGUI:
    """Test suite for NERDemoGUI class."""
    
    @pytest.fixture
    def mock_root(self):
        """Fixture providing a mock tkinter root."""
        mock = Mock(spec=tk.Tk)
        mock.title = Mock()
        mock.geometry = Mock()
        mock.update = Mock()
        return mock
    
    @patch('gui.tk.Tk')
    @patch('gui.ttk.LabelFrame')
    @patch('gui.scrolledtext.ScrolledText')
    @patch('gui.ttk.Combobox')
    def test_gui_initialization(self, mock_combo, mock_scrolled, mock_frame, mock_tk):
        """Test GUI initialization."""
        try:
            from gui import NERDemoGUI
            
            mock_root = Mock()
            mock_root.title = Mock()
            mock_root.geometry = Mock()
            
            # Mock the pack and grid methods that will be called
            mock_widget = Mock()
            mock_widget.pack = Mock()
            mock_widget.grid = Mock()
            
            mock_frame.return_value = mock_widget
            mock_scrolled.return_value = mock_widget
            mock_combo.return_value = mock_widget
            
            gui = NERDemoGUI(mock_root)
            
            # Verify initialization
            assert gui.root == mock_root
            assert gui.nlp is None
            assert gui.model_name is None
            assert gui.output_dir == PROJECT_ROOT / "data" / "outputs"
            assert gui.models_dir == PROJECT_ROOT / "models"
            
        except ImportError:
            pytest.skip("GUI module or tkinter not available")
    
    def test_check_models_empty_directory(self):
        """Test check_models with empty models directory."""
        try:
            from gui import NERDemoGUI
            
            with patch('gui.tk.Tk'):
                mock_root = Mock()
                mock_root.title = Mock()
                mock_root.geometry = Mock()
                
                with patch('gui.NERDemoGUI.create_widgets'):
                    gui = NERDemoGUI(mock_root)
                    
                    # Mock the models directory as empty
                    with patch.object(Path, 'exists', return_value=True), \
                         patch.object(Path, 'iterdir', return_value=[]):
                        
                        gui.model_combo = Mock()
                        gui.model_combo.__setitem__ = Mock()
                        gui.status_var = Mock()
                        gui.status_var.set = Mock()
                        
                        with patch('gui.messagebox.showinfo'):
                            gui.check_models()
                        
                        # Should show no models found
                        assert gui.status_var.set.called
                        
        except ImportError:
            pytest.skip("GUI module or tkinter not available")
    
    def test_load_sample_text(self):
        """Test loading sample text."""
        try:
            from gui import NERDemoGUI
            
            with patch('gui.tk.Tk'):
                mock_root = Mock()
                mock_root.title = Mock()
                mock_root.geometry = Mock()
                
                with patch('gui.NERDemoGUI.create_widgets'):
                    gui = NERDemoGUI(mock_root)
                    
                    # Mock input_text widget
                    gui.input_text = Mock()
                    gui.input_text.delete = Mock()
                    gui.input_text.insert = Mock()
                    gui.status_var = Mock()
                    gui.status_var.set = Mock()
                    
                    gui.load_sample_text()
                    
                    # Verify text was loaded
                    gui.input_text.delete.assert_called_once()
                    gui.input_text.insert.assert_called_once()
                    gui.status_var.set.assert_called_with("Sample text loaded")
                    
        except ImportError:
            pytest.skip("GUI module or tkinter not available")
    
    def test_process_text_without_model(self):
        """Test processing text without loading a model."""
        try:
            from gui import NERDemoGUI
            
            with patch('gui.tk.Tk'):
                mock_root = Mock()
                mock_root.title = Mock()
                mock_root.geometry = Mock()
                
                with patch('gui.NERDemoGUI.create_widgets'):
                    gui = NERDemoGUI(mock_root)
                    gui.nlp = None
                    
                    with patch('gui.messagebox.showwarning') as mock_warning:
                        gui.process_text()
                        
                        # Should show warning
                        mock_warning.assert_called_once()
                        args = mock_warning.call_args[0]
                        assert "No Model Loaded" in args[0]
                        
        except ImportError:
            pytest.skip("GUI module or tkinter not available")
    
    def test_process_text_without_input(self):
        """Test processing text without input."""
        try:
            from gui import NERDemoGUI
            
            with patch('gui.tk.Tk'):
                mock_root = Mock()
                mock_root.title = Mock()
                mock_root.geometry = Mock()
                
                with patch('gui.NERDemoGUI.create_widgets'):
                    gui = NERDemoGUI(mock_root)
                    gui.nlp = Mock()  # Model is loaded
                    
                    # Mock input_text to return empty string
                    gui.input_text = Mock()
                    gui.input_text.get = Mock(return_value="   ")
                    
                    with patch('gui.messagebox.showwarning') as mock_warning:
                        gui.process_text()
                        
                        # Should show warning
                        mock_warning.assert_called_once()
                        args = mock_warning.call_args[0]
                        assert "No Input Text" in args[0]
                        
        except ImportError:
            pytest.skip("GUI module or tkinter not available")
    
    def test_view_last_output_no_file(self):
        """Test viewing output when no file exists."""
        try:
            from gui import NERDemoGUI
            
            with patch('gui.tk.Tk'):
                mock_root = Mock()
                mock_root.title = Mock()
                mock_root.geometry = Mock()
                
                with patch('gui.NERDemoGUI.create_widgets'):
                    gui = NERDemoGUI(mock_root)
                    
                    # Mock empty output directory
                    with patch.object(Path, 'glob', return_value=[]), \
                         patch('gui.messagebox.showinfo') as mock_info:
                        
                        gui.view_last_output()
                        
                        # Should show info message
                        mock_info.assert_called_once()
                        args = mock_info.call_args[0]
                        assert "No Output" in args[0]
                        
        except ImportError:
            pytest.skip("GUI module or tkinter not available")


class TestGUIIntegration:
    """Integration tests for GUI workflows."""
    
    def test_model_path_construction(self):
        """Test that model paths are constructed correctly."""
        try:
            from gui import NERDemoGUI
            
            with patch('gui.tk.Tk'):
                mock_root = Mock()
                mock_root.title = Mock()
                mock_root.geometry = Mock()
                
                with patch('gui.NERDemoGUI.create_widgets'):
                    gui = NERDemoGUI(mock_root)
                    
                    # Test model path construction
                    expected_path = gui.models_dir / "test_model" / "model-best"
                    
                    # Verify path structure
                    assert expected_path.parent.parent == gui.models_dir
                    assert expected_path.name == "model-best"
                    
        except ImportError:
            pytest.skip("GUI module or tkinter not available")
    
    def test_output_directory_creation(self):
        """Test that output directory is created on initialization."""
        try:
            from gui import NERDemoGUI
            
            with patch('gui.tk.Tk'):
                mock_root = Mock()
                mock_root.title = Mock()
                mock_root.geometry = Mock()
                
                with patch.object(Path, 'mkdir') as mock_mkdir:
                    with patch('gui.NERDemoGUI.create_widgets'):
                        gui = NERDemoGUI(mock_root)
                        
                        # Verify mkdir was called with correct parameters
                        mock_mkdir.assert_called_with(parents=True, exist_ok=True)
                        
        except ImportError:
            pytest.skip("GUI module or tkinter not available")


class TestGUIConstants:
    """Test GUI constants and URLs."""
    
    def test_attribution_urls(self):
        """Test that attribution URLs are defined."""
        try:
            from gui import TESLA_URL, JERTEH_URL
            
            assert TESLA_URL == "https://tesla.rgf.bg.ac.rs/"
            assert JERTEH_URL == "https://jerteh.rs/"
            
        except ImportError:
            pytest.skip("GUI module not available")


class TestGUIErrorHandling:
    """Test error handling in GUI."""
    
    def test_load_model_not_found(self):
        """Test loading a model that doesn't exist."""
        try:
            from gui import NERDemoGUI
            
            with patch('gui.tk.Tk'):
                mock_root = Mock()
                mock_root.title = Mock()
                mock_root.geometry = Mock()
                
                with patch('gui.NERDemoGUI.create_widgets'):
                    gui = NERDemoGUI(mock_root)
                    gui.model_var = Mock()
                    gui.model_var.get = Mock(return_value="nonexistent_model")
                    
                    with patch.object(Path, 'exists', return_value=False), \
                         patch('gui.messagebox.showerror') as mock_error:
                        
                        gui.load_model()
                        
                        # Should show error
                        mock_error.assert_called_once()
                        args = mock_error.call_args[0]
                        assert "Model Not Found" in args[0]
                        
        except ImportError:
            pytest.skip("GUI module or tkinter not available")
    
    def test_load_model_no_selection(self):
        """Test loading a model with no selection."""
        try:
            from gui import NERDemoGUI
            
            with patch('gui.tk.Tk'):
                mock_root = Mock()
                mock_root.title = Mock()
                mock_root.geometry = Mock()
                
                with patch('gui.NERDemoGUI.create_widgets'):
                    gui = NERDemoGUI(mock_root)
                    gui.model_var = Mock()
                    gui.model_var.get = Mock(return_value="")
                    
                    with patch('gui.messagebox.showwarning') as mock_warning:
                        gui.load_model()
                        
                        # Should show warning
                        mock_warning.assert_called_once()
                        args = mock_warning.call_args[0]
                        assert "No Model Selected" in args[0]
                        
        except ImportError:
            pytest.skip("GUI module or tkinter not available")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
