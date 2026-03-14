import ttkbootstrap as ttk
from tkinter import filedialog as fd
from image_processing import ImageProcessing
import threading

FONT = ("Helvetica", 20)

class WatermarkGui:

    def __init__(self, image_proc: ImageProcessing):
        self.image_processing = image_proc

        self.to_watermark = []

        self.root = ttk.Window(themename="darkly")
        self.root.title('Watermark App')
        self.root.geometry('1000x800')
        self.frame = ttk.Frame(self.root)

        self.frame.place(relx=0.5, rely=0.5, anchor="center")
        self.selected_files = []
        self.path_labels = []
        self.notselected_label = None
        self.delete_buttons = []
        self.delete_directory_btn = None
        self.file_path = "Not directory selected."

        l1 = ttk.Label(self.frame, text="Watermark Text", font=FONT,  width=40)
        l1.grid(row=1, column=0, padx=40, pady=(20, 5), sticky='ew')

        self.entry = ttk.Entry(self.frame)
        self.entry.grid(row=2, column=0, padx=40, pady=(5, 20), sticky='ew')


        self.button = ttk.Button(
            self.frame,
            text="Watermark",
            state="disabled",
            command= self.btn_watermark
        )


        self.button.grid(row=2, column=1, padx=40, pady=(5, 20), sticky='w')

        choose_path_label = ttk.Label(self.frame, text="Output Directory", font=FONT, width=40)
        choose_path_label.grid(row=3, column=0, padx=40, pady=(20, 5), sticky='ew')
        choose_path_btn = ttk.Button(self.frame, text="Choose Output Directory", command=self.choose_output_path)
        choose_path_btn.grid(row=4, column=0, padx=40, pady=(5, 3), sticky='ew', columnspan=2)

        self.directory_path_label = ttk.Label(self.frame, text="Not directory selected", width=40)
        self.directory_path_label.grid(row=5, column=0, padx=40, pady=(5,3), sticky='ew', columnspan=2)

        l2 = ttk.Label(self.frame, text="Select Target Images", font=FONT, width=40)
        l2.grid(row=6, column=0, padx=40, pady=(20, 5), sticky='ew')
        b1 = ttk.Button(self.frame, text="Open file manager", command=self.open_files)
        b1.grid(row=7, column=0, padx=40, pady=(5, 3), sticky='ew', columnspan=2)

        self.notselected_label = ttk.Label(self.frame, text="No file selected", width=40)
        self.notselected_label.grid(row=8, column=0, padx=40, pady=(5, 0), sticky='ew')

        self.ready_id = self.root.after(200, self.check_button_responsiveness)

    def choose_output_path(self) -> None:

        self.file_path = fd.askdirectory()
        self.directory_path_label.configure(text=self.file_path)

        self.delete_directory_btn = ttk.Button(
            self.frame,
            text='X',
            bootstyle='danger-link',
            command= self.remove_directory)

        self.delete_directory_btn.grid(row=5, column=1, padx=3, pady=(5,0), sticky='w')


    def check_button_responsiveness(self) -> None:
        if self.entry.get() and self.selected_files and self.file_path:
            self.button.configure(state='')
        else:
            self.button.configure(state='disabled')

        self.ready_id = self.root.after(200, self.check_button_responsiveness)

    def open_files(self) -> None:
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
            self.path_labels[i].grid(row=8+i, column=0 ,padx=40, pady=(5, 0), sticky='ew')
            self.delete_buttons[i].grid(row=8+i, column=1, padx=3, pady=(5,0), sticky='w')


    def remove_file(self, label: ttk.Label, file: str) -> None:
        label.destroy()
        self.path_labels.remove(label)
        position = self.selected_files.index(file)
        self.selected_files.remove(file)
        self.delete_buttons[position].destroy()
        self.delete_buttons.pop(position)

        for i in range(len(self.path_labels)):
            self.path_labels[i].grid(row=8+i, column=0 ,padx=40, pady=(5, 0), sticky='ew')
            self.delete_buttons[i].grid(row=8+i, column=1, padx=3, pady=(5,0), sticky='w')

        if not self.selected_files:
            self.notselected_label.grid(row=8, column=0, padx=40, pady=(5, 0), sticky='ew')


    def remove_directory(self) -> None:
        self.file_path = "Not directory selected"
        self.directory_path_label.configure(text=self.file_path)
        self.delete_directory_btn.destroy()

    def get_file_path(self) -> str | None:
        return None if self.file_path == "Not directory selected" else self.file_path


    def get_photos_to_watermark(self) -> list[str] | None:
        return None if not self.selected_files else self.selected_files

    def run_process(self, images, text, path) -> None:
        for image in images:
            self.image_processing.watermark(image, text, path)


        self.root.after(0, self.show_success)


    def show_success(self):
        self.entry.delete(0, 'end')
        self.button.configure(text="Success!  ", state="normal", bootstyle="success")
        self.root.after(1500, self.reset_btn)

    def btn_watermark(self):
        self.root.after_cancel(self.ready_id)

        self.button.configure(command="")
        self.button.configure(text="Processing...", state="disabled", bootstyle="secondary")
        self.root.update()

        text = self.entry.get()
        path = self.get_file_path()
        images = self.selected_files

        threading.Thread(
            target= self.run_process,
            args=(images, text, path),
            daemon=True
        ).start()


    def reset_btn(self):
        self.button.configure(text="Watermark", state="disable", bootstyle="primary")
        self.button.configure(command=self.btn_watermark)
        self.ready_id = self.root.after(200, self.check_button_responsiveness)


if __name__ == "__main__":
    watermark = WatermarkGui(ImageProcessing())
    watermark.root.mainloop()
