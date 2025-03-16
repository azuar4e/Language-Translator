# TDL

Proyecto de la asignatura **Traductores de Lenguajes**, realizado en Java con el uso de Maven.

Implementacion de un **traductor de lenguajes** sobre un procesador de lenguajes facilitado por la asignatura. El traductor genera, en base a un archivo de codigo escrito en _lenguaje boreal_, a parte de los archivos del procesador (tabla de simbolos, parse, errores, tokens), uno con el codigo intermedio en el formato de un fichero de cuartetos.

Para descargar la libreria del procesador es necesario ejecutar el siguiente comando para que se instale en el repositoro local de maven:

```powershell
mvn install:install-file -Dfile=".\lib\ts-lib.jar" -DgroupId=tslib -DartifactId=ts-lib -Dversion="1.0" -Dpackaging=jar
```

Para ejecutar el traductor es necesario ejecutar el siguiente comando:

```powershell
java -jar .\target\tdl-1.0-SNAPSHOT-jar-with-dependencies.jar .\ruta\al\ficheroBoreal
```

---

#### Especificaciones del lenguaje boreal

👉 https://dlsiis.fi.upm.es/traductores/IntroBoreal.html

#### Formato de los ficheros de cuartetos

👉 https://dlsiis.fi.upm.es/traductores/Documentos/formato_fichero_cuartetos.pdf
