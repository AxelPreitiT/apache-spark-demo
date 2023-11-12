# ingsoft2-tpe-spark

Demo de Apache Spark para la materia 72.40 - Ingenieria del Software II del ITBA.
Contiene diversos ejemplos para mostrar el potencial de cómputo distribuido de Spark.

### Requisitos

* [Apache Spark](https://spark.apache.org/)
* [Python 3](https://www.python.org/)
* [pip](https://pypi.org/project/pip/)

### Consideraciones
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

### Ejecución
#### Nodo master
Para levantar el nodo master, se debe ejecutar el siguiente comando desde el directorio ``sbin`` de Spark:
```bash
./start-master.sh -h 0.0.0.0
```
Se levantará un servidor web en la dirección ``http://localhost:8080`` donde se podrá monitorear el estado de los nodos workers y las aplicaciones ejecutadas.

En la salida se informará la ubicación del archivo de logs que genera el nodo master, por ejemplo:
```bash
starting org.apache.spark.deploy.master.Master, logging to /mnt/c/Users/Axel/Downloads/spark-3.5.0-bin-hadoop3/logs/spark-axel-preitit-org.apache.spark.deploy.master.Master-1-DESKTOP-K6FJ9D4.out
```
Se recomienda utilizar el comando ``tail -f`` para monitorear el archivo de logs:
```bash
tail -f /mnt/c/Users/Axel/Downloads/spark-3.5.0-bin-hadoop3/logs/spark-axel-preitit-org.apache.spark.deploy.master.Master-1-DESKTOP-K6FJ9D4.out
```

Si se desea detener el nodo master, se debe ejecutar el siguiente comando desde el directorio ``sbin`` de Spark:
```bash
./stop-master.sh
```

#### Nodo worker
Para levantar un nodo worker, se debe ejecutar el siguiente comando desde el directorio ``sbin`` de Spark:
```bash
./start-worker.sh spark://<master-ip>:7077 -m [memory] -c [cores]
```
En ``<master-ip>`` se debe indicar la dirección IP del nodo master.
En ``[memory]`` se debe indicar la cantidad de memoria RAM que se le asignará al nodo worker.
En ``[cores]`` se debe indicar la cantidad de cores que se le asignará al nodo worker.
Una vez levantado el nodo worker, se podrá monitorear su estado desde la interfaz web del nodo master, en la dirección ``http://localhost:8080``.

En la salida se informará la ubicación del archivo de logs que genera el nodo worker, por ejemplo:
```bash
starting org.apache.spark.deploy.worker.Worker, logging to /mnt/c/Users/Axel/Downloads/spark-3.5.0-bin-hadoop3/logs/spark-axel-preitit-org.apache.spark.deploy.worker.Worker-1-DESKTOP-K6FJ9D4.out
```
Se recomienda utilizar el comando ``tail -f`` para monitorear el archivo de logs:
```bash
tail -f /mnt/c/Users/Axel/Downloads/spark-3.5.0-bin-hadoop3/logs/spark-axel-preitit-org.apache.spark.deploy.worker.Worker-1-DESKTOP-K6FJ9D4.out
```

Si se desea detener el nodo worker, se debe ejecutar el siguiente comando desde el directorio ``sbin`` de Spark:
```bash
./stop-worker.sh
```

#### Aplicación
##### `src/rangeCollector.py`
Este script permite distribuir la carga de procesamiento para la generación de un rango de números.
Para ejecutarlo en el cluster de Spark, se debe ejecutar el siguiente comando desde el directorio `bin` de Spark:
```bash
./spark-submit --master spark://<master-ip>:7077 [Ubicación del repo]/src/rangeCollector.py [limit]
```
__Parámetros:__
- ``<master-ip>``: Dirección IP del nodo master.
- ``[limit]``: Límite superior del rango de números a generar.

Devolverá un archivo en el directorio `src/results` con el rango de números generado, con el nombre `range_<limit>.txt`.


##### `src/piEstimator.py`
Este script permite estimar el valor de pi utilizando el método de Monte Carlo.
Para ejecutarlo en el cluster de Spark, se debe ejecutar el siguiente comando desde el directorio `bin` de Spark:
```bash
./spark-submit --master spark://<master-ip>:7077 [Ubicación del repo]/src/piEstimator.py [samples]
```
__Parámetros:__
- ``<master-ip>``: Dirección IP del nodo master.
- ``[samples]``: Cantidad de muestras a utilizar para la estimación.

Devolverá un archivo en el directorio `src/results` con el valor estimado de pi, con el nombre `pi_<samples>.txt`.


##### `src/wordCounter.py`
Este script permite contar la cantidad de apariciones de cada palabra en un archivo de texto.
Para ejecutarlo en el cluster de Spark, se debe ejecutar el siguiente comando desde el directorio `bin` de Spark:
```bash
./spark-submit --master spark://<master-ip>:7077 [Ubicación del repo]/src/wordCounter.py [path]
```
__Parámetros:__
- ``<master-ip>``: Dirección IP del nodo master.
- ``[path]``: Ruta al archivo de texto.

Devolverá un archivo en el directorio `src/results` con la cantidad de apariciones de cada palabra, con el nombre `wordCounter_<path>.txt`.


### Contribuidores
* [Alejo Flores Lucey](https://github.com/alejofl)
* [José Mentasti](https://github.com/JoseMenta)
* [Nehuén Llanos](https://github.com/NehuenLlanos)
* [Andrés Carro Wetzel](https://github.com/AndresCarro)
* [Gastón Francois](https://github.com/francoisgaston)
* [Axel Preiti Tasat](https://github.com/AxelPreitiT)