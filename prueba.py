import re
from pprint import pprint
from _slr import slr, cargar_slr
patronparser = r"^(\w+)\s+(\d+(\s+\d+)*)$"
reglacnt = 0
fichparser = None
lineaparser = None

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

def main():
    while True:
        aux = parser()
        if aux == -1:
            break
        print(aux)
        
if __name__=='__main__':
    # main()
    cargar_slr("./data/SLR_data.csv")
    pprint(slr)