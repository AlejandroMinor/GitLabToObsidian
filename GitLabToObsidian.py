import gitlab
import os
from datetime import date
import re

class gitLabtoObsidian:
    ## Constructor
    def __init__(self):
        
        # Verificar si existe el archivo data.txt
        if not os.path.exists('data.txt'):
            print("No existe el archivo de configuración data.txt. Se crearán los datos por defecto")
            with open('data.txt', 'w') as f:
                f.write(f"url,default \n")
                f.write(f"token,default \n")
                f.write(f"path,default \n")
                f.write(f"issue_url,default\n")            
        
        # Inicializar las variables
        self.url = ""
        self.token = ""
        self.path = ""
        self.issue_url = ""
        self.upload_url = ""

        # Leer el archivo data.txt
        try:
            with open('data.txt', 'r') as f:
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
                        
        except FileNotFoundError:
            print("El archivo data.txt no se encuentra.")
        except Exception as e:
            print("Error al leer el archivo data.txt:", str(e))

        self.createFile()

    def createFile(self):
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
        titulo_limpio = issue.title.replace("/", "").replace(":", "")
        nombre_archivo = f"{numero_issue} {titulo_limpio}.md"
        fecha = date.today()
        descripcion = self.remove_markdown_formatting(issue.description)
        # Definir contenido del archivo
        contenido = f"""
## #{numero_issue}  {issue.title}
[[Issue]]
Asingado: 📅 [[{fecha}]]
Estatus: [[🔄 En desarrollo]] |  📅 Fecha finalización
URL GitLab: {self.issue_url}{numero_issue}
#### Información 

{descripcion}

#### Codigo para resolver


Ruta ODOO:


Ruta a programar : `ruta`


A partir de la linea:  

Codigo

```Python
```

#### Commit 

```shell
git commit -m "[CHANGE] Contexto programador" -m "Para analistas #NUMISSUE"
```

#### Comentarios
- 1

#### Analista: {issue.author['name']}

        """

        # Definir la ruta del archivo
        ruta = self.path + nombre_archivo

        # Escribir el archivo
        try:
            directorio = os.path.dirname(ruta)
            with open(ruta, "w") as archivo:
                archivo.write(contenido)
            print("Archivo escrito exitosamente en:", ruta)
        except Exception as e:
            print("Error al escribir el archivo:", e)



    def remove_markdown_formatting(self,text):
        # Remover los enlaces en formato [texto](url)
        #text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
        
        # Remover los énfasis en formato *texto* o _texto_
        #text = re.sub(r'(\*|_)(.*?)\1', r'\2', text)
        
        # Remover los encabezados en formato # Encabezado
        text = re.sub(r'#+\s+(.*?)\s*(?:\n|$)', r'\1', text)
        
        # Remover las listas en formato * elemento o 1. elemento
        #text = re.sub(r'^\s*([\*\-]|(?:\d+\.))\s+', '', text, flags=re.MULTILINE)
        
        # Remover las líneas horizontales en formato --- o ***
        #text = re.sub(r'^\s*[-*_]{3,}\s*$', '', text, flags=re.MULTILINE)
        
        # cambiar la palabra /uploads/ por la url del servidor de carga de archivos
        text = re.sub(r'/uploads/', rf'{self.upload_url}', text)

        return text


## Inicializar la clase y crear el archivo
init = gitLabtoObsidian
init()