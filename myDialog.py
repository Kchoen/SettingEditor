import tkinter as tk
from tkinter import ttk

class NodeDialog:
    def __init__(self, parent, node_data):
        self.top = tk.Toplevel(parent)
        self.result = {"isDelete": False, "data": node_data}
        self.node_data = node_data.copy()
        self.cancelled = True
        
        # Create main frame
        main_frame = ttk.Frame(self.top, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create position coordinates section first
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
        
        # Create basic information fields
        row = 2
        for field in ['building', 'floor', 'canTakeElevator', 'NodeId2DA', 'NodeId2DB', 
                     'nodeIdA', 'nodeIdB', 'OtherBuildEndNodeId2D', 'OtherBuildStartNodeId2D', 'turnTo']:
            ttk.Label(main_frame, text=field).grid(row=row, column=0, sticky=tk.W)
            entry = ttk.Entry(main_frame)
            entry.insert(0, str(node_data.get(field, '')))
            entry.grid(row=row, column=1, sticky=(tk.W, tk.E))
            setattr(self, f'{field}_entry', entry)
            row += 1
        
        # Create nodes section (destinations and bureaus)
        ttk.Label(main_frame, text="目的地名稱").grid(row=row, column=0, columnspan=2, sticky=tk.W)
        row += 1
        
        self.nodes_frame = ttk.Frame(main_frame)
        self.nodes_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        self.node_entries = []
        for dest_data in node_data.get('nodes', []):
            self.add_destination_entry(dest_data)
        
        # Add destination button
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=row+1, column=0, columnspan=2, sticky=(tk.W, tk.E))
        ttk.Button(button_frame, text="新增目的地名稱", command=self.add_destination_entry).pack(side=tk.LEFT)
        
        # OK/Cancel buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=row+2, column=0, columnspan=2, sticky=(tk.W, tk.E))
        ttk.Button(button_frame, text="確認", command=self.on_ok).pack(side=tk.LEFT)
        ttk.Button(button_frame, text="取消", command=self.on_cancel).pack(side=tk.LEFT)
        ttk.Button(button_frame, text="刪除節點", command=self.on_delete).pack(side=tk.LEFT)
        
        # Make dialog modal
        self.top.transient(parent)
        self.top.grab_set()
        parent.wait_window(self.top)
        
    def add_destination_entry(self, dest_data=None):
        entry_frame = ttk.Frame(self.nodes_frame)
        entry_frame.pack(fill=tk.X)
        
        # Add labels for each field
        ttk.Label(entry_frame, text="目的地名稱:").pack(side=tk.LEFT)
        dest_entry = ttk.Entry(entry_frame, width=30)
        if dest_data:
            dest_entry.insert(0, dest_data['destination'])
        dest_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(entry_frame, text="局處分類:").pack(side=tk.LEFT)
        bureau_entry = ttk.Entry(entry_frame, width=30)
        if dest_data:
            bureau_entry.insert(0, dest_data['bureau'])
        bureau_entry.pack(side=tk.LEFT, padx=5)
        
        # Add remove button for this specific entry
        remove_btn = ttk.Button(entry_frame, text="移除", 
                              command=lambda f=entry_frame, e=(dest_entry, bureau_entry): 
                              self.remove_specific_destination(f, e))
        remove_btn.pack(side=tk.LEFT, padx=5)
        
        self.node_entries.append((dest_entry, bureau_entry))
    
    def remove_specific_destination(self, frame, entries):
        self.node_entries.remove(entries)
        frame.destroy()
    
    def on_ok(self):
        try:
            # Update coordinates
            self.node_data['x'] = float(self.x_entry.get())
            self.node_data['y'] = float(self.y_entry.get())
            
            # Update basic fields
            for field in ['building', 'floor', 'canTakeElevator', 'NodeId2DA', 'NodeId2DB', 
                         'nodeIdA', 'nodeIdB', 'OtherBuildEndNodeId2D', 'OtherBuildStartNodeId2D', 'turnTo']:
                entry_value = getattr(self, f'{field}_entry').get()
                # Convert numeric fields to integers
                if field in ['NodeId2DA', 'NodeId2DB', 'nodeIdA', 'nodeIdB', 
                            'OtherBuildEndNodeId2D', 'OtherBuildStartNodeId2D', 'turnTo']:
                    try:
                        self.node_data[field] = int(entry_value)
                    except ValueError:
                        self.node_data[field] = 0
                else:
                    self.node_data[field] = entry_value
            
            # Update nodes array
            self.node_data['nodes'] = []
            for dest_entry, bureau_entry in self.node_entries:
                if dest_entry.get() and bureau_entry.get():
                    self.node_data['nodes'].append({
                        'destination': dest_entry.get(),
                        'bureau': bureau_entry.get()
                    })
            
            self.result = {"isDelete": False, "data": self.node_data}
            self.cancelled = False
            self.top.destroy()
        except ValueError as e:
            tk.messagebox.showerror("Error", "Invalid coordinate values. Please enter numbers only.")

    def on_cancel(self):
        self.result = {"isDelete": False, "data": self.node_data}
        self.cancelled = True
        self.top.destroy()

    def on_delete(self):
        self.result = {"isDelete": True, "data": self.node_data}
        self.cancelled = False
        self.top.destroy()

def main(node_data):
    root = tk.Tk()
    dialog = NodeDialog(root, node_data)
    if dialog.cancelled:
        result = {"isDelete": False, "data": node_data}
    else:
        result = dialog.result
    root.destroy()
    return result