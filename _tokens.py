#_____________________________________________________________________________
#imports
import re

#_____________________________________________________________________________
#funciones

def convertir():
    global tokens
    with open("tokens.txt", "r") as f:   
        for token in f:
            tokens.append(token)
            
        tokens.append('$')
        
#____________________________________________

def generador():
    convertir()
    for entrada in tokens:
        yield entrada

#____________________________________________

gen = generador()
def siguiente_token():
    try:
        return next(gen)
    except StopIteration:
        return None

#____________________________________________
#cambiar esta funcion con los tokes de los chinos
def toks(token):
    # patron_valor = r'<Const , (\d+)>'
    # patron_cadena = r'<Cadena , \"([^\"]+)\">'
    
    if "OPa" in token:
        return '+'

    elif "Parentesis" in token:
        if '0' in token:
            return '('
        else:
            return ')'

    elif "Llave" in token:
        if '0' in token:
            return '{'
        else:
            return '}'

    elif "PuntoComa" in token:
        return ';'

    elif "Coma" in token:
        return ','

    elif "Cadena" in token:
        return 'cad'

    elif "Const" in token:
        return 'ent'

    elif "Igual" in token:
        return '='

    elif "OPl" in token:
        return '&&'

    elif "OPe" in token:
        return '/='

    elif "OPr" in token:
        return '>'
                
    elif "Entero" in token:
        return 'int'
        
    elif "Boolean" in token:
        return 'boolean'
        
    elif "Str" in token:
        return 'string'
        
    elif "If" in token:
        return 'if'
        
    elif "Else" in token:
        return 'else'
        
    elif "Return" in token:
        return 'return'
        
    elif "Input" in token:
        return 'input'
        
    elif "Output" in token:
        return 'output'
        
    elif "Funcion" in token:
        return 'function'
        
    elif "Void" in token:    
        return 'void'
        
    elif "Var" in token:
        return 'var'
        
    elif "Id" in token:
        aux = re.match(r"<[a-zA-Z]+ , (\d+)>", token)
        posts = int(aux.group(1))
        id[posts] = buscaridtslex(posts)
        global pos
        pos = posts
        return "id"
    else:
        return '$'