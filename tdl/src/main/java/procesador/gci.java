package procesador;

import java.io.BufferedWriter;
import java.io.IOException;


public class gci {
    private static BufferedWriter ptw;
    private static int conttemp = 0;
    private static int contetiq = 0;

    public static class tupla<A, B> {
        private final A primerElemento;
        private final B segundoElemento;

        public tupla(A primerElemento, B segundoElemento) {
            this.primerElemento = primerElemento;
            this.segundoElemento = segundoElemento;
        }

        public A getPrimerElemento() {
            return primerElemento;
        }
    
        public B getSegundoElemento() {
            return segundoElemento;
        }

        @Override
        public String toString() {
            return "{" + primerElemento + ", " + segundoElemento + "}";
        }
    }

    public static cuarteto emite (String operador, Object arg1, Object arg2, Object resultado) {
        cuarteto c = new cuarteto(operador, arg1, arg2, resultado);
        printCuarteto(c);
        return c;
    }

    public static tupla<String, Integer> nuevatemp(String tipo) {
        String nuevatemp = "t" + conttemp;
        conttemp++;
    
        if (ASem.tsGlobal) {
            Integer pos = Procesador.gestorTS.addEntradaTSGlobal(nuevatemp);
            if (!tipo.equals("tipo_error")) {
                Procesador.gestorTS.setTipo(pos, tipo);
            }
            Procesador.gestorTS.setValorAtributoEnt(pos, "desplazamiento", ASem.despGlobal);
            switch (tipo) {
                case "lógico":
                    ASem.despGlobal += 1;
                    break;
                case "entero":
                    ASem.despGlobal += 4;
                    break;
                case "cadena":
                    ASem.despGlobal += 64;
                    break;
                default:
                    break;
            }
            return new tupla<>("VAR_GLOBAL", ASem.despGlobal);
		} else {
            Integer pos = Procesador.gestorTS.addEntradaTSLocal(nuevatemp);
            if (!tipo.equals("tipo_error")) {
                Procesador.gestorTS.setTipo(pos, tipo);
            }
            Procesador.gestorTS.setValorAtributoEnt(pos, "desplazamiento", ASem.despLocal);
            switch (tipo) {
                case "lógico":
                    ASem.despLocal += 1;
                    break;
                case "entero":
                    ASem.despLocal += 4;
                    break;
                case "cadena":
                    ASem.despLocal += 64;
                    break;
                default:
                    break;
            }
            return new tupla<>("VAR_LOCAL", ASem.despLocal);
		}
    }

    public static tupla<String, String> nuevaetiq(String nombre) {
        String nuevaetiq;
        if (nombre == null){
            nuevaetiq = "Etiq" + contetiq;
            contetiq++;
        } else {
            nuevaetiq = nombre;
        }

        tupla<String, String> tupla = new tupla<>("ET", nuevaetiq);
        return tupla;
    }

    private static void printCuarteto(cuarteto c) {
        try {
			ptw.write(c.toString());
		} catch (IOException e) {
			e.printStackTrace();
		}
    }

    public static void setOutputfile(BufferedWriter archivo) { ptw = archivo; }
}