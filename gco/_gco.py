#________________________________________________________________________
#imports 
import sys
import subprocess
import re
from _ens import escribir

#________________________________________________________________________
# patrones
patron_mul = r"(MUL, (.*), (.*), (.*))"
patron_and = r"(AND, (.*), (.*), (.*))"
patron_asig = r"(ASIG, (.*), (.*), (.*))"
patron_asig_cad = r"(ASIG_CAD, (.*), (.*), (.*))"
patron_goto = r"(GOTO, (.*), (.*), (.*))"
patron_goto_ig = r"(GOTO_IG, (.*), (.*), (.*))"
patron_goto_dist = r"(GOTO_DIST, (.*), (.*), (.*))"
patron_goto_may_ig = r"(GOTO_MAY_IG, (.*), (.*), (.*))"
patron_goto_men_ig = r"(GOTO_MEN_IG, (.*), (.*), (.*))"
patron_goto_men = r"(GOT_MEN, (.*), (.*), (.*))"
patron_goto_may = r"(GOTO_MAY, (.*), (.*), (.*))"
patron_param = r"(PARAM, (.*), (.*), (.*))"
patron_param_cad = r"(PARAM_CAD, (.*), (.*), (.*))"
patron_ret = r"(RETURN, (.*), (.*), (.*))"
patron_ret_cad = r"(RETURN_CAD, (.*), (.*), (.*))"
patron_ret_ent = r"(RETURN_ENT, (.*), (.*), (.*))"
patron_etiq = r"(ETIQ, (.*), (.*), (.*))"
patron_call = r"(CALL, (.*), (.*), (.*))"
patron_call_fun = r"(CALL_FUN, (.*), (.*), (.*))"
patron_call_fun_cad = r"(CALL_FUN_CAD, (.*), (.*), (.*))"

#________________________________________________________________________
# resto de variables
archivo = None

def leer():
    global archivo
    if archivo is None:
        archivo = open(sys.argv[1], 'r')
        
    return archivo.readline()

def procesar_linea(linea):
    return None

def main():
    linea = leer()

    # escribimos la cabecera para el fichero de codigo objeto
    # tenemos que hacer una primera pasada para dar valor a etiquetas
    # registros de activacion etc etc para que en la segunda ya conozcamos 
    # las direcciones de memorial, los tamaños, etc
    # ver si hay alguna informacion que nos pueda indicar que el return esta
    # en la funcion principal, y si no implementarlo porque no parece q aurora
    # tenga mucha idea y puede haber mas de un return, por ejemplo dentro de un if

    cabecera_ens = "DE: RES 200\n"
    cabecera_ens += "PILA: NOP\n"

    escribir(cabecera_ens)
    
    while linea:
        if re.match(patron_mul, linea):
            coincidencia = re.match(patron_mul, linea)
            cadena = "MUL "+coincidencia.group(1)+", "+coincidencia.group(2)
            escribir(cadena)
            cadena = "MOVE .A, "+coincidencia.group(3) 
            escribir(cadena)
        
        elif re.match(patron_and, linea):
            coincidencia = re.match(patron_and, linea)
            cadena = "AND "+coincidencia.group(1)+", "+coincidencia.group(2)
            escribir(cadena)
            cadena = "MOVE .A, "+coincidencia.group(3) 
            escribir(cadena)
            
        elif re.match(patron_etiq, linea):
            coincidencia = re.match(patron_etiq, linea)
            cadena = coincidencia.group(1)+":"
            escribir(cadena)
            
        elif re.match(patron_asig, linea):
            coincidencia = re.match(patron_asig, linea)
            cadena = "MOVE "+coincidencia.group(1)+", "+coincidencia.group(3)
            escribir(cadena)
            
        elif re.match(patron_asig_cad, linea):
            coincidencia = re.match(patron_asig_cad, linea)
            cadena = "MOVE "+coincidencia.group(1)+", "+coincidencia.group(3)
            escribir(cadena)

        elif re.match(patron_goto, linea):
            coincidencia = re.match(patron_goto, linea)
            cadena = "BR /"+coincidencia.group(1)
            escribir(cadena)
            
        elif re.match(patron_goto_may, linea):
            coincidencia = re.match(patron_goto_may, linea)
            cadena = "CMP "+coincidencia.group(1)+", "+ coincidencia.group(2)
            escribir(cadena)
            cadena = "BP /"+coincidencia.group(3)
            escribir(cadena)
            
        elif re.match(patron_goto_men, linea):
            coincidencia = re.match(patron_goto_men, linea)
            cadena = "CMP "+coincidencia.group(1)+", "+ coincidencia.group(2)
            escribir(cadena)
            cadena = "BN /"+coincidencia.group(3)
            escribir(cadena)
            
        elif re.match(patron_goto_ig, linea):
            coincidencia = re.match(patron_goto_ig, linea)
            cadena = "CMP "+coincidencia.group(1)+", "+ coincidencia.group(2)
            escribir(cadena)
            cadena = "BZ /"+coincidencia.group(3)
            escribir(cadena)
            
        elif re.match(patron_goto_dist, linea):
            coincidencia = re.match(patron_goto_dist, linea)
            cadena = "CMP "+coincidencia.group(1)+", "+ coincidencia.group(2)
            escribir(cadena)
            cadena = "BNZ /"+coincidencia.group(3)
            escribir(cadena)
            
        elif re.match(patron_goto_may_ig, linea):
            coincidencia = re.match(patron_goto_may_ig, linea)
            cadena = "CMP "+coincidencia.group(1)+", "+ coincidencia.group(2)
            escribir(cadena)
            cadena = "BZ /"+coincidencia.group(3)
            escribir(cadena)
            cadena = "BP /"+coincidencia.group(3)
            escribir(cadena)
            
        elif re.match(patron_goto_men_ig, linea):
            coincidencia = re.match(patron_goto_men_ig, linea)
            cadena = "CMP "+coincidencia.group(1)+", "+ coincidencia.group(2)
            escribir(cadena)
            cadena = "BZ /"+coincidencia.group(3)
            escribir(cadena)
            cadena = "BN /"+coincidencia.group(3)
            escribir(cadena)

        elif re.match(patron_param, linea):
            coincidencia = re.match(patron_param, linea)
            cadena = "MOVE "+coincidencia.group(2)
            escribir(cadena)
        
        elif re.match(patron_param_cad, linea):
            coincidencia = re.match(patron_param_cad, linea)
            cadena = "MOVE "+coincidencia.group(2)
            escribir(cadena)
        
        elif re.match(patron_ret, linea):  #chequea si es el del main o de una funcion
            coincidencia = re.match(patron_ret, linea)
            linea = leer()
            if linea == None:
                cadena = "HALT"
                escribir(cadena)
                break
            else :
                if coincidencia.group(2) != "_":
                    cadena = "MOVE "+coincidencia.group(2)+", .A"
                    escribir(cadena)
                cadena = "RET"
                escribir(cadena)
                continue

        elif re.match(patron_ret_cad, linea):
            coincidencia = re.match(patron_ret_cad, linea)
            if coincidencia.group(2) != "_":
                cadena = "MOVE "+coincidencia.group(2)+", .A"
                escribir(cadena)
            cadena = "RET"
            escribir(cadena)
        
        elif re.match(patron_ret_ent, linea):
            coincidencia = re.match(patron_ret_ent, linea)
            if coincidencia.group(2) != "_":
                cadena = "MOVE "+coincidencia.group(2)+", .A"
                escribir(cadena)
            cadena = "RET"
            escribir(cadena)
            
        elif re.match(patron_call, linea):
            coincidencia = re.match(patron_call, linea)
            cadena = f"""
            \t\t\tMOVE #dir_ret1, #Tam_RA_llamador[.IX]
            \t\t\tMOVE #1[.IX], .R9 
            \t\t\tMOVE [.R9], .R9
            

            \t\t\tMOVE [.R9], .R9
            \t\t\tADD #Tam_RA_llamador, .IX
            \t\t\tINC .A
            \t\t\tMOVE .R9, [.A]
            \t\t\tADD #Tam_RA_llamador, .IX
            \t\t\tMOVE .A, .IX
            \t\t\tBR /{coincidencia.group(1)}

            dir_ret1:   SUB .IX, #Tam_RA_llamador
            \t\t\tMOVE .A, .IX
            """
            escribir(cadena)
            
        elif re.match(patron_call_fun, linea):
            coincidencia = re.match(patron_call_fun, linea)
            cadena = f"""
            \t\t\tMOVE #dir_ret, #Tam_RA_llamador[.IX]
            \t\t\tMOVE #1[.IX], .R9 
            \t\t\tMOVE [.R9], .R9

            \t\t\tMOVE [.R9], .R9

            \t\t\tADD #Tam_RA_llamador, .IX
            \t\t\tINC .A
            \t\t\tMOVE .R9, [.A]
            \t\t\tADD #Tam_RA_llamador, .IX
            \t\t\tMOVE .A, .IX
            \t\t\tBR /{coincidencia.group(1)}

            dir_ret1:   SUB #Tam_RA_p, #1
            \t\t\tADD .A, .IX
            \t\t\tMOVE [.A], .R9
            
            \t\t\tSUB .IX, #Tam_RA_llamador
            \t\t\tMOVE .A, .IX
            
            \t\t\tMOVE .R9, #32[.IX]
            """
            escribir(cadena)
        
        elif re.match(patron_call_fun_cad, linea):
            coincidencia = re.match(patron_call_fun_cad, linea)
            cadena = f"""
            \t\t\tMOVE #dir_ret, #Tam_RA_llamador[.IX]
            \t\t\tMOVE #1[.IX], .R9 
            \t\t\tMOVE [.R9], .R9

            \t\t\tMOVE [.R9], .R9

            \t\t\tADD #Tam_RA_llamador, .IX
            \t\t\tINC .A
            \t\t\tMOVE .R9, [.A]
            \t\t\tADD #Tam_RA_llamador, .IX
            \t\t\tMOVE .A, .IX
            \t\t\tBR /{coincidencia.group(1)}

            dir_ret1:   SUB #Tam_RA_p, #1
            \t\t\tADD .A, .IX
            \t\t\tMOVE [.A], .R9
            
            \t\t\tSUB .IX, #Tam_RA_llamador
            \t\t\tMOVE .A, .IX
            
            \t\t\tMOVE .R9, #32[.IX]
            """
            escribir(cadena)
            

        linea = leer()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("\n[+] ERROR: No se ha pasado ningun archivo de entrada.\n")
        exit(1)
 
    comando = ["java", "-jar", "../tdl/target/tdl-1.0-SNAPSHOT-jar-with-dependencies.jar", sys.argv[1]]
 
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
  
    main()