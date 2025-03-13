# TDL

Implementacion de un **traductor de lenguajes** sobre un procesador de lenguajes facilitado por la asignatura. El traductor genera, en base a un archivo de codigo escrito en _lenguaje boreal_, a parte de los archivos del procesador (tabla de simbolos, parse, errores, tokens), uno con el codigo intermedio en el formato de un fichero de cuartetos.

Para descargar la libreria del procesador es necesario ejecutar el siguiente comando para que se instale en el repositoro local de maven:

```powershell
mvn install:install-file -Dfile=".\lib\ts-lib.jar" -DgroupId=tslib -DartifactId=ts-lib -Dversion="1.0" -Dpackaging=jar
```

---

#### Especificaciones del lenguaje boreal
👉 https://dlsiis.fi.upm.es/traductores/IntroBoreal.html
