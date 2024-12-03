import os
import shutil

# Rutas de los archivos
backup_dir = "backend/app/services/backup"
mod_file = "backend/modifications/services/document_analysis_service.py"
target_file = "backend/app/services/document_analysis_service.py"

# Crear carpeta de respaldo si no existe
os.makedirs(backup_dir, exist_ok=True)
backup_file = os.path.join(backup_dir, "document_analysis_service.py")

def replace_file():
    """Reemplaza el archivo objetivo con el archivo modificado."""
    if not os.path.exists(mod_file):
        print("El archivo modificado no existe.")
        return

    # Crear un respaldo del archivo original
    if os.path.exists(target_file):
        shutil.copy2(target_file, backup_file)
        print(f"Respaldo creado en {backup_file}.")
    else:
        print("El archivo original no existe, no se creó un respaldo.")

    # Reemplazar el archivo
    shutil.copy2(mod_file, target_file)
    print(f"El archivo {target_file} ha sido reemplazado con la versión modificada.")

def revert_changes():
    """Restaura el archivo original desde el respaldo."""
    if not os.path.exists(backup_file):
        print("No hay respaldo disponible para revertir.")
        return

    # Restaurar el archivo desde el respaldo
    shutil.copy2(backup_file, target_file)
    print(f"El archivo original ha sido restaurado desde el respaldo.")
    # Opcional: eliminar el archivo de respaldo después de revertir
    os.remove(backup_file)
    print("El respaldo ha sido eliminado.")

# Menú interactivo
def main():
    while True:
        print("\nSeleccione una opción:")
        print("1. Reemplazar archivo")
        print("2. Revertir cambios")
        print("3. Salir")
        choice = input("Ingrese su elección: ")

        if choice == "1":
            replace_file()
        elif choice == "2":
            revert_changes()
        elif choice == "3":
            print("Saliendo...")
            break
        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    main()
