#________________________________________________________________________
# imports

from _ens import escribir
from _gco import leer
import re

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


def main():
    linea = leer()

    while linea:
        #________________________________________________________________________
# switch con la accion a ejecutar en ensamblador

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
            
if __name__ == '__main__':
    main()