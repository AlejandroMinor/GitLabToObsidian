import gitlab
import os
from datetime import date
import re

class gitLabtoObsidian:
    ## Constructor
    def __init__(self):
        
        # Inicializar las variables
        self.url = ""
        self.token = ""
        self.path = ""
        self.issue_url = ""
        self.upload_url = ""
        self.issue_list = ""
        self.project_id = ""

        # Verificar si existe el archivo config.txt
        self.configuration_file = 'config.txt'
        if not os.path.exists(self.configuration_file):
            print("No existe el archivo de configuración config.txt. Se crearán los datos por defecto")
            self.create_data(self.configuration_file)        

        # Leer el archivo config.txt
        self.load_settings(self.configuration_file)

        self.main_menu()

    def connect(self):
        # Configurar la conexión con GitLab
        try:
            self.gl = gitlab.Gitlab(self.url, private_token=self.token)
                    # Obtener información de un repositorio
            project_id = self.project_id  # ID del repositorio en GitLab
            self.repo = self.gl.projects.get(project_id)
        except Exception as e:
            print("Error al conectar con GitLab:", e)
            print("\n Error al conectar con GitLab. Verifique los datos en el archivo config.txt \n")
            self.show_data()
            response = input("Desea crear un nuevo archivo de configuración? (s/n)")
            if response.lower() == "s":
                self.create_data(self.configuration_file)
            else:
                self.main_menu()


    def main_menu(self):
        print("\n\nSeleccione una opción:")
        print("1. Crear archivo")
        print("2. Configurar datos")
        print("3. Ver datos")
        print("0. Salir")
        option = input("====> ")
        if option == "1":
            self.create_file()
        elif option == "2":
            self.create_data(self.configuration_file)
        elif option == "3":
            self.show_data()
            self.main_menu()
        elif option == "0":
            exit()

    def create_file(self):

        self.connect()
        
        repo = self.repo

        print("\n\nxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
        print("Nombre del repositorio:", repo.name)
        print("Descripción del repositorio:", repo.description)
        print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx \n\n")

        numero_issue = input("====> Ingrese el número del issue: ")
        print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx \n\n")

        try:
            issue = repo.issues.get(numero_issue)
            print("Información del issue:")
            print("Título:", issue.title)
            print("Descripción:", issue.description)
            print("Autor:", issue.author['name'])
            print("Fecha de creación:", issue.created_at)
        
            # Pregunta si quiere crear el archivo
            crear_archivo = input("\n\n\n¿Desea crear el archivo? (s/n): ")
            if crear_archivo.lower() != "s":
                print("No se realizaron cambios")
                exit()

        except gitlab.exceptions.GitlabGetError as e:
            print("Error al obtener la información del issue:", e)
            raise ValueError(f"Ocurrió un error: {e}")


        # Definir parametros para el archivo
        titulo_limpio = issue.title.replace("/", " ").replace(":", " ")
        # Quitar doble espacio de la cadena de titulo_limpio
        while "  " in titulo_limpio:
            titulo_limpio = titulo_limpio.replace("  ", " ")
        
        nombre_archivo = f"{numero_issue} {titulo_limpio}.md"
        fecha = date.today()
        descripcion = self.remove_markdown_formatting(issue.description)
        # Definir contenido del archivo
        contenido = f"""## #{numero_issue}  {issue.title}
[[Issue]]
Asignado: 📅 [[{fecha}]]
Estatus: [[🔄 En desarrollo]] |  📅 Fecha finalización
URL GitLab: {self.issue_url}{numero_issue}
#### Información 

{descripcion}

#### Código para resolver



#### Commit 

```shell
git commit -m "[CHANGE] #{numero_issue} Contexto programador" -m "#{numero_issue} Contexto Para analistas"
```

#### Comentarios
- 1

#### Analista: {issue.author['name']}
"""

        # Definir la ruta del archivo
        ruta = self.path + nombre_archivo

        # Escribir el archivo
        try:
            with open(ruta, "w") as archivo:
                archivo.write(contenido)
            print("Archivo escrito exitosamente en:", ruta)

            self.add_to_issue_list(self.issue_list, numero_issue+" "+titulo_limpio)
        except Exception as e:
            print("Error al escribir el archivo:", e)

    def remove_markdown_formatting(self,text):
        
        # Remover los encabezados en formato # Encabezado
        text = re.sub(r'#+\s+(.*?)\s*(?:\n|$)', r'\1', text)
                
        # cambiar la palabra /uploads/ por la url del servidor de carga de archivos
        text = text.replace('/uploads/', self.upload_url)


        return text
    
    def add_to_issue_list(self,archivo, texto):
        with open(archivo, 'r+') as file:
            lines = file.readlines()

            # Buscar la última línea no vacía
            for i in range(len(lines) - 1, -1, -1):
                if lines[i].strip():
                    last_line_index = i
                    break

            # Agregar el texto en la siguiente línea
            texto = f"\n- [[{texto}]]"
            lines.insert(last_line_index + 1, texto)

            # Sobreescribir el archivo con las líneas modificadas
            file.seek(0)
            file.writelines(lines)
            file.truncate()

    def create_data(self, path_name):
        field_defaults = {
            "url": self.url,
            "token": self.token,
            "path": self.path,
            "issue_url": self.issue_url,
            "upload_url": self.upload_url,
            "issue_list": self.issue_list,
            "project_id": self.project_id,
        }

        with open(path_name, 'w') as f:
            while True:
                print("Ingrese los datos para configurar el programa. Deje el campo vacío para mantener el valor actual.")
                for field, default_value in field_defaults.items():
                    user_input = input(f"Ingrese {field.replace('_', ' ')} [{default_value}]: ")
                    #value = user_input if user_input != "" else default_value
                    if user_input != "":
                        value = user_input
                    else:
                        value = default_value

                    f.write(f"{field},{value}\n")

                response = input("Datos correctos? (s/n): ")
                if response.lower() == "s":
                    break

        
    def load_settings(self,path_name):
        try:
            with open(path_name, 'r') as f:
                for line in f:
                    parts = line.split(',')
                    if line.startswith('url'):
                        self.url = parts[1].strip()
                    elif line.startswith('token'):
                        self.token = parts[1].strip()
                    elif line.startswith('path'):
                        self.path = parts[1].strip()
                    elif line.startswith('issue_url'):
                        self.issue_url = parts[1].strip()
                    elif line.startswith('upload_url'):
                        self.upload_url = parts[1].strip()
                    elif line.startswith('issue_list'):
                        self.issue_list = parts[1].strip()
                    elif line.startswith('project_id'):
                        self.project_id = parts[1].strip()
            print(f"Configuración cargada del archivo {path_name}")
                        
        except FileNotFoundError:
            print("El archivo config.txt no se encuentra.")
        except Exception as e:
            print("Error al leer el archivo config.txt:", str(e))

    def show_data(self):
        self.load_settings(self.configuration_file)
        print("""\n Datos de configuración:""")
        print("URL:", self.url)
        print("Token:", self.token)
        print("Path:", self.path)
        print("Issue URL:", self.issue_url)
        print("Upload URL:", self.upload_url)
        print("Issue List:", self.issue_list)
        print("Project ID:", self.project_id)