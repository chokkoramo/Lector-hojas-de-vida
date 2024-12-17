import os
from utils.pdf_reader import extract_cv_data, save_to_json

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
            try:
                cv_data = extract_cv_data(pdf_path)
            except Exception as e:
                print(f"Error procesando el archivo {file_name}: {e}")
                continue

            # Guardar datos en JSON
            output_path = os.path.join(output_dir, f"{os.path.splitext(file_name)[0]}.json")
            save_to_json(cv_data, output_path)
            print(f"Datos guardados en: {output_path}")

if __name__ == "__main__":
    main()