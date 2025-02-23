#_____________________________________________________________________________
#imports
from _ts import TablaSimbolos
from pprint import pprint
import re

ts = TablaSimbolos()

#_____________________________________________________________________________
#patrones

tipo = r"Tipo: '(\w+)'"
despl = r"Despl: (\d+)"
numparam = r"numParam: (\d+)"
tipoparam = r"TipoParam(\d+): '(\w+)'"
modoparam = r"ModoParam(\d+): '(\w+)'"
tiporet = r"TipoRetorno: '(\w+)'"
etiqfuncion = r"EtiqFuncion: '(\w+)'"
lexema = r"LEXEMA: '(\w+)'"
lexemaact = None
tablaact = None

def init():
    with open("ts.txt", "r") as f:
        for line in f:
            if line.startswith("TABLA LOCAL"):
                ts.crearts(str(line[-3]))
                tablaact = str(line[-3])
                
                while line != "----------------------------------------\n":
                    if re.search(lexema, line):
                        lexemaact = re.search(lexema, line).group(1)
                        ts.insertarlexema(lexemaact, tablaact)
                    elif re.search(tipo, line):
                        ts.insertartipots(lexemaact, re.search(tipo, line).group(1), tablaact)
                    elif re.search(despl, line):
                        ts.insertardesplts(lexemaact, re.search(despl, line).group(1), tablaact)

                    line = f.readline()
                lexemaact = None
                tablaact = None
            elif line.startswith("TABLA PRINCIPAL"):
                while line != "":
                    if re.search(lexema, line):
                            lexemaact = re.search(lexema, line).group(1)
                            ts.insertarlexema(lexemaact, None)
                    elif re.search(tipo, line):
                        ts.insertartipots(lexemaact, re.search(tipo, line).group(1), None)
                    elif re.search(despl, line):
                        ts.insertardesplts(lexemaact, re.search(despl, line).group(1), None)
                    elif re.search(numparam, line):
                        ts.insertarnumparam(lexemaact, re.search(numparam, line).group(1))
                    elif re.search(tipoparam, line):
                        ts.insertartipoparam(lexemaact, re.search(tipoparam, line).group(2), re.search(tipoparam, line).group(1))
                    elif re.search(modoparam, line):
                        ts.insertarmodoparam(lexemaact, re.search(modoparam, line).group(2), re.search(modoparam, line).group(1))
                    elif re.search(tiporet, line):
                        ts.insertartiporet(lexemaact, re.search(tiporet, line).group(1))
                    elif re.search(etiqfuncion, line):
                        ts.insertaretiqfuncion(lexemaact, re.search(etiqfuncion, line).group(1))
                    
                    line = f.readline()