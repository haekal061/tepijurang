import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2

class CitraDigitalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplikasi Citra Digital")
        self.root.configure(bg='#23272e')

        self.img1 = None
        self.img2 = None

        # Frame Input Gambar
        input_frame = tk.Frame(root, bg='#f0e6f6', pady=10, padx=10)
        input_frame.pack(side=tk.TOP, fill=tk.X, padx=20, pady=10)

        input_frame.grid_columnconfigure(0, weight=1)
        input_frame.grid_columnconfigure(6, weight=1)

        tk.Button(input_frame, text="Input Gambar 1", command=self.load_img1, bg='#2980b9', fg='white').grid(row=0, column=1, padx=5, pady=5)
        tk.Button(input_frame, text="Hapus Gambar 1", command=self.hapus_img1, bg='#c0392b', fg='white').grid(row=0, column=2, padx=(5, 50), pady=5)       
        tk.Button(input_frame, text="Input Gambar 2", command=self.load_img2, bg='#2980b9', fg='white').grid(row=0, column=3, padx=5, pady=5)
        tk.Button(input_frame, text="Hapus Gambar 2", command=self.hapus_img2, bg='#c0392b', fg='white').grid(row=0, column=4, padx=5, pady=5)

        # Frame Tampilan Gambar
        gambar_frame = tk.Frame(root, bg='#23272e')
        gambar_frame.pack(side=tk.TOP, pady=10)

        self.panel_img1 = tk.Label(gambar_frame, text="Gambar 1", bg='#2d3e50', fg='white')
        self.panel_img1.grid(row=0, column=0, padx=5)
        self.panel_img2 = tk.Label(gambar_frame, text="Gambar 2", bg='#2d3e50', fg='white')
        self.panel_img2.grid(row=0, column=1, padx=5)

    def load_img1(self):
        path = filedialog.askopenfilename()
        if path:
            img = cv2.imread(path)
            if img is not None:
                self.img1 = img
                self.display_image(img, self.panel_img1)

    def hapus_img1(self):
        self.img1 = None
        self.panel_img1.config(image='', text='Gambar 1')

    def load_img2(self):
        path = filedialog.askopenfilename()
        if path:
            img = cv2.imread(path)
            if img is not None:
                self.img2 = img
                self.display_image(img, self.panel_img2)

    def hapus_img2(self):
        self.img2 = None
        self.panel_img2.config(image='', text='Gambar 2')

    def display_image(self, img, panel, max_size=(400, 400)):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img)
        w, h = img_pil.size
        max_w, max_h = max_size
        if w > max_w or h > max_h:
            ratio = min(max_w/w, max_h/h)
            new_size = (int(w*ratio), int(h*ratio))
            img_pil = img_pil.resize(new_size, Image.LANCZOS)
        imgtk = ImageTk.PhotoImage(img_pil)
        panel.config(image=imgtk, text='')
        panel.image = imgtk

if __name__ == "__main__":
    root = tk.Tk()
    app = CitraDigitalApp(root)
    root.mainloop()
