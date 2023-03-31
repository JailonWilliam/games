import pygame
import random

# Definir as cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
VERDE = (0, 255, 0)
VERMELHO = (255, 0, 0)
CINZA = (100, 100, 100)

# Definir a largura e altura da tela
largura_tela = 800
altura_tela = 600

# Inicializar o pygame
pygame.init()

# Definir a fonte
fonte = pygame.font.SysFont("Times new roman", 32)
fonte_morte = pygame.font.SysFont("Arial", 42)

# Criar a tela
tela = pygame.display.set_mode([largura_tela, altura_tela])

# Definir o título da janela
pygame.display.set_caption('Jogo da Cobrinha')

# Definir o clock
clock = pygame.time.Clock()
velocidade_jogo = 15

# Definir a posição e tamanho da cobra
posicao_x = largura_tela / 2
posicao_y = altura_tela / 2

# Definir a direcao da cobra
direcao_x = 10
direcao_y = 0
ultima_tecla = 'direita'

# Definir a lista de segmentos da cobra
segmentos_cobra = []
comprimento_inicial = 5

# Gerar a maçã em uma posição aleatória
posicao_maca = [random.randrange(0, (largura_tela // 10)) * 10, random.randrange(0, altura_tela // 10) * 10]

# Definir a pontuação
pontuacao = 0

nome_arquivo = 'record.txt'

# Lendo o arquivo, caso não exista, cria um arquivo com record 0
try:
    with open('record.txt', 'r') as arquivo:
        linhas = arquivo.read()
        record = int(linhas)

except FileNotFoundError:
        with open('record.txt', 'w') as arquivo:
            arquivo.write('0')
            record = 0

def atualiza_record():
        # Criando um novo arquivo em modo de escrita
        with open('record.txt', 'w') as arquivo:
            arquivo.write(str(pontuacao))

# Lista de obstáculo
obstaculo = []
# Defini a função para criar obstáculo no jogo
def desenhar_obstaculo():
    global obstaculo
    for barreira in obstaculo:
        pygame.draw.rect(tela, BRANCO, [barreira[0], barreira[1], 10, 10])

# Definir a função para desenhar a cobra
def desenhar_cobra(segmentos_cobra):
    for segmento in segmentos_cobra:
        pygame.draw.rect(tela, VERDE, [segmento[0], segmento[1], 10, 10])

# Definir a função para desenhar a maçã
def desenhar_maca(posicao_maca):
    pygame.draw.rect(tela, VERMELHO, [posicao_maca[0], posicao_maca[1], 10, 10])

# Definir a função para mostrar a pontuação
def mostrar_pontuacao(pontuacao):
    texto = fonte.render("Pontuação: "+str(pontuacao), True, BRANCO)
    tela.blit(texto, [0, 0])

def mostrar_record(record):
    texto = fonte.render("Record: "+str(record), True, BRANCO)
    tela.blit(texto, [500, 0])

def texto_morte():
    texto = fonte_morte.render(f'Pressione "R" para recomeçar', True, VERMELHO)
    tela.blit(texto, [120, 250])


def morreu():
    global jogo_ativo, segmentos_cobra, pontuacao, obstaculo, velocidade_jogo, record
    recomecar = False
    while recomecar == False:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                jogo_ativo = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:
                    recomecar = True
        tela.fill(PRETO)
        texto_morte()
        desenhar_jogo()
    
    #redefinindo cobra
    segmentos_cobra = []

    #atualizando record
    if pontuacao > record:
        record = pontuacao
        atualiza_record()
    #redefinindo pontuação
    pontuacao = 0

    #redefinindo obstaculo
    obstaculo = []

    #redefinindo velocidade
    velocidade_jogo = 15


def desenhar_jogo():
    desenhar_obstaculo()
    desenhar_cobra(segmentos_cobra)
    desenhar_maca(posicao_maca)
    mostrar_pontuacao(pontuacao)
    mostrar_record(record)
    pygame.display.update()


# Definir a função principal
def jogo():
    # Definir as variáveis globais
    global posicao_x, posicao_y, segmentos_cobra, posicao_maca, pontuacao, direcao_x, direcao_y, velocidade_jogo, ultima_tecla, obstaculo

    # Definir a variável para controlar o jogo
    jogo_ativo = True

    while jogo_ativo:
        # Processar eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                jogo_ativo = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT and ultima_tecla != 'direita':
                    direcao_x = -10
                    direcao_y = 0
                    ultima_tecla = 'esquerda'

                elif evento.key == pygame.K_RIGHT and ultima_tecla != 'esquerda':
                    direcao_x = 10
                    direcao_y = 0
                    ultima_tecla = 'direita'

                elif evento.key == pygame.K_UP and ultima_tecla != 'baixo':
                    direcao_x = 0
                    direcao_y = -10
                    ultima_tecla = 'cima'

                elif evento.key == pygame.K_DOWN and ultima_tecla != 'cima':
                    direcao_x = 0
                    direcao_y = 10
                    ultima_tecla = 'baixo'

        # Mover a cobra
        posicao_x += direcao_x
        posicao_y += direcao_y

        # Verificar se a cobra colidiu com a parede
        if posicao_x < 0:
            posicao_x += largura_tela
        if posicao_x > largura_tela -10:
            posicao_x -= largura_tela

        if posicao_y < 0:
            posicao_y += altura_tela
        if posicao_y > altura_tela -10:
            posicao_y -= altura_tela  

        # Verifica se a cobra bateu no corpo
        if [posicao_x, posicao_y] in segmentos_cobra:
            if pontuacao > record:
                atualiza_record()
            # jogo_ativo = False
            morreu()

         # Verifica se a cobra colidiu com a barreira
        if [posicao_x, posicao_y] in obstaculo:
            if pontuacao > record:
                atualiza_record()
            # jogo_ativo = False
            morreu()

        # Verificar se a cobra comeu a maçã
        if posicao_x == posicao_maca[0] and posicao_y == posicao_maca[1]:
            aux = posicao_maca

            posicao_maca = [random.randrange(0, largura_tela // 10) * 10, random.randrange(0, altura_tela // 10) * 10]

            obstaculo.append(aux)
            pontuacao += 1
            segmentos_cobra.append([posicao_x, posicao_y])
            velocidade_jogo *= 1.05


        # Adicionar o segmento da cobra
        segmentos_cobra.insert(0, [posicao_x, posicao_y])

        # atualiza o tamanho da cobra ao andar
        if len(segmentos_cobra) > comprimento_inicial:
            del segmentos_cobra[-1]

        # Fundo = preto
        tela.fill(PRETO)

        # Desenhar a tela
        desenhar_jogo()

        # Definir a velocidade do jogo
        clock.tick(velocidade_jogo)

    # Encerrar o jogo
    pygame.quit()

# Iniciar o jogo
jogo()

