import os
import json
import pdfplumber

def extract_cv_data(pdf_path):
    """
    Extrae datos relevantes de un PDF con formato específico.

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
            "LinkedIn": ""
        },
        "Perfil Profesional": "",
        "Experiencia Profesional": [],
        "Educación": [],
        "Idiomas": [],
        "Habilidades": [],
        "Intereses": []
    }

    with pdfplumber.open(pdf_path) as pdf:
        text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
        
        # Extraer Nombre (en el encabezado)
        lines = text.split("\n")
        data["Nombre"] = lines[0].strip()  # Primera línea
        
        # Extraer Contacto
        for line in lines:
            if "@" in line:  # Correo
                data["Contacto"]["Correo"] = line.strip()
            elif "linkedin" in line.lower():  # LinkedIn
                data["Contacto"]["LinkedIn"] = line.strip()
            elif "+" in line:  # Teléfono
                data["Contacto"]["Teléfono"] = line.strip()

        # Extraer Perfil Profesional
        # if "PERFIL PROFESIONAL" in text:
        #     data["Perfil Profesional"] = extract_section(text, "PERFIL PROFESIONAL", "IDIOMAS")

        if "DATOS PERSONALES" in text:
            data["Perfil Profesional"] = extract_section(text, "PERFIL PROFESIONAL", "IDIOMAS")

        # Extraer Experiencia Profesional
        if "EXPERIENCIA PROFESIONAL" in text:
            data["Experiencia Profesional"] = extract_section(text, "EXPERIENCIA PROFESIONAL", "FORMACIÓN").split("\n")
        
        # Extraer Educación
        if "FORMACIÓN" in text:
            data["Educación"] = extract_section(text, "FORMACIÓN", "IDIOMAS").split("\n")

        # Extraer Idiomas
        if "IDIOMAS" in text:
            data["Idiomas"] = extract_section(text, "IDIOMAS", "HABILIDADES").split("\n")
        
        # Extraer Habilidades
        if "HABILIDADES" in text:
            data["Habilidades"] = extract_section(text, "HABILIDADES", "INTERESES").split("\n")
        
        # Extraer Intereses
        if "INTERESES" in text:
            data["Intereses"] = extract_section(text, "INTERESES", "").split("\n")

    return data

def extract_section(text, start_keyword, end_keyword):
    """
    Extrae una sección de texto entre dos palabras clave.

    Args:
        text (str): Texto completo del documento.
        start_keyword (str): Inicio de la sección.
        end_keyword (str): Fin de la sección.

    Returns:
        str: Texto contenido en la sección.
    """
    try:
        start_idx = text.index(start_keyword) + len(start_keyword)
        end_idx = text.index(end_keyword) if end_keyword else len(text)
        return text[start_idx:end_idx].strip()
    except ValueError:
        return ""

def save_to_json(data, output_path):
    """
    Guarda los datos extraídos en un archivo JSON.

    Args:
        data (dict): Datos a guardar.
        output_path (str): Ruta del archivo JSON de salida.
    """
    with open(output_path, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

def main():
    input_dir = "data"  # Carpeta donde se almacenan los PDFs
    output_dir = "output"  # Carpeta para guardar los resultados

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for file_name in os.listdir(input_dir):
        if file_name.endswith(".pdf"):
            pdf_path = os.path.join(input_dir, file_name)
            print(f"Procesando: {file_name}")

            # Extraer datos
            cv_data = extract_cv_data(pdf_path)

            # Guardar datos en JSON
            output_path = os.path.join(output_dir, f"{os.path.splitext(file_name)[0]}.json")
            save_to_json(cv_data, output_path)
            print(f"Datos guardados en: {output_path}")

if __name__ == "__main__":
    main()

