#!/usr/bin/env python3
"""
NEL Demo - spaCy NER+NEL GUI Application

A simple GUI for demonstrating Named Entity Recognition (NER) and 
Named Entity Linking (NEL) using spaCy models.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime
import webbrowser

# Add the project root to the path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

try:
    import spacy
    from spacy import displacy
except ImportError:
    print("Error: spaCy is not installed.")
    print("Please run the installer script (install.ps1 or install.sh) first.")
    sys.exit(1)

# Import text chunker module
try:
    from text_chunker import process_text_in_chunks, split_into_paragraphs, DEFAULT_MAX_CHUNK_SIZE
except ImportError:
    print("Warning: text_chunker module not found. Large text processing may fail.")
    process_text_in_chunks = None
    split_into_paragraphs = None
    # Fallback value matches the default in text_chunker.py
    DEFAULT_MAX_CHUNK_SIZE = 100000  # 100K characters per chunk

# Attribution URLs
TESLA_URL = "https://tesla.rgf.bg.ac.rs/"
JERTEH_URL = "https://jerteh.rs/"

# File loading constants
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB limit for file loading


class ToolTip:
    """Simple tooltip widget for tkinter labels."""
    
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)
    
    def show_tooltip(self, event=None):
        if self.tooltip_window or not self.text:
            return
        x = self.widget.winfo_rootx() + 25
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 5
        
        self.tooltip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        
        label = tk.Label(
            tw, 
            text=self.text, 
            justify=tk.LEFT,
            background="#ffffe0", 
            relief=tk.SOLID, 
            borderwidth=1,
            font=("Arial", 9)
        )
        label.pack()
    
    def hide_tooltip(self, event=None):
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None


class NERDemoGUI:
    """Main GUI application for NER+NEL demonstration."""
    
    def __init__(self, root):
        """Initialize the GUI application.
        
        Args:
            root: The root tkinter window
        """
        self.root = root
        self.root.title("spaCy NER+NEL Demo")
        self.root.geometry("900x700")
        
        self.nlp = None
        self.model_name = None
        self.output_dir = PROJECT_ROOT / "data" / "outputs"
        self.models_dir = PROJECT_ROOT / "models"
        self.inputs_dir = PROJECT_ROOT / "inputs"
        
        # Ensure output and inputs directories exist
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.inputs_dir.mkdir(parents=True, exist_ok=True)
        
        self.create_widgets()
        self.check_models()
        
    def create_widgets(self):
        """Create and layout all GUI widgets."""
        # Title
        title_label = tk.Label(
            self.root,
            text="spaCy NER+NEL Demo",
            font=("Arial", 18, "bold"),
            pady=10
        )
        title_label.pack()
        
        # Attribution
        attribution_frame = tk.Frame(self.root)
        attribution_frame.pack()
        
        made_by_label = tk.Label(
            attribution_frame,
            text="Made by ",
            font=("Arial", 9),
            fg="#808080"
        )
        made_by_label.pack(side=tk.LEFT)
        
        tesla_link = tk.Label(
            attribution_frame,
            text="TESLA",
            font=("Arial", 9, "underline"),
            fg="#0066CC",
            cursor="hand2"
        )
        tesla_link.pack(side=tk.LEFT)
        tesla_link.bind("<Button-1>", lambda e: webbrowser.open(TESLA_URL))
        ToolTip(tesla_link, "TESLA - Text Embeddings - Serbian Language Applications\nClick to visit: https://tesla.rgf.bg.ac.rs/")
        
        and_label = tk.Label(
            attribution_frame,
            text=" and ",
            font=("Arial", 9),
            fg="#808080"
        )
        and_label.pack(side=tk.LEFT)
        
        jerteh_link = tk.Label(
            attribution_frame,
            text="Jerteh",
            font=("Arial", 9, "underline"),
            fg="#0066CC",
            cursor="hand2"
        )
        jerteh_link.pack(side=tk.LEFT)
        jerteh_link.bind("<Button-1>", lambda e: webbrowser.open(JERTEH_URL))
        ToolTip(jerteh_link, "Language Resources and Technologies Society - Jerteh\nClick to visit: https://jerteh.rs/")

        # Model selection frame
        model_frame = ttk.LabelFrame(self.root, text="Model Selection", padding=10)
        model_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(model_frame, text="Model:").grid(row=0, column=0, sticky=tk.W, padx=5)
        
        self.model_var = tk.StringVar()
        self.model_combo = ttk.Combobox(
            model_frame,
            textvariable=self.model_var,
            state="readonly",
            width=40
        )
        self.model_combo.grid(row=0, column=1, padx=5, sticky=tk.W)
        
        ttk.Button(
            model_frame,
            text="Load Model",
            command=self.load_model
        ).grid(row=0, column=2, padx=5)
        
        ttk.Button(
            model_frame,
            text="Refresh",
            command=self.check_models
        ).grid(row=0, column=3, padx=5)
        
        self.model_status_label = ttk.Label(model_frame, text="No model loaded", foreground="red")
        self.model_status_label.grid(row=1, column=0, columnspan=4, sticky=tk.W, padx=5, pady=5)
        
        # Input frame
        input_frame = ttk.LabelFrame(self.root, text="Input Text", padding=10)
        input_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.input_text = scrolledtext.ScrolledText(
            input_frame,
            wrap=tk.WORD,
            height=10,
            font=("Arial", 10)
        )
        self.input_text.pack(fill=tk.BOTH, expand=True)
        
        # Sample text button
        sample_frame = tk.Frame(input_frame)
        sample_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(
            sample_frame,
            text="Load Sample Text",
            command=self.load_sample_text
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            sample_frame,
            text="Load from File",
            command=self.load_text_from_file
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            sample_frame,
            text="Clear",
            command=lambda: self.input_text.delete(1.0, tk.END)
        ).pack(side=tk.LEFT, padx=5)
        
        # Action buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(
            button_frame,
            text="Process Text (NER)",
            command=self.process_text,
            style="Accent.TButton"
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame,
            text="View Last Output",
            command=self.view_last_output
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame,
            text="Open Output Folder",
            command=self.open_output_folder
        ).pack(side=tk.LEFT, padx=5)
        
        # Results frame
        results_frame = ttk.LabelFrame(self.root, text="Results", padding=10)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.results_text = scrolledtext.ScrolledText(
            results_frame,
            wrap=tk.WORD,
            height=8,
            font=("Courier", 9)
        )
        self.results_text.pack(fill=tk.BOTH, expand=True)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(
            self.root,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)
        
    def check_models(self):
        """Check for available models in the models directory."""
        self.model_combo['values'] = []
        
        if not self.models_dir.exists():
            self.models_dir.mkdir(parents=True, exist_ok=True)
            self.status_var.set("Created models directory. Please add trained models.")
            return
        
        # Look for models in the models directory
        available_models = []
        
        # Check for model-best directories
        for model_dir in self.models_dir.iterdir():
            if model_dir.is_dir():
                model_best_path = model_dir / "model-best"
                if model_best_path.exists() and model_best_path.is_dir():
                    available_models.append(model_dir.name)
        
        if available_models:
            self.model_combo['values'] = available_models
            self.model_combo.current(0)
            self.status_var.set(f"Found {len(available_models)} model(s)")
        else:
            self.status_var.set("No models found. Please add models to the models/ directory.")
            messagebox.showinfo(
                "No Models Found",
                "No trained models found in the models/ directory.\n\n"
                "Please place your trained spaCy model in:\n"
                "models/{model_name}/model-best/\n\n"
                "Or download a pre-trained model:\n"
                "python -m spacy download en_core_web_sm"
            )
    
    def load_model(self):
        """Load the selected spaCy model."""
        model_name = self.model_var.get()
        
        if not model_name:
            messagebox.showwarning("No Model Selected", "Please select a model first.")
            return
        
        model_path = self.models_dir / model_name / "model-best"
        
        if not model_path.exists():
            messagebox.showerror(
                "Model Not Found",
                f"Model path does not exist:\n{model_path}"
            )
            return
        
        try:
            self.status_var.set(f"Loading model: {model_name}...")
            self.root.update()
            
            self.nlp = spacy.load(model_path)
            self.model_name = model_name
            
            self.model_status_label.config(
                text=f"Model loaded: {model_name}",
                foreground="green"
            )
            self.status_var.set(f"Model loaded successfully: {model_name}")
            
            # Display model info
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, f"Model: {model_name}\n")
            self.results_text.insert(tk.END, f"Path: {model_path}\n")
            self.results_text.insert(tk.END, f"Pipeline: {self.nlp.pipe_names}\n")
            
            if self.nlp.meta:
                self.results_text.insert(tk.END, f"\nModel Metadata:\n")
                for key, value in self.nlp.meta.items():
                    self.results_text.insert(tk.END, f"  {key}: {value}\n")
            
        except Exception as e:
            messagebox.showerror(
                "Error Loading Model",
                f"Failed to load model:\n{str(e)}"
            )
            self.status_var.set("Error loading model")
    
    def load_sample_text(self):
        """Load sample text for demonstration."""
        sample_text = (
            "Народна банка Србије је централна банка Републике Србије са седиштем у Београду. "
            "Гувернер Народне банке Србије је Јорданка Табаковић која се налази на тој позицији од 2012. године. "
            "Народна банка Србије је основана 1884. године као Привилегована народна банка Краљевине Србије.\n\n"
            
            "Универзитет у Београду је најстарији и највећи универзитет у Србији, основан 1808. године. "
            "Ректор Универзитета у Београду је професор Владан Ђокић. "
            "Универзитет има 31 факултет и више од 90.000 студената. "
            "Налази се у Београду, а његов главни кампус је на Студентском тргу.\n\n"
            
            "Новак Ђоковић је српски тенисер рођен у Београду 1987. године. "
            "Ђоковић је освојио 24 Гренд слем титуле у појединачној конкуренцији. "
            "Тренутно живи у Монте Карлу, али редовно посећује Србију. "
            "Његов тренер је био Горан Иванишевић, бивши хрватски тенисер."
        )
        self.input_text.delete(1.0, tk.END)
        self.input_text.insert(1.0, sample_text)
        self.status_var.set("Sample text loaded")
    
    def load_text_from_file(self):
        """Load text from a file using file dialog."""
        # Open file dialog starting in the inputs directory if it exists
        initial_dir = self.inputs_dir if self.inputs_dir.exists() else None
        file_path = filedialog.askopenfilename(
            title="Select Text File",
            initialdir=initial_dir,
            filetypes=[
                ("Text Files", "*.txt"),
                ("All Files", "*.*")
            ]
        )
        
        if file_path:
            try:
                # Check file size to prevent memory issues
                file_size = Path(file_path).stat().st_size
                if file_size > MAX_FILE_SIZE:
                    messagebox.showwarning(
                        "File Too Large",
                        f"File size ({file_size / 1024 / 1024:.1f} MB) exceeds maximum allowed size (10 MB)."
                    )
                    self.status_var.set("File too large to load")
                    return
                
                # Try to read the file with UTF-8 encoding first
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='strict') as f:
                        text = f.read()
                except UnicodeDecodeError:
                    # Fallback to latin-1 encoding if UTF-8 fails (latin-1 accepts all bytes)
                    with open(file_path, 'r', encoding='latin-1') as f:
                        text = f.read()
                
                # Load into text area
                self.input_text.delete(1.0, tk.END)
                self.input_text.insert(1.0, text)
                
                # Update status
                file_name = Path(file_path).name
                self.status_var.set(f"Loaded file: {file_name}")
                
            except Exception as e:
                messagebox.showerror(
                    "Error Loading File",
                    f"Failed to load file:\n{str(e)}"
                )
                self.status_var.set("Error loading file")
    
    def process_text(self):
        """Process the input text and display NER results."""
        if self.nlp is None:
            messagebox.showwarning(
                "No Model Loaded",
                "Please load a model first."
            )
            return
        
        text = self.input_text.get(1.0, tk.END).strip()
        
        if not text:
            messagebox.showwarning(
                "No Input Text",
                "Please enter some text to process."
            )
            return
        
        try:
            self.status_var.set("Processing text...")
            self.root.update()
            
            # Check if text has multiple paragraphs (chunking improves NER with paragraph context)
            text_length = len(text)
            if split_into_paragraphs is not None:
                paragraphs = split_into_paragraphs(text)
            else:
                # Fallback paragraph detection if text_chunker module failed to import
                paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
            
            has_multiple_paragraphs = len(paragraphs) > 1
            
            if has_multiple_paragraphs and process_text_in_chunks is not None:
                # Use chunking for multi-paragraph texts
                self.status_var.set(f"Processing text ({text_length:,} chars, {len(paragraphs)} paragraphs) in chunks...")
                self.root.update()
                
                # Save output file path
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_file = self.output_dir / f"ner_output_{timestamp}.html"
                
                # Process text in chunks
                all_entities, html, num_chunks = process_text_in_chunks(
                    self.nlp, 
                    text, 
                    max_chunk_size=DEFAULT_MAX_CHUNK_SIZE,
                    output_path=output_file
                )
                
                # Display entities in results
                self.results_text.delete(1.0, tk.END)
                self.results_text.insert(tk.END, "Named Entities Found (Chunked Processing):\n")
                self.results_text.insert(tk.END, "=" * 60 + "\n\n")
                
                if all_entities:
                    # Show first 100 entities to avoid overwhelming the UI
                    display_limit = 100
                    for i, ent in enumerate(all_entities[:display_limit]):
                        self.results_text.insert(
                            tk.END,
                            f"Text: {ent.text:20} | Label: {ent.label_:10} | "
                            f"Start: {ent.start_char:4} | End: {ent.end_char:4}\n"
                        )
                        # If entity has KB ID (for NEL)
                        if hasattr(ent, 'kb_id_') and ent.kb_id_:
                            self.results_text.insert(tk.END, f"  KB ID: {ent.kb_id_}\n")
                    
                    if len(all_entities) > display_limit:
                        self.results_text.insert(
                            tk.END, 
                            f"\n... and {len(all_entities) - display_limit} more entities\n"
                        )
                else:
                    self.results_text.insert(tk.END, "No entities found.\n")
                
                self.results_text.insert(tk.END, f"\n\nTotal entities: {len(all_entities)}\n")
                self.results_text.insert(tk.END, f"Text was split into {num_chunks} chunk(s) from {len(paragraphs)} paragraph(s) for better context.\n")
                
                self.last_output_file = output_file
                self.status_var.set(f"Processing complete. Output saved to: {output_file.name}")
                
                messagebox.showinfo(
                    "Processing Complete",
                    f"Found {len(all_entities)} entities in {text_length:,} characters.\n\n"
                    f"Processed as {num_chunks} chunk(s) from {len(paragraphs)} paragraph(s) for better context.\n\n"
                    f"HTML visualization saved to:\n{output_file.name}\n\n"
                    "Click 'View Last Output' to open in browser."
                )
            else:
                # Process text normally (single paragraph or no chunking available)
                doc = self.nlp(text)
                
                # Display entities in results
                self.results_text.delete(1.0, tk.END)
                self.results_text.insert(tk.END, "Named Entities Found:\n")
                self.results_text.insert(tk.END, "=" * 60 + "\n\n")
                
                if doc.ents:
                    for ent in doc.ents:
                        self.results_text.insert(
                            tk.END,
                            f"Text: {ent.text:20} | Label: {ent.label_:10} | "
                            f"Start: {ent.start_char:4} | End: {ent.end_char:4}\n"
                        )
                        # If entity has KB ID (for NEL)
                        if hasattr(ent, 'kb_id_') and ent.kb_id_:
                            self.results_text.insert(tk.END, f"  KB ID: {ent.kb_id_}\n")
                else:
                    self.results_text.insert(tk.END, "No entities found.\n")
                
                self.results_text.insert(tk.END, f"\n\nTotal entities: {len(doc.ents)}\n")
                
                # Generate HTML visualization with displaCy
                html = displacy.render(doc, style="ent", page=True)
                
                # Save HTML to output directory
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_file = self.output_dir / f"ner_output_{timestamp}.html"
                
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(html)
                
                self.last_output_file = output_file
                self.status_var.set(f"Processing complete. Output saved to: {output_file.name}")
                
                messagebox.showinfo(
                    "Processing Complete",
                    f"Found {len(doc.ents)} entities.\n\n"
                    f"HTML visualization saved to:\n{output_file.name}\n\n"
                    "Click 'View Last Output' to open in browser."
                )
            
        except Exception as e:
            messagebox.showerror(
                "Processing Error",
                f"Error processing text:\n{str(e)}"
            )
            self.status_var.set("Error processing text")
    
    def view_last_output(self):
        """Open the last generated HTML output in the default browser."""
        if hasattr(self, 'last_output_file') and self.last_output_file.exists():
            webbrowser.open(f"file://{self.last_output_file.absolute()}")
            self.status_var.set(f"Opened: {self.last_output_file.name}")
        else:
            # Try to find the most recent output
            output_files = sorted(self.output_dir.glob("ner_output_*.html"), reverse=True)
            if output_files:
                webbrowser.open(f"file://{output_files[0].absolute()}")
                self.status_var.set(f"Opened: {output_files[0].name}")
            else:
                messagebox.showinfo(
                    "No Output",
                    "No output files found. Process some text first."
                )
    
    def open_output_folder(self):
        """Open the output folder in the system file explorer."""
        try:
            if sys.platform == 'win32':
                subprocess.run(['explorer', str(self.output_dir)], check=False)
            elif sys.platform == 'darwin':  # macOS
                subprocess.run(['open', str(self.output_dir)], check=False)
            else:  # Linux
                subprocess.run(['xdg-open', str(self.output_dir)], check=False)
            
            self.status_var.set(f"Opened output folder")
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Could not open output folder:\n{str(e)}"
            )


def main():
    """Main entry point for the application."""
    root = tk.Tk()
    app = NERDemoGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
