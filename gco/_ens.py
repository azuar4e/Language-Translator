archivo = None

def escribir(linea):
    global archivo
    if archivo is None:
        archivo = open("codobj.ens", 'w')
    archivo.write(linea)