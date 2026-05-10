from pix2tex.cli import LatexOCR
from PIL import Image, ImageEnhance # Añadimos ImageEnhance
import pytesseract
import numpy as np
import re

# Configura aquí la ruta exacta donde tienes instalado Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class FormulaExtractor:
    def __init__(self):
        print("Cargando el modelo de IA para LaTeX...")
        self.model = LatexOCR()

    def _clean_latex(self, raw_latex: str) -> str:
        text = raw_latex
        text = text.replace(r'\\', '\n')
        text = re.sub(r'\\begin\{[^}]+\}', '', text)
        text = re.sub(r'\\end\{[^}]+\}', '', text)
        text = text.replace('&', ' ')
        text = re.sub(r'\\mathrm\{([^}]+)\}', r'\1', text)
        text = re.sub(r'\\operatorname\{([^}]+)\}', r'\1', text)
        text = re.sub(r'\\text\{([^}]+)\}', r'\1', text)
        text = re.sub(r'\\quad', '  ', text)
        text = text.replace('~', ' ')
        text = text.replace(r'\ ', ' ')
        text = text.replace('{{', '{').replace('}}', '}')
        text = '\n'.join([line.strip() for line in text.split('\n') if line.strip()])
        return text

    def extract_from_image(self, image: Image.Image) -> str:
        if image is None: return ""
        try:
            raw_latex = self.model(image)
            return self._clean_latex(raw_latex)
        except Exception as e:
            return f"Error en OCR Matemático: {str(e)}"

class TextExtractor:
    def __init__(self):
        print("Inicializando Tesseract para texto normal...")

    def extract_from_image(self, image: Image.Image) -> str:
        if image is None: return ""
        try:
            # --- PREPROCESAMIENTO DE IMAGEN PARA MEJORAR PRECISIÓN ---
            
            # 1. Escalar la imagen (x3) para separar los píxeles de letras como 'rr'
            ancho, alto = image.size
            factor_escala = 3 
            # Nota: Si usas una versión antigua de PIL, usa Image.LANCZOS en lugar de Image.Resampling.LANCZOS
            img_ampliada = image.resize((ancho * factor_escala, alto * factor_escala), Image.Resampling.LANCZOS)
            
            # 2. Convertir a escala de grises
            img_gris = img_ampliada.convert('L')
            
            # 3. Aumentar el contraste al doble
            optimizador = ImageEnhance.Contrast(img_gris)
            img_optimizada = optimizador.enhance(2.0)
            
            # ---------------------------------------------------------

            # Convertir a numpy array y pasar a Tesseract
            img_array = np.array(img_optimizada)
            
            # El parámetro --psm 6 le dice a Tesseract que asuma un bloque uniforme de texto, 
            # lo cual reduce las alucinaciones estructurales.
            configuracion = r'--oem 3 --psm 6'
            text = pytesseract.image_to_string(img_array, config=configuracion)
            
            return text.strip()
        except Exception as e:
            return f"Error en OCR de Texto: {str(e)}"