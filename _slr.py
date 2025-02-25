# genera la tabla slr del analizador ascendente que se necesita para generar el codigo intermedio
#________________________________________________________________________
#imports
import csv
import re

#________________________________________________________________________
#variables

slr = {}
colidtok = {}

class acc_asin:
    def __init__(self, tipo, valor):
        self.tipo = tipo
        self.valor = valor

#________________________________________________________________________
#functions
def cambio(celda):    
    if celda == "PRODUCTO":
        return '*'
    
    elif celda == "PARENT_ABRIR":
        return '('
    
    elif celda == "PARENT_CERRAR":   
        return ')'
        
    elif celda == "BEGIN":
        return 'begin'

    elif celda == "END":
        return 'end'
        
    elif celda == "DOSPUNTOS":
        return ':'

    elif celda == "PYC":
        return ';'

    elif celda == "COMA":
        return ','

    elif celda == "CADENA":
        return 'cadena'

    elif celda == "ENTERO":
        return 'entero'

    elif celda == "AND":
        return 'and'

    elif celda == "IGUAL":
        return '='
                
    elif celda == "INTEGER":
        return 'int'
        
    elif celda == "BOOLEAN":
        return 'boolean'
        
    elif celda == "STRING":
        return 'string'
        
    elif celda == "IF":
        return 'if'
        
    elif celda == "ELSE":
        return 'else'
        
    elif celda == "RETURN":
        return 'return'
        
    elif celda == "ASIGNACION":
        return ':='
        
    elif celda == "THEN":
        return 'then'
        
    elif celda == "FUNCTION":
        return 'function'
        
    elif celda == "Void":    
        return 'void'
        
    elif celda == "VAR":
        return 'var'
    
    elif celda == "PROCEDURE":
        return 'procedure'
    
    elif celda == "PROGRAM":
        return 'program'

    elif celda == "WRITE":
        return 'write'

    elif celda == "WRITELN":
        return 'writeln'

    elif celda == "READ":
        return 'read'

    elif celda == "DO":
        return 'do'

    elif celda == "WHILE":
        return 'while'

    elif celda == "REPEAT":
        return 'repeat'

    elif celda == "UNTIL":
        return 'until'

    elif celda == "LOOP":
        return 'loop'

    elif celda == "FOR":
        return 'for'

    elif celda == "CASE":
        return 'case'

    elif celda == "OF":
        return 'of'

    elif celda == "OTHERWISE":
        return 'otherwise'

    elif celda == "WHEN":
        return 'when'

    elif celda == "TRUE":
        return 'true'

    elif celda == "FALSE":
        return 'false'

    elif celda == "EXIT":
        return 'exit'

    elif celda == "MAYOR_IGUAL":
        return '>='

    elif celda == "MAYOR":
        return '>'

    elif celda == "MENOR":
        return '<'

    elif celda == "DISTINTO":
        return '!='

    elif celda == "MENOR_IGUAL":
        return '<='

    elif celda == "POTENCIA":
        return '**'

    elif celda == "MAS":
        return '+'

    elif celda == "MENOS":
        return '-'

    elif celda == "DIVISION":
        return '/'

    elif celda == "OR":
        return 'or'

    elif celda == "XOR":
        return 'xor'

    elif celda == "IN":
        return 'in'

    elif celda == "MOD":
        return 'mod'

    elif celda == "NOT":
        return 'not'

    elif celda == "MAX":
        return 'max'

    elif celda == "MIN":
        return 'min'

    elif celda == "TO":
        return 'to'

    elif celda == "ID":
        return 'id'
    
    elif celda == "EOF" or celda == "$":
        return 'EOF'
    
    else:
        return 'FIN'

def genvalue(value):
    number = re.findall(r'\d+', value)
    return int(number[0]) if number else 0

def cargar_slr(archivo):
    with open(archivo, mode='r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        cabecera = next(reader)
        
        for col_index, celda in enumerate(cabecera[1:], start=1):
            celda = celda.upper().replace(" ", "")
            celda = cambio(celda)
            # if celda == "$":
            #     celda = "EOF"
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
                    slr[key] = acc_asin(0, genvalue(celda))
                elif celda.startswith('r'):
                    slr[key] = acc_asin(1, genvalue(celda))
                elif celda == 'accept':
                    slr[key] = acc_asin(2, 0)
                else:
                    slr[key] = acc_asin(0, genvalue(celda))

            state += 1