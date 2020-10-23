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

import config as cf
from App import model
import datetime
import csv

"""
El controlador se encarga de mediar entre la vista y el modelo.
Existen algunas operaciones en las que se necesita invocar
el modelo varias veces o integrar varias de las respuestas
del modelo en una sola respuesta.  Esta responsabilidad
recae sobre el controlador.
"""

# ___________________________________________________
#  Inicializacion del catalogo
# ___________________________________________________


def init():
    """
    Llama la funcion de inicializacion  del modelo.
    """
    # catalog es utilizado para interactuar con el modelo
    analyzer = model.newAnalyzer()
    return analyzer


# ___________________________________________________
#  Funciones para la carga de datos y almacenamiento
#  de datos en los modelos
# ___________________________________________________

def loadData(analyzer, archivo,number):
    """
    Carga los datos de los archivos CSV en el modelo
    """
    archivo = cf.data_dir + archivo
    input_file = csv.DictReader(open(archivo, encoding="utf-8"),
                                delimiter=",")
    for accidente in input_file:
        model.addAccident(analyzer, accidente,number)
        
    return analyzer

# ___________________________________________________
#  Funciones para consultas
# ___________________________________________________


def accidentSize(analyzer):
    """
    Numero de crimenes leidos
    """
    return model.accidentSize(analyzer)


def indexHeight(analyzer):
    """
    Altura del indice (arbol)
    """
    return model.indexHeight(analyzer)


def indexSize(analyzer):
    """
    Numero de nodos en el arbol
    """
    return model.indexSize(analyzer)


def minKey(analyzer):
    """
    La menor llave del arbol
    """
    return model.minKey(analyzer)


def maxKey(analyzer):
    """
    La mayor llave del arbol
    """
    return model.maxKey(analyzer)


def getAccidentsByRange(analyzer, initialDate, finalDate):
    """
    Retorna el total de crimenes en un rango de fechas
    """
    initialDate = datetime.datetime.strptime(initialDate, "%H:%M")
    finalDate = datetime.datetime.strptime(finalDate, '%H:%M')
    initialDate=model.conversion(initialDate)
    finalDate=model.conversion(finalDate)
    return model.getAccidentsByRange(analyzer, initialDate,
                                  finalDate)
    

def getAccidentsBydate(analyzer, date):
    fecha=datetime.datetime.strptime(date,"%Y-%m-%d")
    retorno=model.getAccidentsbydate(analyzer,fecha.date(),1)
    return retorno




def estado_mayor(analyzer, initialDate, finalDate):
    """
    Retorna el total de crimenes en un rango de fechas
    """
    initialDate = datetime.datetime.strptime(initialDate, '%Y-%m-%d')
    finalDate = datetime.datetime.strptime(finalDate, '%Y-%m-%d')
    return model.estado_mayor(analyzer, initialDate.date(),
                                  finalDate.date())

def getfechas_anteriores(analyzer,Date):
    theDate = datetime.datetime.strptime(Date, '%Y-%m-%d')
    inicio= model.minKey(analyzer)
    return model.fechas_anteriores(inicio,analyzer,theDate.date())
    


