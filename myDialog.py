
#### Save this as dual_input.py ####
#! /usr/bin/env python
# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import Tk, Text, TOP, BOTH, X, N, LEFT, RIGHT
from tkinter.ttk import Frame, Label, Entry, Button

# Good habit to put your GUI in a class to make it self-contained
class myDialog(Frame):

    def __init__(self, root):
        # self allow the variable to be used anywhere in the class
        super().__init__()
        self.output1 = ""
        self.output2 = ""
        self.root = root
        self.root.title("修改")
        self.initUI(root)


    """ //**   TODO   **// """
    # 1. 加入刪除功能 (已完成)
    # 2. 還要把能設定的東西都搞上去
    # 3. 排版 / 可能要加入拖拉功能

    def initUI(self, root):

        self.center_frame = tk.Frame(root, bg="white")
        self.center_frame.pack(expand=True, fill=tk.BOTH)
        frame = self.center_frame

        # Use a grid layout to better align labels and entries
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=3)
        frame.grid_columnconfigure(2, weight=1)

        font_settings = ("Arial", 14)  # Set font size and style
        # 文心/惠中
        lbl1 = Label(frame, text="Input 1", width=6, font=font_settings)
        lbl1.grid(row=0, column=0, padx=2, pady=10, sticky="e")
        self.entry1 = Entry(frame, textvariable=self.output1, font=font_settings)
        self.entry1.grid(row=0, column=1, padx=5, pady=10, sticky="we")

        lbl1 = Label(frame, text="Input 1", width=6, font=font_settings)
        lbl1.grid(row=0, column=0, padx=2, pady=10, sticky="e")
        self.entry1 = Entry(frame, textvariable=self.output1, font=font_settings)
        self.entry1.grid(row=0, column=1, padx=5, pady=10, sticky="we")

        lbl1 = Label(frame, text="Input 1", width=6, font=font_settings)
        lbl1.grid(row=0, column=0, padx=2, pady=10, sticky="e")
        self.entry1 = Entry(frame, textvariable=self.output1, font=font_settings)
        self.entry1.grid(row=0, column=1, padx=5, pady=10, sticky="we")

        lbl1 = Label(frame, text="Input 1", width=6, font=font_settings)
        lbl1.grid(row=0, column=0, padx=2, pady=10, sticky="e")
        self.entry1 = Entry(frame, textvariable=self.output1, font=font_settings)
        self.entry1.grid(row=0, column=1, padx=5, pady=10, sticky="we")

        lbl1 = Label(frame, text="Input 1", width=6, font=font_settings)
        lbl1.grid(row=0, column=0, padx=2, pady=10, sticky="e")
        self.entry1 = Entry(frame, textvariable=self.output1, font=font_settings)
        self.entry1.grid(row=0, column=1, padx=5, pady=10, sticky="we")



        # Place buttons on the same row with spacing and centered alignment
        btn_submit = Button(frame, text="確認", command=self.onSubmit)
        btn_submit.grid(row=2, column=0, sticky="e")

        btn_delete = Button(frame, text="刪除", command=self.onDelete)
        btn_delete.grid(row=2, column=1,  sticky="e")

    def onSubmit(self):

        self.output1 = self.entry1.get()
        self.output2 = self.entry2.get()
        self.quit()
    def onDelete(self):
        self.isDelete = True
        self.quit()

def main():

    # This part triggers the dialog
    root = Tk()
    root.geometry("300x200")
    app = myDialog(root)
    root.mainloop()
    # Here we can act on the form components or
    # better yet, copy the output to a new variable
    user_input = {"isDelete" : app.isDelete,"output1": app.output1,"output2": app.output2}
    # print(app.output1)
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