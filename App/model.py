"""
 * Copyright 2020, Departamento de sistemas y Computación
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 """
import config
from DISClib.ADT import list as lt
from DISClib.DataStructures import listiterator as it
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import map as m
import datetime
assert config
from math import radians, cos, sin, asin, sqrt


"""
En este archivo definimos los TADs que vamos a usar,
es decir contiene los modelos con los datos en memoria

Se define la estructura de un catálogo de libros.
El catálogo tendrá  una lista para los libros.

Los autores, los tags y los años se guardaran en
tablas de simbolos.
"""

# -----------------------------------------------------
# API del TAD Catalogo de Libros
# -----------------------------------------------------


def newAnalyzer():
    """ Inicializa el analizador

    Crea una lista vacia para guardar todos los crimenes
    Se crean indices (Maps) por los siguientes criterios:
    -Fechas

    Retorna el analizador inicializado.
    """
    analyzer = {'accidentes': None,
                'fechas': None
                }

    analyzer['accidentes'] = lt.newList('SINGLE_LINKED', compareIds)
    analyzer['fechas'] = om.newMap(omaptype='RBT',
                                      comparefunction=compareDates)
    return analyzer


# Funciones para agregar informacion al catalogo


def addAccident(analyzer, accidente):
    """
    """
    lt.addLast(analyzer['accidentes'], accidente)
    updateDateIndex(analyzer['fechas'], accidente)
    return analyzer


def updateDateIndex(map, accidente):
    """
    Se toma la fecha del crimen y se busca si ya existe en el arbol
    dicha fecha.  Si es asi, se adiciona a su lista de crimenes
    y se actualiza el indice de tipos de crimenes.

    Si no se encuentra creado un nodo para esa fecha en el arbol
    se crea y se actualiza el indice de tipos de crimenes
    """
    occurreddate = accidente['Start_Time']
    accidentdate = datetime.datetime.strptime(occurreddate, '%Y-%m-%d %H:%M:%S')
    entry = om.get(map, accidentdate.date())
    if entry is None:
        datentry = newDataEntry(accidente)
        om.put(map, accidentdate.date(), datentry)
    else:
        datentry = me.getValue(entry)
    addDateIndex(datentry, accidente)
    return map

def estado_mayor(analyzer, initial, final):
    lst = om.values(analyzer['fechas'], initial, final)
    dict={}
    dict_fechas={}
    #mapa=mp.newMap(20030,20111,maptype='CHAINING',loadfactor=0.9,comparefunction=None)
    first=lst["first"]
    accidente=first["info"]["offenseIndex"]["table"]["elements"]
    for nodo in accidente:
        if nodo["value"]!=None:
            actual=nodo["value"]["lstoffenses"]["first"]["info"]["State"]
            dict[actual]=dict.get(actual,0)+1
            fecha=nodo["value"]["lstoffenses"]["first"]["info"]["Start_Time"]
            fecha=fecha[0:10]
            dict_fechas[fecha]=dict_fechas.get(fecha,0)+1
    then=lst["first"]["next"]
    #then=None
    while then!=None:
        accidente2=then["info"]["offenseIndex"]["table"]["elements"]
        for nodo in accidente2:
            if nodo["value"]!=None:
                fecha2=nodo["value"]["lstoffenses"]["first"]["info"]["Start_Time"]
                fecha2=fecha2[0:10]
                dict_fechas[fecha2]=dict_fechas.get(fecha2,0)+1
                actual2=nodo["value"]["lstoffenses"]["first"]["info"]["State"]
                dict[actual2]=dict.get(actual2,0)+1
        then=then["next"]
    max=0
    dia=""
    for llave in dict_fechas:
        if dict_fechas[llave]>max:
            max=dict_fechas[llave]
            dia=llave
    max2=0           
    estado=""
    for llave2 in dict:
        if dict[llave2]>max2:
            max2=dict[llave2]
            estado=llave2

    
    return print((estado,max2),(dia,max))

def addDateIndex(datentry, accidente):
    """
    Actualiza un indice de tipo de crimenes.  Este indice tiene una lista
    de crimenes y una tabla de hash cuya llave es el tipo de crimen y
    el valor es una lista con los crimenes de dicho tipo en la fecha que
    se está consultando (dada por el nodo del arbol)
    """
    lst = datentry['lstaccidents']
    lt.addLast(lst, accidente)
    offenseIndex = datentry['offenseIndex']
    offentry = m.get(offenseIndex, accidente['Description'])
    if (offentry is None):
        entry = newOffenseEntry(accidente['Description'], accidente)
        lt.addLast(entry['lstoffenses'], accidente)
        m.put(offenseIndex, accidente['Description'], entry)
    else:
        entry = me.getValue(offentry)
        lt.addLast(entry['lstoffenses'], accidente)
    return datentry


def newDataEntry(accidente):
    """
    Crea una entrada en el indice por fechas, es decir en el arbol
    binario.
    """
    entry = {'offenseIndex': None, 'lstaccidents': None}
    entry['offenseIndex'] = m.newMap(numelements=30,
                                     maptype='PROBING',
                                     comparefunction=compareOffenses)
    entry['lstaccidents'] = lt.newList('SINGLE_LINKED', compareDates)
    return entry


def newOffenseEntry(offensegrp, crime):
    """
    Crea una entrada en el indice por tipo de crimen, es decir en
    la tabla de hash, que se encuentra en cada nodo del arbol.
    """
    ofentry = {'offense': None, 'lstoffenses': None}
    ofentry['offense'] = offensegrp
    ofentry['lstoffenses'] = lt.newList('SINGLELINKED', compareOffenses)
    return ofentry


# ==============================
# Funciones de consulta
# ==============================


def accidentSize(analyzer):
    """
    Número de crimenes
    """
    return lt.size(analyzer['accidentes'])


def indexHeight(analyzer):
    """
    Altura del arbol
    """
    return om.height(analyzer['fechas'])


def indexSize(analyzer):
    """
    Numero de elementos en el indice
    """
    return om.size(analyzer['fechas'])


def minKey(analyzer):
    """
    Llave mas pequena
    """
    return om.minKey(analyzer['fechas'])


def maxKey(analyzer):
    """
    Llave mas grande
    """
    return om.maxKey(analyzer['fechas'])


def getCrimesByRange(analyzer, initialDate, finalDate):
    """
    Retorna el numero de crimenes en un rago de fechas.
    """
    lst = om.values(analyzer['dateIndex'], initialDate, finalDate)
    lstiterator = it.newIterator(lst)
    totcrimes = 0
    while (it.hasNext(lstiterator)):
        lstdate = it.next(lstiterator)
        totcrimes += lt.size(lstdate['lstcrimes'])
    return totcrimes

def getcrimesbydate(analyzer,date):
    lst=om.get(analyzer["fechas"],date)
    #print(lst)
    pos=lst["value"]["lstaccidents"]["first"]
    a1=0
    a2=0
    a3=0
    a4=0
    while pos!=None:
        if pos["info"]["Severity"]=="1":
            a1+=1
        elif pos["info"]["Severity"]=="2":
            a2+=1
        elif pos["info"]["Severity"]=="3":
            a3+=1
        elif pos["info"]["Severity"]=="4":
            a4+=1
        pos=pos["next"]

    total_crimenes={"total":lt.size(lst["value"]["lstaccidents"]),"grado_1":a1,"grado_2":a2,"grado_3":a3,"grado_4":a4}
    return total_crimenes


def getCrimesByRangeCode(analyzer, initialDate, offensecode):
    """
    Para una fecha determinada, retorna el numero de crimenes
    de un tipo especifico.
    """
    crimedate = om.get(analyzer['dateIndex'], initialDate)
    if crimedate['key'] is not None:
        offensemap = me.getValue(crimedate)['offenseIndex']
        numoffenses = m.get(offensemap, offensecode)
        if numoffenses is not None:
            return m.size(me.getValue(numoffenses)['lstoffenses'])
        return 0

# ==============================
# Funciones de Comparacion
# ==============================


def compareIds(id1, id2):
    """
    Compara dos crimenes
    """
    if (id1 == id2):
        return 0
    elif id1 > id2:
        return 1
    else:
        return -1


def compareDates(date1, date2):
    """
    Compara dos fechas
    """
    if (date1 == date2):
        return 0
    elif (date1 > date2):
        return 1
    else:
        return -1


def compareOffenses(offense1, offense2):
    """
    Compara dos tipos de crimenes
    """
    offense = me.getKey(offense2)
    if (offense1 == offense):
        return 0
    elif (offense1 > offense):
        return 1
    else:
        return -1


def compare_accidents(accident1,accident2):
    offense = me.getKey(accident2)
    if (accident1 == offense):
        return 0
    elif (accident1 > offense):
        return 1
    else:
        return -1

def prueba(arbol,fecha1,fecha2):
    print(arbol)
    retorno=om.values(arbol,fecha1,fecha2)
    return print(retorno)

def bono(cont,lat,lon,radio):
    lat=radians(lat)
    lon=radians(lon)
    dict={}
    contador=0
    #arbol=cont["fechas"]
    first=cont["accidentes"]["first"]
    fecha_analisis_first=first["info"]["Start_Time"][0:10]
    day_first= datetime.datetime.strptime(fecha_analisis_first, '%Y-%m-%d').strftime("%A")
    first_lat=radians(float(first["info"]["Start_Lat"]))
    first_lon=radians(float(first["info"]["Start_Lng"]))
    dlon=first_lon-lon
    dlat=first_lat-lat
    a=sin(dlat/2)**2+cos(lat)*cos(first_lat)*sin(dlon/2)**2
    c=2*asin(sqrt(a))
    r=6371
    resultado=c*r
    if resultado<=radio:
        dict[day_first]=dict.get(day_first,0)+1
        contador+=1
    then=first["next"]
    while then!=None:
        fecha_analisis_then=then["info"]["Start_Time"][0:10]
        day_then=datetime.datetime.strptime(fecha_analisis_then, '%Y-%m-%d').strftime("%A")
        then_lat=radians(float(then["info"]["Start_Lat"]))
        then_lon=radians(float(then["info"]["Start_Lng"]))
        dlon2=then_lon-lon
        dlat2=then_lat-lat
        a=sin(dlat/2)**2+cos(lat)*cos(then_lat)*sin(dlon2/2)**2
        c=2*asin(sqrt(a))
        resultado2=c*r
        if resultado2<=radio:
            dict[day_then]=dict.get(day_then,0)+1
            contador+=1
        then=then["next"]

    return print(dict,"El total es "+str(contador))
