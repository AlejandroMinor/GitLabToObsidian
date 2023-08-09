import gitlab
import os
from datetime import date
import re

class gitLabtoObsidian:
    ## Constructor
    def __init__(self):
        
        # Verificar si existe el archivo data.txt
        path_name= 'data.txt'
        if not os.path.exists(path_name):
            print("No existe el archivo de configuración data.txt. Se crearán los datos por defecto")
            self.create_data(path_name)        
        
        # Inicializar las variables
        self.url = ""
        self.token = ""
        self.path = ""
        self.issue_url = ""
        self.upload_url = ""
        self.issue_list = ""

        # Leer el archivo data.txt
        self.load_settings(path_name)

        self.create_file()

    def create_file(self):
        # Configurar la conexión con GitLab
        gl = gitlab.Gitlab(self.url, private_token=self.token)

        # Obtener información de un repositorio
        project_id = 41  # ID del repositorio en GitLab
        repo = gl.projects.get(project_id)

        print("\n\nxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
        print("Nombre del repositorio:", repo.name)
        print("Descripción del repositorio:", repo.description)
        print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx \n\n")

        numero_issue = input("====> Ingrese el número del issue: ")
        print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx \n\n")

        try:
            issue = repo.issues.get(numero_issue)
            users = issue.participants()

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
Asingado: 📅 [[{fecha}]]
Estatus: [[🔄 En desarrollo]] |  📅 Fecha finalización
URL GitLab: {self.issue_url}{numero_issue}
#### Información 

{descripcion}

#### Código para resolver


Ruta ODOO:


Ruta a programar : `ruta`


A partir de la linea:  

Código

```python
```

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

            self.add_to_issue_list("/home/minor/Documentos/Cerebro/👨‍💻 Issues/Issue.md", numero_issue+" "+titulo_limpio)
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

    def create_data(self,path_name):
        with open(path_name, 'w') as f:
            url_default=input("Ingrese la url del repositorio: ")
            token_default=input("Ingrese el token del repositorio: ")
            path_default=input("Ingrese la ruta donde se creará el archivo: ")
            issue_url_default=input("Ingrese la url para issues en gitlab: ")
            issue_upload_url_default=input("Ingrese la url para subir archivos en gitlab: ")
            issue_list_default=input("Ingrese la ruta del archivo donde se guardará la lista de issues: ")
            f.write(f"url,{url_default} \n")
            f.write(f"token,{token_default} \n")
            f.write(f"path,{path_default} \n")
            f.write(f"issue_url,{issue_url_default}\n")
            f.write(f"upload_url,{issue_upload_url_default}\n")
            f.write(f"issue_list,{issue_list_default}")
        
    def load_settings(self,path_name):
        try:
            with open(path_name, 'r') as f:
                for line in f:
                    parts = line.split(',')
                    if line.startswith('url') and len(parts) == 2:
                        self.url = parts[1].strip()
                    elif line.startswith('token') and len(parts) == 2:
                        self.token = parts[1].strip()
                    elif line.startswith('path') and len(parts) == 2:
                        self.path = parts[1].strip()
                    elif line.startswith('issue_url') and len(parts) == 2:
                        self.issue_url = parts[1].strip()
                    elif line.startswith('upload_url') and len(parts) == 2:
                        self.upload_url = parts[1].strip()
                    elif line.startswith('issue_list') and len(parts) == 2:
                        self.issue_list = parts[1].strip()
                        
        except FileNotFoundError:
            print("El archivo data.txt no se encuentra.")
        except Exception as e:
            print("Error al leer el archivo data.txt:", str(e))
