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
bucles = 0
cads = None
cds = 0
contador_llamadas = 0 # Para generar etiquetas unicas de retorno
tamraact = None
es_vacia = False
contparam = 0

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
    ("[^"]*"|\{[^{}]*\}|[^,()]+)?\s*,\s*
    ("[^"]*"|\{[^{}]*\}|[^,()]+)?\s*,\s*
    ("[^"]*"|\{[^{}]*\}|[^,()]+)?\s*
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

patron_param_ref = r"""
\(PARAM_REF,\s*
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

patron_ret_halt = r"""
\(RETURN,\s*
    (-)  ,\s*
    (-)  ,\s*
    (-) 
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

p = r"\"\s*\""
ptloc = r"{VAR_LOCAL, (.+)}"
ptglob = r"{VAR_GLOBAL, (.+)}"
ptp = r"EtiqProc(\d+)"
ptf = r"EtiqFunc(\d+)"
ptm = r"main"


#________________________________________________________________________
# funciones

def leer():
    global archivo
    if archivo is None:
        archivo = open("cuartetos.txt", 'r')

    return archivo.readline()


# para las de escribir por terminal poner una reserva de memoria con RES
def declarar_cads(cadena, write):
    global cads, cds
        
    if cadena is not None and not re.match(p, cadena):

        if cads is None:
            cads = f"\ncadena{cds}:\tDATA " + cadena
        else:
            cads = cads + f"\ncadena{cds}:\tDATA " + cadena

    if write and cads is not None:
        cads += "\n\t\t\tEND"
        escribir(cads)




def leer_cadena_ens(cadena, escad):
    global bucles
    if escad:
        codobj = f"""
            MOVE #{cadena}, .R7
            DEC .R2
            DEC .R7
bucle{bucles}:	    INC .R2
            INC .R7
            MOVE [.R7], [.R2]
            CMP [.R7], #0
            BNZ $bucle{bucles}
        """
    else:
        codobj = f"""
            DEC .R3
            DEC .R2
bucle{bucles}:	    INC .R3
            INC .R2
            MOVE [.R2], [.R3]
            CMP [.R2], #0
            BNZ $bucle{bucles}
        """

    bucles += 1
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
            cad = f"\t\t\tADD #{re.match(ptglob, dir).group(1)}, .IY\n\t\t\tMOVE .A, .R{nreg}\n"
            nreg += 1
            escribir(cad)
        
        elif re.match(ptloc, dir):
            cad = f"\t\t\tADD #{re.match(ptloc, dir).group(1)}, .IX\n\t\t\tMOVE .A, .R{nreg}\n"
            nreg += 1
            escribir(cad)
    escribir("\n")


#________________________________________________________________________
# main

def main():
    global cds, contador_llamadas, contparam  # Añadir estas variables globales
    _calcprev.main() # calculo de la cabecera del ensamblador

    esFuncion = 0
    
    linea = leer()
    while linea:
        if re.match(patron_mul, linea, re.VERBOSE):
            coincidencia = re.match(patron_mul, linea, re.VERBOSE)
            transformar_dir(coincidencia.group(1), coincidencia.group(2), coincidencia.group(3))
            cadena = "\t\t\tMUL [.R2], [.R3]"
            escribir(cadena)
            escribir("\n")
            cadena = "\t\t\tMOVE .A, [.R4]"
            escribir(cadena)
            escribir("\n")
        
        elif re.match(patron_and, linea, re.VERBOSE):
            coincidencia = re.match(patron_and, linea, re.VERBOSE)
            transformar_dir(coincidencia.group(1), coincidencia.group(2), coincidencia.group(3))
            cadena = "\t\t\tAND .R2, .R3"
            escribir(cadena)
            escribir("\n")
            cadena = "\t\t\tMOVE .A, .R4"
            escribir(cadena)
            escribir("\n")

        elif re.match(patron_etiq, linea, re.VERBOSE):
            coincidencia = re.match(patron_etiq, linea, re.VERBOSE)
            aux = coincidencia.group(1)
            et = re.match(etiqueta, aux).group(1)
            if re.match(ptp, et):
                tamraact = _calcprev.coleccion[f"ra{int(re.match(ptp, et).group(1)) - 1}"]
                
            if re.match(ptf, et):
                tamraact = _calcprev.coleccion[f"ra{int(re.match(ptf, et).group(1)) - 1}"]
                
            if re.match(ptm, et):
                uc = list(_calcprev.coleccion.keys())[-1]
                tamraact = _calcprev.coleccion[uc]

            cadena = et +":"
            escribir(cadena)
            escribir("\n")
            
        elif re.match(patron_asig, linea, re.VERBOSE):
            coincidencia = re.match(patron_asig, linea, re.VERBOSE)
            if re.match(ptglob, coincidencia.group(1)) or re.match(ptloc, coincidencia.group(1)):
                transformar_dir(coincidencia.group(1), None, coincidencia.group(3))
                cadena = "\t\t\tMOVE [.R2], [.R3]"
                escribir(cadena)
            else:
                transformar_dir(None, None, coincidencia.group(3))
                escribir(f"\t\t\tMOVE #{coincidencia.group(1)}, [.R2]")
            escribir("\n")
            
        elif re.match(patron_asig_cad, linea, re.VERBOSE):
            coincidencia = re.match(patron_asig_cad, linea, re.VERBOSE)
            if re.match(ptglob, coincidencia.group(1)) or re.match(ptloc, coincidencia.group(1)):
                transformar_dir(coincidencia.group(1), None, coincidencia.group(3))
                if not es_vacia:
                    # transformar_dir(coincidencia.group(1), None, coincidencia.group(3))
                    leer_cadena_ens(None, False)
                else:
                    # transformar_dir(None, None, coincidencia.group(3))
                    escribir("\t\t\tMOVE #0, [.R2]\n")
                    escribir("\t\t\tMOVE [.R2], [.R3]\n")
                
            else:
                c = coincidencia.group(1)
                es_vacia = re.match(p, c)
                if not es_vacia:
                    transformar_dir(None, None, coincidencia.group(3))
                    leer_cadena_ens(f"cadena{cds}", True)
                    declarar_cads(coincidencia.group(1), False)
                    cds += 1

            escribir("\n")

        elif re.match(patron_goto, linea, re.VERBOSE):
            coincidencia = re.match(patron_goto, linea, re.VERBOSE)
            aux = coincidencia.group(3)
            cadena = "\t\t\tBR $"+re.match(etiqueta, aux).group(1)
            escribir(cadena)
            escribir("\n")
            
        elif re.match(patron_goto_may, linea, re.VERBOSE):
            coincidencia = re.match(patron_goto_may, linea, re.VERBOSE)
            transformar_dir(coincidencia.group(1), coincidencia.group(2), None)

            cadena = "\t\t\tCMP .R2, .R3"
            escribir(cadena)
            escribir("\n")
            aux = coincidencia.group(3)
            cadena = "\t\t\tBP $"+re.match(etiqueta, aux).group(1)
            escribir(cadena)
            escribir("\n")
            
        elif re.match(patron_goto_men, linea, re.VERBOSE):
            coincidencia = re.match(patron_goto_men, linea, re.VERBOSE)
            transformar_dir(coincidencia.group(1), coincidencia.group(2), None)
            cadena = "\t\t\tCMP .R2, .R3"
            escribir(cadena)
            escribir("\n")
            aux = coincidencia.group(3)
            cadena = "\t\t\tBN $"+re.match(etiqueta, aux, re.VERBOSE).group(1)
            escribir(cadena)
            escribir("\n")
            
        elif re.match(patron_goto_ig, linea, re.VERBOSE):
            coincidencia = re.match(patron_goto_ig, linea, re.VERBOSE)
            transformar_dir(coincidencia.group(1), coincidencia.group(2), None)
            cadena = "\t\t\tCMP .R2, .R3"
            escribir(cadena)
            escribir("\n")
            aux = coincidencia.group(3)
            cadena = "\t\t\tBZ $"+re.match(etiqueta, aux).group(1)
            escribir(cadena)
            escribir("\n")
            
        elif re.match(patron_goto_dist, linea, re.VERBOSE):
            coincidencia = re.match(patron_goto_dist, linea, re.VERBOSE)
            transformar_dir(coincidencia.group(1), coincidencia.group(2), None)
            cadena = "\t\t\tCMP .R2, .R3"
            escribir(cadena)
            escribir("\n")
            aux = coincidencia.group(3)
            cadena = "\t\t\tBNZ $"+re.match(etiqueta, aux).group(1)
            escribir(cadena)
            escribir("\n")
            
        elif re.match(patron_goto_may_ig, linea, re.VERBOSE):
            coincidencia = re.match(patron_goto_may_ig, linea, re.VERBOSE)
            transformar_dir(coincidencia.group(1), coincidencia.group(2), None)
            cadena = "\t\t\tCMP .R2, .R3"
            escribir(cadena)
            escribir("\n")
            aux = coincidencia.group(3)
            cadena = "\t\t\tBZ $"+re.match(etiqueta, aux).group(1)
            escribir(cadena)
            escribir("\n")
            aux = coincidencia.group(3)
            cadena = "\t\t\tBP $"+re.match(etiqueta, aux).group(1)
            escribir(cadena)
            escribir("\n")
            
        elif re.match(patron_goto_men_ig, linea, re.VERBOSE):
            coincidencia = re.match(patron_goto_men_ig, linea, re.VERBOSE)
            transformar_dir(coincidencia.group(1), coincidencia.group(2), None)
            cadena = "\t\t\tCMP .R2, .R3"            
            escribir(cadena)
            escribir("\n")
            aux = coincidencia.group(3)
            cadena = "\t\t\tBZ $"+re.match(etiqueta, aux).group(1)
            escribir(cadena)
            escribir("\n")
            aux = coincidencia.group(3)
            cadena = "\t\t\tBN $"+re.match(etiqueta, aux).group(1)
            escribir(cadena)
            escribir("\n")

        elif re.match(patron_param, linea, re.VERBOSE):
            coincidencia = re.match(patron_param, linea, re.VERBOSE)
            transformar_dir(coincidencia.group(1), None, None)
            t = 2 + contparam
            contparam += 1
            cadena = f"\t\t\tADD #{tamraact}, .IX\n\t\t\tADD #{t}, .A\n\t\t\tMOVE [.R2], [.A]\n"

            escribir(cadena)
            escribir("\n")
            
        elif re.match(patron_param_ref, linea, re.VERBOSE):
            coincidencia = re.match(patron_param_ref, linea, re.VERBOSE)
            transformar_dir(coincidencia.group(1), None, None)
            t = 2 + contparam
            contparam += 1
            cadena = f"\t\t\tADD #{tamraact}, .IX\n\t\t\tADD #{t}, .A\n\t\t\tMOVE .R2, [.A]\n"

            escribir(cadena)
            escribir("\n")
        
        elif re.match(patron_param_cad, linea, re.VERBOSE):
            coincidencia = re.match(patron_param_cad, linea, re.VERBOSE)
            # MIRAR ESTO PORQUE CREO QUE HAY QUE COPIAR LA CADENA EN LUGAR DEL MOVE
            # creo q no se tiene en cuenta para la practica
            # *********************************************************************
            # *********************************************************************
            # *********************************************************************
            transformar_dir(coincidencia.group(1), None, None)
            
            cadena = "\t\t\tMOVE .R2"
            escribir(cadena)
            escribir("\n")
        
        elif re.match(patron_ret, linea, re.VERBOSE):  #chequea si es el del main o de una funcion
            coincidencia = re.match(patron_ret, linea, re.VERBOSE)
            linea = leer()
            cadena = "\n\t\t\tBR [.IX]\n"
            escribir(cadena)
            # continue

        elif re.match(patron_ret_halt, linea, re.VERBOSE):  #chequea si es el del main o de una funcion
            coincidencia = re.match(patron_ret_halt, linea, re.VERBOSE)
            cadena = "\t\t\tHALT"
            escribir(cadena)
            escribir("\n")
            # break
            

        elif re.match(patron_ret_cad, linea, re.VERBOSE):
            coincidencia = re.match(patron_ret_cad, linea, re.VERBOSE)
            if coincidencia.group(2) != "_":
                cadena = "\t\t\tMOVE "+coincidencia.group(2)+", .A"
                escribir(cadena)
                escribir("\n")
            cadena = "\t\t\tRET"
            escribir(cadena)
            escribir("\n")
        
        elif re.match(patron_ret_ent, linea, re.VERBOSE):
            coincidencia = re.match(patron_ret_ent, linea, re.VERBOSE)
            c = re.match(ptglob, coincidencia.group(3))
            if c is None:
                c = re.match(ptloc, coincidencia.group(3))
            # *********************************************************************
            # *********************************************************************
            # *********************************************************************
            cadena = f"\t\t\tSUB #{tamraact}, #1\n\t\t\tADD .A, .IX\n\t\t\tMOVE #{c.group(1)}[.IX], [.A]\n\t\t\tBR [.IX]\n"
            escribir(cadena)
            escribir("\n")
            
        elif re.match(patron_call, linea, re.VERBOSE):
            coincidencia = re.match(patron_call, linea, re.VERBOSE)
            # *********************************************************************
            # *********************************************************************
            # *********************************************************************
            et = coincidencia.group(1)
            if re.match(ptp, et):
                tam_ra_llamado = _calcprev.coleccion[f"ra{int(re.match(ptp, et).group(1)) - 1}"]
                
            if re.match(ptf, et):
                tam_ra_llamado = _calcprev.coleccion[f"ra{int(re.match(ptf, et).group(1)) - 1}"]

            cadena = f"""
            MOVE #dir_ret{contador_llamadas}, #{tamraact}[.IX]
            MOVE #{tamraact + 1}[.IX], .R9 
            MOVE [.R9], .R9

            MOVE [.R9], .R9
            ADD #{tam_ra_llamado}, .IX
            INC .A
            MOVE .R9, [.A]
            ADD #{tam_ra_llamado}, .IX
            MOVE .A, .IX
            BR /{et}

dir_ret{contador_llamadas}:   SUB .IX, #{tam_ra_llamado}
            MOVE .A, .IX
            """
            escribir(cadena)
            escribir("\n")
            contador_llamadas += 1
            
        elif re.match(patron_call_fun, linea, re.VERBOSE):
            coincidencia = re.match(patron_call_fun, linea, re.VERBOSE)
            # *********************************************************************
            # *********************************************************************
            # *********************************************************************
            et = coincidencia.group(1)
            desp = re.match(ptloc, coincidencia.group(3)).group(1)
            if re.match(ptp, et):
                tam_ra_llamado = _calcprev.coleccion[f"ra{int(re.match(ptp, et).group(1)) - 1}"]
                
            if re.match(ptf, et):
                tam_ra_llamado = _calcprev.coleccion[f"ra{int(re.match(ptf, et).group(1)) - 1}"]

            cadena = f"""
            MOVE #dir_ret{contador_llamadas}, #{tamraact}[.IX]
            MOVE #{tamraact + 1}[.IX], .R9 
            MOVE [.R9], .R9

            MOVE [.R9], .R9

            ADD #{tam_ra_llamado}, .IX
            INC .A
            MOVE .R9, [.A]
            ADD #{tam_ra_llamado}, .IX
            MOVE .A, .IX
            BR /{et}

dir_ret{contador_llamadas}:   SUB #{tam_ra_llamado}, #1
            ADD .A, .IX
            MOVE [.A], .R9

            SUB .IX, #{tam_ra_llamado}
            MOVE .A, .IX

            MOVE .R9, #{desp}[.IX]
            """
            escribir(cadena)
            escribir("\n")
            contador_llamadas += 1
        
        elif re.match(patron_call_fun_cad, linea, re.VERBOSE):
            coincidencia = re.match(patron_call_fun_cad, linea, re.VERBOSE)
            # *********************************************************************
            # *********************************************************************
            # *********************************************************************
            et = coincidencia.group(1)
            if re.match(ptp, et):
                tam_ra_llamado = _calcprev.coleccion[f"ra{int(re.match(ptp, et).group(1)) - 1}"]
                
            if re.match(ptf, et):
                tam_ra_llamado = _calcprev.coleccion[f"ra{int(re.match(ptf, et).group(1)) - 1}"]

            cadena = f"""
            MOVE #dir_ret{contador_llamadas}, #{tamraact}[.IX]
            MOVE #{tamraact + 1}[.IX], .R9 
            MOVE [.R9], .R9

            MOVE [.R9], .R9

            ADD #{tam_ra_llamado}, .IX
            INC .A
            MOVE .R9, [.A]
            ADD #{tam_ra_llamado}, .IX
            MOVE .A, .IX
            BR /{et}

dir_ret{contador_llamadas}:   SUB #{tam_ra_llamado}, #1
            ADD .A, .IX
            MOVE [.A], .R9

            SUB .IX, #{tam_ra_llamado}
            MOVE .A, .IX

            MOVE .R9, #32[.IX]
            """
            escribir(cadena)
            escribir("\n")
            contador_llamadas += 1

        # Para la sección de procesamiento de READ
        elif re.match(patron_read, linea, re.VERBOSE):
            coincidencia = re.match(patron_read, linea, re.VERBOSE)
            # Usar ININT en lugar de IN para leer enteros
            cadena = """
                ININT """ + coincidencia.group(3)
            escribir(cadena)
            escribir("\n")

        elif re.match(patron_read_cad, linea, re.VERBOSE):
            coincidencia = re.match(patron_read_cad, linea, re.VERBOSE)
            # Usar INSTR en lugar de IN_STR para leer cadenas
            cadena = """
                INSTR """ + coincidencia.group(3)
            escribir(cadena)
            escribir("\n")

        elif re.match(patron_write, linea, re.VERBOSE):
            coincidencia = re.match(patron_write, linea, re.VERBOSE)
            # Usar WRINT en lugar de OUT para escribir enteros
            cadena = "\t\t\tWRINT " + coincidencia.group(1)
            escribir(cadena)
            escribir("\n")

        elif re.match(patron_write_cad, linea, re.VERBOSE):
            coincidencia = re.match(patron_write_cad, linea, re.VERBOSE)
            # Usar WRSTR en lugar de OUT_STR para escribir cadenas
            cadena = "\t\t\tWRSTR " + coincidencia.group(1)
            escribir(cadena)
            escribir("\n")

        elif re.match(patron_writeln, linea, re.VERBOSE):
            # Usar WRSTR con una cadena de salto de línea
            # Declaramos la cadena de salto de línea en la sección de datos
            cadena = """
                WRSTR /nl
            """
            escribir(cadena)
            escribir("\n")
            # Asegurarse de que "nl" esté declarado en la sección de datos
            if cads is None:
                cads = "\nnl:\tDATA \"\\n\\0\""
            else:
                # Verificar si ya está declarado para evitar duplicados
                if "\nnl:" not in cads:
                    cads += "\nnl:\tDATA \"\\n\\0\""
        
        linea = leer()
    escribir("\t\t\tHALT\n")
    declarar_cads(None, True)

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