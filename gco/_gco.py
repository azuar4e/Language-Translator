#________________________________________________________________________
#imports 
import sys
import subprocess
import re
from _ens import escribir
import _calcprev
from pprint import pprint

#________________________________________________________________________
# resto de variables
archivo = None
bucles = 0
cads = None
cds = 0
contador_llamadas = 0 # Para generar etiquetas unicas de retorno
tamraact = None
raact = None
es_vacia = False
contparam = 0
where = ""
sumra = 0
contmin = 0
param_min = []

#________________________________________________________________________
# patrones

patron_mul = r"""
\(MUL,\s*
    ((?:\{[^{}]*\}|[^,()])+)  ,\s*
    ((?:\{[^{}]*\}|[^,()])+)  ,\s*
    ((?:\{[^{}]*\}|[^,()])+) 
\)
"""

# patron_mul_ptr_1 = r"""
# \(MUL_PTR_1,\s*
#     ((?:\{[^{}]*\}|[^,()])+)  ,\s*
#     ((?:\{[^{}]*\}|[^,()])+)  ,\s*
#     ((?:\{[^{}]*\}|[^,()])+) 
# \)
# """

# patron_mul_ptr_2 = r"""
# \(MUL_PTR_2,\s*
#     ((?:\{[^{}]*\}|[^,()])+)  ,\s*
#     ((?:\{[^{}]*\}|[^,()])+)  ,\s*
#     ((?:\{[^{}]*\}|[^,()])+) 
# \)
# """

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

# patron_asig_ptr = r"""
# \(ASIG_PTR,\s*
#     ((?:\{[^{}]*\}|[^,()])+)  ,\s*
#     ((?:\{[^{}]*\}|[^,()])+)  ,\s*
#     ((?:\{[^{}]*\}|[^,()])+) 
# \)
# """

# patron_asig_cad_ptr = r"""
# \(ASIG_CAD_PTR,\s*
#     ("[^"]*"|\{[^{}]*\}|[^,()]+)?\s*,\s*
#     ("[^"]*"|\{[^{}]*\}|[^,()]+)?\s*,\s*
#     ("[^"]*"|\{[^{}]*\}|[^,()]+)?\s*
# \)
# """

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
\(GOTO_MEN,\s*
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
\(INPUT_ENT,\s*
    ((?:\{[^{}]*\}|[^,()])+)  ,\s*
    ((?:\{[^{}]*\}|[^,()])+)  ,\s*
    ((?:\{[^{}]*\}|[^,()])+) 
\)
"""

patron_read_cad = r"""
\(INPUT_CAD,\s*
    ((?:\{[^{}]*\}|[^,()])+)  ,\s*
    ((?:\{[^{}]*\}|[^,()])+)  ,\s*
    ((?:\{[^{}]*\}|[^,()])+) 
\)
"""

patron_read_ref = r"""
\(INPUT_ENT_REF,\s*
    ((?:\{[^{}]*\}|[^,()])+)  ,\s*
    ((?:\{[^{}]*\}|[^,()])+)  ,\s*
    ((?:\{[^{}]*\}|[^,()])+) 
\)
"""

patron_read_cad_ref = r"""
\(INPUT_CAD_REF,\s*
    ((?:\{[^{}]*\}|[^,()])+)  ,\s*
    ((?:\{[^{}]*\}|[^,()])+)  ,\s*
    ((?:\{[^{}]*\}|[^,()])+) 
\)
"""

patron_write = r"""
\(PRINT_ENT,\s*
    ((?:\{[^{}]*\}|[^,()])+)  ,\s*
    ((?:\{[^{}]*\}|[^,()])+)  ,\s*
    ((?:\{[^{}]*\}|[^,()])+) 
\)
"""

patron_write_cad = r"""
\(PRINT_CAD,\s*
    ((?:\{[^{}]*\}|[^,()])+)  ,\s*
    ((?:\{[^{}]*\}|[^,()])+)  ,\s*
    ((?:\{[^{}]*\}|[^,()])+) 
\)
"""

patron_writeln = r"""
\(PRINT_ENT_LN,\s*
    ((?:\{[^{}]*\}|[^,()])+)  ,\s*
    ((?:\{[^{}]*\}|[^,()])+)  ,\s*
    ((?:\{[^{}]*\}|[^,()])+) 
\)
"""

patron_writeln_cad = r"""
\(PRINT_CAD_LN,\s*
    ((?:\{[^{}]*\}|[^,()])+)  ,\s*
    ((?:\{[^{}]*\}|[^,()])+)  ,\s*
    ((?:\{[^{}]*\}|[^,()])+) 
\)
"""

patron_write_ref = r"""
\(PRINT_ENT_REF,\s*
    ((?:\{[^{}]*\}|[^,()])+)  ,\s*
    ((?:\{[^{}]*\}|[^,()])+)  ,\s*
    ((?:\{[^{}]*\}|[^,()])+) 
\)
"""

patron_write_cad_ref = r"""
\(PRINT_CAD_REF,\s*
    ((?:\{[^{}]*\}|[^,()])+)  ,\s*
    ((?:\{[^{}]*\}|[^,()])+)  ,\s*
    ((?:\{[^{}]*\}|[^,()])+) 
\)
"""

patron_writeln_ref = r"""
\(PRINT_ENT_LN_REF,\s*
    ((?:\{[^{}]*\}|[^,()])+)  ,\s*
    ((?:\{[^{}]*\}|[^,()])+)  ,\s*
    ((?:\{[^{}]*\}|[^,()])+) 
\)
"""

patron_writeln_cad_ref = r"""
\(PRINT_CAD_LN_REF,\s*
    ((?:\{[^{}]*\}|[^,()])+)  ,\s*
    ((?:\{[^{}]*\}|[^,()])+)  ,\s*
    ((?:\{[^{}]*\}|[^,()])+) 
\)
"""

patron_min = r"""
\(MIN,\s*
    ((?:\{[^{}]*\}|[^,()])+)  ,\s*
    ((?:\{[^{}]*\}|[^,()])+)  ,\s*
    ((?:\{[^{}]*\}|[^,()])+)
\)
"""

patron_param_min = r"""
\(PARAM_MIN,\s*
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
            cads = f"\ncadena{cds}:\t" + cadena
        else:
            cads = cads + f"\ncadena{cds}:\t" + cadena

    if write and cads is not None:
        # cads += "\n\t\t\tEND"
        cads += "\n\n"
        escribir(cads)
        return True




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
    
def paramcad(des, desra):
    global bucles
    codobj = f"""
            ADD #{des}, .IX
            MOVE .A, .R2
            ADD #{desra}, .IX
            MOVE .A, .R3
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
        
        elif re.match(ptloc, dir): # al ser local se le suma el tamaño del EM y PA
            desp = int(re.match(ptloc, dir).group(1)) + 1
            cad = f"\t\t\tADD #{desp}, .IX\n\t\t\tMOVE .A, .R{nreg}\n"
            if raact in _calcprev.referencias and desp in _calcprev.referencias[raact]:
                cad += f"\t\t\tMOVE [.R{nreg}], .R{nreg}\n"
                
            nreg += 1
            escribir(cad)
    escribir("\n")


#________________________________________________________________________
# main

def main():
    global cds, contador_llamadas, contparam, where, contmin, param_min, raact
    _calcprev.main()

    linea = leer()
    while linea:
        if re.match(patron_mul, linea, re.VERBOSE):
            coincidencia = re.match(patron_mul, linea, re.VERBOSE)
            transformar_dir(coincidencia.group(1), coincidencia.group(2), coincidencia.group(3))
            cadena = "\t\t\tMUL [.R2], [.R3]\n"
            escribir(cadena)
            cadena = "\t\t\tMOVE .A, [.R4]\n"
            escribir(cadena)
            
        # elif re.match(patron_mul_ptr_1, linea, re.VERBOSE):
        #     coincidencia = re.match(patron_mul_ptr_1, linea, re.VERBOSE)
        #     transformar_dir(coincidencia.group(1), coincidencia.group(2), coincidencia.group(3))
        #     cadena = "\t\t\tMOVE [.R2], .R2\n"
        #     escribir(cadena)
        #     cadena = "\t\t\tMUL [.R2], [.R3]\n"
        #     escribir(cadena)
        #     cadena = "\t\t\tMOVE .A, [.R4]\n"
        #     escribir(cadena)

        # elif re.match(patron_mul_ptr_2, linea, re.VERBOSE):
        #     coincidencia = re.match(patron_mul_ptr_2, linea, re.VERBOSE)
        #     transformar_dir(coincidencia.group(1), coincidencia.group(2), coincidencia.group(3))
        #     cadena = "\t\t\tMOVE [.R3], .R3\n"
        #     escribir(cadena)
        #     cadena = "\t\t\tMUL [.R2], [.R3]\n"
        #     escribir(cadena)
        #     cadena = "\t\t\tMOVE .A, [.R4]\n"
        #     escribir(cadena)
        
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
                raact = f"ra{int(re.match(ptp, et).group(1)) - 1}"
                where = "procedure"
                
            if re.match(ptf, et):
                tamraact = _calcprev.coleccion[f"ra{int(re.match(ptf, et).group(1)) - 1}"]
                raact = f"ra{int(re.match(ptf, et).group(1)) - 1}"
                where = "function"

            if re.match(ptm, et):
                uc = list(_calcprev.coleccion.keys())[-1]
                tamraact = _calcprev.coleccion[uc]
                raact = uc
                where = "main"

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
                # cadsdict[coincidencia.group(3)] = cadsdict[coincidencia.group(1)]
                if not es_vacia:
                    leer_cadena_ens(None, False)
                else:
                    escribir("\t\t\tMOVE #0, [.R2]\n")
                    escribir("\t\t\tMOVE [.R2], [.R3]\n")
                
            else:
                c = coincidencia.group(1)
                es_vacia = re.match(p, c)
                if not es_vacia:
                    transformar_dir(None, None, coincidencia.group(3))
                    leer_cadena_ens(f"cadena{cds}", True)
                    declarar_cads("DATA "+coincidencia.group(1), False)
                    # cadsdict[coincidencia.group(3)] = f"cadena{cds}"
                    cds += 1

            escribir("\n")

        # elif re.match(patron_asig_ptr, linea, re.VERBOSE):
        #     coincidencia = re.match(patron_asig_ptr, linea, re.VERBOSE)
        #     if re.match(ptglob, coincidencia.group(1)) or re.match(ptloc, coincidencia.group(1)):
        #         transformar_dir(coincidencia.group(1), None, coincidencia.group(3))
        #         cadena = "\t\t\tMOVE [.R3], .R3\n"
        #         cadena += "\t\t\tMOVE [.R2], [.R3]"
        #         escribir(cadena)
        #     else:
        #         transformar_dir(None, None, coincidencia.group(3))
        #         escribir(f"\t\t\tMOVE #{coincidencia.group(1)}, [.R2]")
        #     escribir("\n")
            
        # elif re.match(patron_asig_cad_ptr, linea, re.VERBOSE):
        #     coincidencia = re.match(patron_asig_cad_ptr, linea, re.VERBOSE)
        #     if re.match(ptglob, coincidencia.group(1)) or re.match(ptloc, coincidencia.group(1)):
        #         transformar_dir(coincidencia.group(1), None, coincidencia.group(3))

        #         if not es_vacia:
        #             cadena = "\t\t\tMOVE [.R3], .R3\n"
        #             escribir(cadena)
        #             leer_cadena_ens(None, False)
        #         else:
        #             escribir("\t\t\tMOVE #0, [.R2]\n")
        #             escribir("\t\t\tMOVE [.R2], [.R3]\n")
                
        #     else:
        #         c = coincidencia.group(1)
        #         es_vacia = re.match(p, c)
        #         if not es_vacia:
        #             transformar_dir(None, None, coincidencia.group(3))
        #             cadena = "\t\t\tMOVE [.R3], .R3\n"
        #             escribir(cadena)
        #             leer_cadena_ens(f"cadena{cds}", True)
        #             declarar_cads("DATA "+coincidencia.group(1), False)
        #             # cadsdict[coincidencia.group(3)] = f"cadena{cds}"
        #             cds += 1

        #     escribir("\n")

        elif re.match(patron_goto, linea, re.VERBOSE):
            coincidencia = re.match(patron_goto, linea, re.VERBOSE)
            aux = coincidencia.group(3)
            cadena = "\t\t\tBR $"+re.match(etiqueta, aux).group(1)
            escribir(cadena)
            escribir("\n")
            
        elif re.match(patron_goto_may, linea, re.VERBOSE):
            coincidencia = re.match(patron_goto_may, linea, re.VERBOSE)
            if (not re.match(ptglob, coincidencia.group(1)) and not re.match(ptloc, coincidencia.group(1))) or (not re.match(ptglob, coincidencia.group(2)) and not re.match(ptloc, coincidencia.group(2))):
                if re.match(ptglob, coincidencia.group(1)) or re.match(ptloc, coincidencia.group(1)):
                    transformar_dir(coincidencia.group(1), None, None)
                    ent = coincidencia.group(2)
                else:
                    transformar_dir(None, coincidencia.group(2), None)
                    ent = coincidencia.group(1)
                cadena = f"\t\t\tCMP [.R2], #{ent}"
            else:
                transformar_dir(coincidencia.group(1), coincidencia.group(2), None)
                cadena = "\t\t\tCMP [.R2], [.R3]"
            escribir(cadena)
            escribir("\n")
            aux = coincidencia.group(3)
            cadena = "\t\t\tBP $"+re.match(etiqueta, aux).group(1)
            escribir(cadena)
            escribir("\n")
            
        elif re.match(patron_goto_men, linea, re.VERBOSE):
            coincidencia = re.match(patron_goto_men, linea, re.VERBOSE)
            if (not re.match(ptglob, coincidencia.group(1)) and not re.match(ptloc, coincidencia.group(1))) or (not re.match(ptglob, coincidencia.group(2)) and not re.match(ptloc, coincidencia.group(2))):
                if re.match(ptglob, coincidencia.group(1)) or re.match(ptloc, coincidencia.group(1)):
                    transformar_dir(coincidencia.group(1), None, None)
                    ent = coincidencia.group(2)
                else:
                    transformar_dir(None, coincidencia.group(2), None)
                    ent = coincidencia.group(1)
                cadena = f"\t\t\tCMP [.R2], #{ent}"
            else:
                transformar_dir(coincidencia.group(1), coincidencia.group(2), None)
                cadena = "\t\t\tCMP [.R2], [.R3]"
            escribir(cadena)
            escribir("\n")
            aux = coincidencia.group(3)
            cadena = "\t\t\tBN $"+re.match(etiqueta, aux, re.VERBOSE).group(1)
            escribir(cadena)
            escribir("\n")
            
        elif re.match(patron_goto_ig, linea, re.VERBOSE):
            coincidencia = re.match(patron_goto_ig, linea, re.VERBOSE)
            if (not re.match(ptglob, coincidencia.group(1)) and not re.match(ptloc, coincidencia.group(1))) or (not re.match(ptglob, coincidencia.group(2)) and not re.match(ptloc, coincidencia.group(2))):
                if re.match(ptglob, coincidencia.group(1)) or re.match(ptloc, coincidencia.group(1)):
                    transformar_dir(coincidencia.group(1), None, None)
                    ent = coincidencia.group(2)
                else:
                    transformar_dir(None, coincidencia.group(2), None)
                    ent = coincidencia.group(1)
                cadena = f"\t\t\tCMP [.R2], #{ent}"
            else:
                transformar_dir(coincidencia.group(1), coincidencia.group(2), None)
                cadena = "\t\t\tCMP [.R2], [.R3]"
            escribir(cadena)
            escribir("\n")
            aux = coincidencia.group(3)
            cadena = "\t\t\tBZ $"+re.match(etiqueta, aux).group(1)
            escribir(cadena)
            escribir("\n")
            
        elif re.match(patron_goto_dist, linea, re.VERBOSE):
            coincidencia = re.match(patron_goto_dist, linea, re.VERBOSE)
            if (not re.match(ptglob, coincidencia.group(1)) and not re.match(ptloc, coincidencia.group(1))) or (not re.match(ptglob, coincidencia.group(2)) and not re.match(ptloc, coincidencia.group(2))):
                if re.match(ptglob, coincidencia.group(1)) or re.match(ptloc, coincidencia.group(1)):
                    transformar_dir(coincidencia.group(1), None, None)
                    ent = coincidencia.group(2)
                else:
                    transformar_dir(None, coincidencia.group(2), None)
                    ent = coincidencia.group(1)
                cadena = f"\t\t\tCMP [.R2], #{ent}"
            else:
                transformar_dir(coincidencia.group(1), coincidencia.group(2), None)
                cadena = "\t\t\tCMP [.R2], [.R3]"
            escribir(cadena)
            escribir("\n")
            aux = coincidencia.group(3)
            cadena = "\t\t\tBNZ $"+re.match(etiqueta, aux).group(1)
            escribir(cadena)
            escribir("\n")
            
        elif re.match(patron_goto_may_ig, linea, re.VERBOSE):
            coincidencia = re.match(patron_goto_may_ig, linea, re.VERBOSE)
            if (not re.match(ptglob, coincidencia.group(1)) and not re.match(ptloc, coincidencia.group(1))) or (not re.match(ptglob, coincidencia.group(2)) and not re.match(ptloc, coincidencia.group(2))):
                if re.match(ptglob, coincidencia.group(1)) or re.match(ptloc, coincidencia.group(1)):
                    transformar_dir(coincidencia.group(1), None, None)
                    ent = coincidencia.group(2)
                else:
                    transformar_dir(None, coincidencia.group(2), None)
                    ent = coincidencia.group(1)
                cadena = f"\t\t\tCMP [.R2], #{ent}"
            else:
                transformar_dir(coincidencia.group(1), coincidencia.group(2), None)
                cadena = "\t\t\tCMP [.R2], [.R3]"
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
            if (not re.match(ptglob, coincidencia.group(1)) and not re.match(ptloc, coincidencia.group(1))) or (not re.match(ptglob, coincidencia.group(2)) and not re.match(ptloc, coincidencia.group(2))):
                if re.match(ptglob, coincidencia.group(1)) or re.match(ptloc, coincidencia.group(1)):
                    transformar_dir(coincidencia.group(1), None, None)
                    ent = coincidencia.group(2)
                else:
                    transformar_dir(None, coincidencia.group(2), None)
                    ent = coincidencia.group(1)
                cadena = f"\t\t\tCMP [.R2], #{ent}"
            else:
                transformar_dir(coincidencia.group(1), coincidencia.group(2), None)
                cadena = "\t\t\tCMP [.R2], [.R3]"          
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
            t = 1 + contparam
            contparam += 1
            cadena = f"\t\t\tADD #{tamraact}, .IX\n\t\t\tADD #{t}, .A\n\t\t\tMOVE [.R2], [.A]\n"

            escribir(cadena)
            escribir("\n")
            
        elif re.match(patron_param_ref, linea, re.VERBOSE):
            coincidencia = re.match(patron_param_ref, linea, re.VERBOSE)
            transformar_dir(coincidencia.group(1), None, None)
            t = 1 + contparam
            contparam += 1
            cadena = f"\t\t\tADD #{tamraact}, .IX\n\t\t\tADD #{t}, .A\n\t\t\tMOVE .R2, [.A]\n"
            escribir(cadena)
            escribir("\n")
        
        elif re.match(patron_param_cad, linea, re.VERBOSE):

            coincidencia = re.match(patron_param_cad, linea, re.VERBOSE)
            if not es_vacia:
                t = contparam + 1 + tamraact
                if re.match(ptloc, coincidencia.group(1)):
                    des = int(re.match(ptloc, coincidencia.group(1)).group(1)) + 1
                else:
                    des = int(re.match(ptglob, coincidencia.group(1)).group(1))
                paramcad(des, t)
                contparam += 64
                # cds += 1

            escribir("\n")
        
        elif re.match(patron_ret, linea, re.VERBOSE):  #chequea si es el del main o de una funcion
            if where == "main":
                cadena = "\n\t\t\tHALT\n"
            else:
                cadena = "\n\t\t\tBR [.IX]\n"
            escribir(cadena)

        elif re.match(patron_ret_cad, linea, re.VERBOSE):
            coincidencia = re.match(patron_ret_cad, linea, re.VERBOSE)
            c = re.match(ptglob, coincidencia.group(3))
            if c is None:
                c = re.match(ptloc, coincidencia.group(3))
                codobj = f"\t\t\tADD #{int(c.group(1))+1}, .IX\n\t\t\tMOVE .A, .R2"
            else:
                codobj = f"ADD #{int(c.group(1))}, .IY\n\t\t\tMOVE .A, .R2"
            escribir(codobj)
            desp = int(c.group(1)) + 1
            cadena = f"\n\t\t\tSUB #{tamraact}, #64\n\t\t\tADD .A, .IX\n\t\t\tMOVE .A, .R3"
            escribir(cadena)
            leer_cadena_ens(None, False)
            cadena = "\n\t\t\tBR [.IX]\n"
            escribir(cadena)
        
        elif re.match(patron_ret_ent, linea, re.VERBOSE):
            coincidencia = re.match(patron_ret_ent, linea, re.VERBOSE)
            c = re.match(ptglob, coincidencia.group(3))
            if c is None:
                c = re.match(ptloc, coincidencia.group(3))
            # *********************************************************************
            # *********************************************************************
            # *********************************************************************
            desp = int(c.group(1)) + 1
            cadena = f"\t\t\tSUB #{tamraact}, #1\n\t\t\tADD .A, .IX\n\t\t\tMOVE #{desp}[.IX], [.A]\n\t\t\tBR [.IX]\n"
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
            ADD #{tamraact}, .IX
            MOVE #dir_ret{contador_llamadas}, [.A]
            
            ADD #{tamraact}, .IX
            MOVE .A, .IX
            BR /{et}

dir_ret{contador_llamadas}:   SUB .IX, #{tamraact}
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
            desp = int(re.match(ptloc, coincidencia.group(3)).group(1)) + 1
            if re.match(ptp, et):
                tam_ra_llamado = _calcprev.coleccion[f"ra{int(re.match(ptp, et).group(1)) - 1}"]
                
            if re.match(ptf, et):
                tam_ra_llamado = _calcprev.coleccion[f"ra{int(re.match(ptf, et).group(1)) - 1}"]

            cadena = f"""
            ADD #{tamraact}, .IX
            MOVE #dir_ret{contador_llamadas}, [.A]

            MOVE .A, .IX
            BR /{et}

dir_ret{contador_llamadas}:   SUB #{tam_ra_llamado}, #1
            ADD .A, .IX
            MOVE [.A], .R9

            SUB .IX, #{tamraact}
            MOVE .A, .IX

            ADD #{desp}, .IX
            MOVE .R9, [.A]
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
            ADD #{tamraact}, .IX
            MOVE #dir_ret{contador_llamadas}, [.A]

            MOVE .A, .IX
            BR /{et}

dir_ret{contador_llamadas}:   SUB #{tam_ra_llamado}, #64
            ADD .A, .IX
            MOVE .A, .R2

            SUB .IX, #{tamraact}
            MOVE .A, .IX
            """
            escribir(cadena)
            c = coincidencia.group(3)
            
            if re.match(ptglob, c):
                cad = f"\n\t\t\tADD #{re.match(ptglob, c).group(1)}, .IY\n\t\t\tMOVE .A, .R3\n"
                escribir(cad)
            
            elif re.match(ptloc, c):
                desp = int(re.match(ptloc, c).group(1)) + 1
                cad = f"\n\t\t\tADD #{desp}, .IX\n\t\t\tMOVE .A, .R3\n"
                escribir(cad)
            leer_cadena_ens(None, False)
            contador_llamadas += 1

        elif re.match(patron_read, linea, re.VERBOSE):
            coincidencia = re.match(patron_read, linea, re.VERBOSE)
            if re.match(ptglob, coincidencia.group(1)):
                des = int(re.match(ptglob, coincidencia.group(1)).group(1))
                cadena = f"\t\t\tADD #{des}, .IY\n"
            else:
                des = int(re.match(ptloc, coincidencia.group(1)).group(1)) + 1
                cadena = f"\t\t\tADD #{des}, .IX\n"
            cadena += "\t\t\tINIT_INT [.A]"
            escribir(cadena)
            escribir("\n")

        elif re.match(patron_read_cad, linea, re.VERBOSE):
            coincidencia = re.match(patron_read_cad, linea, re.VERBOSE)
            declarar_cads("RES 500", False)
            cadena = f"\n\t\t\tINSTR /cadena{cds}\n"
            escribir(cadena)
            transformar_dir(None, None, coincidencia.group(3))
            leer_cadena_ens(f"cadena{cds}", True)
            cds += 1
            escribir("\n")
            
        elif re.match(patron_read_ref, linea, re.VERBOSE):
            coincidencia = re.match(patron_read_ref, linea, re.VERBOSE)
            if re.match(ptglob, coincidencia.group(1)):
                des = int(re.match(ptglob, coincidencia.group(1)).group(1))
                cadena = f"\t\t\tADD #{des}, .IY\n"
                cadena += "\t\t\tMOVE [.A], .A\n"
            else:
                des = int(re.match(ptloc, coincidencia.group(1)).group(1)) + 1
                cadena = f"\t\t\tADD #{des}, .IX\n"
                cadena += "\t\t\tMOVE [.A], .A\n"
            cadena += "\t\t\tINIT_INT [.A]"
            escribir(cadena)
            escribir("\n")

        elif re.match(patron_read_cad_ref, linea, re.VERBOSE):
            coincidencia = re.match(patron_read_cad_ref, linea, re.VERBOSE)
            declarar_cads("RES 500", False)
            cadena = f"\n\t\t\tINSTR /cadena{cds}\n"
            escribir(cadena)
            transformar_dir(None, None, coincidencia.group(3))
            # cadena = "\t\t\tMOVE [.R2], .R2\n"
            # escribir(cadena)
            leer_cadena_ens(f"cadena{cds}", True)
            cds += 1
            escribir("\n")

        elif re.match(patron_write, linea, re.VERBOSE):
            coincidencia = re.match(patron_write, linea, re.VERBOSE)
            # Usar WRINT en lugar de OUT para escribir enteros
            if re.match(ptglob, coincidencia.group(1)):
                des = int(re.match(ptglob, coincidencia.group(1)).group(1))
                cadena = f"\t\t\tADD #{des}, .IY\n"

            else:
                des = int(re.match(ptloc, coincidencia.group(1)).group(1)) + 1
                cadena = f"\t\t\tADD #{des}, .IX\n"

            cadena += "\t\t\tWRINT [.A]"
            escribir(cadena)
            escribir("\n")

        elif re.match(patron_write_cad, linea, re.VERBOSE):
            coincidencia = re.match(patron_write_cad, linea, re.VERBOSE)
            
            if re.match(ptglob, coincidencia.group(1)):
                des = int(re.match(ptglob, coincidencia.group(1)).group(1))
                cadena = f"\t\t\tADD #{des}, .IY\n"

            else:
                des = int(re.match(ptloc, coincidencia.group(1)).group(1)) + 1
                cadena = f"\t\t\tADD #{des}, .IX\n"

            
            cadena += f"\t\t\tWRSTR [.A]\n"
            escribir(cadena)

        elif re.match(patron_writeln, linea, re.VERBOSE):
            coincidencia = re.match(patron_writeln, linea, re.VERBOSE)
            cad = f"cadena{cds}"
            declarar_cads("DATA \"\\n\"", False)
            cds +=1

            if re.match(ptglob, coincidencia.group(1)):
                des = int(re.match(ptglob, coincidencia.group(1)).group(1))
                cadena = f"\t\t\tADD #{des}, .IY\n"
                cadena += "\t\t\tWRINT [.A]"
            else:
                des = int(re.match(ptloc, coincidencia.group(1)).group(1)) + 1
                cadena = f"\t\t\tADD #{des}, .IX\n"
                cadena += "\t\t\tWRINT [.A]"
                
            cadena += f"\n\t\t\tWRSTR /{cad}\n"
            escribir(cadena)
            
        elif re.match(patron_writeln_cad, linea, re.VERBOSE):
            coincidencia = re.match(patron_writeln_cad, linea, re.VERBOSE)
            cad = f"cadena{cds}"
            declarar_cads("DATA \"\\n\"", False)
            cds += 1

            if re.match(ptglob, coincidencia.group(1)):
                des = int(re.match(ptglob, coincidencia.group(1)).group(1))
                cadena = f"\t\t\tADD #{des}, .IY\n"
            else:
                des = int(re.match(ptloc, coincidencia.group(1)).group(1)) + 1
                cadena = f"\t\t\tADD #{des}, .IX\n"
            
            cadena += f"\t\t\tWRSTR [.A]\n"
            cadena += f"\t\t\tWRSTR /{cad}\n"
            escribir(cadena)
            
            
            
        elif re.match(patron_write_ref, linea, re.VERBOSE):
            coincidencia = re.match(patron_write_ref, linea, re.VERBOSE)
            # Usar WRINT en lugar de OUT para escribir enteros
            if re.match(ptglob, coincidencia.group(1)):
                des = int(re.match(ptglob, coincidencia.group(1)).group(1))
                cadena = f"\t\t\tADD #{des}, .IY\n"
                cadena += "\t\t\tMOVE [.A], .A\n"
            else:
                des = int(re.match(ptloc, coincidencia.group(1)).group(1)) + 1
                cadena = f"\t\t\tADD #{des}, .IX\n"
                cadena += "\t\t\tMOVE [.A], .A\n"
            cadena += "\t\t\tWRINT [.A]"
            escribir(cadena)
            escribir("\n")

        elif re.match(patron_write_cad_ref, linea, re.VERBOSE):
            coincidencia = re.match(patron_write_cad_ref, linea, re.VERBOSE)
            
            if re.match(ptglob, coincidencia.group(1)):
                des = int(re.match(ptglob, coincidencia.group(1)).group(1))
                cadena = f"\t\t\tADD #{des}, .IY\n"
                cadena += "\t\t\tMOVE [.A], .A\n"
            else:
                des = int(re.match(ptloc, coincidencia.group(1)).group(1)) + 1
                cadena = f"\t\t\tADD #{des}, .IX\n"
                cadena += "\t\t\tMOVE [.A], .A\n"
            
            cadena += f"\t\t\tWRSTR [.A]\n"
            escribir(cadena)

        elif re.match(patron_writeln_ref, linea, re.VERBOSE):
            coincidencia = re.match(patron_writeln_ref, linea, re.VERBOSE)
            cad = f"cadena{cds}"
            declarar_cads("DATA \"\\n\"", False)
            cds +=1

            if re.match(ptglob, coincidencia.group(1)):
                des = int(re.match(ptglob, coincidencia.group(1)).group(1))
                cadena = f"\t\t\tADD #{des}, .IY\n"
                cadena += "\t\t\tMOVE [.A], .A\n"
                cadena += "\t\t\tWRINT [.A]"
            else:
                des = int(re.match(ptloc, coincidencia.group(1)).group(1)) + 1
                cadena = f"\t\t\tADD #{des}, .IX\n"
                cadena += "\t\t\tMOVE [.A], .A\n"
                cadena += "\t\t\tWRINT [.A]"
                
            cadena += f"\n\t\t\tWRSTR /{cad}\n"
            escribir(cadena)
            
        elif re.match(patron_writeln_cad_ref, linea, re.VERBOSE):
            coincidencia = re.match(patron_writeln_cad_ref, linea, re.VERBOSE)
            cad = f"cadena{cds}"
            declarar_cads("DATA \"\\n\"", False)
            cds += 1

            if re.match(ptglob, coincidencia.group(1)):
                des = int(re.match(ptglob, coincidencia.group(1)).group(1))
                cadena = f"\t\t\tADD #{des}, .IY\n"
                cadena += "\t\t\tMOVE [.A], .A\n"
            else:
                des = int(re.match(ptloc, coincidencia.group(1)).group(1)) + 1
                cadena = f"\t\t\tADD #{des}, .IX\n"
                cadena += "\t\t\tMOVE [.A], .A\n"
            
            cadena += f"\t\t\tWRSTR [.A]\n"
            cadena += f"\t\t\tWRSTR /{cad}\n"
            escribir(cadena)
        

        elif re.match(patron_param_min, linea, re.VERBOSE):
            coincidencia = re.match(patron_param_min, linea, re.VERBOSE)
            transformar_dir(coincidencia.group(1), None, dirmin)
            if contmin == 0:
                cadena = "\t\t\tMOVE [.R2], [.R3]\n"
            else:
                cadena = "\t\t\tCMP [.R2], [.R3]\n"
                cadena += f"\t\t\tBP $EtiqMin{contmin}\n"
                cadena += "\t\t\tMOVE [.R2], [.R3]\n"

            escribir(cadena)
            contmin +=1
            
        elif re.match(patron_min, linea, re.VERBOSE):
            coincidencia = re.match(patron_min, linea, re.VERBOSE)
            dirmin = coincidencia.group(3)
            escribir(f"\t\t\tMOVE [.R2], [.R3]\n")         
            
        linea = leer()
    escribir("\t\t\tHALT\n\n")
    i = declarar_cads(None, True)
    escribir(_calcprev.cadfinal)
    if i:
        escribir("\n\t\t\tEND\n")

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