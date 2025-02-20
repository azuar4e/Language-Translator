#_________________________________
#imports
import sys
import subprocess

#_________________________________
#variables
archivo = None
edt = {
    #cuando este completa la edt, 
    # ponerla en formato clave valor, 
    # imagino que habra q hacer los firsts y esas bainas
}

#_________________________________
#funciones
def leer() -> str:
    global archivo
    if archivo is None:
        archivo = open(sys.argv[1], "r")
        
def emite(operador, arg1, arg2, resultado) -> None:
    return 


def main():
    return

if __name__=='__main__':
    if len(sys.argv) < 2:
        print("\n[+] ERROR: No se ha pasado ningun archivo de entrada.\n")
        exit(1)

    comando = ["java", "-jar", "PBoreal.jar", sys.argv[1]]
    try:
        resultado = subprocess.run(comando, capture_output=True, text=True, check=True)

        print(f"\nComando: {' '.join(comando)}")
        print(f"\n✔ Código de retorno: {resultado.returncode}")
        print(f"\n➜ Salida:\n{resultado.stdout.strip() or 'No hubo salida.'}")

    except subprocess.CalledProcessError as e:
        print(f"\nComando fallido: {' '.join(e.cmd)}")
        print(f"✘ Código de retorno: {e.returncode}")
        print(f"⚠️  Error:\n{e.stderr.strip() or 'No hubo errores.'}")
        
    main()