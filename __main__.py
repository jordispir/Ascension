import framework
import pygame

pygame.init()

ventana = framework.Ventana()
juego = framework.Juego(ventana)

while not juego.finDeJuego():
    ventana.empiezaFrame()
    juego.leeEntradas()
    juego.ejecutaPaso()
    juego.dibuja()
    ventana.finalizaFrame()

pygame.quit()


