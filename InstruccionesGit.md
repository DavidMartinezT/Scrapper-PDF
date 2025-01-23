# Instrucciones para Gestionar Repositorio Git

## 1. Crear un Repositorio Local
1. Abre tu terminal o línea de comandos.
2. Navega al directorio donde deseas crear el repositorio:
    ```bash
    cd <ruta_del_directorio>
    ```
3. Inicializa un nuevo repositorio Git:
    ```bash
    git init
    ```

## 2. Conectar Repositorio Local con Repositorio Remoto
1. Copia la URL del repositorio remoto (por ejemplo, de GitHub).
2. Agrega el repositorio remoto a tu repositorio local:
    ```bash
    git remote add origin <URL_del_repositorio>
    ```

3. Verifica que se haya agregado correctamente:
    ```bash
    git remote -v
    ```

## 3. Obtener Ramas del Repositorio Remoto
1. Obtén las ramas del repositorio remoto:
    ```bash
    git fetch origin
    ```

## 4. Configurar Ramas para Seguimiento
1. Para la rama `main`:
    ```bash
    git branch --set-upstream-to=origin/main main
    ```
2. Para la rama `scrapperweb`:
    ```bash
    git branch --set-upstream-to=origin/scrapperweb scrapperweb
    ```

## 5. Cambiar entre Ramas
1. Cambiar a la rama `main`:
    ```bash
    git checkout main
    ```
2. Cambiar a la rama `scrapperweb`:
    ```bash
    git checkout scrapperweb
    ```

## 6. Sincronizar Ramas con Repositorio Remoto
1. Para actualizar la rama `main`:
    ```bash
    git pull origin main
    ```
2. Para actualizar la rama `scrapperweb`:
    ```bash
    git pull origin scrapperweb
    ```

## 7. Solución del Error: "couldn't find remote ref scrapperweb"
1. Verifica las ramas en el repositorio remoto:
    ```bash
    git ls-remote --heads origin
    ```
2. Si la rama `scrapperweb` no aparece en el repositorio remoto:
    - Crea la rama en tu repositorio local:
    ```bash
    git checkout -b scrapperweb
    ```
    - Sube la rama al repositorio remoto:
    ```bash
    git push origin scrapperweb
    ```

## 8. Configurar Seguimiento de Ramas Remotas
1. Configura la rama local `scrapperweb` para seguir a la rama remota:
    ```bash
    git branch --set-upstream-to=origin/scrapperweb scrapperweb
    ```

## 9. Actualizar Ramas Locales y Remotas
1. Asegúrate de estar en la rama que quieres actualizar:
    ```bash
    git checkout scrapperweb
    ```

2. Haz los cambios necesarios en tu código local.

3. Añade los cambios al área de preparación:
    ```bash
    git add .
    ``
4. Confirma los cambios:
    ```bash
    git commit -m "Descripción de los cambios"
    ``
5. Envía los cambios al repositorio remoto:
    ```bash
    git push origin scrapperweb

 