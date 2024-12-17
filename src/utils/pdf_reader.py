import os
import json
import pdfplumber
import re
from transformers import pipeline
from pdf2image import convert_from_path
import pytesseract

# Cargar un modelo de IA preentrenado para procesamiento de texto
nlp = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")

def extract_cv_data(pdf_path):
    """
    Extrae datos relevantes de un PDF con formato flexible usando regex y procesamiento de lenguaje natural.

    Args:
        pdf_path (str): Ruta del archivo PDF.

    Returns:
        dict: Diccionario con los datos extraídos.
    """
    data = {
        "Nombre": "",
        "Contacto": {
            "Correo": "",
            "Teléfono": "",
            "Dirección": ""
        },
        "Perfil Profesional": "",
        "Experiencia Profesional": [],
        "Educación": [],
        "Referencias": []
    }

    def search_pattern(pattern, text):
        match = re.search(pattern, text, re.IGNORECASE)
        return match.group(1).strip() if match else ""

    def ocr_from_pdf(pdf_path):
        images = convert_from_path(pdf_path)
        full_text = ""
        for img in images:
            full_text += pytesseract.image_to_string(img)
        return full_text

    # Extraer texto del PDF
    full_text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                full_text += page_text + "\n"

    # Si no se extrajo texto, usar OCR
    if not full_text.strip():
        print(f"El archivo {pdf_path} no contiene texto seleccionable. Usando OCR.")
        full_text = ocr_from_pdf(pdf_path)

    # Buscar información clave usando patrones regulares
    data["Nombre"] = search_pattern(r"NOMBRES Y APELLIDOS:?\s*(.*)", full_text)
    data["Contacto"]["Teléfono"] = search_pattern(r"TEL[ÉE]FONO:?\s*(.*)", full_text)
    data["Contacto"]["Correo"] = search_pattern(r"E-MAIL:?\s*(.*)", full_text)
    data["Contacto"]["Dirección"] = search_pattern(r"DIRECCI[ÓO]N:?\s*(.*)", full_text)

    # Extraer perfil profesional usando IA
    if "PERFIL PROFESIONAL" in full_text:
        context = full_text
        question = "¿Cuál es el perfil profesional del candidato?"
        try:
            result = nlp(question=question, context=context)
            data["Perfil Profesional"] = result["answer"] if result["score"] > 0.5 else "No se pudo procesar"
        except Exception as e:
            print(f"Error al procesar 'Perfil Profesional': {e}")
            data["Perfil Profesional"] = "No se pudo procesar"

    # Extraer experiencia profesional usando IA
    if "EXPERIENCIA PROFESIONAL" in full_text:
        context = full_text
        question = "¿Cuál es la experiencia profesional del candidato?"
        try:
            result = nlp(question=question, context=context)
            data["Experiencia Profesional"].append(result["answer"] if result["score"] > 0.5 else "No se pudo procesar")
        except Exception as e:
            print(f"Error al procesar 'Experiencia Profesional': {e}")

    # Extraer educación usando IA
    if "FORMACIÓN" in full_text:
        context = full_text
        question = "¿Cuál es la formación académica del candidato?"
        try:
            result = nlp(question=question, context=context)
            data["Educación"].append(result["answer"] if result["score"] > 0.5 else "No se pudo procesar")
        except Exception as e:
            print(f"Error al procesar 'Formación Académica': {e}")

    # Extraer referencias usando IA
    if "REFERENCIAS" in full_text:
        context = full_text
        question = "¿Cuáles son las referencias del candidato?"
        try:
            result = nlp(question=question, context=context)
            data["Referencias"].append(result["answer"] if result["score"] > 0.5 else "No se pudo procesar")
        except Exception as e:
            print(f"Error al procesar 'Referencias': {e}")

    return data

def save_to_json(data, output_path):
    """
    Guarda los datos extraídos en un archivo JSON.

    Args:
        data (dict): Datos a guardar.
        output_path (str): Ruta del archivo JSON de salida.
    """
    with open(output_path, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)
