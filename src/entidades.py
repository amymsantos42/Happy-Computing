
import heapq
from utils import *

class Trabajador:
    def __init__(self, id):
        self.disponible = True
        self.tiempoDeFinalizacion = 1e6
        self.servicio = ""
        self.id = id

class Vendedor(Trabajador):
    def __repr__(self):
        return 'Vendedor'

    def __str__(self):
        return self.__repr__()

class Tecnico(Trabajador):
    def __repr__(self):
        return 'Tecnico'

    def __str__(self):
        return self.__repr__()

class Especialista(Trabajador):
    def __repr__(self):
        return 'Especialista'

    def __str__(self):
        return self.__repr__()

class Tienda:
    

    def __init__(self, vendedores = 5, tecnicos = 3, especialistas = 1, tiempoDeTrabajo = 1440):
       
        self.tiempoDeTrabajo = tiempoDeTrabajo
        self.vendedores = []
        self.tecnicos = []
        self.especialistas = []
        self.inf = 1e6

        self.id = 0
        for x in range(vendedores):
            self.vendedores.append(Vendedor(self.id))
            self.id += 1
        self.id = 0
        for x in range(tecnicos):
            self.tecnicos.append(Tecnico(self.id))
            self.id += 1
        self.id = 0
        for x in range(especialistas):
            self.especialistas.append(Especialista(self.id))
            self.id += 1


        self.costos = {'ReparacionGratis': 0,
                      'Reparacion': 350,
                      'Cambiar': 500,
                      'Vender': 750,
                      'Esperar': 0}

        self.servicios = {1: 'ReparacionGratis',
                         2: 'Reparacion',
                         3: 'Cambiar',
                         4: 'Vender',
                         5: 'Esperar'}


    def __str__(self):
        return  self.__repr__()

    def __repr__(self):
        return "Tienda"

    def trabajadorDisponible(self,llist):
        for i in range(len(llist)):
            if llist[i].disponible:
                return llist[i]
        return None
    
    def liberarTrabajador(self, id ,llist):
        llist[id].disponible = True
        llist[id].tiempoDeFinalizacion = self.inf
        llist[id].servicio = ''

    def trabajar(self, id,servicio, tiempoDeFinalizacion,llist):
        llist[id].disponible = False
        llist[id].tiempoDeFinalizacion = tiempoDeFinalizacion
        llist[id].servicio = servicio

    def generarServicio(self):
        r = random.random()
        if r < 0.45:
            return 1
        if 0.45 <= r < 0.7:
            return 2
        if 0.7 <= r < 0.8:
            return 3
        else:
            return 4

    def generarProximoArribo(self):
        return my_poisson(20)

    def generarTiempoDeReparacion(self):
        return my_exponential(1/20)

    def generarTiempoDeCambio(self):
        return my_exponential(1/15)

    def generarTiempoDeVenta(self):
        return my_normal(5, 2)

    def proximoEvento(self):
        a = [(self.proximoArribo[0] + self.tiempoActual , None) , self.proximoCambio , self.proximaReparacion , self.proximaVenta]
        return min(a)


    def cambiar(self):
        tiempoDeCambio = self.tiempoActual + self.generarTiempoDeCambio()

        especialista = self.trabajadorDisponible(self.especialistas)
        if len(self.colaDeCambios) == 0 and especialista:
            self.trabajar(especialista.id,self.servicios[3],tiempoDeCambio,self.especialistas)
            tiempoDeCambioF = (tiempoDeCambio, especialista)
            self.proximoCambio = min(self.proximoCambio, tiempoDeCambioF)

        else:
            print('No hay tecnicos especialistas disponibles para realizar cambios, ultimo!!!')
            self.colaDeCambios.append((self.tiempoActual,self.servicios[3]))

    def reparar(self,servicio):
        tiempoDeReparacion = self.tiempoActual + self.generarTiempoDeReparacion()

        tecnico = self.trabajadorDisponible(self.tecnicos)
        especialista = self.trabajadorDisponible(self.especialistas)
        if len(self.colaDeReparaciones) == 0 and (tecnico or especialista):
            
            if not tecnico:
                print('Un cliente ha reparado su equipo con un tecnico especialista')
                self.trabajar(especialista.id,self.servicios[servicio],tiempoDeReparacion,self.especialistas)
                tiempoDeReparacionF= (tiempoDeReparacion, especialista)

            else:
                print('Un cliente ha reparado su equipo con un tecnico')
                self.trabajar(tecnico.id,self.servicios[servicio],tiempoDeReparacion,self.tecnicos)
                tiempoDeReparacionF= (tiempoDeReparacion, especialista)

            # Actualizar proxima reparacion
            self.proximaReparacion = min(self.proximaReparacion, tiempoDeReparacionF)
            self.proximaReparacion = self.actualizarProximaReparacion()

        else:
            print('No hay tecnicos disponibles para reparaciones, ultimo!!!')
            self.colaDeReparaciones.append((self.tiempoActual, self.servicios[servicio]))

    
    def actualizarProximaVenta(self):
        proximaVenta = (self.inf , None)
        for x in self.vendedores:
            if x.tiempoDeFinalizacion < proximaVenta[0]:
                proximaVenta = (x.tiempoDeFinalizacion,x)
        return proximaVenta 

    def actualizarProximoCambio(self):
        proximoCambio = (self.inf, None)
        for x in self.especialistas:
            if x.servicio == 'Cambiar' and x.tiempoDeFinalizacion < proximoCambio[0]:
                proximoCambio = (x.tiempoDeFinalizacion,x)
        return proximoCambio

    def actualizarProximaReparacion(self):
        proximaReparacion = (self.inf ,None)
        for x in self.especialistas:
            if x.servicio == 'Reparacion' or x.servicio == 'ReparacionGratis' and x.tiempoDeFinalizacion < proximaReparacion[0]:
                proximaReparacion = (x.tiempoDeFinalizacion,x)
        for x in self.tecnicos:
            if x.tiempoDeFinalizacion < proximaReparacion[0]:
                proximaReparacion = (x.tiempoDeFinalizacion,x)
        return proximaReparacion
        


    def simular(self):

        # Tules that represent an evvent
        # t[0]: time
        # t[1]: worker
        self.tiempoActual= 0
        self.proximaReparacion = (self.inf, None)
        self.proximaVenta = (self.inf, None)
        self.proximoCambio = (self.inf, None)
        self.proximoArribo = (self.inf, None)

        
        self.colaDeReparaciones = []
        self.colaDeCambios = []
        self.cola = []
        self.clientesActuales = 0
        self.ganancia = 0

        self.proximoArribo = (self.generarProximoArribo(), None)
        print('Comienza un nuevo dia en la Tienda')

        # Simulation Loop
        while not (self.tiempoActual + self.proximoArribo[0] > self.tiempoDeTrabajo  and self.clientesActuales == 0):
            print('='*50)
            print('La ganancia actual es de: ' + str(self.ganancia))
            print('Cantidad de clientes en el tienda: ' + str(self.clientesActuales))

            self.proximaReparacion = self.actualizarProximaReparacion()

            proximoEvento = self.proximoEvento()
            # Arrival
            if self.tiempoActual + self.proximoArribo[0] == proximoEvento[0] and \
                    self.tiempoActual + self.proximoArribo[0] <= self.tiempoDeTrabajo:
                # Move the time and add a client
                self.tiempoActual += self.proximoArribo[0]
                self.clientesActuales += 1
                print('Arriba un nuevo cliente en el minuto' + str(self.tiempoActual))
                print('Cantidad de clientes en la tienda:' + str(self.clientesActuales))
                
                vendedor = self.trabajadorDisponible(self.vendedores)
                if len(self.cola) == 0 and vendedor:
                    servicio = self.generarServicio()

                    print('El cliente pide servicio ' + self.servicios[servicio])
                    # Nueva Reparacion
                    if servicio == 1 or servicio == 2:
                        self.reparar(servicio)

                    # Nuevo Cambio
                    elif servicio == 3:
                        self.cambiar()

                    # Nueva Venta
                    else:
                        tiempoDeVenta = self.tiempoActual + self.generarTiempoDeVenta()                     
                        self.trabajar(vendedor.id,self.servicios[4],tiempoDeVenta,self.vendedores)
                        tiempoDeVentaF = (tiempoDeVenta, vendedor)
                        self.proximaVenta = min(self.proximaVenta, tiempoDeVentaF)
                        self.proximaVenta = self.actualizarProximaVenta()
                else:
                    print('No hay vendedores disponibles, ultimo!!!')
                    self.cola.append((self.tiempoActual, 'Wait'))

                # Generate next arrival time
                self.proximoArribo = (self.generarProximoArribo(), None)

            # Reparation

            elif self.proximaReparacion[0] == proximoEvento[0]:
                self.ganancia += self.costos[self.proximaReparacion[1].servicio]
                self.tiempoActual = self.proximaReparacion[0]
                self.clientesActuales -= 1
                print('Un cliente deja la tienda luego de terminar su reparacion')

                if str(self.proximaReparacion[1]) == 'Especialista':
                    self.liberarTrabajador(self.proximaReparacion[1].id,self.especialistas)

                    if len(self.colaDeCambios) > 0:
                        tiempoDeCambio = self.tiempoActual + self.generarTiempoDeCambio()
                        cliente = self.colaDeCambios.pop(0)
                        self.trabajar(self.proximaReparacion[1].id,cliente[1],tiempoDeCambio,self.especialistas)
                        self.proximoCambio = self.actualizarProximoCambio()

                    elif len(self.colaDeReparaciones) > 0 :
                        tiempoDeReparacion = self.tiempoActual + self.generarTiempoDeReparacion()
                        cliente = self.colaDeReparaciones.pop(0)
                        self.trabajar(self.proximaReparacion[1].id,cliente[1],tiempoDeReparacion,self.especialistas)

                    self.proximaReparacion = self.actualizarProximaReparacion()
                else:
                    self.liberarTrabajador(self.proximaReparacion[1].id,self.tecnicos)

                    if len(self.colaDeReparaciones) > 0:
                        tiempoDeReparacion = self.tiempoActual + self.generarTiempoDeReparacion()
                        cliente = self.colaDeReparaciones.pop(0)
                        self.trabajar(self.proximaReparacion[1].id,cliente[1],tiempoDeReparacion,self.tecnicos)
                        
                    self.proximaReparacion = self.actualizarProximaReparacion()
            # Change
            elif self.proximoCambio[0] == proximoEvento[0]:
                self.ganancia += self.costos[self.proximoCambio[1].servicio]
                self.tiempoActual = self.proximoCambio[0]
                self.clientesActuales -= 1
                print('Un cliente deja la tienda luego de haber cambiado su equipo')
                self.liberarTrabajador(self.proximoCambio[1].id,self.especialistas)

                if len(self.colaDeCambios) > 0:
                    tiempoDeCambio = self.tiempoActual + self.generarTiempoDeCambio()
                    cliente = self.colaDeCambios.pop(0)
                    self.trabajar(self.proximoCambio[1].id,cliente[1],tiempoDeCambio,self.especialistas)

                self.proximoCambio = self.actualizarProximoCambio()
            # Sell
            elif self.proximaVenta[0] == proximoEvento[0]:
                self.ganancia += self.costos[self.proximaVenta[1].servicio]
                self.tiempoActual = self.proximaVenta[0]
                self.clientesActuales -= 1
                print('Un cliente deja la tienda despues de haber terminado su compra')
                self.liberarTrabajador(self.proximaVenta[1].id,self.vendedores)

                if len(self.cola) > 0:
                    tiempoDeVenta = self.tiempoActual + self.generarTiempoDeVenta()
                    cliente = self.cola.pop(0)
                    servicio = self.generarServicio()

                    if servicio == 4:
                        tiempoDeVenta = self.tiempoActual + self.generarTiempoDeVenta()
                        self.trabajar(self.proximaVenta[1].id,cliente[1],tiempoDeVenta)
                        self.proximaVenta = self.actualizarProximaVenta()

                    elif servicio == 1 or servicio == 2:
                        self.reparar(servicio)

                    elif servicio == 3:
                        self.cambiar()

                self.proximaVenta = self.actualizarProximaVenta()

            else:
                self.proximoArribo = (self.inf, None)

        print('Se obtuvo una ganancia de : ' + str(self.ganancia))
        return self.ganancia




