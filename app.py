import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog
from PIL import Image, ImageTk
from functools import reduce
import myDialog
import json
FONT_SIZE = 16
MARK_SIZE = 10
class BuildingFloorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("導覽點位修改器")
        self.root.state("zoomed")

        # Main frames
        self.top_frame = tk.Frame(root, height=50, bg="lightgray")
        self.top_frame.pack(side=tk.TOP, fill=tk.X)
        self.left_frame = tk.Frame(root, width=200, bg="white")
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y)
        self.right_frame = tk.Frame(root, width=200, bg="lightblue")
        self.right_frame.pack(side=tk.RIGHT, fill=tk.Y)
        self.center_frame = tk.Frame(root, bg="white")
        self.center_frame.pack(expand=True, fill=tk.BOTH)

        # Variables
        self.building_selection = tk.StringVar()
        self.selected_floor = tk.StringVar()
        self.isHover = False
        # Dictionary for floors
        self.a_floors = [f"A樓-{i}樓" for i in range(1, 11)]
        self.b_floors = [f"B樓-{i}樓" for i in range(1, 11)]
        self.floor_images = {
            "A樓-1樓": "./image/A1F.jpg",
            "A樓-2樓": "./image/A2F.jpg",
            "A樓-3樓": "./image/A3F.jpg",
            "A樓-4樓": "./image/A4F.jpg",
            "A樓-5樓": "./image/A5F.jpg",
            "A樓-6樓": "./image/A6F.jpg",
            "A樓-7樓": "./image/A7F.jpg",
            "A樓-8樓": "./image/A8F.jpg",
            "A樓-9樓": "./image/A9F.jpg",
            "A樓-10樓": "./image/A10F.jpg",
            "B樓-1樓": "./image/B1F.jpg",
            "B樓-2樓": "./image/B2F.jpg",
            "B樓-3樓": "./image/B3F.jpg",
            "B樓-4樓": "./image/B4F.jpg",
            "B樓-5樓": "./image/B5F.jpg",
            "B樓-6樓": "./image/B6F.jpg",
            "B樓-7樓": "./image/B7F.jpg",
            "B樓-8樓": "./image/B8F.jpg",
            "B樓-9樓": "./image/B9F.jpg",
            "B樓-10樓": "./image/B10F.jpg"
        }
        self.marked_nodes = {
            "A樓-1樓": [],
            "A樓-2樓": [],
            "A樓-3樓": [],
            "A樓-4樓": [],
            "A樓-5樓": [],
            "A樓-6樓": [],
            "A樓-7樓": [],
            "A樓-8樓": [],
            "A樓-9樓": [],
            "A樓-10樓": [],
            "B樓-1樓": [],
            "B樓-2樓": [],
            "B樓-3樓": [],
            "B樓-4樓": [],
            "B樓-5樓": [],
            "B樓-6樓": [],
            "B樓-7樓": [],
            "B樓-8樓": [],
            "B樓-9樓": [],
            "B樓-10樓": []
        }
        # Initialize UI
        self.create_menu()
        self.create_building_selector()
        self.create_floor_list()
        self.create_floor_canvas()
        self.init_setting()

    # MENU選單選項設定(儲存/匯入點位設定)
    def create_menu(self):
        """Create a menu bar with Save and Import options."""
        self.menu_bar = tk.Menu(self.root)
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="儲存點位設定", command=self.save_nodes_to_json)
        file_menu.add_command(label="匯入點位設定", command=self.import_nodes_from_json)
        file_menu.add_command(label="轉換設定檔", command=self.transform_nodes_from_setting)
        file_menu.add_command(label="匯出為初始設定檔格式", command=self.export_initial_format)
        self.menu_bar.add_cascade(label="儲存/匯入設定檔", menu=file_menu)
        self.root.config(menu=self.menu_bar)
    # 初始化AB棟選項及按鈕
    def create_building_selector(self):
        """Create building selection buttons in the top frame."""
        self.a_building_button = tk.Button(
            self.top_frame, text="A棟(惠中樓)", width=10, command=lambda: self.select_building('A樓')
        )
        self.b_building_button = tk.Button(
            self.top_frame, text="B棟(文心樓)", width=10, command=lambda: self.select_building('B樓')
        )
        self.b_building_button.pack(side=tk.RIGHT, padx=10, pady=10)
        self.a_building_button.pack(side=tk.RIGHT, padx=10, pady=10)
        # Top label

        self.selected_lable = tk.Label(
            self.top_frame, text="", bg="lightgray", font=("Arial", FONT_SIZE)
        )
        self.selected_lable.pack(side=tk.TOP)
        # Initially collapsed state
        self.current_building = None
        self.floor_buttons = []

    # 初始化樓層列表
    def create_floor_list(self):
        """Create the floor list on the right frame with scrollbar."""
        self.floor_listbox = tk.Listbox(
            self.right_frame, height=20, bg="white"
        )
        self.floor_listbox.pack(side=tk.LEFT, fill=tk.Y)
        self.floor_listbox.bind("<ButtonRelease-1>", self.select_floor)

    # 選擇AB棟行為內容
    def select_building(self, building):
        """Expand building floors and collapse the other building."""
        if self.current_building == building:
            return
        self.current_building = building
        self.floor_listbox.delete(0, tk.END)
        floor_list = self.a_floors if building == 'A樓' else self.b_floors
        for floor in floor_list:
            self.floor_listbox.insert(tk.END, floor)

    # 初始化中央Canvas
    def create_floor_canvas(self):
        """Create canvas for displaying floor plan in the center frame."""
        self.canvas = tk.Canvas(self.center_frame, bg="white")
        self.canvas.pack(expand=True, fill=tk.BOTH)
        self.canvas.bind("<Motion>", self.hover_node)
        self.canvas.bind("<Button-1>", self.create_mark)
        self.hover_label = tk.Label(self.center_frame, text="", bg="yellow", relief="solid")
        self.hover_label.pack_forget()
        
        

    # 選擇樓層行為內容
    def select_floor(self, event):
        """Display the selected floor plan on the canvas and render nodes."""
        try:
            try:
                index = self.floor_listbox.curselection()[0]
                self.floor_name = self.floor_listbox.get(index)
                self.selected_floor.set(self.floor_name)
            except:
                pass
            floor_name = self.floor_name
            self.selected_lable.config(text=f"目前顯示位置 : {floor_name}")
            self.canvas.delete("all")
            
            image_path = self.floor_images.get(floor_name, "./image/1F.jpg")
            try:
                # Display image
                img = Image.open(image_path)
                self.image = img.resize((self.canvas.winfo_width()//2, self.canvas.winfo_height()))
                self.floor_image = ImageTk.PhotoImage(self.image)
                self.canvas.create_image(self.canvas.winfo_width() // 2, self.canvas.winfo_height() // 2, image=self.floor_image)

                # Display nodes
                for node in self.marked_nodes.get(floor_name, []):
                    x, y = node.get('x'), node.get('y')
                    key = node.get('nodeIdA') if "A樓" in node.get('floor') else node.get('nodeIdB')
                    # Get primary destination from first node
                    # node_name = node['nodes'][0]['destination'] if node['nodes'] else "Unknown"
                    self.canvas.create_oval(x-MARK_SIZE, y-MARK_SIZE, x+MARK_SIZE, y+MARK_SIZE, fill="red")
                    self.canvas.create_text(x, y-2*MARK_SIZE, text=key, fill="blue", font=("Arial", FONT_SIZE))
                self.canvas.pack()
            except Exception:
                self.canvas.create_text(
                    400, 300, text=f"{floor_name} 平面圖未找到", font=("Arial", 20), fill="gray"
                )
        except IndexError:
            pass

    """ //**   TODO   **// """

    # 1. 把能設定的屬性都搞上去  (已完成)
    # 2. 能根據樓層跟相對位置，初始化LOGO的3D位置
    # 3. (未來式)能複製附近點的屬性



    # 新增點位
    def create_mark(self, event):
        """Create a new node after clicking."""
        if not self.selected_floor.get():
            messagebox.showerror("Error", "Please select a building first!")
            return
        if self.isHover:
            self.edit_node_properties(event)
            return
            
        bureau = simpledialog.askstring("局處", "輸入局處名稱:")
        if not bureau:
            return
            
        node_name = simpledialog.askstring("點位名稱", "輸入名稱:")
        if node_name:
            # Get new node ID based on building
            max_id = max([
                (node['nodeIdA'] if 'A樓' in node['building'] else node['nodeIdB'])
                for floor_nodes in self.marked_nodes.values()
                for node in floor_nodes
            ], default=0) + 1
            
            node = {
                "x": event.x,
                "y": event.y,
                "building": self.current_building,
                "canTakeElevator": "0",
                "floor": self.selected_floor.get(),
                "id": len(self.marked_nodes[self.selected_floor.get()]) + 1,
                "NodeId2DA": 0,
                "NodeId2DB": 0,
                "nodeIdA": max_id if 'A樓' in self.current_building else 0,
                "nodeIdB": max_id if 'B樓' in self.current_building else 0,
                "OtherBuildEndNodeId2D": 0,
                "OtherBuildStartNodeId2D": 0,
                "turnTo": 0,
                "nodes": [{"bureau": bureau, "destination": node_name}]
            }
            
            self.marked_nodes.get(self.selected_floor.get()).append(node)
            self.canvas.create_oval(
                event.x-MARK_SIZE, y=event.y-MARK_SIZE, 
                x2=event.x+MARK_SIZE, y2=event.y+MARK_SIZE, 
                fill="red"
            )
            self.canvas.create_text(
                event.x, event.y-2*MARK_SIZE, 
                text=f"{node_name}", 
                fill="blue",
                font=("Arial", FONT_SIZE)
            )
    # 浮現點位資訊
    def hover_node(self, event):
        """Display node details when hovering over a marked point."""
        if not self.selected_floor.get():
            return
        for node in self.marked_nodes.get(self.selected_floor.get()):
            if abs(event.x - float(node["x"])) <= MARK_SIZE and abs(event.y - float(node["y"])) <= MARK_SIZE:
                self.isHover = True
                # Get the appropriate nodeId based on building
                node_id = node['nodeIdA'] if 'A樓' in node['building'] else node['nodeIdB']
                
                # Create destination list text
                destinations_text = "\nDestinations:"
                for dest in node["nodes"]:
                    destinations_text += f"\n- {dest['destination']} ({dest['bureau']})"
                
                text = f"NodeID: {node_id}" + destinations_text
                self.hover_label.config(text=text)
                self.hover_label.place(x=event.x + 10, y=event.y + 10)
                return
        self.isHover = False
        self.hover_label.place_forget()
    
    def edit_node_properties(self, event):
        
        for node in self.marked_nodes.get(self.selected_floor.get(), []):
            if abs(event.x - int(node["x"])) <= MARK_SIZE and abs(event.y - int(node["y"])) <= MARK_SIZE:
                inputs = myDialog.main(node)
                if(inputs["isDelete"]==True):
                    self.marked_nodes[self.selected_floor.get()].remove(node)
                    self.update() # renew
                else:
                    self.marked_nodes[self.selected_floor.get()].remove(node)
                    self.marked_nodes[self.selected_floor.get()].append(inputs["data"])
                    # print(inputs["data"])
                    # print(self.marked_nodes[self.selected_floor.get()])
                    self.update()
                # if new_name:
                #     node["destination"] = new_name
                #     self.select_floor(None)
                return
    def export_initial_format(self):
        """Export the data in initial setting format."""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")]
        )
        if file_path:
            try:
                transformed_data = self.transform_to_initial_format(self.marked_nodes)
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(transformed_data, f, ensure_ascii=False, indent=4)
                messagebox.showinfo("匯出成功", "成功匯出為初始設定檔格式")
            except Exception as e:
                messagebox.showerror("匯出失敗", f"匯出失敗: {str(e)}") 
    def transform_to_initial_format(self,marked_nodes):
        """Transform the marked nodes data into the initial setting format."""
        result = []
        
        # Process each floor's nodes
        for floor_name, floor_nodes in marked_nodes.items():
            floor_num = int(''.join(filter(str.isdigit, floor_name)))
            building_num = 0 if 'A樓' in floor_name else 1
            
            for node in floor_nodes:
                # Get node positions
                node_id = str(node['nodeIdA'] if building_num == 0 else node['nodeIdB'])
                
                # Process each destination in the node
                for dest in node.get('nodes', []):
                    transformed_node = {
                        "building": building_num,
                        "bureau": dest.get('bureau', ''),
                        "canTakeElevator": node.get('canTakeElevator', '0'),
                        "destination": dest.get('destination', ''),
                        "elevatorA": 0,  # Default values, can be updated if needed
                        "elevatorB": 0,
                        "enable": dest.get('enable', True),
                        "englishDestination": dest.get('englishDestination', ''),
                        "floor": floor_num,
                        "id": node.get('id', 0),
                        "logoPositionA": {
                            "x": 0,  # Default values, can be updated if needed
                            "y": 0,
                            "z": 0
                        },
                        "logoPositionB": {
                            "x": 0,
                            "y": 0,
                            "z": 0
                        },
                        "NodeId2DA": node.get('NodeId2DA', 0),
                        "NodeId2DB": node.get('NodeId2DB', 0),
                        "nodeIdA": node.get('nodeIdA', 0),
                        "nodeIdB": node.get('nodeIdB', 0),
                        "OtherBuildEndNodeId2D": node.get('OtherBuildEndNodeId2D', 0),
                        "OtherBuildStartNodeId2D": node.get('OtherBuildStartNodeId2D', 0),
                        "turnTo": node.get('turnTo', 0)
                    }
                    result.append(transformed_node)
        
        return result
    # 儲存點位資訊
    def save_nodes_to_json(self):
        """Save the marked nodes to a JSON file in the transformed format."""
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            # Transform the data to the new format
            transformed_data = {}
            
            for floor, nodes in self.marked_nodes.items():
                transformed_data[floor] = []
                
                # Group nodes by their node ID
                grouped_by_id = {}
                for node in nodes:
                    node_id = str(node['nodeIdA'] if 'A樓' in node['building'] else node['nodeIdB'])
                    if node_id not in grouped_by_id:
                        grouped_by_id[node_id] = {
                            "x": node["x"],
                            "y": node["y"],
                            "building": node["building"],
                            "canTakeElevator": node["canTakeElevator"],
                            "floor": node["floor"],
                            "id": node["id"],
                            "NodeId2DA": node["NodeId2DA"],
                            "NodeId2DB": node["NodeId2DB"],
                            "nodeIdA": node["nodeIdA"],
                            "nodeIdB": node["nodeIdB"],
                            "OtherBuildEndNodeId2D": node["OtherBuildEndNodeId2D"],
                            "OtherBuildStartNodeId2D": node["OtherBuildStartNodeId2D"],
                            "turnTo": node["turnTo"],
                            "nodes": node["nodes"]
                        }
                
                # Convert grouped nodes to the desired format
                for node_id, node_data in grouped_by_id.items():
                    transformed_data[floor].append({
                        node_id: node_data
                    })
            
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(transformed_data, f, ensure_ascii=False, indent=4)
                messagebox.showinfo("儲存成功", "成功儲存設定檔")
            except Exception as e:
                messagebox.showerror("儲存失敗", f"儲存設定檔失敗: {str(e)}")

    # 匯入點位資訊
    def import_nodes_from_json(self):
        """Import node data from the new JSON format."""
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    merged_data = json.load(f)
                    # Convert merged format back to flat format for display
                    flat_data = {}
                    for floor, nodes in merged_data.items():
                        flat_data[floor] = []
                        for node_obj in nodes:
                            for node_id, node_data in node_obj.items():
                                # Convert positions to float to ensure compatibility
                                node_data['x'] = float(node_data['x'])
                                node_data['y'] = float(node_data['y'])
                                flat_data[floor].append(node_data)
                    
                    self.marked_nodes = flat_data
                    self.update()
                messagebox.showinfo("匯入成功", "匯入設定檔成功")
            except Exception as e:
                messagebox.showerror("Import Error", f"Failed to import nodes: {e}")

    def init_setting(self):
        file_path = "C:/Users/kchoen/Desktop/dirtyholder/py/設定檔功能程式/newEditor/最新儲存設定檔.json"
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                merged_data = json.load(f)
                flat_data = {}
                for floor, nodes in merged_data.items():
                    flat_data[floor] = []
                    for node_obj in nodes:
                        for node_id, node_data in node_obj.items():
                            # Convert positions to float to ensure compatibility
                            node_data['x'] = float(node_data['x'])
                            node_data['y'] = float(node_data['y'])
                            flat_data[floor].append(node_data)
                
                self.marked_nodes = flat_data
            self.select_building("A樓")
            self.selected_floor.set("A樓-1樓")
            self.update()
        except Exception as e:
            messagebox.showerror("Import Error", f"Failed to import nodes: {e}")

    def transform_nodes_from_setting(self):
        """Transform the settings from source format to target format with elevator and logo positions."""
        setting_file_path = filedialog.askopenfilename(
            title="Select setting file (設定檔說明)",
            filetypes=[("JSON files", "*.json")]
        )
        if not setting_file_path:
            return
            
        position_file_path = filedialog.askopenfilename(
            title="Select position file (轉換設定檔 for x,y coordinates)",
            filetypes=[("JSON files", "*.json")]
        )
        if not position_file_path:
            return

        try:
            # Read source data and position data
            with open(setting_file_path, "r", encoding="utf-8") as f:
                source_data = json.load(f)
            with open(position_file_path, "r", encoding="utf-8") as f:
                position_data = json.load(f)

            # Transform data
            transformed_data = {}

            # Create position lookup dictionary
            position_lookup = {}
            for floor, nodes in position_data.items():
                for node_obj in nodes:
                    for node_id, node_data in node_obj.items():
                        key = (floor, node_id)
                        position_lookup[key] = {
                            "x": node_data["x"],
                            "y": node_data["y"]
                        }

            # Group nodes by floor
            floor_groups = {}
            for node in source_data:
                if not node.get('enable', True):  # Skip disabled nodes
                    continue

                floor_key = f"{'A樓' if node['building'] == 0 else 'B樓'}-{node['floor']}樓"
                if floor_key not in floor_groups:
                    floor_groups[floor_key] = []

                # Node ID based on building
                node_id = str(node['nodeIdA'] if node['building'] == 0 else node['nodeIdB'])
                
                # Get position from lookup
                position = position_lookup.get((floor_key, node_id), {"x": 0, "y": 0})

                # Create transformed node structure
                transformed_node = {
                    node_id: {
                        "x": position["x"],
                        "y": position["y"],
                        "building": 'A樓' if node['building'] == 0 else 'B樓',
                        "canTakeElevator": str(node.get('canTakeElevator', '0')),
                        "elevatorA": node.get('elevatorA', 0),
                        "elevatorB": node.get('elevatorB', 0),
                        "floor": floor_key,
                        "id": node.get('id', 0),
                        "logoPositionA": node.get('logoPositionA', {
                            "x": 0,
                            "y": 0,
                            "z": 0
                        }),
                        "logoPositionB": node.get('logoPositionB', {
                            "x": 0,
                            "y": 0,
                            "z": 0
                        }),
                        "NodeId2DA": node.get('NodeId2DA', 0),
                        "NodeId2DB": node.get('NodeId2DB', 0),
                        "nodeIdA": node.get('nodeIdA', 0),
                        "nodeIdB": node.get('nodeIdB', 0),
                        "OtherBuildEndNodeId2D": node.get('OtherBuildEndNodeId2D', 0),
                        "OtherBuildStartNodeId2D": node.get('OtherBuildStartNodeId2D', 0),
                        "turnTo": node.get('turnTo', 0),
                        "nodes": [
                            {
                                "bureau": node.get('bureau', ''),
                                "destination": node.get('destination', ''),
                                "englishDestination": node.get('englishDestination', ''),
                                "enable": node.get('enable', True)
                            }
                        ]
                    }
                }

                # Try to find and merge with existing node
                existing_node = None
                for idx, n in enumerate(floor_groups[floor_key]):
                    if node_id in n:
                        existing_node = n
                        break

                if existing_node:
                    # Add destination to existing node's nodes array if not already present
                    new_dest = {
                        "bureau": node.get('bureau', ''),
                        "destination": node.get('destination', ''),
                        "englishDestination": node.get('englishDestination', ''),
                        "enable": node.get('enable', True)
                    }
                    if new_dest not in existing_node[node_id]['nodes']:
                        existing_node[node_id]['nodes'].append(new_dest)
                else:
                    # Add new node to floor group
                    floor_groups[floor_key].append(transformed_node)

            # Convert floor_groups to transformed_data
            for floor_key, nodes in floor_groups.items():
                transformed_data[floor_key] = nodes

            # Save transformed data
            save_path = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json")]
            )
            if save_path:
                with open(save_path, "w", encoding="utf-8") as f:
                    json.dump(transformed_data, f, ensure_ascii=False, indent=4)
                messagebox.showinfo("轉換成功", "已成功轉換並儲存設定檔")

        except Exception as e:
            messagebox.showerror("Error", f"轉換設定檔失敗: {str(e)}")

    def update(self):
        try:
            self.select_floor(self.selected_floor.get())
        except:
            pass
# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = BuildingFloorGUI(root)
    root.mainloop()
