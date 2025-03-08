package procesador;

import java.io.BufferedWriter;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;


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

    public static tupla<String, Integer> nuevatemp() {
        String nuevatemp = "t" + conttemp;
        conttemp++;
        
        if (ASem.tsGlobal) {
            tupla<String, Integer> tupla = new tupla<>("VAR_GLOBAL", Procesador.gestorTS.addEntradaTSGlobal(nuevatemp));
            return tupla;
		} else {
            tupla<String, Integer> tupla = new tupla<>("VAR_LOCAL", Procesador.gestorTS.addEntradaTSLocal(nuevatemp));
            return tupla;
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

        tupla<String, String> tupla = new tupla<>("ETIQ", nuevaetiq);
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