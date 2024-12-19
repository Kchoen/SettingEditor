
#### Save this as dual_input.py ####
#! /usr/bin/env python
# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import Frame, Label, Entry, Button, StringVar

# Good habit to put your GUI in a class to make it self-contained
class myDialog(Frame):

    def __init__(self, root, node):
        # self allow the variable to be used anywhere in the class
        super().__init__()
        self.root = root
        self.root.title("修改")
        self.data = {},
        self.isDelete = False,
        self.output_vars = {
            "x": StringVar(value=node.get("x", "")),
            "y": StringVar(value=node.get("y", "")),
            "destination": StringVar(value=node.get("destination", "")),
            "building": StringVar(value=node.get("building", "")),
            "bureau": StringVar(value=node.get("bureau", "")),
            "canTakeElevator": StringVar(value=node.get("canTakeElevator", "")),
            "floor": StringVar(value=node.get("floor", "")),
            "NodeId2DA": StringVar(value=node.get("NodeId2DA", "")),
            "NodeId2DB": StringVar(value=node.get("NodeId2DB", "")),
            "nodeIdA": StringVar(value=node.get("nodeIdA", "")),
            "nodeIdB": StringVar(value=node.get("nodeIdB", "")),
            "OtherBuildEndNodeId2D": StringVar(value=node.get("OtherBuildEndNodeId2D", "")),
            "OtherBuildStartNodeId2D": StringVar(value=node.get("OtherBuildStartNodeId2D", "")),
            "turnTo": StringVar(value=node.get("turnTo", ""))
        }
        self.initUI(root)


    """ //**   TODO   **// """
    # 1. 加入刪除功能 (已完成)
    # 2. 還要把能設定的東西都搞上去
    # 3. 排版 / 可能要加入拖拉功能

    def initUI(self, root):

        frame = Frame(self.root)
        frame.pack(padx=10, pady=10)

        # Dynamic creation of input fields
        for idx, (key, var) in enumerate(self.output_vars.items()):
            lbl = Label(frame, text=key, width=20, anchor="e")
            lbl.grid(row=idx, column=0, padx=5, pady=5, sticky="e")
            entry = Entry(frame, textvariable=var, width=30)
            entry.insert(0,var.get())
            entry.grid(row=idx, column=1, padx=5, pady=5, sticky="w")

        # Buttons for actions
        btn_submit = Button(frame, text="確認", command=self.onSubmit)
        btn_submit.grid(row=len(self.output_vars), column=0, padx=5, pady=10, sticky="e")

        btn_delete = Button(frame, text="刪除", command=self.onDelete)
        btn_delete.grid(row=len(self.output_vars), column=1, padx=5, pady=10, sticky="w")

    def onSubmit(self):

        self.data = {key: var.get() for key, var in self.output_vars.items()}
        self.quit()
    def onDelete(self):
        self.isDelete = True
        self.quit()

def main(node):

    # This part triggers the dialog
    root = tk.Tk()
    root.geometry("400x500")
    app = myDialog(root, node)
    root.mainloop()
    # Here we can act on the form components or
    # better yet, copy the output to a new variable
    user_input = {"isDelete" : app.isDelete,"data": app.data}
    # Get rid of the error message if the user clicks the
    # close icon instead of the submit button
    # Any component of the dialog will no longer be available
    # past this point
    try:
        app.destroy()
        root.destroy()
    except:
        pass
    # To use data outside of function
    # Can either be used in __main__
    # or by external script depending on
    # what calls main()
    return user_input

# Allow dialog to run either as a script or called from another program
if __name__ == '__main__':
    follow_on_variable = main()
    # This shows the outputs captured when called directly as `python dual_input.py`
    print(follow_on_variable)