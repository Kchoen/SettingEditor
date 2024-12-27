import tkinter as tk
from tkinter import ttk, messagebox

class NodeDialog:
    def __init__(self, node_data):
        self.root = tk.Tk()
        self.root.deiconify()  # Hide the root window
        
        self.top = tk.Toplevel(self.root)
        self.result = {"isDelete": False, "data": node_data}
        self.node_data = node_data.copy()
        self.cancelled = True
        
        # Set dialog title
        self.top.title("Edit Node")
        
        # Create main frame
        main_frame = ttk.Frame(self.top, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create position coordinates section
        ttk.Label(main_frame, text="顯示座標位置(X:[0,1500],Y:[0,1000])").grid(row=0, column=0, columnspan=2, sticky=tk.W)
        coord_frame = ttk.Frame(main_frame)
        coord_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        # X coordinate
        ttk.Label(coord_frame, text="X座標:").grid(row=0, column=0, sticky=tk.W)
        self.x_entry = ttk.Entry(coord_frame, width=10)
        self.x_entry.insert(0, str(node_data.get('x', '')))
        self.x_entry.grid(row=0, column=1, padx=5)
        
        # Y coordinate
        ttk.Label(coord_frame, text="Y座標:").grid(row=0, column=2, sticky=tk.W)
        self.y_entry = ttk.Entry(coord_frame, width=10)
        self.y_entry.insert(0, str(node_data.get('y', '')))
        self.y_entry.grid(row=0, column=3, padx=5)

        # Create nodes section
        row = 3
        ttk.Label(main_frame, text="目的地設定").grid(row=row, column=0, columnspan=2, sticky=tk.W)
        row += 1
        
        self.nodes_frame = ttk.Frame(main_frame)
        self.nodes_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        self.node_entries = []
        for dest_data in node_data.get('nodes', []):
            self.add_destination_entry(dest_data)
        
        # Add/Remove destination buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=row+1, column=0, columnspan=2, sticky=(tk.W, tk.E))
        ttk.Button(button_frame, text="新增目的地", command=lambda: self.add_destination_entry()).pack(side=tk.LEFT)
        
        # OK/Cancel/Delete buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=row+2, column=0, columnspan=2, sticky=(tk.W, tk.E))
        ttk.Button(button_frame, text="確認", command=self.on_ok).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="取消", command=self.on_cancel).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="刪除節點", command=self.on_delete).pack(side=tk.LEFT, padx=5)

        # Center the dialog on screen
        self.center_window()
        
        # Make dialog modal
        self.top.transient(self.root)
        self.top.grab_set()
        
        # Handle window close button
        self.top.protocol("WM_DELETE_WINDOW", self.on_cancel)
        
        self.root.wait_window(self.top)
        
    def center_window(self):
        # Get screen dimensions
        screen_width = self.top.winfo_screenwidth()
        screen_height = self.top.winfo_screenheight()
        
        # Wait for the window to be ready
        self.top.update_idletasks()
        
        # Calculate position
        width = self.top.winfo_width()
        height = self.top.winfo_height()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        # Set the position
        self.top.geometry(f'+{x}+{y}')
        
    def add_destination_entry(self, dest_data=None):
        entry_frame = ttk.Frame(self.nodes_frame)
        entry_frame.pack(fill=tk.X, pady=2)
        
        # Add labels and entries for each field
        ttk.Label(entry_frame, text="名稱:").pack(side=tk.LEFT)
        dest_entry = ttk.Entry(entry_frame, width=20)
        if dest_data:
            dest_entry.insert(0, dest_data.get('destination', ''))
        dest_entry.pack(side=tk.LEFT, padx=2)
        
        ttk.Label(entry_frame, text="英文名稱:").pack(side=tk.LEFT)
        eng_entry = ttk.Entry(entry_frame, width=20)
        if dest_data:
            eng_entry.insert(0, dest_data.get('englishDestination', ''))
        eng_entry.pack(side=tk.LEFT, padx=2)
        
        ttk.Label(entry_frame, text="局處:").pack(side=tk.LEFT)
        bureau_entry = ttk.Entry(entry_frame, width=15)
        if dest_data:
            bureau_entry.insert(0, dest_data.get('bureau', ''))
        bureau_entry.pack(side=tk.LEFT, padx=2)

        enable_check = ttk.Checkbutton(
            entry_frame, 
            text="啟用"
        )
        enable_check.pack(side=tk.LEFT, padx=2)
        if (dest_data and dest_data.get('enable', True)):
            enable_check.state(['selected'])
        else:
            enable_check.state(['!alternate'])
        
        # Add remove button
        remove_btn = ttk.Button(entry_frame, text="移除", 
                              command=lambda f=entry_frame, e=(dest_entry, eng_entry, bureau_entry, enable_check): 
                              self.remove_specific_destination(f, e))
        remove_btn.pack(side=tk.LEFT, padx=2)
        
        self.node_entries.append((dest_entry, eng_entry, bureau_entry, enable_check))
    
    def remove_specific_destination(self, frame, entries):
        self.node_entries.remove(entries)
        frame.destroy()
    
    def on_ok(self):
        try:
            # Update coordinates
            self.node_data['x'] = float(self.x_entry.get())
            self.node_data['y'] = float(self.y_entry.get())
            # Update nodes array
            self.node_data['nodes'] = []
            for dest_entry, eng_entry, bureau_entry, enable_check in self.node_entries:
                if dest_entry.get() and bureau_entry.get():
                    self.node_data['nodes'].append({
                        'destination': dest_entry.get(),
                        'englishDestination': eng_entry.get(),
                        'bureau': bureau_entry.get(),
                        'enable': 'selected' in enable_check.state()
                    })
            
            self.result = {"isDelete": False, "data": self.node_data}
            self.cancelled = False
            self.top.destroy()
            self.root.destroy()
        except ValueError as e:
            messagebox.showerror("Error", "座標值必須為數字")

    def on_cancel(self):
        self.result = {"isDelete": False, "data": self.node_data}
        self.cancelled = True
        self.top.destroy()
        self.root.destroy()

    def on_delete(self):
        self.result = {"isDelete": True, "data": self.node_data}
        self.cancelled = False
        self.top.destroy()
        self.root.destroy()

def main(node_data):
    dialog = NodeDialog(node_data)
    return dialog.result