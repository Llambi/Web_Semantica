# Crawler

El objetivo del ejercicio es crear un script en Python que implemente un ​crawler ​básico 
para la descarga de archivos HTML. Dicho script deberá permitir al menos la configuración 
mediante el paso de 3 parámetros:

1. El nombre del fichero que contiene las URLs semilla (--file): Por defecto _resources/links.txt_.
2. El máximo de archivos a descargar (--mx): Por defecto _10_.
3. El tiempo (en segundos) que debe esperar entre dos peticiones ​GET​ (--sec): Por defecto _2_.

Ademas se han añadido los siguientes argumentos a la ejecución:

1. El nombre del fichero en el que se guardan los resultados de la exploración (--output): Por defecto resources/result[StrategyType].txt
2. El nombre del crawler que se usará para el user-agent (--name): Por defecto _UOCrawler_
3. El tipo de exploración que se realizará (No se podran realizar los dos tipos a la vez):
    1. Profundidad (-d).
    2. Anchura (-w).
    
Además el Crawler comprobara si, con el user-agent dado, puede explorar las urls.

## Ejecuciones 

Con el siguiente archivo (28/09/19):

```txt 
https://www.elconfidencial.com
```

Y esta ejecucion con los argumentos por defecto:

````cmd
python3 Main.py 
````
 
 Se realiza una exploracion en anchura:
 
 ```txt
Crawling https://www.elconfidencial.com
        Crawling https://www.elconfidencial.com/tecnologia/ciencia/2019-09-27/ultima-hora-huelga-clima_2258607/
        Crawling https://www.elconfidencial.com/tecnologia/ciencia/2019-09-27/huelga-clima-horario-recorrido-manifestaciones-328_2253435/
        Crawling https://www.elconfidencial.com/elecciones-generales/2019-09-27/errejon-lista-barcelona-dilema-5-colau-mas-pais_2256675/
        Crawling https://www.elconfidencial.com/espana/2019-09-27/direccion-podemos-murcia-se-pasa-a-mas-pais_2257663/
        Crawling https://www.elconfidencial.com/tecnologia/2019-09-27/iphone-11-pro-opinion-precio-caracteristicas-espana-316_2253103/
        Crawling https://www.elconfidencial.com/mundo/2019-09-27/le-falta-sexo-un-locutor-brasileno-despedido-por-insultar-a-greta-en-directo_2257623/
        Crawling https://www.elconfidencial.com/tecnologia/ciencia/2019-09-27/hallan-planeta-desafia-teoria-formacion-planetaria_2257679/
        Crawling https://www.elconfidencial.com/espana/andalucia/2019-09-27/sucesos-muerto-pirotecnia-guadiz-granada_2259568/
        Crawling https://www.elconfidencial.com/espana/tiempo/
        Crawling https://www.elconfidencial.com/mundo/2019-09-27/sucesos-rescatan-300-personas-torturadas_2259360/
```

Y esta ejecucion con los argumentos por defecto salvo la opcion dada -d para que la exploracion sea en profundidad:

````cmd
python3 Main.py -d
````
 
 Se realiza una exploracion en profundidad:
 
 ```txt
https://www.elconfidencial.com
	https://www.elconfidencial.com/tecnologia/ciencia/2019-09-27/ultima-hora-huelga-clima_2258607/
	https://www.elconfidencial.com/descuentos/yoigo
	https://www.elconfidencial.com/descuentos/yoigo/descuentos/vertbaudet
	https://www.elconfidencial.com/descuentos/yoigo/descuentos/ulanka
	https://www.elconfidencial.com/descuentos/yoigo/descuentos/tiendanimal
	https://www.elconfidencial.com/descuentos/yoigo/descuentos/sklum
	https://www.elconfidencial.com/descuentos/yoigo/descuentos/shein
	https://www.elconfidencial.com/descuentos/yoigo/descuentos/sarenza
	https://www.elconfidencial.com/descuentos/yoigo/descuentos/prozis
	https://www.elconfidencial.com/descuentos/yoigo/descuentos/pccomponentes
```

Si realizamos los mismo pasos pero cambiando el archivo de urls a este (28/09/19):

```txt
https://www.elconfidencial.com
https://www.elcomercio.es
```

Se obtiene respectivamente:

``` txt
https://www.elconfidencial.com
	https://www.elconfidencial.com/tecnologia/ciencia/2019-09-27/ultima-hora-huelga-clima_2258607/
	https://www.elconfidencial.com/tecnologia/ciencia/2019-09-27/huelga-clima-horario-recorrido-manifestaciones-328_2253435/
	https://www.elconfidencial.com/elecciones-generales/2019-09-27/errejon-lista-barcelona-dilema-5-colau-mas-pais_2256675/
	https://www.elconfidencial.com/espana/2019-09-27/direccion-podemos-murcia-se-pasa-a-mas-pais_2257663/
	https://www.elconfidencial.com/tecnologia/2019-09-27/iphone-11-pro-opinion-precio-caracteristicas-espana-316_2253103/
	https://www.elconfidencial.com/mundo/2019-09-27/le-falta-sexo-un-locutor-brasileno-despedido-por-insultar-a-greta-en-directo_2257623/
	https://www.elconfidencial.com/tecnologia/ciencia/2019-09-27/hallan-planeta-desafia-teoria-formacion-planetaria_2257679/
	https://www.elconfidencial.com/espana/andalucia/2019-09-27/sucesos-muerto-pirotecnia-guadiz-granada_2259568/
	https://www.elconfidencial.com/espana/tiempo/
	https://www.elconfidencial.com/mundo/2019-09-27/sucesos-rescatan-300-personas-torturadas_2259360/
https://www.elcomercio.es
	https://www.elcomercio.es/
	https://www.elcomercio.es/asturias/
	https://www.elcomercio.es/oviedo/
	https://www.elcomercio.es/gijon/
	https://www.elcomercio.es/aviles/
	https://www.elcomercio.es/asturias/cuencas/
	https://www.elcomercio.es/asturias/siero-centro/
	https://www.elcomercio.es/asturias/oriente/
	https://www.elcomercio.es/asturias/occidente/
	https://www.elcomercio.es/asturias/mas-concejos/
```

```txt
https://www.elconfidencial.com
	https://www.elconfidencial.com/tecnologia/ciencia/2019-09-27/ultima-hora-huelga-clima_2258607/
	https://www.elconfidencial.com/descuentos/yoigo
	https://www.elconfidencial.com/descuentos/yoigo/descuentos/vertbaudet
	https://www.elconfidencial.com/descuentos/yoigo/descuentos/ulanka
	https://www.elconfidencial.com/descuentos/yoigo/descuentos/tiendanimal
	https://www.elconfidencial.com/descuentos/yoigo/descuentos/sklum
	https://www.elconfidencial.com/descuentos/yoigo/descuentos/shein
	https://www.elconfidencial.com/descuentos/yoigo/descuentos/sarenza
	https://www.elconfidencial.com/descuentos/yoigo/descuentos/prozis
	https://www.elconfidencial.com/descuentos/yoigo/descuentos/pccomponentes
https://www.elcomercio.es
	https://www.elcomercio.es/
	https://www.elcomercio.es//sociedad/historias-asturias/
	https://www.elcomercio.es//sociedad/historias-asturias//sociedad/historias-asturias/
	https://www.elcomercio.es//sociedad/historias-asturias//
	https://www.elcomercio.es//sociedad/historias-asturias///sociedad/historias-asturias/
	https://www.elcomercio.es//sociedad/historias-asturias///
	https://www.elcomercio.es//sociedad/historias-asturias////sociedad/historias-asturias/
	https://www.elcomercio.es//sociedad/historias-asturias////
	https://www.elcomercio.es//sociedad/historias-asturias/////sociedad/historias-asturias/
	https://www.elcomercio.es//sociedad/historias-asturias/////
```