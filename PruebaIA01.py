import PyPDF2
import easyocr
import cv2
import subprocess

# Modulo que imprime las intruciones del programa
def Instrucciones():
    print()
    print("="*60)
    print("*"*17)
    print("* INSTRUCCIÓNES *")
    print("*"*17)
    print("0. Este es un prototipo(Prueba). Puede tener errores")
    print("1. Solo funciona con deepseek-r1 de Ollama")
    print("2. Sirve principalmete para tratar archivos")
    print("3. Primero pasas los datos del modelo que usas")
    print("4. Pasas la ubicación de tu archivo")
    print("5. solo archivo IMAGEN o PDF")
    print("6. Finalizas pasando tu pregunta")
    print("7. Es posible que se demore un poco")
    print("8. La ruta del archivo debe usar '\\'")
    print("="*60)
    print()

def MostrarModelo():
    print()
    print("=================")
    print("INGRESE EL MODELO")
    print("1- deepseek-r1:1.5b")
    print("2- deepseek-r1:7b")
    print("3- deepseek-r1:8b")
    print("4- deepseek-r1:14b")
    print("5- deepseek-r1:32b")
    print("6- deepseek-r1:70b")
    print("7- deepseek-r1:671b")

def TipoModelo(N_Modelo):
    Modelo = "deepseek-r1:671b"
    if (N_Modelo == 1):
        Modelo = "deepseek-r1:1.5b"
    elif (N_Modelo == 2):
        Modelo = "deepseek-r1:7b"
    elif (N_Modelo == 3):
        Modelo = "deepseek-r1:8b"
    elif (N_Modelo == 4):
        Modelo = "deepseek-r1:14b"
    elif (N_Modelo == 5):
        Modelo = "deepseek-r1:32b"
    elif (N_Modelo == 6):
        Modelo = "deepseek-r1:70b"
    return Modelo

def ExtraerNombre(Ruta):
    Nombre = ""
    for k in Ruta[::-1]: 
        if k == "\\":
            break
        Nombre += k
    return Nombre[::-1]

# MODULO PRINCIPAL
def main():
    Continuar = "Si" # variabla para continuar la conversación
    Instrucciones() #Instruciónes
    # Ingresar el modelo de IA
    MostrarModelo()
    Nro_Modelo = int(input("Ingrese el modelo->"))
    Modelo = TipoModelo(Nro_Modelo)

    while (Continuar.upper() == "SI"):
        # Ruta del archivo
        file_path = input("Ingrese la ruta del archivo: ")

        # Variables necesarias para el promt
        question = "N/A"
        file_content = "N/A"
        file_name = ExtraerNombre(file_path)

        # Extraer el texto del archivo
        extencion = file_path[-3:]
        if extencion.upper() == "PDF" :
            try:
                # Extraer el contenido del archivo PDF
                file_content = ""
                with open(file_path, "rb") as file:
                    reader = PyPDF2.PdfReader(file)
                    for page in reader.pages:
                        text = page.extract_text()
                        if text:
                            file_content += text

                # Validar si se extrajo contenido
                if not file_content:
                    print("No se pudo extraer texto del PDF. Verifica si contiene texto seleccionable.")
                    break
            except:
                print("ERROR AL LEER EL PDF")
        else:
            try:
                # Cargar la imagen
                image = cv2.imread(file_path)

                # Crear el lector de EasyOCR para el idioma español
                reader = easyocr.Reader(['es'])

                # Extraer texto de la imagen
                resultados = reader.readtext(image, detail=0)

                # Unir el texto extraído en una sola cadena
                file_content = ' '.join(resultados)

                if not file_content:
                    print("No se pudo extraer texto de la imagen.")

            except Exception as e:
                print(f"ERROR AL LEER LA IMAGEN: {e}")

        # Crear el prompt usando la plantilla oficial de DeepSeek
        question = input("Ingrese su pregunta: ") # Ingrese su pregunta
        file_template = f"""
        [file name]: {file_name}
        [file content begin]
        {file_content}
        [file content end]
        {question}
        """

        # Enviar el prompt a DeepSeek usando Ollama
        print(Modelo)
        comando = ["ollama", "run", Modelo]
        resultado = subprocess.run(comando, input=file_template, capture_output=True, text=True, encoding='utf-8')

        # Respuesta
        print("\n================== RESPUESTA ================")
        print(resultado.stdout)

        # Continuar?
        Continuar = input("\nQuiere continuar? (si/no): ")

    print("GRACIAS POR USAR MI SCRIPT")

if __name__ == "__main__":
    main()
