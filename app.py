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
            "A樓-1樓": "./image/1F.jpg",
            "A樓-2樓": "./image/1F.jpg",
            "A樓-3樓": "./image/1F.jpg",
            "A樓-4樓": "./image/1F.jpg",
            "A樓-5樓": "./image/1F.jpg",
            "A樓-6樓": "./image/1F.jpg",
            "A樓-7樓": "./image/1F.jpg",
            "A樓-8樓": "./image/1F.jpg",
            "A樓-9樓": "./image/1F.jpg",
            "A樓-10樓": "./image/1F.jpg",
            "B樓-1樓": "./image/1F.jpg",
            "B樓-2樓": "./image/1F.jpg",
            "B樓-3樓": "./image/1F.jpg",
            "B樓-4樓": "./image/1F.jpg",
            "B樓-5樓": "./image/1F.jpg",
            "B樓-6樓": "./image/1F.jpg",
            "B樓-7樓": "./image/1F.jpg",
            "B樓-8樓": "./image/1F.jpg",
            "B樓-9樓": "./image/1F.jpg",
            "B樓-10樓": "./image/1F.jpg"
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

    # MENU選單選項設定(儲存/匯入點位設定)
    def create_menu(self):
        """Create a menu bar with Save and Import options."""
        self.menu_bar = tk.Menu(self.root)
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="儲存點位設定", command=self.save_nodes_to_json)
        file_menu.add_command(label="匯入點位設定", command=self.import_nodes_from_json)
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
            except :
                pass
            floor_name = self.floor_name
            self.selected_lable.config(text=f"目前顯示位置 : {floor_name}")
            self.canvas.delete("all")
            
            image_path = self.floor_images.get(floor_name, "./image/1F.jpg")
            try:
                # 顯示圖片
                img = Image.open(image_path)
                self.image = img.resize((self.canvas.winfo_width()//2, self.canvas.winfo_height()))
                self.floor_image = ImageTk.PhotoImage(self.image)
                self.canvas.create_image(self.canvas.winfo_width() // 2, self.canvas.winfo_height() // 2, image=self.floor_image)

                # 顯示點位
                for node in self.marked_nodes.get(floor_name, []):
                    x, y, node_name = node.get('x'), node.get('y'), node.get('destination')
                    self.canvas.create_oval(x-MARK_SIZE, y-MARK_SIZE, x+MARK_SIZE, y+MARK_SIZE, fill="red")
                    self.canvas.create_text(x, y-2*MARK_SIZE, text=node_name, fill="blue",font=("Arial", FONT_SIZE))
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
        node_name = simpledialog.askstring("點位名稱", "輸入名稱:")
        if node_name:
            node = {
                "x": event.x, "y": event.y,
                "destination": node_name,
                "building": self.current_building,
                "bureau":"公共空間",
                "canTakeElevator": "9、11、14、16",
                "floor": self.selected_floor.get() or "Unknown",
                "id": reduce(lambda acc, key: acc + len(self.marked_nodes[key]), self.marked_nodes, 0) + 1,
                "NodeId2DA":29,
                "NodeId2DB":29,
                "nodeIdA":28,
                "nodeIdB":28,
                "OtherBuildEndNodeId2D":39,
                "OtherBuildStartNodeId2D":0,
                "turnTo": 2

            }
            self.marked_nodes.get(self.selected_floor.get()).append(node)
            self.canvas.create_oval(event.x-MARK_SIZE, event.y-MARK_SIZE, event.x+MARK_SIZE, event.y+MARK_SIZE, fill="red")
            self.canvas.create_text(event.x, event.y-2*MARK_SIZE, text=node_name, fill="blue",font=("Arial", FONT_SIZE))
    # 浮現點位資訊
    def hover_node(self, event):
        """Display node details when hovering over a marked point."""
        if not self.selected_floor.get():
            return
        for node in self.marked_nodes.get(self.selected_floor.get()):
            if abs(event.x - int(node["x"])) <= MARK_SIZE and abs(event.y - int(node["y"])) <= MARK_SIZE:
                self.isHover = True
                text = f"類型: {node['bureau']}\n點位名稱: {node['destination']}\nID: {node['id']}\nA/B棟: {node['building']}\n搭乘電梯: {node['canTakeElevator']}\n \
                NodeId2DA: {node['NodeId2DA']}\nNodeId2DB: {node['NodeId2DB']}\nnodeIdA: {node['nodeIdA']}\nnodeIdB: {node['nodeIdB']}\nOtherBuildEndNodeId2D: {node['OtherBuildEndNodeId2D']}\n \
                OtherBuildStartNodeId2D: {node['OtherBuildStartNodeId2D']}"
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
            
    # 儲存點位資訊
    def save_nodes_to_json(self):
        """Save the marked nodes to a JSON file."""
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(self.marked_nodes, f, ensure_ascii=False, indent=4)
            messagebox.showinfo("Save Complete", "Nodes have been successfully saved.")

    # 匯出點位資訊
    def import_nodes_from_json(self):
        """Import node data from a JSON file."""
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    self.marked_nodes = json.load(f)
                    self.update()
                messagebox.showinfo("Import Complete", "Nodes have been successfully imported.")
            except Exception as e:
                messagebox.showerror("Import Error", f"Failed to import nodes: {e}")
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
