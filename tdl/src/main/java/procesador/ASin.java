package procesador;

import java.io.BufferedWriter;
import java.io.IOException;
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Deque;

public class ASin { // Hacer Bucle

	static final int SHIFT = 0;
	static final int REDUCTION = 1;
	static final int ACCEPTED = 2;

	private static int ciclo = 0;

	private static Deque<Integer> pila;
	public static Deque<Atributos> pilaSem;
	public static Token<?> token;
	private static BufferedWriter ptwParse;

	public static void setOutputParseFile(BufferedWriter parsePtr) {
		ptwParse = parsePtr;
	}

	static {
		pila = new ArrayDeque<Integer>();
		pila.addFirst(0); // Estado inicial I0

		pilaSem = new ArrayDeque<Atributos>();
		pilaSem.addFirst(new Atributos());
	}

	// Debug method
	public static String imprimirPila() {
		Deque<Integer> pilaAux = new ArrayDeque<>();
		ArrayList<Integer> kk = new ArrayList<>();
		String res = "PILA CICLO " + ciclo++ + ", Línea: " + GestorError.getCountLine() + "\n";
		boolean esEstado = true;
		while (!pila.isEmpty()) {
			int valor_pila = pila.pop();
			if (esEstado) {
				res += valor_pila + "\n";
				esEstado = false;
			} else {
				res += MT_ASINT.getNoTerminalPorIndice(valor_pila) + "\n";
				esEstado = true;
			}
			kk.addLast(valor_pila);
		}
		while (!kk.isEmpty()) {
			pilaAux.add(kk.removeFirst());
		}
		pila = pilaAux;
		return res;
	}

	public static void pedirTokens() {
		// Comienzo del parse
		try {
			ptwParse.write("ascendente ");
		} catch (IOException e) {
			e.printStackTrace();
		}

		// Primer token devuelto en el analisis lexico
		token = ALex.generarToken();

		while (true) {
			int tokenId = token.getId();

			// String calculado a partir del codigo de token recibido
			String tokenType = Token.getType(tokenId);

			// Consultar tabla ACCION, teniendo en cuenta el estado de la cima de la pila y
			// el terminal almacenado en token
			Acc_ASin accion = MT_ASINT.getAction("" + pila.peek() + ":" + tokenId);

			// Error en el acceso a la tabla Accion
			if (accion == null) {
				String mensajeError = Token.getType(tokenId) + "#";
				boolean first = true;
				for (int i = 0; i < 59; i++) {
					accion = MT_ASINT.getAction("" + pila.peek() + ":" + i);
					if (accion != null) {
						if (first) {
							mensajeError += Token.getType(i);
							first = false;
						} else {
							mensajeError += "@" + Token.getType(i);
						}
					}
				}
				GestorError.setError(Acciones.eSin0_ERROR_SINTACTICO, mensajeError);
				GestorError.printError();
				break;
			}

			// Desplazamiento
			if (accion.type == SHIFT) {

				// Introducir el token leido a la pila
				pila.push(tokenId);

				// Si el token corresponde a 'ID' entonces introducir id.pos junto con el
				// terminal
				if (Token.getType(tokenId).equals("ID")) {
					Atributos idAtb = new Atributos();
					idAtb.setTipo(tokenType);
					idAtb.setPos((int) token.getAtributo());
					pilaSem.push(idAtb);
				} else {
					pilaSem.push(new Atributos());
				}

				// Introducir el nuevo estado
				pila.push(accion.value);

				// Introducir objeto vacio para poder realizar un calculo de posicion correcto
				// posteriormente
				// en analisis semantico
				pilaSem.push(new Atributos());

				// Pedir siguiente token
				token = ALex.generarToken();
				if (token == null) {
					break;
				}

				// Reduccion
			} else if (accion.type == REDUCTION) {
				// Objeto Regla: antecedente, consecuente y numElement del consecuente
				Regla reduction = MT_ASINT.getRegla(accion.value);

				// Tratamiento: seleccion de funcion correspondiente a cada regla cuyo
				// almacenado en accion.value
				// Analisis semantica al realizar una reduccion
				Atributos atributos = ASem.selectFunction(accion.value);

				// Completando parse con la regla reducida
				try {
					ptwParse.write(" " + accion.value);
				} catch (IOException e) {
					e.printStackTrace();
				}

				// Sacar el conssecuente y los estados intercalados
				for (int i = 0; i < 2 * reduction.numElementos; i++) {
					pila.pop();
					pilaSem.pop();
				}

				// Consultar tabla Goto
				Acc_ASin gotoo = MT_ASINT.getAction("" + pila.peek() + ":" + reduction.antecedenteId);

				// Error en el acceso a Goto
				if (gotoo == null) {
					GestorError.setError(Acciones.eSin0_ERROR_SINTACTICO, Token.getType(reduction.antecedenteId));
					GestorError.printError();
					break;
				}

				// Introducir a la pila el no terminal y nuevo estado
				pila.push(reduction.antecedenteId);
				pilaSem.push(atributos); // Semantica
				pila.push(gotoo.value);
				pilaSem.push(new Atributos()); // Semantica

			} else { // ACCEPTED
				return;
			}
		}
	}
}
