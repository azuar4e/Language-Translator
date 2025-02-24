# genera la tabla slr del analizador ascendente que se necesita para generar el codigo intermedio
#________________________________________________________________________
#imports
import csv
import re

#________________________________________________________________________
#variables

slr = {}
colidtok = {}

class Acc_ASin:
    def __init__(self, tipo, valor):
        self.tipo = tipo
        self.valor = valor

#________________________________________________________________________
#functions

def genvalue(value):
    number = re.findall(r'\d+', value)
    return int(number[0]) if number else 0

def cargar_slr(archivo):
    with open(archivo, mode='r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        cabecera = next(reader)
        
        for col_index, celda in enumerate(cabecera[1:], start=1):
            celda = celda.upper().replace(" ", "")
            if celda == "$":
                celda = "EOF"
            if celda == "FIN":
                break

            colidtok[col_index] = celda
            
        state = 0
        for row in reader:
            for i, celda in enumerate(row[1:], start=1):
                if not celda:
                    continue

                key = f"{state}:{colidtok.get(i)}"
                if celda.startswith('s'):  
                    slr[key] = Acc_ASin(0, genvalue(celda))
                elif celda.startswith('r'):
                    slr[key] = Acc_ASin(1, genvalue(celda))
                elif celda == 'accept':
                    slr[key] = Acc_ASin(2, 0)
                else:  # Aceptar (accept)
                    slr[key] = Acc_ASin(0, genvalue(celda))

            state += 1