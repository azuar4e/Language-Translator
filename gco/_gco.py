#________________________________________________________________________
#imports 
import sys
import subprocess
# import re
from _ens import escribir
import _segundapasada
import _primerapasada

#________________________________________________________________________
# resto de variables
archivo = None

#________________________________________________________________________
# funciones

def leer():
    global archivo
    if archivo is None:
        archivo = open(sys.argv[1], 'r')
        
    return archivo.readline()           
            
#________________________________________________________________________
# main

def main():
    # linea = leer()

    # escribimos la cabecera para el fichero de codigo objeto
    # tenemos que hacer una primera pasada para dar valor a etiquetas
    # registros de activacion etc etc para que en la segunda ya conozcamos 
    # las direcciones de memorial, los tamaños, etc
    # ver si hay alguna informacion que nos pueda indicar que el return esta
    # en la funcion principal, y si no implementarlo porque no parece q aurora
    # tenga mucha idea y puede haber mas de un return, por ejemplo dentro de un if
    
    # las palabras son de 16 bits

    cabecera_ens = "InicioEstaticas: RES 200\n"
    cabecera_ens += "Pila: NOP\n"
    cabecera_ens += "MOVE #InicioEstaticas, .IY\n"
    cabecera_ens += "MOVE #Pila, .IX\n"

    escribir(cabecera_ens)
 
    # primera vuelta
    # hay que generar una tabla de etiquetas, de errores y de referencias adelantadas
    # esto lo leera en la segunda pasada y se generara una lista de errores y 
    # el codigo maquina
    
    _primerapasada.main()
    archivo = None    
    
    # para la segunda vuelta hacemos esto aunque igual es mejor hacerlo directamente
    # en el main en lugar de usar una funcion auxiliar
    _segundapasada.main() # va a haber que modificarlo evidentemente
    # añadir que lea de los archivos generados en la primera pasada
    # y modificar el codigo maquina que no esta del todo bien
    # habria que ver si hay un cuarteto de etiqueta con etiqueta de funcion o de procedimiento
            

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("\n[+] ERROR: No se ha pasado ningun archivo de entrada.\n")
        exit(1)
 
    comando = ["java", "-jar", "../tdl/target/tdl-1.0-SNAPSHOT-jar-with-dependencies.jar", sys.argv[1]]
 
    try:
 
        # ejecuta el comando del pdl que genera los ficheros de salida
        resultado = subprocess.run(comando, capture_output=True, text=True, check=True)
        print(f"\nComando: {' '.join(comando)}")
        print(f"\n✔ Código de retorno: {resultado.returncode}")
        print(f"\n➜ Salida:\n{resultado.stdout.strip() or 'No hubo salida.'}")
 
    except subprocess.CalledProcessError as e:
 
        print(f"\nComando fallido: {' '.join(e.cmd)}")
        print(f"✘ Código de retorno: {e.returncode}")
        print(f"⚠️  Error:\n{e.stderr.strip() or 'No hubo errores.'}")
  
    main()