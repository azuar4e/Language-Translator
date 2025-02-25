#_____________________________________________________________________________
#imports
import sys
import subprocess
import re
from _ts import TablaSimbolos
from _leerts import ts, init
from pprint import pprint
from _slr import slr, cargar_slr
from _tokens import token
from _errores import errores

#_____________________________________________________________________________
#clases
#cambiar por los atributos del codigo intermedio
class atributos:
    def __init__(self, pos=None,tipo=None, tiporet=None, tipofunc=None):
        self.pos = pos
        self.tipo = tipo
        self.tiporet = tiporet
        self.tipofunc = tipofunc
    
    def set_pos(self, pos):
        self.pos = pos
        
    def set_tipo_func(self, tipofunc):
        self.tipofunc = tipofunc

    def set_tipo(self, tipo):
        self.tipo = tipo

    def set_tiporet(self, tiporet):
        self.tiporet = tiporet

#estructura de datos para pila
class ep:
    def __init__(self, elemento, valor=None):
        if valor is None:
            valor = atributos()
        self.elemento = elemento
        self.valor = valor

#_____________________________________________________________________________
#variables
archivo = None
fich_cuartetos = None
fichparser = None
pila = [ep(0)]
#contador de variables temporales
tmpcnt = 0
etiqcnt = 0
lineaparser = None
patronparser = r"^(\w+)\s+(\d+(\s+\d+)*)$"
reglacnt = 0
patronregla = r"(.+) -> (.+)"
edt = {
    #cuando este completa la edt, 
    # ponerla en formato clave valor, 
    # imagino que habra q hacer los firsts y esas bainas
}



#tabla simbolos
# hay que conseguir pasar todo el archivo 
# de la ts a una estructura de datos
# ts = TablaSimbolos()

#gramatica de los chinos
#imagino que habra q usar el parser para saber q regla han usado
#y luego hacer lo propio con nuestra gramatica
gramatica = {
    1: "P -> M1 D R",
    2: "M1 -> Lambda",
    3: "R -> PP R",
    4: "R -> PF R",
    5: "R -> PR R",
    6: "R -> Lambda",
    7: "PP -> program PPid ; D M2 Bloque ;",
    8: "PPid -> Pid",
    9: "Pid -> id",
    10: "M2 -> Lambda",
    11: "PR -> procedure PRidA ; D M2 Bloque ;",
    12: "PRidA -> Pid A",
    13: "PF -> function PFidAT ; D M2 Bloque ;",
    14: "PFidAT -> Pid A : T",
    15: "D -> var id : T ; DD",
    16: "D -> Lambda",
    17: "DD -> id : T ; DD",
    18: "DD -> Lambda",
    19: "T -> boolean",
    20: "T -> integer",
    21: "T -> string",
    22: "A -> ( X id : T AA )",
    23: "A -> Lambda",
    24: "AA -> ; X id : T AA",
    25: "AA -> Lambda",
    26: "Bloque -> begin C end",
    27: "C -> B C",
    28: "C -> Lambda",
    29: "B -> if EE then S",
    30: "EE -> E",
    31: "B -> S",
    32: "B -> if EE then Bloque ;",
    33: "B -> if THEN else Bloque ;",
    34: "THEN -> EE then Bloque ;",
    35: "B -> while M3 EE do Bloque ;",
    36: "M3 -> Lambda",
    37: "B -> repeat M3 C until E ;",
    38: "B -> loop M3 C end ;",
    39: "B -> FOR do Bloque ;",
    40: "FOR -> for id := E to E",
    41: "B -> case EXP of N O end ;",
    42: "EXP -> E",
    43: "N -> N VALOR : Bloque ;",
    44: "VALOR -> entero",
    45: "N -> Lambda",
    46: "O -> otherwise : M3 Bloque ;",
    47: "O -> Lambda",
    48: "S -> write LL ;",
    49: "S -> writeln LL ;",
    50: "S -> read ( V ) ;",
    51: "S -> id := E ;",
    52: "S -> id LL ;",
    53: "S -> return Y ;",
    54: "S -> exit when E ;",
    55: "LL -> ( L )",
    56: "LL -> Lambda",
    57: "L -> E Q",
    58: "Q -> , E Q",
    59: "Q -> Lambda",
    60: "V -> id W",
    61: "W -> , id W",
    62: "W -> Lambda",
    63: "Y -> E",
    64: "Y -> Lambda",
    65: "E -> E or F",
    66: "E -> E xor F",
    67: "E -> F",
    68: "F -> F and G",
    69: "F -> G",
    70: "G -> G = H",
    71: "G -> G <> H",
    72: "G -> G > H",
    73: "G -> G >= H",
    74: "G -> G < H",
    75: "G -> G <= H",
    76: "G -> H",
    77: "H -> H + I",
    78: "H -> H - I",
    79: "H -> I",
    80: "I -> I * J",
    81: "I -> I / J",
    82: "I -> I mod J",
    83: "I -> J",
    84: "J -> J ** K",
    85: "J -> K",
    86: "K -> not K",
    87: "K -> + K",
    88: "K -> - K",
    89: "K -> Z",
    90: "Z -> entero",
    91: "Z -> cadena",
    92: "Z -> true",
    93: "Z -> false",
    94: "Z -> id LL",
    95: "Z -> ( E )",
    96: "Z -> Z in ( L )",
    97: "Z -> max ( L )",
    98: "Z -> min ( L )",
    99: "X -> var",
    100: "X -> Lambda"
}

#_____________________________________________________________________________
#funciones
def nuevatemp() -> str:
    global tmpcnt
    tmpcnt += 1
    return f"t{tmpcnt}"

def nuevaetiq() -> str:
    global etiqcnt
    etiqcnt += 1
    return f"Etiq{etiqcnt}"

#devuelve el numero de la regla a ejecutar
def parser() -> int:
    global fichparser, lineaparser, reglas, reglacnt
    if fichparser is None:
        fichparser = open("parse.txt", "r")
        lineaparser = fichparser.readline()
        match = re.match(patronparser, lineaparser)
        if match is None:
            print("\n[+] ERROR: Regla no reconocida en el fichero de parser.")
            exit(1)
        reglas = match.group(2).split()
    try:
        aux = reglas[reglacnt]
        reglacnt += 1
        return int(aux)
    except IndexError:
        return -1
    

def leer() -> str:
    global archivo
    if archivo is None:
        archivo = open(sys.argv[1], "r")
        
def emite(operador: str, arg1, arg2, resultado) -> None:
    global fich_cuartetos
    if fich_cuartetos is None:
        fich_cuartetos = open("cuartetos.txt", "w")
       
    if arg1 is not None:
        contiene, tabla, despl = ts.contiene(arg1) 
        if contiene:
            if tabla == "global":
                arg1impr = f"{{VAR_GLOBAL, {despl}}}"
            if tabla == "local":
                arg1impr = f"{{VAR_LOCAL, {despl}}}"
        elif arg1 is int:
            arg1impr = f"{{CTE_ENT, {arg1}}}"
        elif arg1 is str:
            arg1impr = f"{{CTE_CADENA, {arg1}}}"
        #ver el resto de opciones ctes parametros y demas
    else:
        arg1impr = None
    
    if arg2 is not None:
        contiene, tabla, despl = ts.contiene(arg2) 
        if contiene:
            if tabla == "global":
                arg2impr = f"{{VAR_GLOBAL, {despl}}}"
            if tabla == "local":
                arg2impr = f"{{VAR_LOCAL, {despl}}}"
        elif arg2 is int:
            arg2impr = f"{{CTE_ENT, {arg2}}}"
        elif arg2 is str:
            arg2impr = f"{{CTE_CADENA, {arg2}}}"
    else:
        arg2impr = None
            
    #a esto le faltan cosas seguro
    fich_cuartetos.write(f"{operador.upper()}, {arg1impr}, {arg2impr}, {resultado}\n")
    
def ejecutaraccion(accion):
    # case '':
    return

def main():
    #habria q consumir tokens y avanzar la pila sustituyendo las reglas segun el parser
    #necesito generar las funciones para los tokens
    # hay que implementar una pila llamar a las funcinoes accion y goto y generar las acciones
    # semanticas a ejecutar, que no pueden tener atributos heredados
    print("todo al semen")
    while True:
        tok = token()
        estado = pila[-1].elemento
        accion = slr.get(f"{estado}:{tok.tipo}")
        print(f"{estado}:{tok.tipo}")
        print(accion)
        print("todo al semen1")
        if not accion:
            print("todo al semen2")
            errores()
            break
        # desplazamiento
        elif accion.tipo == 0:
            
            if tok == 'id':
                pila.append(ep(tok.tipo, atributos(pos=tok.atributo)))
            else:
                pila.append(ep(tok.tipo))
                
            pila.append(ep(accion.valor))
            tok = token()

            if tok is None:
                print("todo al semen3")
                errores()
                break

            if tok.tipo == 'EOF':
                print("fin")
                break
        
        # reduccion
        elif accion.tipo == 1:
            regla = gramatica.get(accion.valor)
            print(f"regla: {regla}")
            valor = re.match(patronregla, regla).group(2).split()
            # ver q hacer si lambda
            for _ in range(2 * len(valor)):
                pila.pop()
            
            # logica para ejecutar la accion semantica
            
            estado = pila[-1].elemento
            # antecedente de la regla
            pila.append(ep(re.match(patronregla, regla).group(1)))
            pila.append(ep(slr.get(f"{estado}:{pila[-1].elemento}").valor))
            
        # aceptar
        else:
            print("todo al semen4")
            return
        
        # print(f"\n\n\n---Pila---")
        # pprint(pila)
        # print("----------\n\n\n")
        

if __name__=='__main__':
    if len(sys.argv) < 2:
        print("\n[+] ERROR: No se ha pasado ningun archivo de entrada.\n")
        exit(1)

    comando = ["java", "-jar", "PBoreal.jar", sys.argv[1]]
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
     
    #cargamos el contenido de las tablas de simbolos
    init()
    # cargamos el contenido de la tabla goto
    cargar_slr("./data/SLR_data.csv")
    # pprint(slr)
    # llamamos al main
    main()