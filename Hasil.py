import tkinter as tk
from PIL import Image, ImageTk
import cv2

class CitraDigitalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplikasi Citra Digital")
        self.root.configure(bg='#23272e')

        # Contoh gambar hasil (bisa diisi apapun dari luar class)
        self.hasil = None

        # Frame Tampilan Hasil
        gambar_frame = tk.Frame(root, bg='#23272e')
        gambar_frame.pack(side=tk.TOP, pady=10)
        self.panel_hasil = tk.Label(gambar_frame, text="Hasil", bg='#34495e', fg='white')
        self.panel_hasil.grid(row=0, column=0, padx=5)

        # Tombol untuk menampilkan hasil (demo)
        tk.Button(root, text="Tampilkan Hasil", command=self.tampilkan_hasil).pack(pady=8)

    def tampilkan_hasil(self):
        # Contoh isi self.hasil (anda bisa assign gambar hasil sendiri)
        self.hasil = cv2.imread('contoh.png')  # Ganti 'contoh.png' dengan path gambar yang ingin ditampilkan
        if self.hasil is not None:
            self.display_image(self.hasil, self.panel_hasil)
        else:
            self.panel_hasil.config(image='', text='Hasil tidak ditemukan')

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
