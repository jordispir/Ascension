import pygame
import tools
import os

class SpriteAnimado(pygame.sprite.Sprite):
    def __init__(self, directorio, xInicial, yInicial, velocidad):
        pygame.sprite.Sprite.__init__(self)
        self.dibujos = []
        listaFicheros = os.listdir(directorio)
        listaFicheros.sort()
    
        for fichero in listaFicheros:
            rutaDibujo = tools.obtenPathDeRecurso(directorio, fichero)
            dibujo = pygame.image.load(rutaDibujo)
            self.dibujos.append(dibujo)
        self.image = self.dibujos[0]
        self.rect = self.image.get_rect()
        self.rect.x = xInicial
        self.rect.y = yInicial
        self.framesPorPaso = velocidad
        self.frames = 0

    def animaFrame(self):
        self.frames += 1
        pasoDeAnimacion = int((self.frames / self.framesPorPaso) % len(self.dibujos))
        self.image = self.dibujos[pasoDeAnimacion]

    def update(self):
        self.animaFrame()
    
    def cambiaPosicion (self, x, y):
        self.rect.x = x
        self.rect.y = y
        
class SpriteAnimadoOrientable(SpriteAnimado):
    def __init__(self, directorio, xInicial, yInicial, velocidad):
        SpriteAnimado.__init__(self, directorio, xInicial, yInicial, velocidad)
        self.dibujosOriginales = []
        self.dibujosReflejados = []
        for dibujo in self.dibujos:
            self.dibujosOriginales.append(dibujo)
            self.dibujosReflejados.append(pygame.transform.flip(dibujo, True, False) )
        self._usaDibujosOriginales()
        

    def _usaDibujosOriginales(self):
        self.dibujos = self.dibujosOriginales

    def _usaDibujosReflejados(self):
        self.dibujos = self.dibujosReflejados
class Ventana:
    def __init__(self):
        self.superficie = pygame.display.set_mode( (1280, 800) )
        pygame.display.set_caption("Ascension")
        pygame.display.flip()
        
        self.reloj = pygame.time.Clock()

    def obtenSuperficie(self):
        return self.superficie

    def finalizado(self):
        salir = False
        evento = pygame.event.poll()
        if evento.type == pygame.QUIT:
            salir = True
        
        return salir


    def empiezaFrame(self):
        negro = (0, 0 ,0)
        self.superficie.fill(negro)

    def finalizaFrame(self):
        pygame.display.flip()
        self.reloj.tick(60)

class Juego:
    E_MENU = 1
    E_PARTIDA = 2
    E_RESULTADO = 3
    E_FIN = 4

    def __init__(self, ventana):
        self.estado = Juego.E_MENU
        self.menu = Menu(ventana)
        self.partida = Partida(ventana)
        self.pantallaResultado = None
        self.ventana = ventana
    
    def leeEntradas(self):
        eventos = pygame.event.get()
        if self.estado == Juego.E_MENU:
            self.menu.gestionaEventos(eventos)
        elif self.estado == Juego.E_PARTIDA:
            self.partida.gestionaEventos(eventos)
        elif self.estado == Juego.E_RESULTADO:
            self.pantallaResultado.gestionaEventos(eventos)
    
    def ejecutaPaso(self):
        if (self.estado == Juego.E_MENU):
            self.menu.ejecutaPaso()
            opcion = self.menu.obtenOpcion()

            if opcion == Menu.O_PARTIDA_NUEVA:
                self.estado = Juego.E_PARTIDA
                self.partida = Partida(self.ventana)

            elif opcion == Menu.O_SALIR:
                self.estado = Juego.E_FIN

        elif (self.estado == Juego.E_PARTIDA):
            self.partida.ejecutaPaso()

            if self.partida.esFinDePartida():
                self.estado = Juego.E_RESULTADO
                self.pantallaResultado = PantallaDerrota()

                if self.partida.esVictoria():
                    self.pantallaResultado = PantallaVictoria()
                else:
                    self.pantallaResultado = PantallaDerrota()

        elif (self.estado == Juego.E_RESULTADO):
            if self.pantallaResultado.esFinPantallaResultado():
                self.estado = Juego.E_MENU
                self.menu = Menu(self.ventana)

    def dibuja(self):
        if self.estado == Juego.E_MENU:
            self.menu.dibuja()
        elif self.estado == Juego.E_PARTIDA:
            self.partida.dibuja()
        elif self.estado == Juego.E_RESULTADO:
            self.pantallaResultado.dibuja()

    def finDeJuego(self):
        return self.estado == Juego.E_FIN
    

class Menu:
    O_NINGUNA = 0
    O_PARTIDA_NUEVA = 1
    O_SALIR = 2

    def __init__(self, ventana):
        self.ventana = ventana
        self.seleccion = Menu.O_PARTIDA_NUEVA
        self.opcionElegida = Menu.O_NINGUNA
        rutaMarcaMenu = tools.obtenPathDeRecurso ("animaciones", "marcamenu")
        self.marca = SpriteAnimado(rutaMarcaMenu, 0, 0, 8)
        self.sprites = pygame.sprite.Group(self.marca)
        fuente = pygame.font.SysFont ("Burbank Big Condensed Bold Font" , 50)
        #generar dibujo
        self.opcionPartida = fuente.render("Empezar partida nueva", True, (255, 0, 0) )
        self.opcionSalir = fuente.render("Salir del juego", True, (255, 0, 0) )

        #imagenFondo
        rutaFondo = tools.obtenPathDeRecurso ("menu", "fondoDefinitivo.jpg") 
        self.imagenFondo = pygame.image.load(rutaFondo)

        directorio= tools.obtenPathDeRecurso("sonidos", "menu")
        rutaSonido= tools.obtenPathDeRecurso(directorio, "SonidoEspada.wav")
        self.sonido = pygame.mixer.Sound(rutaSonido)

    def gestionaEventos (self, eventos):
        for evento in eventos:
            if evento.type == pygame.QUIT:
                self.opcionElegida = Menu.O_SALIR
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    self.sonido.play()
                    self.seleccion -= 1
                    if self.seleccion == 0:
                        self.seleccion = Menu.O_SALIR
                elif evento.key == pygame.K_DOWN:
                    self.sonido.play()
                    self.seleccion += 1
                    if self.seleccion > Menu.O_SALIR:
                        self.seleccion = Menu.O_PARTIDA_NUEVA
                elif evento.key == pygame.K_RETURN:
                    self.opcionElegida = self.seleccion
                
    def ejecutaPaso(self):
        marcaX = 100
        if self.seleccion == Menu.O_PARTIDA_NUEVA:
            marcaY = 390
        elif self.seleccion == Menu.O_SALIR:
            marcaY = 525 
        self.marca.cambiaPosicion (marcaX, marcaY)
        self.sprites.update()

    def obtenOpcion(self):
        return self.opcionElegida

    def dibuja(self):
        #Fondo
        self.ventana.obtenSuperficie().blit(self.imagenFondo, (0, 0) )

        self.ventana.obtenSuperficie().blit( self.opcionPartida, (155, 390) )
        self.ventana.obtenSuperficie().blit( self.opcionSalir, (155, 525) )
        self.sprites.draw(self.ventana.obtenSuperficie())
        


class Partida:
    def __init__(self, ventana):
    
        self.ventana = ventana
        self.finPartida = False
        self.mapa = Mapa()
        self.personaje = Personaje(90, 220, "personaje")
        self.barraEnergia = BarraEnergia()
        self.victoria = False

    def esVictoria(self):
        return self.victoria

    def gestionaEventos(self, eventos):

        self.mapa.obtenPantalla().gestionaEventos()

        for evento in eventos:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    self.finPartida = True
                elif evento.key == pygame.K_RIGHT:
                    self.personaje.mueveDerecha()
                elif evento.key == pygame.K_LEFT:
                    self.personaje.mueveIzquierda()
                elif evento.key == pygame.K_UP:
                    self.personaje.salta()
                
            if evento.type == pygame.KEYUP:
                if evento.key == pygame.K_RIGHT:
                    self.personaje.para()
                elif evento.key == pygame.K_LEFT:
                    self.personaje.para()

    def ejecutaPaso(self):
        self.personaje.ejecutaPaso( self.mapa.obtenPantalla() )
        pantalla = self.mapa.obtenPantalla()
        pantalla.ejecutaPaso()

        herido = self.personaje.colisiona(pantalla.obtenEnemigos() )
        if herido:
            self.personaje.modificaEnergia(-5)
            if self.personaje.obtenPorcentajeEnergia() <= 0:
                self.finPartida = True

        objetoVictoria = self.mapa.obtenPantalla().obtenObjetoVictoria()
        if objetoVictoria != None:
            self.victoria = self.personaje.colisiona( pygame.sprite.Group(objetoVictoria) )
            if self.victoria:
                self.finPartida = True
        
        if pantalla.personajeEnSalidaDerecha(self.personaje):
            self.mapa.activaPantallaSiguiente()
            pantallaNueva = self.mapa.obtenPantalla()
            x, y = pantallaNueva.obtenEntradaIzquierda()
            self.personaje.cambiaPosicion(x, y)

        elif pantalla.personajeEnSalidaIzquierda(self.personaje):
            self.mapa.activaPantallaAnterior()
            pantallaNueva = self.mapa.obtenPantalla()
            x, y = pantallaNueva.obtenEntradaDerecha()
            self.personaje.cambiaPosicion(x, y)

    def dibuja(self):
        self.mapa.dibuja()
        self.barraEnergia.dibuja(self.personaje.obtenPorcentajeEnergia() )
        self.personaje.dibuja()


    def esFinDePartida(self):
        return self.finPartida
    
    def esVictoria(self):
        return self.victoria

class MotorFisico:
    C_GRAVEDAD = 3
    def __init__(self):
        pass

    def aplicaGravedad(self, velocidadInicial):
        return velocidadInicial + MotorFisico.C_GRAVEDAD

class MotorColisiones:
    def __init__(self):
        pass
    
    def obtenCorreccionCoordenadaX(self, sprite, avanzando, colisiones ): 
        deltaX = 0
        for colision in colisiones:
            colisionXiz = colision.rect.x
            colisionXdr = colisionXiz + colision.image.get_width()
            spriteXiz = sprite.rect.x + deltaX
            spriteXdr = spriteXiz + sprite.image.get_width() 
            
            if spriteXdr > colisionXiz and spriteXdr < colisionXdr:  
                deltaX += -(spriteXdr - (colisionXiz + 1) )
            elif spriteXiz < colisionXdr and spriteXiz > colisionXiz:  
                deltaX += spriteXiz - (colisionXdr - 1)
            elif spriteXdr > colisionXdr and spriteXiz < colisionXiz:  
                if avanzando: 
                    deltaX += -(spriteXdr-colisionXdr + colision.image.get_width() + 1)
                else:
                    deltaX += colisionXiz-spriteXiz + colision.image.get_width() + 1
                
        return deltaX

    def obtenCorreccionCoordenadaY(self, sprite, subiendo, colisiones):
        deltaY = 0
        for colision in colisiones:
            colisionYar = colision.rect.y
            colisionYab = colisionYar + colision.image.get_height()
            spriteYar = sprite.rect.y + deltaY
            spriteYab = spriteYar + sprite.image.get_height()
            
            if spriteYab > colisionYar and spriteYab < colisionYab:
                ### dibujo incrusta los pies en loseta ###
                deltaY += colisionYar - (spriteYab + 1)
            elif spriteYar < colisionYab and spriteYar > colisionYar:
                ### dibujo incrusta la cabeza en loseta ###
                deltaY += colisionYab - (spriteYar - 1)
            elif spriteYar < colisionYar and spriteYab > colisionYab:  ## dibujo contiene loseta
                if not subiendo:
                    deltaY += -(spriteYab - colisionYab + colision.image.get_height() + 1)
                else:
                    deltaY += colisionYar - spriteYar + colision.image.get_height() + 1

        return deltaY


    def detectaSpriteConGrupo(self, sprite, grupo):
        return pygame.sprite.spritecollide(sprite, grupo, False)


class BarraEnergia:
    C_DISTANCIA_LIMITE_IZQUIERDO = 100
    C_DISTANCIA_LIMITE_INFERIOR = 700

    def __init__(self):
        rutaMango = tools.obtenPathDeRecurso("barraenergia","mango.png")
        rutaHoja = tools.obtenPathDeRecurso("barraenergia","hoja.png")
        self.imagenMango = pygame.image.load(rutaMango)
        self.imagenHoja = pygame.image.load(rutaHoja)
        self.x = BarraEnergia.C_DISTANCIA_LIMITE_IZQUIERDO
        self.y = pygame.display.get_surface().get_height() - (self.imagenMango.get_height() + BarraEnergia.C_DISTANCIA_LIMITE_INFERIOR)

        
    def dibuja(self, porcentaje):
        pygame.display.get_surface().blit(self.imagenMango, (self.x, self.y))
        Xfinal = porcentaje * self.imagenHoja.get_width()
        Yfinal = self.imagenHoja.get_height()
        pygame.display.get_surface().blit(self.imagenHoja, (self.x + self.imagenMango.get_width(), self.y + (self.imagenMango.get_height()/2)-(self.imagenHoja.get_height()/2)),(0, 0, Xfinal, Yfinal))



class MecanismoDeControl:
    def __init__(self):
        self.elementos = [ ]

    def registra(self, elemento):
        self.elementos.append(elemento)

    def generaEventos(self):
        for elemento in self.elementos:
            self.generaEvento(elemento)

    def generaEvento(self, elemento):
        pass

class MecanismoCaminante(MecanismoDeControl):
    def __init__(self):
        MecanismoDeControl.__init__(self)

    def generaEvento(self, elemento):
        if elemento.orientacion == Personaje.O_DERECHA:
            if elemento.x < elemento.obtenLimiteDerecho():
                elemento.mueveDerecha()
            else:
                elemento.mueveIzquierda()
        else:
            if elemento.x > elemento.obtenLimiteIzquierdo():
                elemento.mueveIzquierda()
            else:
                elemento.mueveDerecha()

class PantallaResultado:
    def __init__(self):
        self.finaliza = False

    def gestionaEventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN or evento.key == pygame.K_ESCAPE:
                    self.finaliza = True

    def ejecutaPaso(self):
        pass
    
    def dibuja(self):
        pass

    def esFinPantallaResultado(self):
        return self.finaliza



class PantallaDerrota(PantallaResultado):
    def __init__(self):
        PantallaResultado.__init__(self)
        rutaPantallaGameOver = tools.obtenPathDeRecurso("resultados", "derrota")
        rutaCelda = tools.obtenPathDeRecurso(rutaPantallaGameOver, "celda.png")
        rutaGameOver = tools.obtenPathDeRecurso(rutaPantallaGameOver, "gameover.png")
        self.imagenFondo = pygame.image.load(rutaCelda)
        self.gameOver = pygame.image.load(rutaGameOver)

    def dibuja(self):
        pygame.display.get_surface().blit(self.imagenFondo,(0, 0) )
        pygame.display.get_surface().blit(self.gameOver, (400, 300) )

class PantallaVictoria(PantallaResultado):

    def __init__(self):
            PantallaResultado.__init__(self)
            rutaVictoria = tools.obtenPathDeRecurso("resultados","victoria")
            self.fondo = pygame.image.load(tools.obtenPathDeRecurso(rutaVictoria,"coronacion.png"))
            rutaFuenteTitulo = tools.obtenPathDeRecurso("fuentes", "PrinceValiant.ttf")
            fuenteTitulo = pygame.font.Font(rutaFuenteTitulo, 110)
            self.titulo = fuenteTitulo.render( "Victoria ", True, (100, 79, 5))
            rutaFuenteMensaje = tools.obtenPathDeRecurso("fuentes", "Enchanted Land.otf")
            fuenteMensaje = pygame.font.Font(rutaFuenteMensaje, 40)
            self.mensaje = []
            self.mensaje.append(fuenteMensaje.render("Has conseguido recuperar la corona y con ella el control", True, (197, 172, 171)) )
            self.mensaje.append(fuenteMensaje.render("del reino.El usurpador ha sido detenido y sera juzgado", True, (197, 172, 171)) )
            self.mensaje.append(fuenteMensaje.render("para que pague por sus ofensas.", True, (197, 172, 171)) )
            self.mensaje.append(fuenteMensaje.render("", True, (197, 172, 171)) )
            self.mensaje.append(fuenteMensaje.render("La gente celebra por las calles el retorno de su Rey.", True, (197, 172, 171)) )
            self.mensaje.append(fuenteMensaje.render("", True, (197, 172, 171)) )
            self.mensaje.append(fuenteMensaje.render("            ... mientras espera a que el siguiente aparezca", True, (197, 172, 171)) )

    def dibuja(self):
        ### imagen de fondo ###
        ### titulo ###

        pygame.display.get_surface().blit(self.fondo, (0, 0))
        pygame.display.get_surface().blit(self.titulo, (400, 30))
        y = 300
        for linea in self.mensaje:
            pygame.display.get_surface().blit(linea,(300,y) )
            y += 60





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
        self.mecanismoCaminante = MecanismoCaminante()
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
                self.objetoVictoria = pygame.sprite.Group (SpriteAnimado(rutaObjetoVictoria, xLoseta, yLoseta, 60) )
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
                estatico = SpriteAnimado(rutaPinchos, xLoseta, yLoseta, 600)
                self.enemigosEstaticos.add(estatico)
                xLoseta += self.anchoLoseta

            elif caracter == "F":
                estatico = SpriteAnimado(rutaFuego, xLoseta, yLoseta, 3)
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
        self.motorFisico = MotorFisico()
        self.motorColisiones = MotorColisiones()
        self.estado = Personaje.E_PARADO
        rutaAnimaciones = tools.obtenPathDeRecurso ("animaciones", animacion)
        rutaCaminar = tools.obtenPathDeRecurso (rutaAnimaciones, "caminar")
        rutaSaltar = tools.obtenPathDeRecurso (rutaAnimaciones, "saltar")
        rutaParado = tools.obtenPathDeRecurso (rutaAnimaciones, "parar")
        self.animacionCaminar = SpriteAnimadoOrientable(rutaCaminar, xInicial, yInicial, 8)
        self.animacionSaltar = SpriteAnimadoOrientable(rutaSaltar, xInicial, yInicial, 8)
        self.animacionParado = SpriteAnimadoOrientable(rutaParado, xInicial, yInicial, 60)
        self.dibujo = self.animacionParado
        self.orientacion = Personaje.O_DERECHA
        self.energia = Personaje.C_ENERGIA_MAXIMA
 #      directorio = tools.obtenPathDeRecurso(directorio, elemento)
        directorio = tools.obtenPathDeRecurso("sonidos", "personaje")
        rutaSonidoPaso = tools.obtenPathDeRecurso(directorio, "pasos.wav")
        self.sonidoPaso = pygame.mixer.Sound()

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

class MotorDeSonido():
    def __init__(self):
       self.listaSonido = []



    def anyadirSonido(self, sonido):
        self.listaSonido.append(sonido)

