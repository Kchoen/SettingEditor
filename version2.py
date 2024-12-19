import json
import pytesseract
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from sklearn.cluster import DBSCAN
import numpy as np

class NodeEditor:
    def __init__(self, image_path=None, setting_path=None, nodestat_path=None):
        self.image_path = image_path
        self.setting_path = setting_path
        self.nodestat_path = nodestat_path
        self.settings = self.load_json(setting_path) if setting_path else []
        self.nodestat = self.initialize_nodestat()

    def load_json(self, path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def save_json(self, path, data):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def initialize_nodestat(self):
        if self.nodestat_path:
            try:
                loaded_nodestat = self.load_json(self.nodestat_path)
                if isinstance(loaded_nodestat, list):
                    # Convert list to dict for compatibility
                    return {node["destination"]: {"marked": False, "info": node} for node in loaded_nodestat}
                return loaded_nodestat
            except FileNotFoundError:
                print(f"{self.nodestat_path} not found. Initializing new nodestat.")
        return {node['destination']: {"marked": False, "info": node} for node in self.settings}

    def extract_departments_from_image(self):
        image = Image.open(self.image_path)
        ocr_data = pytesseract.image_to_data(image, lang="chi_tra+eng", output_type=pytesseract.Output.DICT)
        positions = []
        texts = []

        for i in range(len(ocr_data['text'])):
            text = ocr_data['text'][i].strip()
            if text:
                x, y, w, h = (ocr_data['left'][i], ocr_data['top'][i], ocr_data['width'][i], ocr_data['height'][i])
                positions.append((x + w / 2, y + h / 2))
                texts.append({"text": text, "x": x, "y": y, "width": w, "height": h})

        clustering = DBSCAN(eps=80, min_samples=1).fit(positions)
        labels = clustering.labels_

        grouped_texts = {}
        for idx, label in enumerate(labels):
            if label not in grouped_texts:
                grouped_texts[label] = []
            grouped_texts[label].append(texts[idx])

        extracted = []
        for group in grouped_texts.values():
            merged_text = "".join([item["text"] for item in group]).replace(" ", "")
            for node in self.settings:
                if node['destination'] in merged_text:
                    bounding_box = {
                        "x": min([item["x"] for item in group]),
                        "y": min([item["y"] for item in group]),
                        "width": max([item["x"] + item["width"] for item in group]) - min([item["x"] for item in group]),
                        "height": max([item["y"] + item["height"] for item in group]) - min([item["y"] for item in group])
                    }
                    extracted.append({"matched_destination": node["destination"], "bounding_box": bounding_box})
                    self.nodestat[node["destination"]]["marked"] = True

        return extracted

    def edit_or_create_node(self, destination, info):
        if destination in self.nodestat:
            self.nodestat[destination]["info"].update(info)
        else:
            self.nodestat[destination] = {"marked": True, "info": info}

    def save_nodestat_as_setting(self, output_path):
        new_settings = [node["info"] for node in self.nodestat.values()]
        self.save_json(output_path, new_settings)

class GUI:
    def __init__(self, master, editor):
        self.master = master
        self.editor = editor
        self.canvas = None
        self.image_tk = None
        self.original_image = None

        self.master.title("Node Editor")

        self.create_menu()
        self.create_canvas()

    def create_menu(self):
        menu = tk.Menu(self.master)
        self.master.config(menu=menu)

        file_menu = tk.Menu(menu, tearoff=0)
        file_menu.add_command(label="Open Image", command=self.open_image)
        file_menu.add_command(label="Import Settings", command=self.import_settings)
        file_menu.add_command(label="Import NodeStat", command=self.import_nodestat)
        file_menu.add_command(label="Extract Nodes", command=self.extract_nodes)
        file_menu.add_command(label="Export Setting", command=self.export_setting)
        menu.add_cascade(label="File", menu=file_menu)

    def create_canvas(self):
        self.canvas = tk.Canvas(self.master, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<Button-1>", self.on_click)
        self.master.bind("<Configure>", self.resize_image)

    def open_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
        if file_path:
            self.editor.image_path = file_path
            self.original_image = Image.open(file_path)
            self.display_image()
            self.mark_nodes()

    def import_settings(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            self.editor.setting_path = file_path
            self.editor.settings = self.editor.load_json(file_path)
            self.editor.nodestat = self.editor.initialize_nodestat()
            self.mark_nodes()

    def import_nodestat(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            self.editor.nodestat_path = file_path
            self.editor.nodestat = self.editor.initialize_nodestat()
            self.mark_nodes()

    def extract_nodes(self):
        if self.editor.image_path and self.editor.settings:
            extracted = self.editor.extract_departments_from_image()
            self.editor.save_json("filtered_departments.json", extracted)
            messagebox.showinfo("Node Extraction", "Nodes extracted successfully!")
            self.mark_nodes()
        else:
            messagebox.showerror("Error", "Please load an image and settings first.")

    def export_setting(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            self.editor.save_nodestat_as_setting(file_path)
            messagebox.showinfo("Export Setting", "Settings exported successfully!")

    def display_image(self):
        if self.original_image:
            width, height = self.canvas.winfo_width(), self.canvas.winfo_height()
            image_ratio = self.original_image.width / self.original_image.height
            canvas_ratio = width / height

            if canvas_ratio > image_ratio:
                new_height = height
                new_width = int(image_ratio * height)
            else:
                new_width = width
                new_height = int(width / image_ratio)

            resized_image = self.original_image.resize((new_width, new_height), Image.LANCZOS)
            self.image_tk = ImageTk.PhotoImage(resized_image)
            self.canvas.create_image(width / 2, height / 2, anchor=tk.CENTER, image=self.image_tk)

    def resize_image(self, event):
        self.display_image()
        self.mark_nodes()

    def mark_nodes(self):
        if self.image_tk:
            self.canvas.delete("node")
            for destination, data in self.editor.nodestat.items():
                if data["marked"]:
                    bbox = data["info"].get("bounding_box", {})
                    x = bbox.get("x", 0)
                    y = bbox.get("y", 0)
                    width = bbox.get("width", 0)
                    height = bbox.get("height", 0)
                    self.canvas.create_rectangle(x, y, x + width, y + height, outline="red", tags="node")
                    self.canvas.create_text(x + width / 2, y + height + 10, text=destination, fill="blue", tags="node")

    def on_click(self, event):
        x, y = event.x, event.y
        destination = simpledialog.askstring("Create Node", "Enter destination:")
        if destination:
            info = {"bounding_box": {"x": x, "y": y, "width": 50, "height": 50}}  # Example bounding box
            self.editor.edit_or_create_node(destination, info)
            self.mark_nodes()

if __name__ == "__main__":
    root = tk.Tk()
    editor = NodeEditor()
    gui = GUI(root, editor)
    root.mainloop()
