package procesador;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;

import tslib.TS_Gestor;

// Clase principal
public class Procesador {

	public static TS_Gestor gestorTS;

	public static void main(String[] args) {

		if(args.length != 1) {
			System.out.println("Debes introducir un fichero para analizar");
			System.exit(1);
		}
		String testFile = args[0];
		
		// Ficheros csv
		String mtFile = "/MTD_data.csv";
		String slr_table = "/SLR_data.csv";

		// Ficheros txt
		String tokensFile = "tokens.txt";
		String errorFile = "errores.txt";
		String tsFile = "ts.txt";
		String parse = "parse.txt";
		String cuartetos = "cuartetos.txt";

		// Entrada/Salida
		BufferedReader ptrTest = null;
		BufferedWriter ptwTokens = null;
		BufferedWriter ptwError = null;
		BufferedWriter ptwParse = null;
		BufferedWriter ptwCuartetos = null;

		try {
			ptrTest = new BufferedReader(new FileReader(testFile));
			ptwTokens = new BufferedWriter(new FileWriter(tokensFile));
			ptwError = new BufferedWriter(new FileWriter(errorFile));
			ptwParse = new BufferedWriter(new FileWriter(parse));
			ptwCuartetos = new BufferedWriter(new FileWriter(cuartetos));
		
		// Tabla de símbolos
		gestorTS = new TS_Gestor(tsFile);
		gestorTS.activarDebug();
		gestorTS.createTPalabrasReservadas();

		// Configuracion Gestor de error
		GestorError.setOutputMessageFile(ptwError);

		// Configuracion Analizador léxico
		ALex.cargar_mt(mtFile);
		ALex.setInputFile(ptrTest);
		ALex.setTokenOutputFile(ptwTokens);
		gci.setOutputfile(ptwCuartetos);

		// Configuracion Analizador sintactico
		MT_ASINT.cargar_mt(slr_table);
		ASin.setOutputParseFile(ptwParse);

		// Inicio de ejecución: Analisis lexico, sintactico y semantico sincronizado
		ASin.pedirTokens();

		// aqui habra q meter los cuartetos generados en el fichero

		// Cierre
		ptrTest.close();
		ptwTokens.close();
		ptwError.close();
		ptwParse.close();
		ptwCuartetos.close();
		
		} catch (FileNotFoundException e) {
			e.printStackTrace(); 
			System.out.println("No ha sido posible encontrar los ficheros");
			System.exit(1);
		} catch (IOException e) {
			e.printStackTrace();
			System.out.println("Error en procesos de entrada o salida");
			System.exit(1);
		}
		
		String currDir = System.getProperty("user.dir"); 
		
		System.out.println("Se han generado los siguientes ficheros: "
							+ "\n \t - Parse en \t\t\t'"+ currDir +"\\" + parse + "'" + 
							"\n \t - Tokens en \t\t\t'" + currDir +"\\" +tokensFile + "'" +
							"\n \t - Tabla de símbolos en \t'"+currDir +"\\" +tsFile + "'"
							+"\n \t - Errores en \t\t\t'" + currDir +"\\" +errorFile + "'"+
							"\n \t - Cuartetos en \t\t'" + currDir +"\\" +cuartetos + "'" );

	}

}
