import ttkbootstrap as ttk
from tkinter import filedialog as fd

FONT = ("Helvetica", 12, "bold")

class WatermarkGui:

    def __init__(self):
        self.root = ttk.Window(themename="darkly")
        self.root.title('Watermark App')
        self.root.geometry('1000x800')

        self.frame = ttk.Frame(self.root)
        self.frame.place(relx=0.5, rely=0.5, anchor="center")
        self.selected_files = []
        self.path_labels = []
        self.notselected_label = None
        self.delete_buttons = []

        l1 = ttk.Label(self.frame, text="Watermark Text", font=FONT,  width=40)
        l1.grid(row=1, column=0, padx=40, pady=(20, 5), sticky='ew')

        e1 = ttk.Entry(self.frame)
        e1.grid(row=2, column=0, padx=40, pady=(5, 20), sticky='ew')

        l2 = ttk.Label(self.frame, text="Select Target Images", font=FONT, width=40)
        l2.grid(row=3, column=0, padx=40, pady=(20, 5), sticky='ew')

        b1 = ttk.Button(self.frame, text="Open file manager", command=self.open_files)
        b1.grid(row=4, column=0, padx=40, pady=(5, 3), sticky='ew', columnspan=2)

        self.notselected_label = ttk.Label(self.frame, text="No file selected", width=40)
        self.notselected_label.grid(row=5, column=0, padx=40, pady=(5, 0), sticky='ew')

    def open_files(self):
        types = (("Image files", "*.jpg *.jpeg *.png"), ("all files", '*.*'))

        filepaths = fd.askopenfilenames(title="Open a file", filetypes=types)

        if not filepaths:
            return

        self.notselected_label.grid_remove()

        for i,label in enumerate(self.path_labels):
            label.destroy()
            self.delete_buttons[i].destroy()

        self.path_labels = []
        self.selected_files = []
        self.delete_buttons = []

        for i, file in enumerate(filepaths):
            self.selected_files.append(file)
            label = ttk.Label(self.frame, text=file.split('/')[-1], width=40)
            self.path_labels.append(label)

            btn = ttk.Button(
                self.frame,
                text='X',
                bootstyle='danger-link',
                command=lambda l=label, f=file: self.remove_file(l, f))

            self.delete_buttons.append(btn)

        for i in range(len(self.path_labels)):
            self.path_labels[i].grid(row=5+i, column=0 ,padx=40, pady=(5, 0), sticky='ew')
            self.delete_buttons[i].grid(row=5+i, column=1, padx=3, pady=(5,0), sticky='w')

    def remove_file(self, label, file):
        label.destroy()
        self.path_labels.remove(label)
        position = self.selected_files.index(file)
        self.selected_files.remove(file)
        self.delete_buttons[position].destroy()
        self.delete_buttons.pop(position)

        for i in range(len(self.path_labels)):
            self.path_labels[i].grid(row=5+i, column=0 ,padx=40, pady=(5, 0), sticky='ew')
            self.delete_buttons[i].grid(row=5+i, column=1, padx=3, pady=(5,0), sticky='w')

        if not self.selected_files:
            self.notselected_label.grid(row=5, column=0, padx=40, pady=(5, 0), sticky='ew')

watermark = WatermarkGui()
watermark.root.mainloop()