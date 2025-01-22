import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configuración de Selenium
def configure_browser():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    return driver

# Función para buscar archivos usando la casilla de búsqueda
def buscar_archivo(driver, query):
    try:
        # Esperar la presencia de la casilla de búsqueda
        search_box = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/div[2]/div/div/div[2]/div/form/div/input[1]"))
        )

        # Escribir la consulta en la casilla de búsqueda y presionar Enter
        search_box.clear()
        search_box.send_keys(query)
        search_box.submit()

        # Esperar a que la tabla de resultados esté cargada
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/div[2]/div/div/div[3]/div/section/table"))
        )

        # Listar los resultados de la búsqueda
        filas = driver.find_elements(By.XPATH, "/html/body/div[1]/div[2]/div[2]/div/div/div[3]/div/section/table/tbody/tr")
        archivos = []
        for i, fila in enumerate(filas, start=1):
            nombre = fila.find_element(By.XPATH, "td[1]").text
            version = fila.find_element(By.XPATH, "td[2]").text
            archivos.append((i, nombre, version))
            print(f"{i}. {nombre} - {version}")

        # Retornar los resultados
        return filas, archivos
    except Exception as e:
        print(f"Error al buscar el archivo: {e}")
        return None, []

# Función para seleccionar un archivo de la lista
def seleccionar_archivo(driver, filas, archivos):
    try:
        # Pedir al usuario que seleccione un archivo
        seleccion = int(input("\nSelecciona el número del archivo que deseas (por ejemplo, 1): "))
        if seleccion < 1 or seleccion > len(archivos):
            print("Selección inválida. Intenta nuevamente.")
            return False

        # Hacer clic en el archivo seleccionado
        archivo_seleccionado = filas[seleccion - 1].find_element(By.XPATH, "td[1]/a")
        archivo_seleccionado.click()

        print(f"\nIngresando a: {archivos[seleccion - 1][1]} - {archivos[seleccion - 1][2]}")
        return True
    except Exception as e:
        print(f"Error al seleccionar el archivo: {e}")
        return False

# Función para extraer información de "1 - Account Policies"
def extraer_account_policies(driver):
    try:
        # Esperar a que esté presente el elemento "1 - Account Policies"
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/div[1]/div[2]/div/div[2]/div/div[1]/p/a"))
        )

        # Ubicar el elemento y extraer su texto
        elemento_account_policies = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[1]/div[2]/div/div[2]/div/div[1]/p/a")
        texto_account_policies = elemento_account_policies.text.strip()

        print("\nInformación extraída de '1 - Account Policies':")
        print(texto_account_policies)

        return texto_account_policies
    except Exception as e:
        print(f"Error al extraer '1 - Account Policies': {e}")
        return None

# Proceso principal
if __name__ == "__main__":
    try:
        # Configuración del navegador
        driver = configure_browser()
        driver.get("https://workbench.cisecurity.org/benchmarks?status=published&sortBy=version&type=desc")

        print("Por favor, inicia sesión manualmente en el navegador.")
        input("Presiona Enter una vez que hayas iniciado sesión y estés en la página inicial: ")

        # Pedir al usuario el nombre o parte del nombre del archivo que desea buscar
        query = input("Introduce el nombre o parte del nombre del archivo que deseas buscar: ")

        # Buscar archivos que coincidan con la consulta
        filas, archivos = buscar_archivo(driver, query)

        # Verificar si hay resultados
        if not archivos:
            print("No se encontraron resultados para la búsqueda.")
        else:
            # Seleccionar un archivo de la lista
            if seleccionar_archivo(driver, filas, archivos):
                # Extraer información de "1 - Account Policies"
                extraer_account_policies(driver)

    except Exception as e:
        print(f"Se produjo un error en el proceso: {e}")

    finally:
        driver.quit()
