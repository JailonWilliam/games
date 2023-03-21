import pygame, os
from random import randint, randrange, choice
from pygame.locals import *

pygame.init()
pygame.mixer.init()
#diretorios
diretorio_principal = os.path.dirname(__file__)
diretorio_imagem = os.path.join(diretorio_principal, "Imagens_Dino")
diretorio_sons = os.path.join(diretorio_principal, "Sons_Dino")

#tela e nome do jogo
largura, altura = 640, 400
screen = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Dino")

#Texto
fonte_grande = pygame.font.SysFont('Arial', 100, 100)
fonte_pequena = pygame.font.SysFont('Times news roman', 30, 30)

#Sprites usadadas
sprite_sheet_dino = pygame.image.load(os.path.join(diretorio_imagem, 'Dino_sprite.png')).convert_alpha()
sprite_sheet_nuvens = pygame.image.load(os.path.join(diretorio_imagem, 'nuvens.png')).convert_alpha()
sprite_sheet_plataforma = pygame.image.load(os.path.join(diretorio_imagem, 'Plataforma-2v-escala-maior.png')).convert_alpha()
sprite_sheet_cactos = pygame.image.load(os.path.join(diretorio_imagem, 'cactos.png')).convert_alpha()
sprite_sheet_esquilo = pygame.image.load(os.path.join(diretorio_imagem, 'Esquilo voador.png')).convert_alpha()


#Musica e sons usados
som_pontos = pygame.mixer.Sound(os.path.join(diretorio_sons, 'sons_score_sound.wav'))
som_pontos.set_volume(0.5)
som_colisao = pygame.mixer.Sound(os.path.join(diretorio_sons, 'smw_bubble_pop.wav'))
musica_fundo = pygame.mixer.music.load(os.path.join(diretorio_sons, 'BoxCat Games - Passing Time.mp3'))
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.3)

#colisão
colidiu = False
escolha_obstaculo = randint(0, 1)

class Dino(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.som_pulo = pygame.mixer.Sound(os.path.join(diretorio_sons, 'sons_jump_sound.wav'))
        self.som_pulo.set_volume(1)
        self.imagem_dino = []
        for i in range(4):
            img = sprite_sheet_dino.subsurface((0, 1000 * i), (1000, 1000))
            img = pygame.transform.scale(img, (1000 // 7, 1000 // 7))
            self.imagem_dino.append(img)

        self.index_lista = 0
        self.image = self.imagem_dino[self.index_lista]
        self.pos_y_inicial = 210
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.topleft = (20, self.pos_y_inicial)
        self.pulo = False

    def pular(self):
        self.pulo = True
        self.som_pulo.play()

    def update(self):
        if self.pulo == True:
            if self.rect.y <= 85:
                self.pulo = False

            self.rect.y -= 15
        else:
            if self.rect.y < self.pos_y_inicial:
                self.rect.y += 15
            else:
                self.rect.y = self.pos_y_inicial

        if self.pulo == False:
            if self.index_lista > 3:
                self.index_lista = 0
            self.index_lista += 0.25
            self.image = self.imagem_dino[int(self.index_lista)]

class Chao(pygame.sprite.Sprite):
    def __init__(self, x_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet_plataforma.subsurface((0, 0), (800, 800))
        self.image = pygame.transform.scale(self.image, (largura + 100, 600))
        self.rect = self.image.get_rect()
        self.rect.topleft = x_pos, 40
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.x -= 15

class Nuvens(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_nuvens = []
        for x in range(5):
            img = sprite_sheet_nuvens.subsurface((0, 64 * x), (64, 64))
            img = pygame.transform.scale(img, (64 * 2, 64 * 2))
            self.image_nuvens.append(img)

        self.index_lista = 0
        self.image = self.image_nuvens[self.index_lista]
        self.rect = pygame.Surface.get_rect(self.image)
        self.rect.y = randrange(0, 200, 50)
        self.rect.x = largura + (randrange(100, 1000, 100))

    def update(self):
        if self.index_lista > 4:
            self.index_lista = 0

        self.index_lista += 0.025
        self.image = self.image_nuvens[int(self.index_lista)]
        if self.rect.topright[0] < 0:
            self.rect.x = largura + (randrange(100, 1000, 100))
            self.rect.y = randrange(0, 200, 50)

        self.rect.x -= 5

class Cacto(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.catos = []
        self.escolha = escolha_obstaculo
        for x in range(2):
            img = sprite_sheet_cactos.subsurface((0, 62 * x), (62, 62))
            img = pygame.transform.scale(img, (62 * 2, 62 * 2))
            self.catos.append(img)

        self.sorte = randint(0, 1)
        self.image = self.catos[self.sorte]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.topleft = 600, 192


    def update(self):
        if self.escolha == 0:
            self.rect.x -= 15
            if self.rect.topright[0] <= -10:
                self.rect.x = largura
                self.sorte = randint(0, 1)
            self.image = self.catos[self.sorte]

class Esquilo(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.esquilo = []
        self.escolha = escolha_obstaculo
        for x in range(4):
            img = sprite_sheet_esquilo.subsurface((0, 140 * x), (140, 140))
            self.esquilo.append(img)
        self.atual = 0
        self.image = self.esquilo[self.atual]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.topleft = 610, 0

    def update(self):
        if self.escolha == 1:
            self.atual += 1
            if self.atual >= len(self.esquilo):
                self.atual = 0
            self.image = self.esquilo[int(self.atual)]
            self.rect.x -= 15
            self.rect.y += 3

sprites = pygame.sprite.Group()

for i in range(3):
    nuvem = Nuvens()
    sprites.add(nuvem)
relogio = pygame.time.Clock()

esquilo = Esquilo()
sprites.add(esquilo)

cacto = Cacto()
sprites.add(cacto)

grupo_obstaculo = pygame.sprite.Group()
grupo_obstaculo.add(cacto)
grupo_obstaculo.add(esquilo)

solo1 = Chao(0)
solo2 = Chao(largura + 10)

sprites.add(solo1)
sprites.add(solo2)

dino = Dino()
sprites.add(dino)

velocidade = 30
pontos = 0
record = 0

while True:
    relogio.tick(int(velocidade))
    screen.fill((0, 200, 255))
    #texto
    texto = f'Game Over'
    texto_GameOver_format = fonte_grande.render(texto, True, (255, 255, 255))
    texto_pontos = f'scored: {pontos}'
    texto_pontos_format = fonte_pequena.render(texto_pontos, True, (255, 255, 255))
    texto_record = f'Rercod: {record}'
    texto_record_format = fonte_pequena.render(texto_record, True, (255, 255, 255))
    texto_restart = f'Press R for restart'
    texto_restart_format = fonte_pequena.render(texto_restart, True, (255, 255, 255))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            quit()
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                if dino.rect.y != dino.pos_y_inicial:
                    pass
                else:
                    dino.pular()
            if event.key == K_r:
                #Pressione r para recomeçar
                if colidiu == True:
                    colidiu = False
                    pygame.mixer.music.play(-1)
                    esquilo.rect.topleft = largura, 0
                    cacto.rect.x = 700
                    pontos = 0
                    velocidade = 30

    velocidade += 0.01
    colisoes = pygame.sprite.spritecollide(dino, grupo_obstaculo, False, pygame.sprite.collide_mask)
    #colocando o texto na tela
    screen.blit(texto_pontos_format, (485, 5))
    screen.blit(texto_record_format, (300, 5))
    #Desenhando todas as sprites na tela
    sprites.draw(screen)

    if cacto.rect.topright[0] <= 0 or esquilo.rect.topright[0] <= 0:
        escolha_obstaculo = randint(0, 1)
        esquilo.rect.x = largura
        esquilo.rect.y = 0
        cacto.rect.x = largura

        esquilo.escolha = escolha_obstaculo
        cacto.escolha = escolha_obstaculo

    if solo1.rect.topright[0] <= 0:
        solo1.rect.x = largura
    if solo2.rect.topright[0] <= 0:
        solo2.rect.x = largura

    if colisoes and colidiu == False:
        pygame.mixer.music.stop()
        som_colisao.play()
        colidiu = True
        
    if colidiu == True:
        screen.blit(texto_GameOver_format, (65, 100))
        screen.blit(texto_restart_format, (220, 200))
        if pontos > record:
            record = pontos
    else:
        if pontos % 100 == 0:
            som_pontos.play()
        pontos += 1
        sprites.update()

    pygame.display.flip()