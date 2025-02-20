cada instruccion del generador de codigo intermedio se traduce a lenguaje ensamblador.

con atributos heredados la info va hacia abajo u horizontal y con los sintetizados va hacia arriba.


---

==**PRACTICA**==
recursividad, cadenas de caracteres comillas simples max 64 cars, true false opcionales, podemos usar parentesis para agrupar operaciones, las expresiones se tienen que evaluar completamente. op aritmeticos, relacionales, logicos, potencia (`**`), concatenacion de cadenas mediante `+`, de pertenencia (si un valor esta dentro de una lista de expresiones), max y min.
los **identificadores** empiezan por letra y pds tener letras y digitos.
**declaraciones** tal que `var nombre: tipo`, si no se inicializan se quedan a 0, false, o ''.

3 tipos:
- entero
- logico
- cadena

2 instrucciones para **imprimir**, `write` y `writeln`.
para leer variables por teclado usamos `read`.
solo sirven para cadenas y enteros.

**asignacion** `:=` y del mismo tipo ==no hay conversion de tipos==

no hay restricciones de cuantos `return` pueden haber en un programa

sentencia condicional sencilla -> `If condicion Then sentencia`
el cuerpa del condicional y while va con `begin - end`

el resto de bucles y tal verlo en la web

el param se pasa por valor a menos que lleve var entonces se pasa por referencia.

**procesador de boreal** -> implementado con un asis ascendente y sin atributos heredados (no usarlos) puede tener errores es el primer año que lo usan.

para darle valor a una cadena tenemos que usar un **operador de asignacion distinto** al que usamos con los logicos y con los enteros.

> e.g.
```
S -> id := E {if (E.tipo pertenece (log, ent)) Then 
				emite(BuscaLugarTS(id.pos), ':=', E.lugar)
			if (E.tipo = cad) Then 
				emite(BuscaLugarTS(id.pos), ':=st', E.lugar)}
```

**cuartetos**: OPERADOR, ARG1, ARG2, RES

con un salto condicional es: goto_oprel X Y etiqueta
un call seria: call et
si es un x := call et entonces: callf et - x
return x es: return - - x
y et: es: ET et - -

>**funcion emite**
``` c
void emite (op, arg1, arg2, res) {
	gco(op, arg1, arg2, res);
}
```

`nueva_temp(tipo)` añadir en la TS una nueva var con su tipo desp.


---

consultar -> https://dlsiis.fi.upm.es/traductores/Practica.html