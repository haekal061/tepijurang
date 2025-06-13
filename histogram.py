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
    
    def show_all_histograms(self):
        self.clear_histogram()
        # Tidak tampilkan apapun jika SEMUA gambar kosong
        if self.img1 is None and self.img2 is None and self.hasil is None:
            return

        fig = plt.Figure(figsize=(10, 2.8), dpi=100)  # 3 histogram berdampingan

        # Histogram Gambar 1
        ax1 = fig.add_subplot(1,3,1)
        if self.img1 is not None:
            if len(self.img1.shape) == 3:
                color = ('b','g','r')
                for i, col in enumerate(color):
                    hist = cv2.calcHist([self.img1], [i], None, [256], [0,256])
                    ax1.plot(hist, color=col, label=col.upper())
                ax1.set_title('Histogram RGB Gambar 1', fontsize=10)
                ax1.legend()
            else:
                ax1.hist(self.img1.ravel(), 256, [0,256], color='#2980b9')
                ax1.set_title('Histogram Gambar 1', fontsize=10)
            ax1.set_xlabel('Intensitas')
            ax1.set_ylabel('Jumlah')
        else:
            ax1.axis('off')

        # Histogram Gambar 2
        ax2 = fig.add_subplot(1,3,2)
        if self.img2 is not None:
            if len(self.img2.shape) == 3:
                color = ('b','g','r')
                for i, col in enumerate(color):
                    hist = cv2.calcHist([self.img2], [i], None, [256], [0,256])
                    ax2.plot(hist, color=col, label=col.upper())
                ax2.set_title('Histogram RGB Gambar 2', fontsize=10)
                ax2.legend()
            else:
                ax2.hist(self.img2.ravel(), 256, [0,256], color='#27ae60')
                ax2.set_title('Histogram Gambar 2', fontsize=10)
            ax2.set_xlabel('Intensitas')
            ax2.set_ylabel('Jumlah')
        else:
            ax2.axis('off')

        # Histogram Hasil
        ax3 = fig.add_subplot(1,3,3)
        if self.hasil is not None:
            if len(self.hasil.shape) == 3:
                color = ('b','g','r')
                for i, col in enumerate(color):
                    hist = cv2.calcHist([self.hasil], [i], None, [256], [0,256])
                    ax3.plot(hist, color=col, label=col.upper())
                ax3.set_title('Histogram RGB Hasil', fontsize=10)
                ax3.legend()
            else:
                ax3.hist(self.hasil.ravel(), 256, [0,256], color='#e67e22')
                ax3.set_title('Histogram Hasil', fontsize=10)
            ax3.set_xlabel('Intensitas')
            ax3.set_ylabel('Jumlah')
        else:
            ax3.axis('off')

        fig.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=self.hist_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)