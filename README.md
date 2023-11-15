# Demo Ing. Software 2 TPE-Spark

Demo de Apache Spark para la materia 72.40 - Ingenieria del Software II del ITBA.
Contiene diversos ejemplos para mostrar el potencial de cómputo distribuido de Spark.

### Requisitos

* [Apache Spark](https://spark.apache.org/)
* [Docker](https://www.docker.com/)


## Ejecución

### Word count distribuído
Para esta prueba, se buscará implementar de manera distribuida un word counter para el guión de una película. En este caso será necesaria la utilización de Docker, y se utilizara 
#### Nodo Master
Para la configuración del nodo master, moverse a la carpeta de spark y levantar el proceso.
```bash
cd <directorio_spark>/sbin

./start-master.sh -h 0.0.0.0
```

Una vez levantada la instancia de Master, el resto de los nodos Workers pueden conectarse

Para ver los workers conectados se sugiere revisar http://localhost:8080/


Cuando todos los nodos workers se hayan conectado dirigirse a la carpeta /bin y levantar una consola de Scala
```bash
cd ./../bin

./spark-shell --master spark://<IP propia>:7077
```

Una vez en la consola proceder a realizar el word count en Scala

```scala
val textFile = sc.textFile("/tmp/texts/HarryPotter.txt")

val counts = textFile.flatMap(line => line.split(" ")).map(word => (word,1)).reduceByKey(_ + _)

counts.collect()
```

Resulta necesario que el nodo master tenga el archivo a procesar en el path /tmp/texts/HarryPotter.txt


#### Nodo Worker
Para la configuración de los nodos workers, moverse a la carpeta de spark y levantar el proceso 
```bash
cd <directorio_spark>/sbin

./start-worker.sh spark://<IP master>:7077
```
Para ver el estado de los trabajos asociados,se sugiere revisar http://localhost:8081/


Resulta necesario que todos los nodos workers tengan el archivo a procesar en el path /tmp/texts/HarryPotter.txt

### Calculo de PI distribuido
En esta prueba se intentará estimar el valor de PI mediante el Método de Monte Carlo, distribuyendo los puntos a procesar entre todos los nodos.

#### Nodo Master
Para la configuración del nodo master, moverse a la carpeta de spark y levantar el proceso.
```bash
cd <directorio_spark>/sbin

./start-master.sh -h 0.0.0.0
```

Una vez levantada la instancia de Master, el resto de los nodos Workers pueden conectarse

Para ver los workers conectados se sugiere revisar http://localhost:8080/


Cuando todos los nodos workers se hayan conectado dirigirse a la carpeta /bin y levantar una consola de Scala
```bash
cd ./../bin

./spark-shell --master spark://<IP propia>:7077
```
Una vez en la consola proceder a realizar el cálculo de PI en scala

```scala
val NUM_SAMPLES=100000000

val count = sc.parallelize(1 to NUM_SAMPLES).filter { _ =>
  val x = math.random
  val y = math.random
  x*x + y*y < 1
}.count()

println(s"Pi es casi ${4.0 * count / NUM_SAMPLES}")
```


#### Nodo Worker
En este caso, vamos a hacer el procedimiento con docker. En primer lugar descargamos la imagen
```bash
docker pull spark
```
Luego, creamos el contenedor 
```bash
docker run -it --rm -p 8081:8081 spark bash
```
Adentro del contenedor, nos registramos con el nodo master
```bash
cd ..
./sbin/start-worker.sh spark://<ip_master>:7077
```

## Consideraciones
Cuando se ejecuta un nuevo trabajo distribuido en el cluster, Spark ofrece una interfaz que permite monitorear el estado de la ejecución y analizar métricas de performance.
Sin embargo, cuando este trabaja finaliza, Spark deja de ofrecer esta interfaz y ya no es posible acceder a las métricas de performance.
Por lo tanto, para poder seguir analizandolo y no perder esa información, se debe configurar Apache Spark para que genere un archivo de logs con la información de la aplicación ejecutada y levantar un servidor web para reconstruir la interfaz de monitoreo.
Los pasos a seguir son los siguientes:
1. Crear el directorio donde se almacenarán los logs de Spark
    ```bash
    mkdir /tmp/spark-events
    ```
   
2. Copiar el template ``conf/spark-defaults.conf.template`` y crear el archivo ``conf/spark-defaults.conf`` en el directorio ``conf`` de Spark
    ```bash
    cp spark-defaults.conf.template spark-defaults.conf
    ```

3. Descomentar la siguiente línea en el archivo ``conf/spark-defaults.conf`` y guardar los cambios
    ```bash
    spark.eventLog.enabled           true
    ```
   Esta línea habilita la generación de logs de Spark para cada aplicación ejecutada.


4. Descomentar la siguiente línea en el archivo ``conf/spark-defaults.conf`` y guardar los cambios
    ```bash
    spark.eventLog.dir               file:///tmp/spark-events
    ```
    Esta línea indica el directorio donde se almacenarán los logs de Spark.

Ahora, luego de levantar el nodo master y los nodos workers, se debe levantar un servidor web para reconstruir la interfaz de monitoreo.
Para esto, se debe ejecutar el siguiente comando desde el directorio ``sbin`` de Spark:
```bash
./start-history-server.sh
```
Luego, se puede acceder a la interfaz de monitoreo desde el navegador web en la dirección ``http://localhost:18080``.

En la salida se informará la ubicación del archivo de logs que genera el servidor web, por ejemplo:
```bash
starting org.apache.spark.deploy.history.HistoryServer, logging to /mnt/c/Users/Axel/Downloads/spark-3.5.0-bin-hadoop3/logs/spark-axel-preitit-org.apache.spark.deploy.history.HistoryServer-1-DESKTOP-K6FJ9D4.out
```
Se recomienda utilizar el comando ``tail -f`` para monitorear el archivo de logs:
```bash
tail -f /mnt/c/Users/Axel/Downloads/spark-3.5.0-bin-hadoop3/logs/spark-axel-preitit-org.apache.spark.deploy.history.HistoryServer-1-DESKTOP-K6FJ9D4.out
```

Si se desea detener el servidor web, se debe ejecutar el siguiente comando desde el directorio ``sbin`` de Spark:
```bash
./stop-history-server.sh
```

Para más información, consultar la [documentación oficial](https://spark.apache.org/docs/latest/monitoring.html) de Apache Spark.


## Contribuidores
* [Alejo Flores Lucey](https://github.com/alejofl)
* [José Mentasti](https://github.com/JoseMenta)
* [Nehuén Llanos](https://github.com/NehuenLlanos)
* [Andrés Carro Wetzel](https://github.com/AndresCarro)
* [Gastón Francois](https://github.com/francoisgaston)
* [Axel Preiti Tasat](https://github.com/AxelPreitiT)

