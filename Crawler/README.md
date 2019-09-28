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
https://www.elcomercio.es
```

Y esta ejecucion con los argumentos por defecto:

````cmd
python3 Main.py 
````
 
 Se realiza una exploracion en anchura:
 
 ```txt
https://www.elcomercio.es
	https://www.elcomercio.es/asturias/
	https://www.elcomercio.es/oviedo/
	https://www.elcomercio.es/gijon/
	https://www.elcomercio.es/aviles/
	https://www.elcomercio.es/asturias/cuencas/
	https://www.elcomercio.es/asturias/siero-centro/
	https://www.elcomercio.es/asturias/oriente/
	https://www.elcomercio.es/asturias/occidente/
	https://www.elcomercio.es/asturias/mas-concejos/
	https://www.elcomercio.es/politica/
```

Y esta ejecucion con los argumentos por defecto salvo la opcion dada -d para que la exploracion sea en profundidad:

````cmd
python3 Main.py -d
````
 
 Se realiza una exploracion en profundidad:
 
 ```txt
https://www.elcomercio.es
	https://www.elcomercio.es/asturias/
	https://www.elcomercio.es/asturias/cuencas/simulacro-accidente-mieres-6089612163001-20190926090933-vi.html#vca=modulos&vso=elcomercio&vmc=lo-mas-visto&vli=asturias
	https://www.elcomercio.es/asturias/cuencas/rescatada-mujer-herida-ruta-5608769846001-20171013121000-vi.html?autoStart=true
	https://www.elcomercio.es/asturias/cuencas/simulacro-accidente-mieres-6089612163001-20190926090933-vi.html?autoStart=true
	https://www.elcomercio.es/asturias/cuencas/rescatada-mujer-herida-ruta-5608769846001-20171013121000-vi.html
	https://www.elcomercio.es/asturias/cuencas/video-viral-dedicado-zoquetes-5707197864001-20180110210132-vi.html?autoStart=true
	https://www.elcomercio.es/asturias/cuencas/video-viral-dedicado-zoquetes-5707197864001-20180110210132-vi.html
	https://www.elcomercio.es/asturias/cuencas/alud-isidro-5713026171001-20180116220108-vi.html?autoStart=true
	https://www.elcomercio.es/asturias/cuencas/alud-isidro-5713026171001-20180116220108-vi.html
	https://www.elcomercio.es/asturias/cuencas/macho-cabrio-destroza-portal-5715030574001-20180119110152-vi.html?autoStart=true
```

Si realizamos los mismo pasos pero cambiando el archivo de urls a este (28/09/19):

```txt
https://cosmere.es
http://www.uniovi.es/
```

Se obtiene respectivamente:

``` txt
https://cosmere.es
	https://cosmere.es/guia-de-lectura/por-donde-empiezo/
	https://cosmere.es/guia-de-lectura/que-es-el-cosmere/
	https://roshar.cosmere.es
	https://cosmere.es/guia-de-lectura/orden-de-lectura-del-cosmere/
	https://cosmere.es/libros-del-cosmere/
	https://cosmere.es/libros-del-cosmere/elantris/
	https://cosmere.es/libros-del-cosmere/#nacidos-de-la-bruma
	https://cosmere.es/libros-del-cosmere/nacidos-de-la-bruma-02-el-pozo-de-la-ascension/
	https://cosmere.es/libros-del-cosmere/nacidos-de-la-bruma-04-aleacion-de-ley/
	https://cosmere.es/libros-del-cosmere/nacidos-de-la-bruma-06-brazales-de-duelo/
http://www.uniovi.es/
	http://www.uniovi.es/inicio
	https://intranet.uniovi.es
	http://www.uniovi.es/inicio;jsessionid=C86D90EF7E687C3EDC6A28F8DA873A1E?p_p_id=82&p_p_lifecycle=1&p_p_state=normal&p_p_mode=view&_82_struts_action=%2Flanguage%2Fview&_82_redirect=%2F&languageId=ast_ES
	http://www.uniovi.es/inicio;jsessionid=C86D90EF7E687C3EDC6A28F8DA873A1E?p_p_id=82&p_p_lifecycle=1&p_p_state=normal&p_p_mode=view&_82_struts_action=%2Flanguage%2Fview&_82_redirect=%2F&languageId=en_US
	http://www.uniovi.es/launiversidad
	http://www.uniovi.es/launiversidad/panoramica
	http://www.uniovi.es/launiversidad/historia
	http://www.uniovi.es/launiversidad/entorno
	http://www.uniovi.es/estudios
	http://www.uniovi.es/estudios/grados
```

```txt
https://cosmere.es
	https://cosmere.es/guia-de-lectura/por-donde-empiezo/
	https://cosmere.es/guia-de-lectura/que-es-el-cosmere/
	https://roshar.cosmere.es
	https://botanicaxu.tumblr.com
	https://www.tumblr.com/register
	https://itsakilahobviously.com/post/187934609742/since-i-announced-my-book-deal-here-it-is-only
	https://statcounter.com/tumblr/
	http://statcounter.com/blogger/
	http://statcounter.com/zine_studio/
	http://statcounter.com/sign-up/?guide=zine_studio
http://www.uniovi.es/
	http://www.uniovi.es/inicio
	http://www.uniovi.es/inicio;jsessionid=3C8279128B3739CECFDA2832DCA1FCBC?p_p_id=82&p_p_lifecycle=1&p_p_state=normal&p_p_mode=view&_82_struts_action=%2Flanguage%2Fview&_82_redirect=%2Finicio&languageId=en_US
	http://www.uniovi.es/en/comunicacion/noticias/-/asset_publisher/33ICSSzZmx4V/content/representantes-de-investigacion-transferencia-e-innovacion-del-g-9-de-universidades-realizan-una-visita-institucional-a-bruselas-para-conocer-las-poli?p_p_auth=3nLGhR5j&redirect=%2Fen%2Finicio%3Bjsessionid%3D71A4B908031CE7F05B967C7748A6F94A
	http://www.uniovi.es/recursos/otraswebs
	https://intranet.uniovi.es/convocatorias/proyeccioninternacional/otrosorganismos
	http://www.uniovi.es/vida/identidad
	http://www.uniovi.es/internacional/extranjeros/planifica/aduo
	http://www.uniovi.es/internacional/extranjeros/planifica;jsessionid=58186D29A4B46B15DEAEE197505295B3
	https://intranet.uniovi.es/convocatorias/proyeccioninternacional
	http://www.uniovi.es/comunicacion/duo/convocatorias/-/asset_publisher/cxX13ntusT2E/content/id/24407674
```