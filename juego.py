import pygame 
import random
import math 
import sys 
import os 

# INICIAR pygame 
pygame.init()

#   ESTABLECER EL TAMAÑO DE LA PANTALLA 
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height)) 

# FUNCION PARA OBTENER RUTA DE LOS RECURSOS 
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

# CARGAR IMAGEN DE FONDO 
asset_background = resource_path('assets/images/fondo.png')
background = pygame.image.load(asset_background)

# CARGAR ICONO DE VENTANA 
asset_icon = resource_path('assets/images/ufo.png')
icon = pygame.image.load(asset_icon)
 
# CARGAR SONIDO DE FONDO  
asset_sound = resource_path('assets/audios/background_music.mp3')
backgroud_sound = pygame.mixer.music.load(asset_sound)


# CARGAR IMAGEN DEL JUGADOR 
asset_playerimg = resource_path('assets/images/militar.png')
playerimg = pygame.image.load(asset_playerimg)

# CARGAR IMAGEN DE BALA 
asset_bulletimg = resource_path('assets/images/bullet.png')
bulletimg = pygame.image.load(asset_bulletimg)

# CARGAR FUENTE PARA TEXTO DE GAME OVER 
asset_over_font = resource_path('assets/fonts/RAVIE.TTF')
over_font = pygame.font.Font(asset_over_font)
 
# CARGAR FUENTE PARA TEXTO DE PUNTAJE 
asset_font = resource_path('assets/fonts/comicbd.ttf')
font = pygame.font.Font(asset_font, 32)

# ESTABLECER TITULO DE VENTANA 
pygame.display.set_caption('Invasión Militar')

# ESTABLECER ICONO DE VENTANA 
pygame.display.set_icon(icon)

# REPRODUCIR SONIDO DE FONDO EN LOOP
pygame.mixer.music.play(-1)

# CREAR RELOJ PARA CONTROLAR LA VELOCIDAD DEL JUEGO
clock = pygame.time.Clock()

# POSICION INICIAL DEL JUGADOR 
playerX = 370
playerY = 470
playerx_change = 0
playery_change = 0


# LISTA PARA ALMACENAR POSICIONES DE LOS ENEMIGOS 
enemyimg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
no_of_enemies = 10
 
# SE INICIALIZAN LAS VARIABLES PARA GUARDAR LAS POSICIONES DE LOS ENEMIGOS 
for i in range(no_of_enemies):
    # SE CARGA LAS IMAGENES DE LOS ENEMIGOS 1 Y 2
    enemy1 = resource_path('assets/images/helicop.png')
    enemyimg.append(pygame.image.load(enemy1))

    enemy2 = resource_path('assets/images/tanquecito.png')
    enemyimg.append(pygame.image.load(enemy2))

# SE ASIGNA UNA POSICION ALEATORIA EN X Y Y EN EL ENEMIGO 
    enemyX.append(random.randint(0,736))
    enemyY.append(random.randint(0,150))

# SE ESTABLECE LA VELOCIDAD EN MOVIMIENTO DEL ENEMIGO EN X Y Y
    enemyX_change.append(random.randint(5, 10))
    enemyY_change.append(random.randint(10,20))

# SE INICIALIZAN LAS VARIABLES PARA GUARDAR LA POSICION DE LA BALA
    bulletX = 0
    bulletY = 480
    bulletX_change = 0
    bulletY_change = 10
    bullet_state = "ready"

    # SE INICIALIZA LA PUNTUACION EN 0
    score = 0

    # FUNCION PARA MOSTRAR LA PUNTUACION EN LA PANTALLA
    def show_score():
        score_value = font.render("SCORE " + str(score), True, (255, 255, 255))
        screen.blit(score_value, (10, 10))
    
    # FUNCION PARA DIBUJAR AL JUGADOR EN LA PANTALLA
    def player(x, y, i):
        screen.blit(playerimg, (x, y))

    # FUNCION PARA DIBUJAR AL ENEMIGO EN LA PANTALLA
    def enemy(x, y, i):
        screen.blit(enemyimg[i], (x, y))

    # FUNCION PARA DISPARAR LA BALA
    def fire_bullet(x, y):
        global bullet_state

        bullet_state = "fire"
        screen.blit(bulletimg, (x + 16, y + 10))

    # FUNCION PARA COMPROBAR SI HAY UNA COLISION ENTRE LA BALA Y EL ENEMIGO 
    def isColision(enemyX, enemyY, bulletX, bulletY):
        distance = math.sqrt((math.pow(enemyX-bulletX, 2)) +
                            (math.pow(enemyY-bulletY, 2)))
        if distance < 27:
            return True 
        else: 
            return False
        
    # FUNCION PARA MOSTRAR EL TEXTO DE GAME OVER EN PANTALLA
    def game_over_text():
        over_text = over_font.render("FIN DEL JUEGO", True, (255, 255, 255))
        text_rect = over_text.get_rect(
            center=(int(screen_width/2), int(screen_height/2)))
        screen.blit(over_text, text_rect)


    # FUNCION PRINCIPAL DEL JUEGO
    def gameloop():

        # DECLARAR VARIABLES GLOBALES 
        global score
        global playerX
        global playerx_change
        global bulletX
        global bulletY
        global colision
        global bullet_state

        in_game = True 
        while in_game:
            # Maneja eventos, actualiza y renderiza el juego
            # limpia la pantalla
            screen.fill((0, 0, 0))
            screen.blit(background, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    in_game = False
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    # MANEJA LOS MOVIMIENTOS DEL JUGADOR Y EL DISPARO
                    if event.key == pygame.K_LEFT:
                        playerx_change = -5
                        
                    if event.key == pygame.K_RIGHT:
                        playerx_change = 5

                    if event.key == pygame.K_SPACE:
                        if bullet_state == "ready":
                            bulletX = playerX
                            fire_bullet(bulletX, bulletY)

                    if event.type == pygame.KEYUP:
                        playerx_change = 0
                     
            # aqui se esta actualizando la posicion del jugador 
            playerX += playerx_change

            if playerX <= 0:
                    playerX = 0
            elif playerX >= 736:
                playerX = 736

            # BUCLE QUE SE EJECUTA PARA CADA ENEMIGO 
            for i in range(no_of_enemies):
                if enemyY[i] > 440:
                    for j in range(no_of_enemies):
                        enemyY[j] = 2000
                    game_over_text()

                enemyX[i]+= enemyX_change[i]
                if enemyX[i] <= 0:
                    enemyX_change[i] = 5
                    enemyY[i] += enemyY_change[i]
                elif enemyX[i] >= 736:
                    enemyX_change[i] = -5
                    enemyY[i] += enemyY_change[i]

                #   AQUI SE COMPRUEBA SI HA HABIDO UNA COLISION ENTRE UN ENEMIGO Y UNA BALA
                
                collision = isColision(enemyX[i], enemyY[i], bulletX, bulletY)
                if collision:
                    bulletY = 454
                    bullet_state = "ready"
                    score += 1
                    enemyX[i] = random.randint(0, 736)
                    enemyY[i] = random.randint(0, 150)
                enemy(enemyX[i], enemyY[i], i)

            if bulletY < 0:
                bulletY = 454
                bullet_state = "ready"
            if bullet_state == "fire":
                fire_bullet(bulletX, bulletY)
                bulletY -= bulletY_change

            player(playerX, playerY, i)
            show_score()

            pygame.display.update()

            clock.tick(120)

gameloop()
