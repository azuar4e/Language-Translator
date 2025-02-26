#_____________________________________________________________________________
#imports
import re

#_____________________________________________________________________________
#clase

class tk:
    def __init__(self, tipo, atributo):
        self.tipo = tipo
        self.atributo = atributo

#_____________________________________________________________________________
#variables

tokens = []
patron = r"<\w+,(.+)>"

#_____________________________________________________________________________
#funciones

def convertir():
    global tokens
    with open("tokens.txt", "r") as f:   
        for token in f:
            tokens.append(token)
            
        tokens.append('$')

#_____________________________________________________________________________

def generador():
    convertir()
    for entrada in tokens:
        yield entrada

#_____________________________________________________________________________

gen = generador()
def siguiente_token():
    try:
        return next(gen)
    except StopIteration:
        return None

#_____________________________________________________________________________
 
def token():
    return toks(siguiente_token())

#_____________________________________________________________________________
#cambiar esta funcion con los tokes de los chinos
def toks(token):
    if "PRODUCTO" in token:
        return tk('*', None)

    elif "PARENT_ABRIR" in token:
        return tk('(', None)
    
    elif "PARENT_CERRAR" in token:   
        return tk(')', None)
        
    elif "BEGIN" in token:
        return tk('begin', None)

    elif "END" in token:
        return tk('end', None)
        
    elif "DOSPUNTOS" in token:
        return tk(':', None)

    elif "PYC" in token:
        return tk(';', None)

    elif "COMA" in token:
        return tk(',', None)

    elif "CADENA" in token:
        return tk('cadena', re.match(patron, token).group(1))

    elif "ENTERO" in token:
        return tk('entero', re.match(patron, token).group(1))

    elif "AND" in token:
        return tk('and', None)

    elif "IGUAL" in token:
        return tk('=', None)
                
    elif "INTEGER" in token:
        return tk('int', None)
        
    elif "BOOLEAN" in token:
        return tk('boolean', None)
        
    elif "STRING" in token:
        return tk('string', None)
        
    elif "IF" in token:
        return tk('if', None)
        
    elif "ELSE" in token:
        return tk('else', None)
        
    elif "RETURN" in token:
        return tk('return', None)
        
    elif "ASIGNACION" in token:
        return tk(':=', None)
        
    elif "THEN" in token:
        return tk('then', None)
        
    elif "FUNCTION" in token:
        return tk('function', None)
        
    elif "Void" in token:    
        return tk('void', None)
        
    elif "VAR" in token:
        return tk('var', None)
    
    elif "PROCEDURE" in token:
        return tk('procedure', None)
    
    elif "PROGRAM" in token:
        return tk('program', None)
        
    # revisar esto
    elif "ID" in token:
        return tk('id', re.match(patron, token).group(1))
    elif "EOF" in token:
        return tk('EOF', None)
    else:
        return None
