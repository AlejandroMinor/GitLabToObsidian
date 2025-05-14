# GitLabToObsidian

GitLabToObsidian es una herramienta que te permite crear archivos en formato Markdown en tu repositorio de Obsidian a partir de los issues de GitLab.

## Descripción

Este proyecto automatiza el proceso de creación de archivos Markdown en Obsidian basados en los issues de GitLab. Los archivos creados contienen información relevante del issue, como el título, la descripción, el autor y más.
El archivo generado en markdown tiene una estructura que uso en mis notas. Tienes la libertad de acomodarlo segun tus necesidades. 
Al crear un archivo con esta herramienta se agreagra a un listado de issues. El listado de issues es un archivo que uso para poder visualizar todos los issues que he realizado en un periodo de tiempo. Se recomienda el crear uno de estos para su mejor control. 

El script utiliza la biblioteca `python-gitlab` para interactuar con la API de GitLab y obtener la información del issue. Luego, genera un archivo Markdown con un formato predefinido, incluyendo detalles como el número del issue, el título, la descripción y más. El archivo se guarda en la ruta especificada en la configuración.


## Dependencias

- Python 3.x
- GitLab Python Library (python-gitlab)

## Instalación

1. Asegurate de tener tu api key de GitLab activa 
2. Instala las dependencias ejecutando el siguiente comando:

```shell
pip install python-gitlab
```

3. Configura los datos de conexión en el archivo `config.txt`.
Ejemplo:
```
url,http://192.168.29.74:8091
token,glTESTcM7
path,/home/minor/Documentos/Minor/👨‍💻 Issues/
issue_url,http://URL/-/issues/
upload_url,http://URL/uploads/
issue_list,/home/minor/Documentos/Minor/👨‍💻 Issues/Issue.md
project_id,41
```

## Tutorial

1. Ejecuta el script `GitLabToObsidian.py`.
```shell
python3 GitLabToObsidian.py
```
2. Ingresa el número del issue que deseas convertir en un archivo Markdown.
2. Revisa la información del issue que se muestra en la consola.
3. Confirma si deseas crear el archivo correspondiente.
4. El archivo Markdown se creará en la ubicación especificada en la configuración.
5. Verifica el archivo en Obsidian y realiza las modificaciones necesarias.
