package procesador;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.HashMap;
import java.util.Map;

// Declaración de clases auxiliares. 

/*
 * type => 0 -> accion de desplazamiento
 * 		   1 -> accion de reduccion
 * 		   2 -> aceptar
 * value => Si type == reduction, value = rule number
 * 		    Si type == shift, value = estado a transitar
 */
class Acc_ASin{
	int type; 
	int value;

	public Acc_ASin(int type, int value) {
		this.type = type; 
		this.value = value; 
	}

	public String toString() {
		String tipo = "ACEPTADO"; 
		if(type == 0) {
			tipo = "SHIFT"; 
		}else if(type == 1) {
			tipo = "REDUCTION"; 
		}
		return "("+ tipo+ "," + value+")";  
	}
}

class Regla{
	int antecedenteId; 
	int numElementos; 
	String consecuente; 
	
	public Regla(int a, int b, String consec) {
		this.antecedenteId = a; 
		this.numElementos = b; 
		this.consecuente = consec; 
	}
	
	public String toString() {
		return "Antecedente: " + antecedenteId + ", numElementos: " + numElementos + ", consecuente: " + consecuente; 
	}
}

public class MT_ASINT {	

	/* Estructuras de datos y variables del programa */ 
	private static final int numTerminales = 59;

	// Mapa princpal de direccionamiento dentro de la tabla: 
	// <String A, Par B> : 	A = "Estado:Caracter"
	//							Estado = indice de la fila
	//							Caracter = indice de la columna
	//						B = Clase Par con la información del tipo de acción y el valor asociado. 
	//							Por ejemplo, si el tipo es desplazamiento, el valor asociado representa el próximo estado a desplazar, 
	//							y si es en el caso de reducción, se representa la regla por la que se aplica la reducción. 
	private static final Map<String, Acc_ASin> mt = new HashMap<>(); 

	// <Número de regla, regla> 
	private static final Map<Integer, Regla> reglas_map = new HashMap<>(); 

	// Asociacion del numero de columna y el id del token o caracter no terminal
	private static final Map<Integer, Integer> column_index_to_Id = new HashMap<>(); 

	// Asociación de tokens y caracteres no terminales con su id. 
	//-  El id del caracter no terminal es el índice de la columna en la ficha excel. 
	private static final Map<String, Integer> tablaIdentificador = new HashMap<>();

	// Lista de caracteres no terminales
	private static final Map<Integer, String> id_to_noTerm = new HashMap<>(); 

	/*------------------------------------------------------------------------------------*/

	// Obtiene el id numerico del token pasado como nombre
	public static int getTokenId(String tokenName) {
		return ALex.tok_id.get(tokenName) == null ? -1 : ALex.tok_id.get(tokenName); 
	}

	// Obtiene el elemento no terminal asociado al indice
	public static String getNoTerminalPorIndice(int index) {
		return id_to_noTerm.get(index) != null ? id_to_noTerm.get(index) : Token.getType(index); 
	}
	// Obtiene el id numerico del elemento no terminal con el id en formato cadena
	public static int getNoTerminalId(String antecedente) { return tablaIdentificador.get(antecedente);}

	// Obtiene la regla dado el numero de la regla
	public static Regla getRegla(int lineNumber) {return reglas_map.getOrDefault(lineNumber, new Regla(0, 0, ""));}

	// Obtiene el numero de elementos terminales
	public static int getNumTerminales() {return numTerminales;}
	
	/*------------------------------------------------------------------------------------*/

	public static Acc_ASin getAction(String key) {return mt.get(key); }	

	/* Funcion para obtener el valor numerico de una cadena */
	private static int getValue(String text) {
		int num = 0; 
		int i = 0; 

		// Evita el primer caracter si este no es numerico. 
		if((int)text.charAt(0)< 48  || (int)text.charAt(0)>57 ) { i++; }
		while(i<text.length()) {
			num = num*10 + ((int)text.charAt(i)-48); 
			i++; 
		}
		return num; 
	}

	// Debug method
	public static void imprimirMT() {
		for(String e : mt.keySet()) {
			String [] arr = e.split(":");
			int aux = Integer.parseInt(arr[1]); 
			String caracterEntrada = "$"; 
			if(aux < numTerminales) {
				caracterEntrada = Token.getType(aux);  
			}else if(aux > numTerminales) {
				caracterEntrada = getNoTerminalPorIndice(aux); 
			}
			System.out.println("Estado: " + arr[0] +", Entrada: "+ caracterEntrada  + " contains: " + mt.get(e));
		}
	}	

	// Method to process each rule and add it to the map
	private static void processRule(int lineNumber, String rule) {
		String[] parts = rule.split("->");
		parts[0] = parts[0].toUpperCase(); 
		int antecedenteId = tablaIdentificador.get(parts[0].trim());
		int consecuenteCount = parts[1].trim().equals("Lambda") ? 0 : parts[1].trim().split("\\s+").length;

		Regla regla = new Regla(antecedenteId, consecuenteCount, parts[1]);
		reglas_map.put(lineNumber, regla);
	}

	/* cargar_mt(filename)
	 * DESCRIPTION: Loads the SLR table from a CSV file.
	 * IN: String filename = The relative path to the file.
	 */
	public static void cargar_mt(String filename) throws IOException {
		InputStream inputStream = Procesador.class.getResourceAsStream(filename);
        BufferedReader br = new BufferedReader(new InputStreamReader(inputStream)); 
		//BufferedReader br = new BufferedReader(new FileReader(filename));
		String fila_cabecera = br.readLine(); 
		String [] cabecera = fila_cabecera.split(","); 
		for(int col_index = 1; col_index< cabecera.length ; col_index++) {

			String cell = cabecera[col_index].toUpperCase(); 
			cell = cell.replaceAll("\\s", "");
			if(cell.equals("$")) {
				cell = "EOF"; 
			}
			if(cell.equals("FIN")) {
				break; 
			}
			if(col_index<= numTerminales) {
				column_index_to_Id.put(col_index, ALex.tok_id.get(cell)); 
			}else {
				tablaIdentificador.put(cell, col_index); 
				id_to_noTerm.put(col_index, cell);  
				column_index_to_Id.put(col_index, col_index); 
			}
		}

		int state = 0; 
		String line;
		while ((line = br.readLine()) != null) {
			String[] transicion = line.split(","); // use comma as separator

			for(int i = 1; i<transicion.length-1; i++) {
				if(transicion[i] == "") {
					continue; 
				}
				String key = ""+state+":"+ column_index_to_Id.get(i); 

				if(transicion[i].charAt(0) == 's') {
					mt.put(key, new Acc_ASin(0,getValue(transicion[i]))); 
				}else if(transicion[i].charAt(0) == 'r'){
					mt.put(key, new Acc_ASin(1,getValue(transicion[i]))); 
				}else if(transicion[i].charAt(0) != 'a'){
					mt.put(key, new Acc_ASin(0,getValue(transicion[i]))); 
				}else {
					mt.put(key, new Acc_ASin(2,0)); 
				}
			}
			state++; 
		}
		br.close();			
		cargar_reglas(); 
	}


	private static void cargar_reglas() {
		processRule(1, "P -> M1 D R");
		processRule(2, "M1 -> Lambda");
		processRule(3, "R -> PP R");
		processRule(4, "R -> PF R");
		processRule(5, "R -> PR R");
		processRule(6, "R -> Lambda");
		processRule(7, "PP -> program PPid ; D M2 Bloque ;");
		processRule(8, "PPid -> Pid"); //done
		processRule(9, "Pid -> id");
		processRule(10, "M2 -> Lambda");
		
		processRule(11, "PR -> procedure PRidA ; D M2 Bloque ;");
		processRule(12, "PRidA -> Pid A"); //done
		processRule(13, "PF -> function PFidAT ; D M2 Bloque ;");
		processRule(14, "PFidAT -> Pid A : T"); //done
		processRule(15, "D -> var id : T ; DD");
		processRule(16, "D -> Lambda");
		processRule(17, "DD -> id : T ; DD");				
		processRule(18, "DD -> Lambda");
		processRule(19, "T -> boolean");
		processRule(20, "T -> integer");
		
		processRule(21, "T -> string");
		processRule(22, "A -> ( X id : T AA )");
		processRule(23, "A -> Lambda");
		processRule(24, "AA -> ; X id : T AA");
		processRule(25, "AA -> Lambda");
		processRule(26, "Bloque -> begin C end");
		processRule(27, "C -> B C");
		processRule(28, "C -> Lambda");
		processRule(29, "B -> if EE then S"); //done
		processRule(30, "EE -> E"); //done
		
		processRule(31, "B -> S"); //done
		processRule(32, "B -> if EE then Bloque ;"); //done
		processRule(33, "B -> if THEN else Bloque ;"); //done
		processRule(34, "THEN -> EE then Bloque ;"); //done
		processRule(35, "B -> while M3 EE do Bloque ;");
		processRule(36, "M3 -> Lambda");
		processRule(37, "B -> repeat M3 C until E ;");
		processRule(38, "B -> loop M3 C end ;");
		processRule(39, "B -> FOR do Bloque ;");
		processRule(40, "FOR -> for id := E to E");
		
		processRule(41, "B -> case EXP of N O end ;");
		processRule(42, "EXP -> E");
		processRule(43, "N -> N VALOR : Bloque ;");
		processRule(44, "VALOR -> entero");
		processRule(45, "N -> Lambda");
		processRule(46, "O -> otherwise : M3 Bloque ;");
		processRule(47, "O -> Lambda");
		processRule(48, "S -> write LL ;"); //done
		processRule(49, "S -> writeln LL ;"); //done
		processRule(50, "S -> read ( V ) ;"); //done pro ns q hay q emitir exactamente
		
		processRule(51, "S -> id := E ;"); //done		 
		processRule(52, "S -> id LL ;"); //done
		processRule(53, "S -> return Y ;"); //done
		processRule(54, "S -> exit when E ;");
		processRule(55, "LL -> ( L )"); //done
		processRule(56, "LL -> Lambda");
		processRule(57, "L -> E Q"); //done
		processRule(58, "Q -> , E Q"); //done
		processRule(59, "Q -> Lambda"); //done
		processRule(60, "V -> id W"); //done			
		
		processRule(61, "W -> , id W"); //done
		processRule(62, "W -> Lambda"); //done
		processRule(63, "Y -> E"); //done
		processRule(64, "Y -> Lambda");
		processRule(65, "E -> E or F");
		processRule(66, "E -> E xor F");
		processRule(67, "E -> F"); //done
		processRule(68, "F -> F and G"); //done
		processRule(69, "F -> G"); //done
		processRule(70, "G -> G = H"); //done
		
		processRule(71, "G -> G <> H");
		processRule(72, "G -> G > H");
		processRule(73, "G -> G >= H");
		processRule(74, "G -> G < H");
		processRule(75, "G -> G <= H");
		processRule(76, "G -> H"); //done
		processRule(77, "H -> H + I");
		processRule(78, "H -> H - I");
		processRule(79, "H -> I"); //done
		processRule(80, "I -> I * J"); //done
		
		processRule(81, "I -> I / J");
		processRule(82, "I -> I mod J");
		processRule(83, "I -> J"); //done
		processRule(84, "J -> J ** K");
		processRule(85, "J -> K"); //done
		processRule(86, "K -> not K");
		processRule(87, "K -> + K");
		processRule(88, "K -> - K");
		processRule(89, "K -> Z"); //done
		processRule(90, "Z -> entero"); //done
		
		processRule(91, "Z -> cadena"); //done
		processRule(92, "Z -> true");
		processRule(93, "Z -> false");
		processRule(94, "Z -> id LL"); //done
		processRule(95, "Z -> ( E )"); 
		processRule(96, "Z -> Z in ( L )"); 
		processRule(97, "Z -> max ( L )");
		processRule(98, "Z -> min ( L )"); //done
		processRule(99, "X -> var");
		processRule(100, "X -> Lambda");
				
	}
}
