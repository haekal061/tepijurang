import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
import cv2

class CitraDigitalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplikasi Citra Digital")
        self.root.configure(bg='#23272e')

        self.img1 = None
        self.hasil = None

        # Frame Input Gambar
        input_frame = tk.Frame(root, bg='#f0e6f6', pady=10, padx=10)
        input_frame.pack(side=tk.TOP, fill=tk.X, padx=20, pady=10)

        input_frame.grid_columnconfigure(0, weight=1)
        input_frame.grid_columnconfigure(6, weight=1)

        tk.Button(input_frame, text="Input Gambar 1", command=self.load_img1, bg='#2980b9', fg='white').grid(row=0, column=1, padx=5, pady=5)
        tk.Button(input_frame, text="Hapus Gambar 1", command=self.hapus_img1, bg='#c0392b', fg='white').grid(row=0, column=2, padx=(5, 50), pady=5)
        tk.Button(input_frame, text="Simpan Hasil", command=self.save_result, bg='#27ae60', fg='white').grid(row=0, column=3, padx=5, pady=5)

        # Frame Tampilan Gambar 1 saja
        gambar_frame = tk.Frame(root, bg='#23272e')
        gambar_frame.pack(side=tk.TOP, pady=10)

        self.panel_img1 = tk.Label(gambar_frame, text="Gambar 1", bg='#2d3e50', fg='white')
        self.panel_img1.grid(row=0, column=0, padx=5)

        # Frame Tombol Fitur
        fitur_frame = tk.Frame(root, bg='#f0e6f6')
        fitur_frame.pack(side=tk.TOP, pady=10)

        btn_style = {'bg':'#2980b9', 'fg':"#FFFFFF", 'padx':8, 'pady':3, 'font':('Arial', 9, 'bold')}
        tk.Button(fitur_frame, text="Grayscale", command=self.grayscale, **btn_style).grid(row=0, column=0, padx=3, pady=3)

    def load_img1(self):
        path = filedialog.askopenfilename()
        if path:
            img = cv2.imread(path)
            if img is not None:
                self.img1 = img
                self.display_image(img, self.panel_img1)
                self.hasil = None

    def hapus_img1(self):
        self.img1 = None
        self.panel_img1.config(image='', text='Gambar 1')
        self.hasil = None

    def save_result(self):
        if self.hasil is not None:
            f = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png"), ("All Files", "*.*")])
            if f:
                cv2.imwrite(f, self.hasil)
                messagebox.showinfo("Info", "Gambar berhasil disimpan.")
        else:
            messagebox.showwarning("Warning", "Tidak ada hasil untuk disimpan.")

    def grayscale(self):
        if self.img1 is not None:
            hasil = cv2.cvtColor(self.img1, cv2.COLOR_BGR2GRAY)
            self.hasil = hasil
            messagebox.showinfo("Info", "Konversi ke grayscale berhasil. Silakan simpan hasil.")
        else:
            messagebox.showerror("Error", "Input Gambar 1 terlebih dahulu!")

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
