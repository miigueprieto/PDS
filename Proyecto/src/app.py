import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import font as tkfont
from PIL import Image, ImageTk
import numpy as np
import cv2

# importamos los filtros
from filtrosepia import filtro_sepia
from Mediana import filtro_mediana
from Media import filtro_media
from filtrosemitono import filtro_semitono
from convolucion import convolucion_manual
from filtrohomomorfico import filtro_homomorfico
from Notch import filtro_notch

class ProcesadorImagenesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Procesador de Filtros")
        self.root.geometry("950x700")
        self.root.config(bg="#1e1e1e") # fondo oscuro principal

        # fuentes
        fuente_btn = tkfont.Font(family="Helvetica", size=10)
        fuente_titulo = tkfont.Font(family="Helvetica", size=11, weight="bold")

        # vars d estado
        self.imagen_original_cv = None
        self.imagen_procesada_cv = None

        # panel izq pa los botones
        frame_controles = tk.Frame(self.root, width=250, bg="#252526", padx=15, pady=15)
        frame_controles.pack(side=tk.LEFT, fill=tk.Y)

        # boton cargar
        btn_cargar = tk.Button(frame_controles, text="Cargar Imagen", command=self.cargar_imagen, 
                               bg="#007acc", fg="white", font=fuente_titulo, relief="flat", 
                               cursor="hand2", pady=8, activebackground="#0098ff", activeforeground="white")
        btn_cargar.pack(pady=(0, 20), fill=tk.X)

        tk.Label(frame_controles, text="FILTROS", bg="#252526", fg="#cccccc", font=fuente_titulo).pack(pady=(10, 5))

        # config base pa q los botones no queden feos
        estilo_btn = {
            "bg": "#333337", "fg": "#e1e1e1", "font": fuente_btn, "relief": "flat", 
            "cursor": "hand2", "pady": 6, "activebackground": "#3f3f46", "activeforeground": "white"
        }

        # botones d todos los filtros
        btn_sepia = tk.Button(frame_controles, text="Aplicar Sepia", command=self.aplicar_sepia, **estilo_btn)
        btn_sepia.pack(pady=4, fill=tk.X)
        
        btn_mediana = tk.Button(frame_controles, text="Aplicar Mediana", command=self.aplicar_mediana, **estilo_btn)
        btn_mediana.pack(pady=4, fill=tk.X)

        btn_media = tk.Button(frame_controles, text="Aplicar Media", command=self.aplicar_media, **estilo_btn)
        btn_media.pack(pady=4, fill=tk.X)

        btn_semitono = tk.Button(frame_controles, text="Aplicar Semitono", command=self.aplicar_semitono, **estilo_btn)
        btn_semitono.pack(pady=4, fill=tk.X)

        btn_convolucion = tk.Button(frame_controles, text="Convolución (Bordes)", command=self.aplicar_convolucion, **estilo_btn)
        btn_convolucion.pack(pady=4, fill=tk.X)

        btn_homomorfico = tk.Button(frame_controles, text="Filtro Homomórfico", command=self.aplicar_homomorfico, **estilo_btn)
        btn_homomorfico.pack(pady=4, fill=tk.X)

        btn_notch = tk.Button(frame_controles, text="Filtro Notch", command=self.aplicar_notch, **estilo_btn)
        btn_notch.pack(pady=4, fill=tk.X)

        # seccion d abajo
        tk.Label(frame_controles, text="ACCIONES", bg="#252526", fg="#cccccc", font=fuente_titulo).pack(pady=(25, 5))
        
        btn_rebobinar = tk.Button(frame_controles, text="Rebobinar (Original)", command=self.rebobinar, 
                                  bg="#986a44", fg="white", font=fuente_btn, relief="flat", 
                                  cursor="hand2", pady=6, activebackground="#b88358", activeforeground="white")
        btn_rebobinar.pack(pady=4, fill=tk.X)

        btn_guardar = tk.Button(frame_controles, text="Guardar Resultado", command=self.guardar_imagen, 
                                bg="#0f4a21", fg="white", font=fuente_btn, relief="flat", 
                                cursor="hand2", pady=6, activebackground="#16662e", activeforeground="white")
        btn_guardar.pack(side=tk.BOTTOM, pady=10, fill=tk.X)

        # panel derecho pa la foto
        frame_vista = tk.Frame(self.root, bg="#1e1e1e")
        frame_vista.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)

        self.label_imagen = tk.Label(frame_vista, text="Sube una imagen para empezar", bg="#1e1e1e", fg="#666666", font=("Helvetica", 14))
        self.label_imagen.pack(expand=True)

    def cargar_imagen(self):
        ruta = filedialog.askopenfilename(title="Selecciona una imagen", filetypes=[("Imágenes", "*.jpg *.jpeg *.png *.bmp")])
        if ruta:
            img = cv2.imread(ruta)
            self.imagen_original_cv = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            self.imagen_procesada_cv = self.imagen_original_cv.copy()
            self.mostrar_imagen(self.imagen_procesada_cv)

    def mostrar_imagen(self, img_array):
        img_pil = Image.fromarray(img_array)
        img_pil.thumbnail((650, 550))
        img_tk = ImageTk.PhotoImage(img_pil)
        self.label_imagen.config(image=img_tk, text="")
        self.label_imagen.image = img_tk

    def rebobinar(self):
        if self.imagen_original_cv is None: return
        self.imagen_procesada_cv = self.imagen_original_cv.copy()
        self.mostrar_imagen(self.imagen_procesada_cv)
        print("rebobinado")

    def aplicar_sepia(self):
        if self.imagen_original_cv is None: return
        print("procesando sepia...")
        resultado_float = filtro_sepia(self.imagen_procesada_cv) 
        # da floats asi q multiplicamos y a 8 bits
        self.imagen_procesada_cv = (resultado_float * 255).astype(np.uint8)
        self.mostrar_imagen(self.imagen_procesada_cv)

    def aplicar_mediana(self):
        if self.imagen_original_cv is None: return
        print("procesando mediana...")
        # a gris temporalmente q el filtro es d 1 canal
        img_gris = cv2.cvtColor(self.imagen_procesada_cv, cv2.COLOR_RGB2GRAY)
        resultado_gris = filtro_mediana(img_gris, K=3)
        self.imagen_procesada_cv = cv2.cvtColor(resultado_gris, cv2.COLOR_GRAY2RGB)
        self.mostrar_imagen(self.imagen_procesada_cv)

    def aplicar_media(self):
        if self.imagen_original_cv is None: return
        print("procesando media...")
        # Pasamos a gris porque convolve2d de scipy es para 2D
        img_gris = cv2.cvtColor(self.imagen_procesada_cv, cv2.COLOR_RGB2GRAY)
        resultado_float = filtro_media(img_gris, K=3)
        resultado_8u = np.clip(resultado_float, 0, 255).astype(np.uint8)
        self.imagen_procesada_cv = cv2.cvtColor(resultado_8u, cv2.COLOR_GRAY2RGB)
        self.mostrar_imagen(self.imagen_procesada_cv)

    def aplicar_semitono(self):
        if self.imagen_original_cv is None: return
        print("procesando semitono...")
        resultado_float = filtro_semitono(self.imagen_procesada_cv, tamano_bloque=8)
        # escalamos a 255
        resultado_8u = (resultado_float * 255).astype(np.uint8)
        self.imagen_procesada_cv = cv2.cvtColor(resultado_8u, cv2.COLOR_GRAY2RGB)
        self.mostrar_imagen(self.imagen_procesada_cv)

    def aplicar_convolucion(self):
        if self.imagen_original_cv is None: return
        print("procesando convolucion...")
        img_gris = cv2.cvtColor(self.imagen_procesada_cv, cv2.COLOR_RGB2GRAY)
        
        # kernel d bordes
        kernel_bordes = np.array([
            [-1, -1, -1],
            [-1,  8, -1],
            [-1, -1, -1]
        ])
        
        resultado = convolucion_manual(img_gris, kernel_bordes)
        resultado_8u = resultado.astype(np.uint8)
        self.imagen_procesada_cv = cv2.cvtColor(resultado_8u, cv2.COLOR_GRAY2RGB)
        self.mostrar_imagen(self.imagen_procesada_cv)

    def aplicar_homomorfico(self):
        if self.imagen_original_cv is None: return
        print("procesando homomorfico...")
        resultado_float = filtro_homomorfico(self.imagen_procesada_cv)
        # clipear x si se va d rango el log
        resultado_8u = np.clip(resultado_float * 255, 0, 255).astype(np.uint8)
        self.imagen_procesada_cv = resultado_8u
        self.mostrar_imagen(self.imagen_procesada_cv)

    def aplicar_notch(self):
        if self.imagen_original_cv is None: return
        print("procesando notch...")
        img_frecuencia = filtro_notch(self.imagen_procesada_cv)
        # dps del ifft hay q normalizar pa q se vea bn
        resultado_8u = cv2.normalize(img_frecuencia, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
        self.imagen_procesada_cv = cv2.cvtColor(resultado_8u, cv2.COLOR_GRAY2RGB)
        self.mostrar_imagen(self.imagen_procesada_cv)

    def guardar_imagen(self):
        if self.imagen_procesada_cv is None: return
        ruta = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg")])
        if ruta:
            # vuelta a bgr para guardar
            img_bgr = cv2.cvtColor(self.imagen_procesada_cv, cv2.COLOR_RGB2BGR)
            cv2.imwrite(ruta, img_bgr)
            messagebox.showinfo("ok", "guardado bn")

if __name__ == "__main__":
    root = tk.Tk()
    app = ProcesadorImagenesApp(root)
    root.mainloop()
