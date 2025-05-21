from _ens import escribir
from pprint import pprint
import re

#______________________________________________________________
# variables
archivo = None
globales = r"TABLA PRINCIPAL #\d:"
locales = r"TABLA LOCAL #\d+:"
lexema = r"\*LEXEMA: '(.+)'"
tipo = r"\s+\+ Tipo: '(.+)'"
parametro = r"\s+\+ TipoParam\d: '(.+)'"
retorno = r"\s+\+ TipoRetorno: '(.+)'"
ras = 1
coleccion = {}
separador = "----------------------------------------"


def leer():
    global archivo
    if archivo is None:
        archivo = open("ts.txt", 'r')
        
    return archivo.readline() 

def reserva(tipo) -> int:
    if tipo == 'entero':
        return 4
    elif tipo == 'logico':
        return 1
    elif tipo == 'cadena':
        return 64
    else:
        return 0

# calculamos el tamaño a reservar para los datos estaticos y el tamaño de cada RA
def main():
    linea = leer()
    tamestaticos = 0
    ras = 1

    while linea:
        if re.match(locales, linea):
            coleccion[f"ra{ras}"] = {}
            desp = 1
            while linea.strip() != separador.strip():
                if re.match(lexema, linea):
                    while not re.match(tipo, linea):
                        linea = leer()
                    desp += reserva(re.match(tipo, linea).group(1))
                linea = leer()

            coleccion[f"ra{ras}"] = desp
            ras+=1

        if re.match(globales, linea):
            rasaux = 1
            while linea:
                if re.match(lexema, linea):
                    while not re.match(tipo, linea):
                        linea = leer()
                    t = re.match(tipo, linea).group(1)
                    if t != 'funcion' and t != 'procedimiento':
                        tamestaticos += reserva(t)

                    else:
                        while not re.match(retorno, linea):
                            linea = leer()

                        aux = coleccion[f"ra{rasaux}"]
                        aux += reserva(re.match(retorno, linea).group(1))

                        # pprint(coleccion)
                        coleccion[f"ra{rasaux}"] = aux
                        rasaux += 1

                linea = leer()
            break # para salir del bucle principal q sino lee otra linea y dara error

        linea = leer()

    escribir("\t\t\tinicio_pila: NOP\n")
    escribir(f"\t\t\tinicio_estaticas: RES {tamestaticos}\n")
    escribir("\t\t\tMOVE #inicio_estaticas, .IY\n")
    escribir("\t\t\tMOVE #inicio_pila, .IX\n")
    
    # generamos las etiquetas para los registros de activacion
    for ra in coleccion:
        escribir(f"\t\t\t{ra}: EQU {coleccion[ra]}\n")


if __name__=='__main__':
    main()