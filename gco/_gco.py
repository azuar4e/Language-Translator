#________________________________________________________________________
#imports 
import sys
import subprocess
import re
from _ens import escribir
import _calcprev

#________________________________________________________________________
# resto de variables
archivo = None

#________________________________________________________________________
# patrones

patron_mul = r"""
\(MUL,\s*
    ((?:\{[^{}]*\}|[^,()])+)  ,\s*
    ((?:\{[^{}]*\}|[^,()])+)  ,\s*
    ((?:\{[^{}]*\}|[^,()])+) 
\)
"""

patron_and = r"""
\(AND,\s*
    ((?:\{[^{}]*\}|[^,()])+)  ,\s*
    ((?:\{[^{}]*\}|[^,()])+)  ,\s*
    ((?:\{[^{}]*\}|[^,()])+) 
\)
"""

patron_asig = r"""
\(ASIG,\s*
    ((?:\{[^{}]*\}|[^,()])+)  ,\s*
    ((?:\{[^{}]*\}|[^,()])+)  ,\s*
    ((?:\{[^{}]*\}|[^,()])+) 
\)
"""

patron_asig_cad = r"""
\(ASIG_CAD,\s*
    ((?:\{[^{}]*\}|[^,()])+)  ,\s*
    ((?:\{[^{}]*\}|[^,()])+)  ,\s*
    ((?:\{[^{}]*\}|[^,()])+) 
\)
"""

patron_goto = r"""
\(GOTO,\s*
    ((?:\{[^{}]*\}|[^,()])+)  ,\s*
    ((?:\{[^{}]*\}|[^,()])+)  ,\s*
    ((?:\{[^{}]*\}|[^,()])+) 
\)
"""

patron_goto_ig = r"""
\(GOTO_IG,\s*
    ((?:\{[^{}]*\}|[^,()])+)  ,\s*
    ((?:\{[^{}]*\}|[^,()])+)  ,\s*
    ((?:\{[^{}]*\}|[^,()])+) 
\)
"""

patron_goto_dist = r"""
\(GOTO_DIST,\s*
    ((?:\{[^{}]*\}|[^,()])+)  ,\s*
    ((?:\{[^{}]*\}|[^,()])+)  ,\s*
    ((?:\{[^{}]*\}|[^,()])+) 
\)
"""

patron_goto_may_ig = r"""
\(GOTO_MAY_IG,\s*
    ((?:\{[^{}]*\}|[^,()])+)  ,\s*
    ((?:\{[^{}]*\}|[^,()])+)  ,\s*
    ((?:\{[^{}]*\}|[^,()])+) 
\)
"""

patron_goto_men_ig = r"""
\(GOTO_MEN_IG,\s*
    ((?:\{[^{}]*\}|[^,()])+)  ,\s*
    ((?:\{[^{}]*\}|[^,()])+)  ,\s*
    ((?:\{[^{}]*\}|[^,()])+) 
\)
"""

patron_goto_men = r"""
\(GOT_MEN,\s*
    ((?:\{[^{}]*\}|[^,()])+)  ,\s*
    ((?:\{[^{}]*\}|[^,()])+)  ,\s*
    ((?:\{[^{}]*\}|[^,()])+) 
\)
"""

patron_goto_may = r"""
\(GOTO_MAY,\s*
    ((?:\{[^{}]*\}|[^,()])+)  ,\s*
    ((?:\{[^{}]*\}|[^,()])+)  ,\s*
    ((?:\{[^{}]*\}|[^,()])+) 
\)
"""

patron_param = r"""
\(PARAM,\s*
    ((?:\{[^{}]*\}|[^,()])+)  ,\s*
    ((?:\{[^{}]*\}|[^,()])+)  ,\s*
    ((?:\{[^{}]*\}|[^,()])+) 
\)
"""

patron_param_cad = r"""
\(PARAM_CAD,\s*
    ((?:\{[^{}]*\}|[^,()])+)  ,\s*
    ((?:\{[^{}]*\}|[^,()])+)  ,\s*
    ((?:\{[^{}]*\}|[^,()])+) 
\)
"""

patron_ret = r"""
\(RETURN,\s*
    ((?:\{[^{}]*\}|[^,()])+)  ,\s*
    ((?:\{[^{}]*\}|[^,()])+)  ,\s*
    ((?:\{[^{}]*\}|[^,()])+) 
\)
"""

patron_ret_cad = r"""
\(RETURN_CAD,\s*
    ((?:\{[^{}]*\}|[^,()])+)  ,\s*
    ((?:\{[^{}]*\}|[^,()])+)  ,\s*
    ((?:\{[^{}]*\}|[^,()])+) 
\)
"""

patron_ret_ent = r"""
\(RETURN_ENT,\s*
    ((?:\{[^{}]*\}|[^,()])+)  ,\s*
    ((?:\{[^{}]*\}|[^,()])+)  ,\s*
    ((?:\{[^{}]*\}|[^,()])+) 
\)
"""

patron_etiq = r"""
\(ETIQ,\s*
    ((?:\{[^{}]*\}|[^,()])+)  ,\s*
    ((?:\{[^{}]*\}|[^,()])+)  ,\s*
    ((?:\{[^{}]*\}|[^,()])+) 
\)
"""

patron_call = r"""
\(CALL,\s*
    ((?:\{[^{}]*\}|[^,()])+)  ,\s*
    ((?:\{[^{}]*\}|[^,()])+)  ,\s*
    ((?:\{[^{}]*\}|[^,()])+) 
\)
"""

patron_call_fun = r"""
\(CALL_FUN,\s*
    ((?:\{[^{}]*\}|[^,()])+)  ,\s*
    ((?:\{[^{}]*\}|[^,()])+)  ,\s*
    ((?:\{[^{}]*\}|[^,()])+) 
\)
"""

patron_call_fun_cad = r"""
\(CALL_FUN_CAD,\s*
    ((?:\{[^{}]*\}|[^,()])+)  ,\s*
    ((?:\{[^{}]*\}|[^,()])+)  ,\s*
    ((?:\{[^{}]*\}|[^,()])+) 
\)
"""

etiqueta = r"\{ET, (.*)\}"


# Añadir patrones para reconocer los cuartetos de I/O
patron_read = r"""
\(READ,\s*
    ((?:\{[^{}]*\}|[^,()])+)  ,\s*
    ((?:\{[^{}]*\}|[^,()])+)  ,\s*
    ((?:\{[^{}]*\}|[^,()])+) 
\)
"""

patron_read_cad = r"""
\(READ_CAD,\s*
    ((?:\{[^{}]*\}|[^,()])+)  ,\s*
    ((?:\{[^{}]*\}|[^,()])+)  ,\s*
    ((?:\{[^{}]*\}|[^,()])+) 
\)
"""

patron_write = r"""
\(WRITE,\s*
    ((?:\{[^{}]*\}|[^,()])+)  ,\s*
    ((?:\{[^{}]*\}|[^,()])+)  ,\s*
    ((?:\{[^{}]*\}|[^,()])+) 
\)
"""

patron_write_cad = r"""
\(WRITE_CAD,\s*
    ((?:\{[^{}]*\}|[^,()])+)  ,\s*
    ((?:\{[^{}]*\}|[^,()])+)  ,\s*
    ((?:\{[^{}]*\}|[^,()])+) 
\)
"""

patron_writeln = r"""
\(WRITELN,\s*
    ((?:\{[^{}]*\}|[^,()])+)  ,\s*
    ((?:\{[^{}]*\}|[^,()])+)  ,\s*
    ((?:\{[^{}]*\}|[^,()])+) 
\)
"""

#________________________________________________________________________
# funciones

def leer():
    global archivo
    if archivo is None:
        archivo = open("cuartetos.txt", 'r')

    return archivo.readline()


def leer_cadena_ens(cadena, destino):
    if cadena != ".R2":
        codobj = f"""
            cad: DATA "{cadena}"
            MOVE /cad, .R7
            DEC .R2
            DEC .R7
    bucle:	INC .R2
            INC .R7
            MOVE [.R7], [.R2]
            CMP [.R7], #0
            BNZ /bucle
        """
    else:
        codobj = """
            DEC .R3
            DEC .R2
    bucle:	INC .R3
            INC .R2
            MOVE [.R2], [.R3]
            CMP [.R2], #0
            BNZ /bucle
        """

    escribir(codobj)
    
def transformar_dir(dir1, dir2, dir3):
    ptglob = r"{VAR_GLOBAL, (.+)}"
    ptloc = r"{VAR_LOCAL, (.+)}"
    
    nreg = 2
    escribir("\n")
    for dir in [dir1, dir2, dir3]:
        if dir is None:
            continue
        
        elif re.match(ptglob, dir):
            cad = f"ADD #{re.match(ptglob, dir).group(1)}, .IY\nMOVE .A, .R{nreg}\n"
            nreg += 1
            escribir(cad)
        
        elif re.match(ptloc, dir):
            cad = f"ADD #{re.match(ptloc, dir).group(1)}, .IX\nMOVE .A, .R{nreg}\n"
            nreg += 1
            escribir(cad)
    escribir("\n")

#________________________________________________________________________
# main

def main():
    _calcprev.main() # calculo de la cabecera del ensamblador
    
    linea = leer()
    while linea:
        if re.match(patron_mul, linea, re.VERBOSE):
            coincidencia = re.match(patron_mul, linea, re.VERBOSE)
            transformar_dir(coincidencia.group(1), coincidencia.group(2), coincidencia.group(3))
            cadena = "MUL .R2, .R3"
            escribir(cadena)
            escribir("\n")
            cadena = "MOVE .A, .R4"
            escribir(cadena)
            escribir("\n")
        
        elif re.match(patron_and, linea, re.VERBOSE):
            coincidencia = re.match(patron_and, linea, re.VERBOSE)
            transformar_dir(coincidencia.group(1), coincidencia.group(2), coincidencia.group(3))
            cadena = "AND .R2, .R3"
            escribir(cadena)
            escribir("\n")
            cadena = "MOVE .A, .R4"
            escribir(cadena)
            escribir("\n")

        elif re.match(patron_etiq, linea, re.VERBOSE):
            coincidencia = re.match(patron_etiq, linea, re.VERBOSE)
            aux = coincidencia.group(1)
            cadena = re.match(etiqueta, aux).group(1) +":"
            escribir(cadena)
            escribir("\n")
            
        elif re.match(patron_asig, linea, re.VERBOSE):
            coincidencia = re.match(patron_asig, linea, re.VERBOSE)
            transformar_dir(coincidencia.group(1), None, coincidencia.group(3))
            cadena = "MOVE .R2, .R3"
            escribir(cadena)
            escribir("\n")
            
        elif re.match(patron_asig_cad, linea, re.VERBOSE):
            coincidencia = re.match(patron_asig_cad, linea, re.VERBOSE)
            ptloc = r"{VAR_LOCAL, (.+)}"
            ptglob = r"{VAR_GLOBAL, (.+)}"
            if re.match(ptglob, coincidencia.group(1)) or re.match(ptloc, coincidencia.group(1)):  
                transformar_dir(coincidencia.group(1), None, coincidencia.group(3))
                leer_cadena_ens(".R2", ".R3")
            else:
                transformar_dir(None, None, coincidencia.group(3))
                leer_cadena_ens(coincidencia.group(1), ".R2")

            escribir("\n")

        elif re.match(patron_goto, linea, re.VERBOSE):
            coincidencia = re.match(patron_goto, linea, re.VERBOSE)
            aux = coincidencia.group(3)
            cadena = "BR /"+re.match(etiqueta, aux).group(1)
            escribir(cadena)
            escribir("\n")
            
        elif re.match(patron_goto_may, linea, re.VERBOSE):
            coincidencia = re.match(patron_goto_may, linea, re.VERBOSE)
            transformar_dir(coincidencia.group(1), coincidencia.group(2), None)

            cadena = "CMP .R2, .R3"
            escribir(cadena)
            escribir("\n")
            aux = coincidencia.group(3)
            cadena = "BP /"+re.match(etiqueta, aux).group(1)
            escribir(cadena)
            escribir("\n")
            
        elif re.match(patron_goto_men, linea, re.VERBOSE):
            coincidencia = re.match(patron_goto_men, linea, re.VERBOSE)
            transformar_dir(coincidencia.group(1), coincidencia.group(2), None)
            cadena = "CMP .R2, .R3"
            escribir(cadena)
            escribir("\n")
            aux = coincidencia.group(3)
            cadena = "BN /"+re.match(etiqueta, aux, re.VERBOSE).group(1)
            escribir(cadena)
            escribir("\n")
            
        elif re.match(patron_goto_ig, linea, re.VERBOSE):
            coincidencia = re.match(patron_goto_ig, linea, re.VERBOSE)
            transformar_dir(coincidencia.group(1), coincidencia.group(2), None)
            cadena = "CMP .R2, .R3"
            escribir(cadena)
            escribir("\n")
            aux = coincidencia.group(3)
            cadena = "BZ /"+re.match(etiqueta, aux).group(1)
            escribir(cadena)
            escribir("\n")
            
        elif re.match(patron_goto_dist, linea, re.VERBOSE):
            coincidencia = re.match(patron_goto_dist, linea, re.VERBOSE)
            transformar_dir(coincidencia.group(1), coincidencia.group(2), None)
            cadena = "CMP .R2, .R3"
            escribir(cadena)
            escribir("\n")
            aux = coincidencia.group(3)
            cadena = "BNZ /"+re.match(etiqueta, aux).group(1)
            escribir(cadena)
            escribir("\n")
            
        elif re.match(patron_goto_may_ig, linea, re.VERBOSE):
            coincidencia = re.match(patron_goto_may_ig, linea, re.VERBOSE)
            transformar_dir(coincidencia.group(1), coincidencia.group(2), None)
            cadena = "CMP .R2, .R3"
            escribir(cadena)
            escribir("\n")
            aux = coincidencia.group(3)
            cadena = "BZ /"+re.match(etiqueta, aux).group(1)
            escribir(cadena)
            escribir("\n")
            aux = coincidencia.group(3)
            cadena = "BP /"+re.match(etiqueta, aux).group(1)
            escribir(cadena)
            escribir("\n")
            
        elif re.match(patron_goto_men_ig, linea, re.VERBOSE):
            coincidencia = re.match(patron_goto_men_ig, linea, re.VERBOSE)
            transformar_dir(coincidencia.group(1), coincidencia.group(2), None)
            cadena = "CMP .R2, .R3"            
            escribir(cadena)
            escribir("\n")
            aux = coincidencia.group(3)
            cadena = "BZ /"+re.match(etiqueta, aux).group(1)
            escribir(cadena)
            escribir("\n")
            aux = coincidencia.group(3)
            cadena = "BN /"+re.match(etiqueta, aux).group(1)
            escribir(cadena)
            escribir("\n")

        elif re.match(patron_param, linea, re.VERBOSE):
            coincidencia = re.match(patron_param, linea, re.VERBOSE)
            transformar_dir(None, coincidencia.group(2), None)
            cadena = "MOVE .R2"
            escribir(cadena)
            escribir("\n")
        
        elif re.match(patron_param_cad, linea, re.VERBOSE):
            coincidencia = re.match(patron_param_cad, linea, re.VERBOSE)
            # MIRAR ESTO PORQUE CREO QUE HAY QUE COPIAR LA CADENA EN LUGAR DEL MOVE
            # *********************************************************************
            # *********************************************************************
            # *********************************************************************
            transformar_dir(None, coincidencia.group(2), None)
            cadena = "MOVE .R2"
            escribir(cadena)
            escribir("\n")
        
        elif re.match(patron_ret, linea, re.VERBOSE):  #chequea si es el del main o de una funcion
            coincidencia = re.match(patron_ret, linea, re.VERBOSE)
            linea = leer()
            # *********************************************************************
            # *********************************************************************
            # *********************************************************************
            if linea == None:
                cadena = "HALT"
                escribir(cadena)
                escribir("\n")
                break
            else :
                if coincidencia.group(2) != "_":
                    cadena = "MOVE "+coincidencia.group(2)+", .A"
                    escribir(cadena)
                    escribir("\n")
                cadena = "RET"
                escribir(cadena)
                escribir("\n")
                continue

        elif re.match(patron_ret_cad, linea, re.VERBOSE):
            coincidencia = re.match(patron_ret_cad, linea, re.VERBOSE)
            if coincidencia.group(2) != "_":
                cadena = "MOVE "+coincidencia.group(2)+", .A"
                escribir(cadena)
                escribir("\n")
            cadena = "RET"
            escribir(cadena)
            escribir("\n")
        
        elif re.match(patron_ret_ent, linea, re.VERBOSE):
            coincidencia = re.match(patron_ret_ent, linea, re.VERBOSE)
            # *********************************************************************
            # *********************************************************************
            # *********************************************************************
            if coincidencia.group(2) != "_":
                cadena = "MOVE "+coincidencia.group(2)+", .A"
                escribir(cadena)
                escribir("\n")
            cadena = "RET"
            escribir(cadena)
            escribir("\n")
            
        elif re.match(patron_call, linea, re.VERBOSE):
            coincidencia = re.match(patron_call, linea, re.VERBOSE)
            # *********************************************************************
            # *********************************************************************
            # *********************************************************************
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
            escribir("\n")
            
        elif re.match(patron_call_fun, linea, re.VERBOSE):
            coincidencia = re.match(patron_call_fun, linea, re.VERBOSE)
            # *********************************************************************
            # *********************************************************************
            # *********************************************************************
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
            escribir("\n")
        
        elif re.match(patron_call_fun_cad, linea, re.VERBOSE):
            coincidencia = re.match(patron_call_fun_cad, linea, re.VERBOSE)
            # *********************************************************************
            # *********************************************************************
            # *********************************************************************
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
            escribir("\n")

        elif re.match(patron_read, linea, re.VERBOSE):
            coincidencia = re.match(patron_read, linea, re.VERBOSE)
            # Código para leer un valor entero
            cadena = """
                MOVE #0, .R1
                IN .R1
                MOVE .R1, """ + coincidencia.group(3)
            escribir(cadena)
            escribir("\n")

        elif re.match(patron_read_cad, linea, re.VERBOSE):
            coincidencia = re.match(patron_read_cad, linea, re.VERBOSE)
            # Código para leer una cadena
            cadena = """
                IN_STR """ + coincidencia.group(3)
            escribir(cadena)
            escribir("\n")

        elif re.match(patron_write, linea, re.VERBOSE):
            coincidencia = re.match(patron_write, linea, re.VERBOSE)
            # Código para escribir un valor entero
            cadena = "OUT " + coincidencia.group(1)
            escribir(cadena)
            escribir("\n")

        elif re.match(patron_write_cad, linea, re.VERBOSE):
            coincidencia = re.match(patron_write_cad, linea, re.VERBOSE)
            # Código para escribir una cadena
            cadena = "OUT_STR " + coincidencia.group(1)
            escribir(cadena)
            escribir("\n")

        elif re.match(patron_writeln, linea, re.VERBOSE):
            # Código para escribir un salto de línea
            cadena = """
                nl: DATA "\\n"
                OUT_STR /nl
            """
            escribir(cadena)
            escribir("\n")

        else:
            print (linea)
            escribir("ramon de mon")
        
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