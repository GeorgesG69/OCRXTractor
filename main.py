import tkinter as tk
from tkinter import scrolledtext, messagebox
import pyperclip
import ctypes # <-- NUEVO: Para la barra de tareas de Windows
from screen_capture import capture_screen_area
from ocr_engine import FormulaExtractor, TextExtractor

class OCRApp:
    def __init__(self, root):
        self.root = root
        self.root.title("OCRXtractor")
        self.root.geometry("550x450")
        self.root.resizable(False, False)

        # --- NUEVO: CONFIGURACIÓN DEL ÍCONO ---
        try:
            # 1. Ícono de la ventana superior
            self.root.iconbitmap("icon.ico") 
            
            # 2. Ícono de la barra de tareas de Windows
            # Le damos a la app un ID único para separarla de Python
            myappid = 'mi_capturador.ocr.inteligente.1' 
            
        except Exception as e:
            print("No se encontró 'icono.ico'. Se usará el ícono por defecto.")
        # --------------------------------------

        print("Iniciando aplicación y cargando modelos...")
        self.text_extractor = TextExtractor()
        self.formula_extractor = FormulaExtractor()
        print("¡Interfaz lista!")

        # --- DISEÑO DE LA INTERFAZ ---
        tk.Label(root, text="¿Qué deseas capturar?", font=("Arial", 14, "bold")).pack(pady=(20, 10))
        
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=5)
        
        btn_texto = tk.Button(btn_frame, text="📝 Capturar Texto", font=("Arial", 11), 
                              command=lambda: self.iniciar_captura("text"), 
                              width=18, bg="#4CAF50", fg="white", cursor="hand2")
        btn_texto.pack(side=tk.LEFT, padx=15)
        
        btn_math = tk.Button(btn_frame, text="🧮 Capturar Fórmula", font=("Arial", 11), 
                             command=lambda: self.iniciar_captura("math"), 
                             width=18, bg="#2196F3", fg="white", cursor="hand2")
        btn_math.pack(side=tk.LEFT, padx=15)

        tk.Label(root, text="Resultado de la captura:", font=("Arial", 11)).pack(pady=(20, 5))

        self.caja_resultado = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=10, font=("Consolas", 11))
        self.caja_resultado.pack(padx=20, pady=5)
        
        tk.Label(root, text="El texto también se copia automáticamente a tu portapapeles.", 
                 font=("Arial", 9, "italic"), fg="gray").pack(pady=5)

    def iniciar_captura(self, mode):
        self.root.withdraw()
        image = capture_screen_area(self.root)
        self.root.deiconify()
        
        if image:
            self.caja_resultado.delete(1.0, tk.END)
            self.caja_resultado.insert(tk.END, "Procesando imagen, por favor espera...\n")
            self.root.update()

            if mode == "text":
                resultado = self.text_extractor.extract_from_image(image)
            else:
                resultado = self.formula_extractor.extract_from_image(image)
            
            self.caja_resultado.delete(1.0, tk.END)
            self.caja_resultado.insert(tk.END, resultado)
            
            if resultado.strip():
                pyperclip.copy(resultado)
        else:
            messagebox.showinfo("Cancelado", "Captura cancelada o área muy pequeña.")

if __name__ == "__main__":
    import os
    import ctypes

    # 1. Cambiamos ligeramente el ID para borrar el caché viejo de Windows
    try:
        myappid = 'mi_capturador.ocr.inteligente.2' 
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    except Exception:
        pass 

    root = tk.Tk()
    
    # 2. MÉTODO INFALIBLE: Usar un archivo .png con iconphoto
    try:
        carpeta_actual = os.path.dirname(os.path.abspath(__file__))
        ruta_icono = os.path.join(carpeta_actual, "icon.png") # ¡Ojo, ahora es .png!
        
        # Cargamos el PNG en la memoria de Tkinter
        icono_img = tk.PhotoImage(file=ruta_icono)
        
        # True = aplica el ícono a la ventana principal y a todos los cuadros de diálogo futuros
        root.iconphoto(True, icono_img)
    except Exception as e:
        print(f"Error cargando el ícono PNG: {e}")

    app = OCRApp(root)
    root.mainloop()