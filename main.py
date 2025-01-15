from core.extract import Extract
from core.clean import Clean
from core.load import Load

def main():
    FILE=""
    while(FILE==""):
        print("Inserte el nombre del archivo:")
        FILE=input()
    ANSWER=""
    while(ANSWER!="y" and ANSWER!="n"):
        print("¿Desea traducir el archivo? (y/n)")
        ANSWER=input()

    Extract(FILE).extraer()
    Clean(FILE).limpiar()
    Load(FILE, "es").cargar() if ANSWER=="y" else Load(FILE, "en").cargar()

if __name__ == '__main__':
    main()