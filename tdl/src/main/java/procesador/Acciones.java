package procesador;

enum Acciones {
	
	// Acciones del analizador léxico
	// Sintaxis: aN_M = Transicion del estado N a M. 

	Leer, 
	
	eol,

	none, 
	
	a1_11, a1_12,

	a0_2,

	a2_2, a2_21,

	a0_3, a3_3, a3_31,

	a0_4, a4_4, a4_41,
	
	a5_51, a5_52,

	a7_71, a7_72, a7_73,

	a8_81, a8_82,

	a0_100, a0_101, a0_102, a0_103, a0_104, a0_105, a0_106, a0_107, a0_108,
	
	
	//Acciones semánticas de error. 
	
	//Error por lectura de caracteres desconocidos desde el estado 0. 
	eLex0_ERROR_OC,

	//Error por lectura del caracter '}' sin iniciar el comentario. 
	eLex0_CIERRE_COMENTARIO_ILEGAL,
	
	//Error por lectura de EOL en una cadena de caracteres. 
	eLex2_ERROR_SALTO_LINEA, 
	
	//Error por superar la longitud máxima de cadena (64 caracteres). 
	eLex2_ERROR_LONGITUD_MAXIMA_CADENA,
	
	//Error por alcanzar el fin de fichero sin finalzar la declaración de cadena. 
	eLex2_ERROR_CADENA_INCOMPLETA,
	
	//Error por superar la longitud máxima de id (32 caracteres). 
	eLex3_ERROR_LONGITUD_MAXIMA_ID,
	
	//Error por superar el valor enterno máximo representable (2e15).
	eLex4_ERROR_VALOR_MAXIMO_ENTERO,
	
	//Error por no cerrar el comentario
	eLex6_ERROR_COMENTARIO_NO_CERRADO,
	
	//Error del analizador sintactico
	eSin0_ERROR_SINTACTICO,
		
	
	// Errores semanticos
	eSem1_loop,
	eSem2_tipo_incompatible,
	eSem3_tipo_retorno_incompatible,
	eSem4_for_error,
	eSem5_case_otherwise_error, 
	eSem6_case_error, 
	eSem7_case_bloque_error,
	eSem8_funcion_parametro_incompatible_error,
	eSem9_retorno_funcion_error,
	eSem10_expresion_error
	
	
	

}
