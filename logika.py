import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
import cv2
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class CitraDigitalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplikasi Citra Digital")
        self.root.configure(bg='#23272e')

        self.img1 = None
        self.img2 = None
        self.hasil = None
        self.erosi_mode = False

        input_frame = tk.Frame(root, bg='#f0e6f6', pady=10, padx=10)
        input_frame.pack(side=tk.TOP, fill=tk.X, padx=20, pady=10)

        input_frame.grid_columnconfigure(0, weight=1) 
        input_frame.grid_columnconfigure(6, weight=1)  

        tk.Button(input_frame, text="Input Gambar 1", command=self.load_img1, bg='#2980b9', fg='white').grid(row=0, column=1, padx=5, pady=5)
        tk.Button(input_frame, text="Hapus Gambar 1", command=self.hapus_img1, bg='#c0392b', fg='white').grid(row=0, column=2, padx=(5, 50), pady=5)       
        tk.Button(input_frame, text="Input Gambar 2", command=self.load_img2, bg='#2980b9', fg='white').grid(row=0, column=3, padx=5, pady=5)
        tk.Button(input_frame, text="Hapus Gambar 2", command=self.hapus_img2, bg='#c0392b', fg='white').grid(row=0, column=4, padx=5, pady=5)
        tk.Button(input_frame, text="Simpan Hasil", command=self.save_result, bg='#27ae60', fg='white').grid(row=0, column=5, padx=5, pady=5)

        gambar_frame = tk.Frame(root, bg='#23272e')
        gambar_frame.pack(side=tk.TOP, pady=10)

        self.panel_img1 = tk.Label(gambar_frame, text="Gambar 1", bg='#2d3e50', fg='white')
        self.panel_img1.grid(row=0, column=0, padx=5)
        self.panel_img2 = tk.Label(gambar_frame, text="Gambar 2", bg='#2d3e50', fg='white')
        self.panel_img2.grid(row=0, column=1, padx=5)
        self.panel_hasil = tk.Label(gambar_frame, text="Hasil", bg='#34495e', fg='white')
        self.panel_hasil.grid(row=0, column=2, padx=5)

        fitur_frame = tk.Frame(root, bg='#f0e6f6')
        fitur_frame.pack(side=tk.TOP, pady=10)

        btn_style = {'bg':'#2980b9', 'fg':"#FFFFFF", 'padx':8, 'pady':3, 'font':('Arial', 9, 'bold')}
        btn_style1 = {'bg':"#174868", 'fg':"#FFFFFF", 'padx':8, 'pady':3, 'font':('Arial', 9, 'bold')}
        tk.Button(fitur_frame, text="Grayscale", command=self.grayscale, **btn_style).grid(row=0, column=0, padx=3, pady=3)
        tk.Button(fitur_frame, text="Biner", command=self.biner, **btn_style).grid(row=0, column=1, padx=3, pady=3)
        tk.Button(fitur_frame, text="Subtract", command=self.subtract, **btn_style).grid(row=0, column=2, padx=3, pady=3)
        tk.Button(fitur_frame, text="Logika OR", command=self.logic_or, **btn_style).grid(row=0, column=3, padx=3, pady=3)
        tk.Button(fitur_frame, text="Edge Detection", command=self.edge_detection, **btn_style).grid(row=0, column=4, padx=3, pady=3)
        
        self.btn_erosi = tk.Button(fitur_frame, text="Erosi", command=self.toggle_erosion_buttons, **btn_style)
        self.btn_erosi.grid(row=0, column=5, padx=3, pady=3)
        self.btn_erosi_plus = tk.Button(fitur_frame, text="Cross +", command=lambda: self.erosion('cross'), **btn_style1)
        self.btn_erosi_diag = tk.Button(fitur_frame, text="Kotak", command=lambda: self.erosion('diagonal'), **btn_style1)

        tk.Button(fitur_frame, text="Tampilkan Histogram", command=self.show_all_histograms, **btn_style).grid(row=0, column=8, padx=3, pady=3)

        self.hist_frame = tk.Frame(root, bg='#f0e6f6')
        self.hist_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=15, pady=5)

    def logic_or(self):
        if self.img1 is not None and self.img2 is not None:
            img1_gray = cv2.cvtColor(self.img1, cv2.COLOR_BGR2GRAY)
            img2_gray = cv2.cvtColor(self.img2, cv2.COLOR_BGR2GRAY)
            img2_resized = cv2.resize(img2_gray, (img1_gray.shape[1], img1_gray.shape[0]))
            hasil = cv2.bitwise_or(img1_gray, img2_resized)
            self.hasil = hasil
            self.display_image(hasil, self.panel_hasil, gray=True)
            self.clear_histogram()
        else:
            messagebox.showerror("Error", "Input kedua gambar terlebih dahulu!")