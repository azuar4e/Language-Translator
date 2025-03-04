package procesador;

import java.io.BufferedWriter;
import java.io.IOException;


public class gci {
    private static BufferedWriter ptw;
    private static int conttemp = 0;
    private static int contetiq = 0;

    public static cuarteto emite (String operador, Object arg1, Object arg2, Object resultado) {
        cuarteto c = new cuarteto(operador, arg1, arg2, resultado);
        printCuarteto(c);
        return c;
    }

    public static Integer nuevatemp() {
        String nuevatemp = "t" + conttemp;
        conttemp++;
        if (ASem.tsGlobal) {
			return Procesador.gestorTS.addEntradaTSGlobal(nuevatemp);
		} else {
			return Procesador.gestorTS.addEntradaTSLocal(nuevatemp);
		}
    }

    public static String nuevaetiq() {
        String nuevaetiq = "Etiq" + contetiq;
        contetiq++;
        return nuevaetiq;
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