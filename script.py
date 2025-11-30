import json
import os
import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox
from pathlib import Path
from deep_translator import GoogleTranslator
import threading

class TranslationSyncGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Translation Sync Tool")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")
        
        self.master_file = None
        self.translation_files = []
        self.folder_path = None
        
        self.create_ui()
    
    def create_ui(self):
        # Title
        title_frame = tk.Frame(self.root, bg="#2c3e50", height=60)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame, 
            text="🌍 Translation File Sync Tool",
            font=("Arial", 18, "bold"),
            bg="#2c3e50",
            fg="white"
        )
        title_label.pack(pady=15)
        
        # Main container
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Folder selection section
        folder_frame = tk.LabelFrame(
            main_frame, 
            text="📁 Select Folder",
            font=("Arial", 11, "bold"),
            bg="#f0f0f0",
            fg="#2c3e50"
        )
        folder_frame.pack(fill=tk.X, pady=(0, 15))
        
        folder_inner = tk.Frame(folder_frame, bg="#f0f0f0")
        folder_inner.pack(fill=tk.X, padx=10, pady=10)
        
        self.folder_label = tk.Label(
            folder_inner,
            text="No folder selected",
            font=("Arial", 10),
            bg="#f0f0f0",
            fg="#7f8c8d",
            anchor="w"
        )
        self.folder_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        browse_btn = tk.Button(
            folder_inner,
            text="Browse",
            command=self.browse_folder,
            bg="#3498db",
            fg="white",
            font=("Arial", 10, "bold"),
            cursor="hand2",
            relief=tk.FLAT,
            padx=20,
            pady=5
        )
        browse_btn.pack(side=tk.RIGHT, padx=(10, 0))
        
        # Files detected section
        files_frame = tk.LabelFrame(
            main_frame,
            text="📄 Detected Files",
            font=("Arial", 11, "bold"),
            bg="#f0f0f0",
            fg="#2c3e50"
        )
        files_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        self.files_text = scrolledtext.ScrolledText(
            files_frame,
            height=8,
            font=("Courier", 9),
            bg="white",
            fg="#2c3e50",
            relief=tk.FLAT,
            borderwidth=2
        )
        self.files_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.files_text.config(state=tk.DISABLED)
        
        # Sync button
        self.sync_btn = tk.Button(
            main_frame,
            text="🔄 Sync Translations",
            command=self.start_sync,
            bg="#27ae60",
            fg="white",
            font=("Arial", 12, "bold"),
            cursor="hand2",
            relief=tk.FLAT,
            padx=30,
            pady=10,
            state=tk.DISABLED
        )
        self.sync_btn.pack(pady=(0, 15))
        
        # Log section
        log_frame = tk.LabelFrame(
            main_frame,
            text="📋 Activity Log",
            font=("Arial", 11, "bold"),
            bg="#f0f0f0",
            fg="#2c3e50"
        )
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            height=10,
            font=("Courier", 9),
            bg="#2c3e50",
            fg="#ecf0f1",
            relief=tk.FLAT,
            borderwidth=2
        )
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.log_text.config(state=tk.DISABLED)
    
    def log(self, message, color=None):
        """Add message to log"""
        self.log_text.config(state=tk.NORMAL)
        if color:
            self.log_text.insert(tk.END, message + "\n", color)
        else:
            self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
        self.root.update()
    
    def browse_folder(self):
        """Open folder browser"""
        folder = filedialog.askdirectory(title="Select Translation Files Folder")
        if folder:
            self.folder_path = folder
            self.folder_label.config(text=folder, fg="#2c3e50")
            self.scan_folder()
    
    def scan_folder(self):
        """Scan folder for translation files"""
        self.log("Scanning folder for translation files...")
        
        json_files = list(Path(self.folder_path).glob("*.json"))
        
        # Find master file
        master_candidates = [
            f for f in json_files 
            if 'en' in f.stem.lower() or 'english' in f.stem.lower()
        ]
        
        if not master_candidates:
            self.log("❌ ERROR: No English master file found!", "error")
            self.log("   Expected filename with 'en' or 'english'")
            messagebox.showerror(
                "Error",
                "No English master file found!\nExpected filename with 'en' or 'english'"
            )
            return
        
        self.master_file = str(master_candidates[0])
        self.translation_files = [
            str(f) for f in json_files 
            if str(f) != self.master_file
        ]
        
        # Display files
        self.files_text.config(state=tk.NORMAL)
        self.files_text.delete(1.0, tk.END)
        
        self.files_text.insert(tk.END, f"✓ Master File:\n", "bold")
        self.files_text.insert(tk.END, f"  {Path(self.master_file).name}\n\n")
        
        self.files_text.insert(tk.END, f"✓ Translation Files ({len(self.translation_files)}):\n", "bold")
        for f in self.translation_files:
            self.files_text.insert(tk.END, f"  • {Path(f).name}\n")
        
        self.files_text.config(state=tk.DISABLED)
        
        self.log(f"✓ Found master file: {Path(self.master_file).name}")
        self.log(f"✓ Found {len(self.translation_files)} translation files")
        
        # Enable sync button
        self.sync_btn.config(state=tk.NORMAL)
    
    def start_sync(self):
        """Start sync in background thread"""
        self.sync_btn.config(state=tk.DISABLED, text="⏳ Syncing...")
        self.log("\n" + "="*50)
        self.log("Starting synchronization...")
        self.log("="*50)
        
        # Run sync in thread to prevent UI freeze
        thread = threading.Thread(target=self.sync_translations)
        thread.daemon = True
        thread.start()
    
    def sync_translations(self):
        """Main sync logic"""
        try:
            # Load master file
            self.log(f"\n📖 Loading master file...")
            with open(self.master_file, 'r', encoding='utf-8') as f:
                master_data = json.load(f)
            
            master_flat = self.flatten_dict(master_data)
            self.log(f"   {len(master_flat)} translation keys found")
            
            # Process each translation file
            for trans_file in self.translation_files:
                filename = Path(trans_file).name
                self.log(f"\n🔄 Processing: {filename}")
                
                # Detect language
                target_lang = self.detect_language(trans_file)
                self.log(f"   Language: {target_lang}")
                
                # Load translation file
                with open(trans_file, 'r', encoding='utf-8') as f:
                    trans_data = json.load(f)
                
                trans_flat = self.flatten_dict(trans_data)
                
                # Find missing keys
                missing_keys = set(master_flat.keys()) - set(trans_flat.keys())
                
                self.log(f"   Missing keys: {len(missing_keys)}")
                
                # Translate missing keys
                if missing_keys:
                    for i, key in enumerate(sorted(missing_keys), 1):
                        english_text = master_flat[key]
                        self.log(f"   [{i}/{len(missing_keys)}] Translating '{key}'...")
                        
                        translated = self.translate_text(english_text, target_lang)
                        trans_flat[key] = translated
                
                # Save updated file
                updated_data = self.unflatten_dict(trans_flat)
                with open(trans_file, 'w', encoding='utf-8') as f:
                    json.dump(updated_data, f, ensure_ascii=False, indent=2)
                
                self.log(f"   ✅ Updated {filename}")
            
            self.log("\n" + "="*50)
            self.log("✅ SYNC COMPLETED SUCCESSFULLY!")
            self.log("="*50)
            
            messagebox.showinfo("Success", "Translation sync completed successfully!")
            
        except Exception as e:
            self.log(f"\n❌ ERROR: {str(e)}")
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")
        
        finally:
            self.sync_btn.config(state=tk.NORMAL, text="🔄 Sync Translations")
    
    def flatten_dict(self, d, parent_key='', sep='.'):
        """Flatten nested dictionary"""
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(self.flatten_dict(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)
    
    def unflatten_dict(self, d, sep='.'):
        """Convert flat dict back to nested"""
        result = {}
        for key, value in d.items():
            parts = key.split(sep)
            current = result
            for part in parts[:-1]:
                if part not in current:
                    current[part] = {}
                current = current[part]
            current[parts[-1]] = value
        return result
    
    def detect_language(self, filepath):
        """Extract language code from filename"""
        filename = Path(filepath).stem
        parts = filename.split('_')
        if len(parts) > 1:
            lang = parts[-1].split('-')[0].lower()
            return lang
        return filename.split('-')[0].lower()
    
    def translate_text(self, text, target_lang):
        """Translate text using Deep Translator"""
        try:
            # Deep Translator uses standard language codes
            translator = GoogleTranslator(source='en', target=target_lang)
            result = translator.translate(text)
            return result
        except Exception as e:
            self.log(f"      ⚠️ Translation failed: {e}")
            return text

if __name__ == "__main__":
    root = tk.Tk()
    app = TranslationSyncGUI(root)
    root.mainloop()