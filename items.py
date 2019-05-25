import pygame
import framework
import os
import tools

    
    
class Loseta(pygame.sprite.Sprite):
        def __init__(self, x, y, imagen):
            pygame.sprite.Sprite.__init__(self)

            self.image = imagen
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y


class Pantalla:
    def __init__(self, directorio):
        pathLoseta = tools.obtenPathDeRecurso (directorio, "loseta.png")
        pathFicheroMapa = tools.obtenPathDeRecurso (directorio, "mapa.txt")
        pathSuelo = tools.obtenPathDeRecurso (directorio, "suelo5.png")
        pathCorona = tools.obtenPathDeRecurso (directorio, "Corona1.png")
        
        imagenLoseta = pygame.image.load(pathLoseta)
        imagenSuelo = pygame.image.load(pathSuelo)
        
        rutaEnemigos = tools.obtenPathDeRecurso("animaciones", "enemigos")
        rutaPinchos = tools.obtenPathDeRecurso(rutaEnemigos, "pinchos")
        rutaFuego = tools.obtenPathDeRecurso(rutaEnemigos, "fuego")

        ficheroMapa = open(pathFicheroMapa, "r")
        mapa = ficheroMapa.read()
        
        self.objetoVictoria = None 
        self.losetas = pygame.sprite.Group()
        self.mecanismoCaminante = framework.MecanismoCaminante()
        self.enemigosEstaticos = pygame.sprite.Group()
        self.personajesControlados = [ ]
        self.salidaDerecha = None
        self.salidaIzquierda = None
        altoLoseta = imagenLoseta.get_height()
        self.anchoLoseta = imagenLoseta.get_width()
        xLoseta = 0
        yLoseta = 0
        xInicialGuerrero = None
        for caracter in mapa:
            if caracter == "*":
                loseta = Loseta(xLoseta, yLoseta, imagenLoseta)
                self.losetas.add(loseta)
                xLoseta += self.anchoLoseta

            elif caracter == "s":
                loseta  = Loseta(xLoseta, yLoseta, imagenSuelo)
                self.losetas.add(loseta)
                xLoseta += self.anchoLoseta
            elif caracter == "+":
                self.salidaDerecha = SalidaPantalla(xLoseta, yLoseta, self.anchoLoseta, altoLoseta)
                xLoseta += self.anchoLoseta
            elif caracter == "-":
                self.salidaIzquierda = SalidaPantalla(xLoseta, yLoseta, self.anchoLoseta, altoLoseta)
                xLoseta += self.anchoLoseta
            elif caracter == "V":
	        rutaObjetoVictoria = tools.obtenPathDeRecurso("animaciones", "corona")
	        self.objetoVictoria = pygame.sprite.Group (framework.SpriteAnimado(rutaObjetoVictoria, xLoseta, yLoseta, 60) )
                xLoseta += self.anchoLoseta
            



            #elif caracter == "c":
                #loseta  = Loseta(xLoseta, yLoseta, imagenCorona)
                #self.losetas.add(loseta)
                #xLoseta += self.anchoLoseta
                
    #CondicionesEnemigos

            elif caracter == "G":
                if xInicialGuerrero == None:
                    xInicialGuerrero = xLoseta
                else:
                    personajeControlado = PersonajeControlado(xInicialGuerrero, yLoseta, xLoseta, self.mecanismoCaminante)
                    self.personajesControlados.append(personajeControlado)
                    xInicialGuerrero = None
                xLoseta += self.anchoLoseta


                
            elif caracter == "P":
                estatico = framework.SpriteAnimado(rutaPinchos, xLoseta, yLoseta, 600)
                self.enemigosEstaticos.add(estatico)
                xLoseta += self.anchoLoseta

            elif caracter == "F": 
                estatico = framework.SpriteAnimado(rutaFuego, xLoseta, yLoseta, 3)
                self.enemigosEstaticos.add(estatico)
                xLoseta += self.anchoLoseta

                
            elif caracter == "\n":
                xLoseta = 0
                yLoseta += altoLoseta
            else:
                xLoseta += self.anchoLoseta
            
        pathFondo = tools.obtenPathDeRecurso(directorio, "fondo.png")
        self.fondo = pygame.image.load(pathFondo)


    #FIN
    
    def obtenEnemigos(self):
        grupoEnemigos = pygame.sprite.Group(self.enemigosEstaticos)

        for personajeControlado in self.personajesControlados:
            grupoEnemigos.add(personajeControlado.obtenDibujo())

        return grupoEnemigos
        

    def personajeEnSalidaDerecha(self, personaje):
        chocado = False
        if self.salidaDerecha != None:
            chocado = pygame.sprite.collide_rect(personaje.dibujo, self.salidaDerecha)
        return chocado

    def personajeEnSalidaIzquierda(self, personaje):
        chocado = False
        if self.salidaIzquierda != None:
            chocado = pygame.sprite.collide_rect(personaje.dibujo, self.salidaIzquierda)
        return chocado

    def dibuja(self):
        pygame.display.get_surface().blit( self.fondo, (0,0) )
        self.losetas.draw(pygame.display.get_surface())

        self.enemigosEstaticos.draw(pygame.display.get_surface())
                
        for personaje in self.personajesControlados:
            personaje.dibuja()

        if self.objetoVictoria!= None:
            self.objetoVictoria.draw(pygame.display.get_surface())
        

    def obtenLosetas(self):
        return self.losetas
    
    
    def obtenEntradaIzquierda(self):
        x = self.salidaIzquierda.rect.x + (self.anchoLoseta + 50)
        y = self.salidaIzquierda.rect.y
        return x,y

    def obtenEntradaDerecha(self):
        x = self.salidaDerecha.rect.x - (self.anchoLoseta + 50)
        y = self.salidaDerecha.rect.y
        return x,y

    def gestionaEventos(self):
	self.mecanismoCaminante.generaEventos()

    def ejecutaPaso(self):
        self.enemigosEstaticos.update()
        for enemigo in self.personajesControlados:
            enemigo.ejecutaPaso(self)
        if self.objetoVictoria!= None:
            self.objetoVictoria.update()
    
    def obtenObjetoVictoria(self):

        return self.objetoVictoria

    

class SalidaPantalla(pygame.sprite.Sprite):
    def __init__(self, x, y, ancho, alto):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x, y, ancho, alto)
 
class Mapa:
	def __init__(self):
            self.pantallas = [ ]
            listaPantallas = os.listdir("pantallas")
            listaPantallas.sort()
            for directorio in listaPantallas:
                directorioPantalla = os.path.join("pantallas",directorio)
                pantalla = Pantalla(directorioPantalla)
                self.pantallas.append(pantalla)

            self.indice = 0
            self.pantalla = self.pantallas[self.indice]

        def activaPantallaSiguiente(self):
            if self.indice < len(self.pantallas) - 1:
                self.indice += 1
                self.pantalla = self.pantallas[self.indice]

        def activaPantallaAnterior(self):
            self.indice -= 1
            if self.indice < 0:
                self.indice = 0
            self.pantalla = self.pantallas[self.indice]

        def reiniciaMapa(self):
            self.indice = 0
            self.pantalla = self.pantallas[self.indice]
        
        def dibuja(self):
            self.pantalla.dibuja()
        
        def obtenPantalla(self):
            return self.pantalla

class Personaje:

    E_PARADO = 0
    E_CAMINANDO = 1
    E_SALTANDO = 2
    
    O_DERECHA = 0
    O_IZQUIERDA = 1

    C_AVANCE = 8

    C_SALTO = -40

    C_ENERGIA_MAXIMA = 2000.0

    def __init__(self, xInicial, yInicial, animacion):
        self.x = xInicial
        self.y = yInicial

        self.velocidadVertical = 0  
        self.motorFisico = framework.MotorFisico() 
        self.motorColisiones = framework.MotorColisiones() 
        self.estado = Personaje.E_PARADO
        rutaAnimaciones = tools.obtenPathDeRecurso ("animaciones", animacion)
        rutaCaminar = tools.obtenPathDeRecurso (rutaAnimaciones, "caminar")
        rutaSaltar = tools.obtenPathDeRecurso (rutaAnimaciones, "saltar")
        rutaParado = tools.obtenPathDeRecurso (rutaAnimaciones, "parar")
        self.animacionCaminar = framework.SpriteAnimadoOrientable(rutaCaminar, xInicial, yInicial, 8)
        self.animacionSaltar = framework.SpriteAnimadoOrientable(rutaSaltar, xInicial, yInicial, 8)
        self.animacionParado = framework.SpriteAnimadoOrientable(rutaParado, xInicial, yInicial, 60)
        self.dibujo = self.animacionParado
        self.orientacion = Personaje.O_DERECHA
        self.energia = Personaje.C_ENERGIA_MAXIMA 
    
    def colisiona(self, grupo):
        colisiones = self.motorColisiones.detectaSpriteConGrupo(self.dibujo, grupo)
        return len(colisiones) > 0

    def modificaEnergia(self, cambio):
	self.energia += cambio
        if self.energia < 0:
	    self.energia = 0
	elif self.energia > Personaje.C_ENERGIA_MAXIMA:
	    self.energia = Personaje.C_ENERGIA_MAXIMA 

    def obtenDibujo(self):
        return self.dibujo

    

    def mueveDerecha(self):
        self.estado = Personaje.E_CAMINANDO
        self.orientacion = Personaje.O_DERECHA

    def mueveIzquierda(self):
        self.estado = Personaje.E_CAMINANDO
        self.orientacion = Personaje.O_IZQUIERDA

    def salta(self):
        self.estado = Personaje.E_SALTANDO

    def para(self):
        self.estado = Personaje.E_PARADO

    def ejecutaPaso(self, pantalla):
        self.dibujo.animaFrame()
        losetas = pantalla.obtenLosetas()
        choquePared = self._ejecutaPasoCoordenadaX(losetas)
        choqueSuelo, choqueTecho = self._ejecutaPasoCoordenadaY(losetas)
        saltando = (self.estado == Personaje.E_SALTANDO)
        if choquePared or (choqueSuelo and saltando):
            self.para()
        if choqueSuelo:
            self.velocidadVertical = 0
        
    def _ejecutaPasoCoordenadaX(self, losetas):
        if self.estado == Personaje.E_CAMINANDO:
            self._ejecutaCaminando()
        elif self.estado == Personaje.E_SALTANDO:
            self._ejecutaSaltando()
        else:
            self._ejecutaParado()
        self.dibujo.cambiaPosicion(self.x, self.y)
        colisionesX = self.motorColisiones.detectaSpriteConGrupo(self.dibujo, losetas)
        self.x += self.motorColisiones.obtenCorreccionCoordenadaX(self.dibujo, self.orientacion==Personaje.O_DERECHA, colisionesX)
        self.dibujo.cambiaPosicion(self.x, self.y)
        return len(colisionesX) > 0

    def _ejecutaPasoCoordenadaY(self, losetas):
        self.velocidadVertical = self.motorFisico.aplicaGravedad(self.velocidadVertical)
        #print self.velocidadVertical
        self.y = self.y + self.velocidadVertical    
        self.dibujo.cambiaPosicion(self.x, self.y)
        subiendo = self.velocidadVertical < 0
        colisionesY = self.motorColisiones.detectaSpriteConGrupo(self.dibujo, losetas )
        self.y += self.motorColisiones.obtenCorreccionCoordenadaY(self.dibujo, subiendo, colisionesY)
        self.dibujo.cambiaPosicion(self.x, self.y)
        chocadoSuelo = (len(colisionesY)>0) and not subiendo
        chocadoTecho = (len(colisionesY)>0) and subiendo
        return chocadoSuelo, chocadoTecho

    def _ejecutaParado(self):
        self.dibujo = self.animacionParado

    def _ejecutaCaminando(self):
        self.dibujo = self.animacionCaminar
        if self.orientacion == Personaje.O_DERECHA:
            self._usaDibujosOriginales()
            self.x += Personaje.C_AVANCE 
        else:
            self._usaDibujosReflejados()
            self.x -= Personaje.C_AVANCE

    def _usaDibujosOriginales(self):
        self.animacionCaminar._usaDibujosOriginales()
        self.animacionSaltar._usaDibujosOriginales()
        self.animacionParado._usaDibujosOriginales()

    def _usaDibujosReflejados(self):
        self.animacionCaminar._usaDibujosReflejados()
        self.animacionSaltar._usaDibujosReflejados()
        self.animacionParado._usaDibujosReflejados()

    def _ejecutaSaltando(self):
        self.dibujo = self.animacionSaltar
        if self.orientacion == Personaje.O_DERECHA:
            self._usaDibujosOriginales()
            self.x += Personaje.C_AVANCE 
        else:
            self._usaDibujosReflejados()
            self.x -= Personaje.C_AVANCE

        if self.velocidadVertical == 0:
            self.velocidadVertical = Personaje.C_SALTO

    def dibuja(self):
        pygame.display.get_surface().blit(self.dibujo.image, (self.x, self.y) )

    def cambiaPosicion(self, x, y):
	    self.x = x
	    self.y = y
	    self.dibujo.cambiaPosicion(self.x, self.y)
   
    def obtenPorcentajeEnergia(self):
	    return self.energia / Personaje.C_ENERGIA_MAXIMA
 
class PersonajeControlado(Personaje):
    def __init__(self, xInicial, yInicial, xFinal, mecanismo):
        Personaje.__init__(self, xInicial, yInicial, tools.obtenPathDeRecurso(tools.obtenPathDeRecurso("animaciones", "enemigos"), "guerrero") )
        self.limiteIzquierdo = xInicial
	self.limiteDerecho = xFinal
        mecanismo.registra(self)


    def obtenLimiteIzquierdo(self):
       return self.limiteIzquierdo 


    def obtenLimiteDerecho(self):
        return self.limiteDerecho

