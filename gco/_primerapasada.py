from _ens import escribir
import re

#______________________________________________________________

archivo = None
globales = r"TABLA PRINCIPAL #\d:"
locales = r"TABLA LOCAL #\d:"
lexema = r"\*LEXEMA: '(.+)'"
tipo = r"\s+\+ Tipo: '(.+)'"
parametro = r"\s+\+ TipoParam\d: '(.+)'"
retorno = r"\s+\+ TipoRetorno: '(.+)'"
ras = 1
coleccion = {}
# estructura general algo como:
# {ra1: DE: a: desp
#         b: desp
#     temp: t0: desp
#     param: param1: desp
#     ...
# ra2: ...}
separador = "----------------------------------------"

def leer():
    global archivo
    if archivo is None:
        archivo = open("../tdl/ts.txt", 'r')
        
    return archivo.readline() 

def reserva(tipo) -> int:
    if tipo == 'entero':
        return 1
    elif tipo == 'logico':
        return 1
    else:
        return 64

def main():
    linea = leer()
    # info de los registros de activacion
    info_de = "inicio_estaticos:\n" # para las globales
    tamestaticos = 0

    while linea:
        if re.match(linea, globales):
            ras = 1
            linea = leer()
            while linea:
                if re.match(linea, lexema):
                    c = re.match(linea, lexema).group(1)
                    while not re.match(linea, tipo):
                        linea = leer()
                    t = re.match(linea, tipo).group(1)
                    if t != 'funcion':
                        info_de += "\tdata "+c+"\n"
                        tamestaticos += reserva(t)
                    else:
                        tam = 0
                        coleccion["ra"+ras]["parametros"] = {}
                        #calcular la reserva de espacio para parametros y retorno
                        param = 0
                        desp = 3
                        while re.match(linea, parametro):
                            # mas tres porque las primeras 3 palabras son PC PA y EM
                            coleccion["ra"+ras]["parametros"][param] = desp
                            desp += reserva(re.match(linea, parametro).group(1))
                            linea = leer()
                            param+=1
                        
                        while not re.match(linea, retorno):
                            linea = leer()
                        # guardamos el tipo de retorno para q para poder acceder a el solo haya q calcular su tamaño
                        # via total - reserva(tipo)
                        aux = re.match(linea, retorno)
                        coleccion["ra"+ras]["retorno"] = aux
                        des += reserva(re.match(linea, retorno))
                        coleccion["ra"+ras]["total"] = des
                        ras += 1
    
                linea = leer()
            break 
        # la tabla principal es la ultima por lo q cuando se acabe se acaba la pasada
        linea = leer()

    # repetimos el bucle pero para las tablas locales, de este modod porque los params
    # estan antes q datos estaticos y temporales en el ra y sino no se calcula bn los desplazamientos
    # el valor devuelto da igual porque como esta al final sera lo q ocupe el ra - 1

    archivo = None
    linea = leer()
    ras = 1
    while not re.match(linea, globales):
        if re.match(linea, locales):
            total = coleccion["ra"+ras]["total"]
            total -= reserva(coleccion["ra"+ras]["retorno"])
            # le restamos al total el retorno q va incluido para saber a partir de q dir van los de

            while linea != separador:
                if re.match(linea, lexema):
                    c = re.match(linea, lexema).group(1)
                    while not re.match(linea, tipo):
                        linea = leer()

                    t = re.match(linea, tipo)
                    if c.startswith('t'):
                        coleccion["ra"+ras]["locales"] = c
                        coleccion["ra"+ras]["locales"][c] = t
                        # si es una temporal, como van despues en el RA q las locales
                        # guardamos el tipo para luego calcular el desplazamiento
                    else:
                        coleccion["ra"+ras]["locales"] = c
                        coleccion["ra"+ras]["locales"][c] = total
                        total += reserva(t)
            
            for temporal in coleccion["ra"+ras]["locales"]:
                aux = reserva(coleccion["ra"+ras]["locales"][temporal])
                coleccion["ra"+ras]["locales"][temporal] = total
                total += aux

            coleccion["ra"+ras]["total"] = total
            ras+=1
        
        linea = leer()

    pilara = 0
    for ra in coleccion:
        pilara += coleccion[ra][total]
    escribir("MOVE #inicio_estaticas, .IY")
    escribir("MOVE #inicio_pila, .IX")
    escribir("inicio_estaticas: RES" + tamestaticos)
    escribir(info_de)
    escribir("inicio_pila: RES " + pilara)


if __name__=='__main__':
    main()