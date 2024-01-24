import subprocess
import os
import shutil

# Función para crear el archivo de configuración si no existe
def crear_configuracion():
    if not os.path.exists("configuracion.py"):
        with open("configuracion.py", "w", encoding='utf-8') as archivo_config:
            archivo_config.write("# configuracion.py\n\n")
            archivo_config.write("import os\n\n")
            archivo_config.write("# Función para guardar las rutas en el archivo de configuración\n")
            archivo_config.write("def guardar_rutas(ruta_yuzu, ruta_exe):\n")
            archivo_config.write("    with open(\"config.dat\", \"w\") as archivo_config:\n")
            archivo_config.write("        archivo_config.write(f\"{ruta_yuzu}\\n{ruta_exe}\")\n\n")
            archivo_config.write("# Función para obtener las rutas\n")
            archivo_config.write("def obtener_rutas():\n")
            archivo_config.write("    # Verificar si el archivo de configuración existe\n")
            archivo_config.write("    if os.path.exists(\"config.dat\"):\n")
            archivo_config.write("        with open(\"config.dat\", \"r\") as archivo_config:\n")
            archivo_config.write("            lineas = archivo_config.readlines()\n")
            archivo_config.write("            ruta_yuzu = lineas[0].strip()\n")
            archivo_config.write("            ruta_exe = lineas[1].strip()\n")
            archivo_config.write("    else:\n")
            archivo_config.write("        # Solicitar al usuario la ruta_yuzu y ruta_exe si el archivo no existe\n")
            archivo_config.write("        ruta_yuzu = input(\"Ingrese la ruta al ejecutable yuzu.exe (usar comillas si hay espacios o caracteres especiales): \")\n")
            archivo_config.write("        ruta_exe = input(\"Ingrese la ruta donde desea guardar los archivos .exe (usar comillas si hay espacios o caracteres especiales): \")\n")
            archivo_config.write("        # Guardar las rutas en el archivo de configuración\n")
            archivo_config.write("        guardar_rutas(ruta_yuzu, ruta_exe)\n")
            archivo_config.write("    return ruta_yuzu, ruta_exe\n\n")
            archivo_config.write("# Obtener rutas al inicio\n")
            archivo_config.write("ruta_yuzu, ruta_exe = obtener_rutas()\n")

# Verificar si existe configuracion.py antes de importar
if not os.path.exists("configuracion.py"):
    crear_configuracion()

from configuracion import obtener_rutas, guardar_rutas

def crear_ejecutable(ruta_yuzu, ruta_exe):

    # Ruta al archivo NSP
    ruta_nsp = input("Ingrese la ruta al archivo NSP (usar comillas si hay espacios o caracteres especiales): ")

    # Solicitar al usuario la ruta al icono (puede ser None si no se desea un icono)
    ruta_ico = input("Ingrese la ruta al archivo .ico (o presione Enter para omitir): ").strip()

    # Solicitar al usuario el nombre del ejecutable
    nombre_exe = input("Ingrese el nombre del ejecutable (sin la extensión .exe): ")

    # Comando completo como lista de argumentos
    comando = [ruta_yuzu, '-f', '-g', ruta_nsp]

    # Contenido del nuevo archivo .py que ejecutará el comando
    nuevo_codigo = f"""
import subprocess
import os
import sys

comando = {comando}

# Ejecutar el comando sin mostrar la consola en sistemas Windows
if sys.platform.startswith('win'):
    si = subprocess.STARTUPINFO()
    si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    subprocess.Popen(comando, startupinfo=si, creationflags=subprocess.CREATE_NO_WINDOW)
else:
    subprocess.Popen(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
"""

    #Nombre script
    nombre_script = 'nps_to_exe_script.py'

    # Codificación que deseas utilizar (por ejemplo, 'utf-8')
    codificacion = 'utf-8'

    # Escribir el contenido en el nuevo archivo con la codificación especificada
    with open(nombre_script, "w", encoding=codificacion) as archivo:
        archivo.write(nuevo_codigo)

    # Crear el archivo .exe con pyinstaller
    comando_pyinstaller = f'pyinstaller --onefile --noconsole --icon={ruta_ico} --distpath="{ruta_exe}" --name="{nombre_exe}" --clean "{nombre_script}"'

    subprocess.run(comando_pyinstaller)

    # Eliminar archivos residuos generados por PyInstaller
    archivos_residuos = [nombre_script[:-3] + ext for ext in (".spec", ".pyc", ".log", ".py")]
    for archivo in archivos_residuos:
        try:
            os.remove(archivo)
        except FileNotFoundError:
            pass

    
    # Eliminar archivo .spec
    try:
        nombre_ejecutable = f"{nombre_exe}.exe"
        os.remove(f"{nombre_ejecutable[:-4]}.spec")
    except FileNotFoundError:
        pass

    # Eliminar la carpeta __pycache__
    try:
        shutil.rmtree("__pycache__", ignore_errors=True)
    except FileNotFoundError:
        pass

    # Eliminar carpetas generadas por PyInstaller
    carpetas_pyinstaller = ["build", "dist"]
    for carpeta in carpetas_pyinstaller:
        try:
            shutil.rmtree(carpeta, ignore_errors=True)
        except FileNotFoundError:
            pass

# Función para mostrar el menú dentro de una caja
def mostrar_menu():
    print("╔══════════════════════════════════════╗")
    print("║  Menú Principal - Convert NSP to Exe ║")
    print("╠══════════════════════════════════════╣")
    print("║ 1. Crear ejecutable                  ║")
    print("║ 2. Modificar rutas                   ║")
    print("║ 3. Salir                             ║")
    print("╚══════════════════════════════════════╝")

# Menú principal
if __name__ == "__main__":
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            # Crear ejecutable
            ruta_yuzu, ruta_exe = obtener_rutas()
            crear_ejecutable(ruta_yuzu, ruta_exe)
        elif opcion == '2':
            # Modificar rutas
            ruta_yuzu = input("Ingrese la nueva ruta al ejecutable yuzu.exe (usar comillas si hay espacios o caracteres especiales): ")
            ruta_exe = input("Ingrese la nueva ruta donde desea guardar los archivos .exe (usar comillas si hay espacios o caracteres especiales): ")

            # Guardar las nuevas rutas en el archivo de configuración
            guardar_rutas(ruta_yuzu, ruta_exe)
        elif opcion == '3':
            # Salir del programa
            break
        else:
            print("Opción no válida. Intente de nuevo.")
