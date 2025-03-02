package procesador;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;

class Token<E> {
	private Integer id;
	private E atributo;

	public Token(Integer id, E atributo) {
		this.id = id;
		this.atributo = atributo;
	}

	@Override
	public String toString() {
		return getType(id).toUpperCase() + ":" + atributo; 
	}

	public Integer getId() { return id; }

	public E getAtributo() { return atributo; }

	public static String getType(int id) {
		return ALex.id_tok.get(id) == null ?"Unkown token":  ALex.id_tok.get(id).toUpperCase() ; 
	}

}

class Acc_MT_AFD {
	private Integer estado;
	private Acciones accion;
	private Integer ptrTS;
	private String type;

	public Acc_MT_AFD(Integer e, Acciones a) { estado = e; accion = a; }

	public Acc_MT_AFD(Integer p, String t) { ptrTS = p; type = t; }

	public Integer getEstado() {return estado;}

	public Acciones getAccion() {return accion;}

	public Integer getPtrTS() {return ptrTS;}

	public String getType() {return type;}
}

public class ALex {

	public static int carAsc;

	private static BufferedReader ptr;
	private static BufferedWriter ptw;
	private static int countString;
	private static int countId;
	private static int valor;
	private static String lexema;

	// Asignacion de Id y nombre de tokens
	public static Map<Integer, String> id_tok;
	public static Map<String, Integer> tok_id;

	// Conjunto de palabras reservadas;
	public static Set<String> pr_set;

	// Traducción de la entrada de la TS de palabras reservadas al id del token de
	// palabra reservada.
	public static Map<Integer, Integer> ts_pr_to_tokenid;


	/* mt[][] = Tabla de transiciones del automata.
	 * 
	 * mt[*][] = estado del automata 
	 * 	  {0...14}
	 * 
	 * mt[][*] = caracter de entrada 
	 *    { 0= l, 1= d, 2= tab/espacio, 3= RC, 4= +, 5= -, 
	 *    6= *, 7= /, 8= =, 9= <, 10= >, 11= (, 12= ), 13= 
	 *    {, 14= }, 15= ', 16 = ; ,17= :, 18= ,, 19= EOF, 20= o.c, 21= LF}
	 */

	private static Acc_MT_AFD[][] mt = new Acc_MT_AFD[13][22];

	/*	Map<Integer, Set<Integer>> oc_exclude = For every state of the automata it stores the characters 
	 * 											that are not considered as O.C.
	 * 		- Key = mt[i][]; 
	 * 		- Value = The columns from the transition matrix that have unique actions. 
	 */
	private static Map<Integer, Set<Integer>> oc_exclude = new HashMap<Integer, Set<Integer>>(); 


	private static final String[] token_names = { "PROGRAM", "INTEGER", "BOOLEAN", "STRING", "WRITE", "WRITELN", "READ",
			"FUNCTION", "PROCEDURE", "RETURN", "BEGIN", "END", "IF", "THEN", "ELSE", "DO", "WHILE", "REPEAT", "UNTIL",
			"LOOP", "FOR", "CASE", "OF", "OTHERWISE", "VAR", "WHEN", "TRUE", "FALSE", "EXIT", "MAYOR_IGUAL", "MAYOR",
			"CADENA", "ID", "ENTERO", "POTENCIA", "PRODUCTO", "MENOR", "DISTINTO", "MENOR_IGUAL", "DOSPUNTOS",
			"ASIGNACION", "MAS", "MENOS", "DIVISION", "IGUAL", "PARENT_ABRIR", "PARENT_CERRAR", "PYC", "COMA", "EOF",
			"AND", "OR", "XOR", "IN", "MOD", "NOT", "MAX", "MIN", "TO" };

	private static final String[] palabras_reservadas = { "PROGRAM", "INTEGER", "BOOLEAN", "STRING", "WRITE", "WRITELN",
			"READ", "FUNCTION", "PROCEDURE", "RETURN", "BEGIN", "END", "IF", "THEN", "ELSE", "DO", "WHILE", "REPEAT",
			"UNTIL", "LOOP", "FOR", "CASE", "OF", "OTHERWISE", "VAR", "WHEN", "TRUE", "FALSE", "EXIT", "AND", "OR",
			"XOR", "IN", "MOD", "NOT", "MAX", "MIN", "TO" };

	static {
		countString = 0;
		countId = 0;
		lexema = "";
		valor = 0;
		tok_id = new HashMap<>();
		id_tok = new HashMap<>();
		ts_pr_to_tokenid = new HashMap<>();

		cargar_datos();
	}

	/*
	 * generarToken DESCRIPTION: It generates the token for the syntax analyzer.
	 * 
	 * OUT: Token<String>, Token<Integer> or null if a compilation error occurs.
	 */
	public static Token<?> generarToken() {
		Integer estado = 0;
		Acciones accion;
		lexema = "";
		while (estado != 888) {

			accion = getAccion(estado, carAsc);
			estado = getEstado(estado, carAsc);

			switch (accion) {
			case Leer:
				leer();
				break;
			case eol:
				leer();
				GestorError.increaseCountLine();
				break;
			case none:
				break;
			case a1_11:
				leer();
				printToken("MAYOR_IGUAL", "");
				return new Token<String>(tok_id.get("MAYOR_IGUAL"), null);
			case a1_12:
				printToken("MAYOR", "");
				return new Token<String>(tok_id.get("MAYOR"), null);
			case a0_2:
				countString = 0;
				leer();
				break;
			case a2_2:
				lexema += (char) carAsc;
				countString++;
				leer();
				break;
			case a2_21:
				leer();
				if (countString < 64) {
					printToken("CADENA", "'" + lexema + "'");
					return new Token<String>(tok_id.get("CADENA"), lexema);
				} else {
					GestorError.defErrorCase(lexema);
					GestorError.setError(Acciones.eLex2_ERROR_LONGITUD_MAXIMA_CADENA, lexema);
					return null;
				}
			case a0_3:
				lexema = "" + (char) carAsc;
				leer();
				countId = 1;
				break;
			case a3_3:
				lexema += (char) carAsc;
				countId++;
				leer();
				break;
			case a3_31:
				if (countId <= 32) {
					// Palabra Reservada
					if (Procesador.gestorTS.getEntradaTPalabrasReservadas(lexema.toUpperCase()) != 0) {
						printToken(lexema.toUpperCase(), "");
						int tokenId = ts_pr_to_tokenid
								.get(Procesador.gestorTS.getEntradaTPalabrasReservadas(lexema.toUpperCase()));
						return new Token<String>(tokenId, null);
						// Identificador
					} else {
						Integer ptrTS = Procesador.gestorTS.getEntradaTS(lexema.toUpperCase());
						// ZonaDec:true
						if (ASem.zonaDec()) {
							if ((ASem.tsGlobal && ptrTS > 0) || (!ASem.tsGlobal && ptrTS < 0)) { // Doble declaracion
								// detectada
								GestorError.writeError("Variable [" + lexema + "] ya declarada");
							} else {
								ptrTS = insertarTablaPtr(lexema.toUpperCase());
								printToken("ID", ptrTS.toString());
								return new Token<Integer>(tok_id.get("ID"), ptrTS);
							}
							// ZonaDec:false
						} else {
							if (ptrTS == 0) { // Uso de variable no declarada
								GestorError.writeError("Variable [" + lexema + "] no declarada");
							} else {
								printToken("ID", ptrTS.toString());
								return new Token<Integer>(tok_id.get("ID"), ptrTS);
							}
						}
					}
				} else { // Lexema mas de 32 caracteres
					GestorError.setError(Acciones.eLex3_ERROR_LONGITUD_MAXIMA_ID, lexema);
					return null;
				}
			case a0_4:
				valor = carAsc - '0';
				leer();
				break;
			case a4_4:
				valor = valor * 10 + (carAsc - '0');
				if (valor > Math.pow(2, 15)) {
					GestorError.setOutOfBoundStatus(true);
				}
				leer();
				break;
			case a4_41:
				if (valor < Math.pow(2, 15) && !GestorError.getOutOfBoundStatus()) {
					printToken("ENTERO", valor + "");
					return new Token<Integer>(tok_id.get("ENTERO"), valor);
				} else {
					GestorError.setError(Acciones.eLex4_ERROR_VALOR_MAXIMO_ENTERO, Integer.toString(valor));
					GestorError.setOutOfBoundStatus(false);
					return new Token<Integer>(tok_id.get("ENTERO"), -1);
				}
			case a5_51:
				leer();
				printToken("POTENCIA", "");
				return new Token<String>(tok_id.get("POTENCIA"), null);
			case a5_52:
				printToken("PRODUCTO", "");
				return new Token<String>(tok_id.get("PRODUCTO"), null);
			case a7_71:
				printToken("MENOR", "");
				return new Token<String>(tok_id.get("MENOR"), null);
			case a7_72:
				leer();
				printToken("DISTINTO", "");
				return new Token<String>(tok_id.get("DISTINTO"), null);
			case a7_73:
				leer();
				printToken("MENOR_IGUAL", "");
				return new Token<String>(tok_id.get("MENOR_IGUAL"), null);
			case a8_81:
				printToken("DOSPUNTOS", "");
				return new Token<String>(tok_id.get("DOSPUNTOS"), null);
			case a8_82:
				leer();
				printToken("ASIGNACION", "");
				return new Token<String>(tok_id.get("ASIGNACION"), null);
			case a0_100:
				leer();
				printToken("MAS", "");
				return new Token<String>(tok_id.get("MAS"), null);
			case a0_101:
				leer();
				printToken("MENOS", "");
				return new Token<String>(tok_id.get("MENOS"), null);
			case a0_102:
				leer();
				printToken("DIVISION", "");
				return new Token<String>(tok_id.get("DIVISION"), null);
			case a0_103:
				leer();
				printToken("IGUAL", "");
				return new Token<String>(tok_id.get("IGUAL"), null);
			case a0_104:
				leer();
				printToken("PARENT_ABRIR", "");
				return new Token<String>(tok_id.get("PARENT_ABRIR"), null);
			case a0_105:
				leer();
				printToken("PARENT_CERRAR", "");
				return new Token<String>(tok_id.get("PARENT_CERRAR"), null);
			case a0_106:
				leer();
				printToken("PYC", "");
				return new Token<String>(tok_id.get("PYC"), null);
			case a0_107:
				leer();
				printToken("COMA", "");
				return new Token<String>(tok_id.get("COMA"), null);
			case a0_108:
				printToken("EOF", "");
				return new Token<String>(tok_id.get("EOF"), null);

				// ACCIONES SEMÁNTICAS DE TRATAMIENTO DE ERRORES
			case eLex0_ERROR_OC:
				GestorError.setError(Acciones.eLex0_ERROR_OC, "" + (char) carAsc);
				leer();
				return null;
			case eLex0_CIERRE_COMENTARIO_ILEGAL:
				GestorError.setError(Acciones.eLex0_CIERRE_COMENTARIO_ILEGAL, lexema);
				return null;
			case eLex2_ERROR_SALTO_LINEA:
				leer();
				GestorError.setError(Acciones.eLex2_ERROR_SALTO_LINEA, lexema);
				return null;
			case eLex2_ERROR_CADENA_INCOMPLETA:
				GestorError.setError(Acciones.eLex2_ERROR_CADENA_INCOMPLETA, lexema);
				return null;
			case eLex6_ERROR_COMENTARIO_NO_CERRADO:
				GestorError.setError(Acciones.eLex6_ERROR_COMENTARIO_NO_CERRADO, lexema);
				return null;
			default:
				return null;
			}
		}
		return null;
	}


	/* getColumnIndex(estado, carASC)
	 * DESCRIPTION: Identifies the character and locates its column index from
	 * the transition matrix.
	 * 
	 * IN: Integer estado = current state 
	 * 	   int carASC = character inserted in ASCII format 
	 * OUT: index of the column from the transition matrix.
	 */
	public static int getColumnIndex(Integer estado, int carASC) {
		// The character is o.c until it is identified.
		int column = 20;

		// carASC in l
		if ((carASC >= 65 && carASC <= 90) || (carASC >= 97 && carASC <= 122)) {
			column = 0;

			// carASC in d
		} else if (carASC >= 48 && carASC <= 57) {
			column = 1;

			// tab/space
		} else if (carASC == 9 || carASC == 32) {
			column = 2;
			// LF 
		} else if (carASC == 10 ) {
			column = 3;
			// RC
		} else if(carASC == 13) {
			column = 21; 
			// +
		} else if (carASC == 43) {
			column = 4;
			// -
		} else if (carASC == 45) {
			column = 5;
			// *
		} else if (carASC == 42) {
			column = 6;
			// /
		} else if (carASC == 47) {
			column = 7;
			// =
		} else if (carASC == 61) {
			column = 8;
			// <
		} else if (carASC == 60) {
			column = 9;
			// >
		} else if (carASC == 62) {
			column = 10;
			// (
		} else if (carASC == 40) {
			column = 11;
			// )
		} else if (carASC == 41) {
			column = 12;
			// {
		} else if (carASC == 123) {
			column = 13;
			// }
		} else if (carASC == 125) {
			column = 14;
			// '
		} else if (carASC == 39) {
			column = 15;
			// ;
		} else if (carASC == 59) {
			column = 16;
			// :
		} else if (carASC == 58) {
			column = 17;
			// ,
		} else if (carASC == 44) {
			column = 18;

			// EOF
		} else if(carASC < 0) {
			column = 19;
		} 

		if(estado == 0 && column != 20) {
			return column; 
		}
		// check if the character read is from the o.c column.
		if (!oc_exclude.get(estado).contains(column)) {
			column = 20;
		}
		return column;
	}


	/* build_oc_cloud
	 * DESCRIPTION: Building up the data structure for oc_exclude map. 
	 */
	private static void build_oc_cloud() {
		Set<Integer> aux = null; 
		for(int i = 0; i<22; i++) {
			aux = new HashSet<Integer>(); 
			switch(i) {
			case 1: 
				aux.add(8); 
				break; 
			case 2:
				aux.add(15); 
				aux.add(19); 
				aux.add(3); 
				aux.add(21); 
				break; 
			case 3: 
				aux.add(0); 
				aux.add(1); 
				break; 
			case 4: 
				aux.add(1); 
				break; 
			case 5: 
				aux.add(6); 
				break; 
			case 6: 
				aux.add(14); 
				aux.add(19); 
				aux.add(3); 	//lectura de FL
				aux.add(21); 	//lectura de RC
				break; 
			case 7: 
				aux.add(10); 
				aux.add(8); 
				break; 
			case 8: 
				aux.add(8); 
				break; 
			case 9: 
				aux.add(21); 
				break; 
			case 10: 
				aux.add(3); 
				break; 
			case 11: 
				aux.add(21); 
				break; 
			case 12:
				aux.add(3); 
				break; 
			}
			oc_exclude.put(i, aux); 
		}
	}
	

	/* cargarTablaIdentificador DESCRIPTION: Builds the data structure to identify
	 * the id of each reserved word from the language.
	 */
	private static void cargar_datos() {
		pr_set = new HashSet<>();
		for (int i = 0; i < palabras_reservadas.length; i++) {
			pr_set.add(palabras_reservadas[i]);
		}
		// Crea los identificadores de cada token en función del orden de aparación en
		// el array token_names.
		// Si el token corresponde con una palabra reservada, se añade a la tabla de
		// palabras reservadas y se almacena el valor de su
		// entrada para traducirlo al token correspondiente
		for (int i = 0; i < token_names.length; i++) {
			if (pr_set.contains(token_names[i])) {
				Procesador.gestorTS.addEntradaTPalabrasReservadas(token_names[i]);
				ts_pr_to_tokenid.put(Procesador.gestorTS.getEntradaTPalabrasReservadas(token_names[i]), i);
			}
			id_tok.put(i, token_names[i]);
			tok_id.put(token_names[i], i);
		}
	}

	/* cargar_mt(filename)
	 * DESCRIPTION: Loads the transition matrix from a CSV file and prepares oc_exclude. 
	 * IN: String filename = The relative path to the file.
	 */
	public static void cargar_mt(String filename) {
		String line;
		build_oc_cloud(); 
		try {
			InputStream inputStream = Procesador.class.getResourceAsStream(filename);
	        BufferedReader br = new BufferedReader(new InputStreamReader(inputStream)); 
			//BufferedReader br = new BufferedReader(new FileReader(filename));
			while ((line = br.readLine()) != null) {

				String[] transicion = line.split(","); // use comma as separator

				int estado_curr = Integer.parseInt(transicion[0]);
				int estado_next = Integer.parseInt(transicion[1]);
				int caracter = Integer.parseInt(transicion[2]);
				Acciones accion = Acciones.valueOf(transicion[3]);

				mt[estado_curr][caracter] = new Acc_MT_AFD(estado_next, accion);
			}
			br.close();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

	public static Acciones getAccion(Integer estado, int carASC) {
		return mt[estado][getColumnIndex(estado, carASC)].getAccion();
	}

	public static Integer getEstado(Integer estado, int carASC) {
		return mt[estado][getColumnIndex(estado, carASC)].getEstado();
	}
	
	public static void setInputFile(BufferedReader inputFileptr) {
		ptr = inputFileptr;
		leer(); // lee el primer caracter
	}

	public static void setTokenOutputFile(BufferedWriter tokenFileptr) {
		ptw = tokenFileptr;
	}

	public static void set_tsGlobal(boolean valor) {
		ASem.tsGlobal = valor;
	}
	
	private static Integer insertarTablaPtr(String lex) {
		if (ASem.tsGlobal) {
			return Procesador.gestorTS.addEntradaTSGlobal(lex);
		} else {
			return Procesador.gestorTS.addEntradaTSLocal(lex);
		}
	}

	public static void leer() {
		carAsc = -1;
		try {
			carAsc = ptr.read();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
	
	private static void printToken(String id, String atributo) {
		atributo = atributo.equals("") ? "-" : atributo; 
		try {
			ptw.write("<" + id + "," + atributo + ">\n");
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

}
