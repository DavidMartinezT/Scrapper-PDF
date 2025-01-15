# Scrapper PDF to excel
## Description
Este programa convierte un archivo PDF a un archivo excel extrayendo de cada PDF los datos que son necesarios.


## Clonar repositorio
Para clonar el repositorio se debe ejecutar el siguiente comando:

```bash
git clone https://github.com/jhsilvaz13/PDF-scrapper-re.git
```

Asegurese de moverse a la carpeta raiz del proyecto para ejecutar los comandos.

```bash
cd PDF-scrapper-re
```

## Dependencias
Para instalar las dependencias se debe ejecutar el siguiente comando:

```bash
pip install -r requirements.txt
```

## Ejecución
Para ejecutar el programa se debe tener instalado python 3.7 o superior y ejecutar el siguiente comando:

```bash
python main.py
```

Recuerde que el programa solicita el nombre del archivo PDF que desea convertir a excel, el archivo con el mismo nombre debe estar en la carpeta **source/OS**. donde OS se refieres al sistema operativo al que pertenece el archivo PDF, puede ser **Windows** o **Linux** o **Mac**.

## Resultados

Los resultados se encuentran en la carpeta **output** con el nombre del archivo PDF que se convirtió a excel. Dependiendo si se decidio traducir los datos el nombre del archivo excel tendra el sufijo **_es** o **_en**. Las carpetas **output/extracted** y **output/clean** contienen archivos excel intermedios puede ignorarlos. Por ejemplo si se selecciono el archivo **Windows.pdf** y se decidio traducir los datos el resultado se encontrara en el archivo **output/Windows_es.xlsx**.

## Importante
Recuerde estar siempre en la carpeta raiz del proyecto para ejecutar los comandos.