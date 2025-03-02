package procesador;

import java.io.BufferedWriter;
import java.io.IOException;

public class GestorError {

	private static BufferedWriter pte;
	private static int countLine = 1;
	private static Acciones currError;
	private static String errorCase;
	private static boolean outOfBound;

	public static void setOutputMessageFile(BufferedWriter buffer) {
		pte = buffer;
	}

	// Define el error a tratar,
	// accion = identificador del error
	// lexema = cadena de caracteres implicada en el error.
	public static void setError(Acciones accion, String lexema) {
		currError = accion;
		errorCase = lexema;
		printError();
	}

	public static Acciones getCurrError() {
		return currError;
	}

	public static void defErrorCase(String badChars) {
		errorCase += badChars;
	}

	public static int getCountLine() {
		return countLine;
	}

	public static void increaseCountLine() {
		countLine++;
	}

	public static boolean getOutOfBoundStatus() {
		return outOfBound;
	}

	public static void setOutOfBoundStatus(boolean t) {
		outOfBound = t;
	}

	public static void writeError(String errorMessage) {
		try {
			pte.write("Error en la linea [" + countLine + "]: " + errorMessage + "\n");
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

	public static void printError() {
		if (currError != null) {
			try {
				switch (currError) {
				case eLex0_ERROR_OC:
					pte.write("Error linea [" + countLine + "]: Caracter no reconocido - " + errorCase + "\n");
					break;
				case eLex0_CIERRE_COMENTARIO_ILEGAL:
					pte.write("Error en la linea [" + countLine + "]: Comentario no inicializado\n");
					break;
				case eLex2_ERROR_SALTO_LINEA:
					pte.write("Error en la linea [" + countLine
							+ "]: La cadena de caracteres no puede contener salto de linea - " + errorCase + "\n");
					break;
				case eLex2_ERROR_LONGITUD_MAXIMA_CADENA:
					pte.write("Error en la linea [" + countLine
							+ "]: La cadena no puede contener más de 64 caracteres - " + errorCase + "\n");
					break;
				case eLex2_ERROR_CADENA_INCOMPLETA:
					pte.write("Error en la linea [" + countLine + "]: La cadena no se ha cerrado");
					break;
				case eLex3_ERROR_LONGITUD_MAXIMA_ID:
					pte.write("Error en la linea [" + countLine
							+ "]: El identificador no puede contener más de 32 caracteres - " + errorCase + "\n");
					break;
				case eLex4_ERROR_VALOR_MAXIMO_ENTERO:
					pte.write("Error en la linea [" + countLine + "]: Entero fuera de rango - " + errorCase + "\n");
					break;
				case eLex6_ERROR_COMENTARIO_NO_CERRADO:
					pte.write("Error en la linea [" + countLine + "]: El comentario no se ha cerrado.");
					break;
				case eSin0_ERROR_SINTACTICO:
					// System.out.println("errorCase es:" + errorCase);
					String[] mensaje = errorCase.split("\\#");
					pte.write("Error en la linea [" + countLine + "]: La lectura de " + mensaje[0]
							+ " no respeta las reglas sintacticas.\n");
					String[] tokensEsperados = mensaje[1].split("@");
					String entradaEsperada = "";
					for (int i = 0; i < tokensEsperados.length; i++) {
						if (i == 0) {
							entradaEsperada += "\n \t - "+ tokensEsperados[i];
						} else {
							entradaEsperada += "\n \t - " + tokensEsperados[i];
						}
					}
					pte.write("Posibles tokens aceptados: " + entradaEsperada);
					break;
				case eSem1_loop:
					pte.write("Error en la linea [" + countLine + "]: Dentro de LOOP debe existir una única sentencia exit.\n");
					break;
				case eSem2_tipo_incompatible:
					pte.write("Error en la linea [" + countLine + "]: Tipos incompatibles - " + errorCase + ".\n");
					break;
				case eSem3_tipo_retorno_incompatible:
					pte.write("Error en la linea [" + countLine + "]: Tipo retorno incompatible, " + errorCase + ".\n");
					break;
				case eSem4_for_error:
					pte.write("Error en la linea [" + countLine + "]: Error en el bucle for.\n");
					break;
				case eSem5_case_otherwise_error:
					pte.write("Error en la linea [" + countLine + "]: Error en la sentencia otherwise.\n");
					break;
				case eSem6_case_error:
					pte.write("Error en la linea [" + countLine + "]: Error en el tratamiento de case.\n");
					break;
				case eSem7_case_bloque_error:
					pte.write("Error en la linea [" + countLine + "]: Error en el bloque de ejecución del case.\n");
					break;
				case eSem8_funcion_parametro_incompatible_error:
					pte.write("Error en la linea [" + countLine + "]: Error en la llamada a la función.\n");
					break;
				case eSem9_retorno_funcion_error:
					pte.write("Error en la linea [" + countLine + "]: Error en el valor de retorno.\n");
					break;
				case eSem10_expresion_error:
					pte.write("Error en la linea [" + countLine + "]: Error en la expresión posterior a when.\n");
					break;

				default:
					break;
				}
				currError = null;
			} catch (Exception e) {
				e.printStackTrace();
			}
		}
	}
}
