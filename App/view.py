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

import sys
import config
from App import controller
assert config
import model as mdl
import datetime
"""
La vista se encarga de la interacción con el usuario.
Presenta el menu de opciones  y  por cada seleccion
hace la solicitud al controlador para ejecutar la
operación seleccionada.
"""

# ___________________________________________________
#  Ruta a los archivos
# ___________________________________________________


accidentfile = 'us_accidents_dis_2016.csv'

# ___________________________________________________
#  Menu principal
# ___________________________________________________


def printMenu():
    print("\n")
    print("*******************************************")
    print("Bienvenido")
    print("1- Inicializar Analizador")
    print("2- Cargar información de accidentes")
    print("3- Consultar accidentes en una fecha")
    print("4- Consultar accidentes anteriores una fecha")
    print("5- Consultar accidentes en un rango de fechas") #Req 3
    print("6- Estado con más accidentes")
    print("7- conocer accidentes por rango de horas")
    print("8- Zona geográfica más accidentada")#Req 6
    print("0- Salir")
    print("*******************************************")


"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n>')

    if int(inputs[0]) == 1:
        print("\nInicializando....")
        # cont es el controlador que se usará de acá en adelante
        cont = controller.init()
        hours = controller.init()

    elif int(inputs[0]) == 2:
        print("\nCargando información de accidentes ....")        
        controller.loadData(cont, accidentfile,1)
        controller.loadData(hours, accidentfile,2)
        print("si se necesita cargar mas archivos llame otra vez la funcion")
        print('Accidentes cargados: ' + str(controller.accidentSize(cont)))
        print('Altura del arbol: ' + str(controller.indexHeight(cont)))
        print('Elementos en el arbol: ' + str(controller.indexSize(cont)))
        print('Menor Llave: ' + str(controller.minKey(cont)))
        print('Mayor Llave: ' + str(controller.maxKey(cont)))
        
    elif int(inputs[0]) == 3:
        print("\nBuscando accidentes en una fecha: ")
        Date = input("Fecha (YYYY-MM-DD): ")
        total = controller.getAccidentsBydate(cont,Date)
        print("\nTotal de accidentes en el rango de fechas: " + str(total["total"]))
        print(total)
    
    elif  int(inputs[0]) == 4:
        print("\nBuscando accidentes anteriores una fecha: \n")
        Date= input("Fecha (YYYY-MM-DD): \n")
        buscar = controller.getfechas_anteriores(cont,Date)
        print (buscar)
        
    elif int(inputs[0]) == 5:
        print("\nBuscando accidentes en un rango de fechas: ")
        Date_0 = input("Fecha inicial (YYYY-MM-DD): ")
        Date_1 = input("Fecha final (YYYY-MM-DD): ")
        total_accidentes_reportados = controller.getAccidentsNumberByRange(cont,Date_0,Date_1)
        categoria_mas_reportada = controller.getAccidentsSeverityByRange(cont, Date_0, Date_1)
        print("\nAccidentes reportados: " + str(total_accidentes_reportados) + ", categoria mas reportada: " + str(categoria_mas_reportada))

    elif int(inputs[0])==6:
        print("\nBuscando estado con más accidentes")
        initialDate = input("Rango Inicial (YYYY-MM-DD): ")
        finalDate = input("Rango Final (YYYY-MM-DD): ")
        mdl.prueba(cont,initialDate,finalDate)
        #controller.estado_mayor(cont, initialDate, finalDate)
    
    elif int(inputs[0]) == 7:
        print("\nBuscando accidentes en un rango de horas")
        initialDate = input("Rango Inicial (HH:MM):\n")
        finalDate = input("Rango Final (HH:MM):\n")
        respuesta=controller.getAccidentsByRange(hours,initialDate,finalDate)
        print(respuesta)
        
        initialDate2 = datetime.datetime.strptime(initialDate, '%Y-%m-%d')
        finalDate2= datetime.datetime.strptime(finalDate, '%Y-%m-%d')
        controller.estado_mayor(cont,initialDate2.date(),finalDate2.date())

    elif int(inputs[0]) == 8:
        print("\nBuscando zona geografica mas accidentada: ")
        lat=float(input("Ingrese latitud: "))
        lon=float(input("Ingrese longitud: "))
        radio=float(input("Ingrese radio: "))
        resultado = controller.bono(cont,lat,lon,radio)
        print(resultado)

    else:
        sys.exit(0)
sys.exit(0)

