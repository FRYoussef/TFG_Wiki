Subcontracting: Subcontracting metric: The main idea is to count the number of times individual 
j executed an activity in-between two activities executed by individual i. 
This may indicate that work was subcontracted from i to j.

Por lo que los usuarios que est�n aislados en el grafo indican que han hecho una secuencia de ediciones seguidas sobre s� mismos,
de modo que entre sus ediciones no edita nadie m�s. Por ejemplo Nachosan hico 4 ediciones seguidas (en el transcurso de 2 horas) a Airbus y 2 a Bifaz. 
Luego aquellos con muchas conexiones indican que han hecho ediciones consistentemente espaciadas en el tiempo. Se ve que muchos hacen
ediciones puntuales en un momento dado, y pueden hacer varias seguidas y luego ya no editan m�s en ese mismo art�culo.

Reassingment no tiene sentido aplicarla pues la estructura de ediciones es an�rquica y el orden en el que se realizan no es jer�rquico


MINERO SOCIAL APLICADO A LOG: 
	-CORPUS_CLEAN.CSV -> CORPUS_CLEAN_LOG.XES elima todos autores menos 5 rev
	-CORPUS_FILTERED.CSV -> CORPUS_FILTERED.XES agropa revisores menos de 5 en casual
	-CORPUS_BEST_EDITORS_FILTERED.XES que proviene de:
		*CORPUS_BEST_EDITORS.CSV pasado a xes y filtrado sin ANONYMOUS

PROCESS MINING:
	-A NIVEL ART�CULO: CORPUS.CSV Y FILTRAR ANONYMOUS
	-A NIVEL RESOURCE: CORPUS_CLEAN Y FILTRAR ANONYMOUS
	-AGRUPAR EDITORES POR CATEGORIAS Y USAR ESO DE RESOURCE PARA ANALISIS A NIVEL DE RESOURCE

en lugar de cambiar el nombre de uuario por casual o lo que sea,
crear otro atributo llamado rol para agrupar, es m�s limpio y puedo usar mismo
dataset para todo