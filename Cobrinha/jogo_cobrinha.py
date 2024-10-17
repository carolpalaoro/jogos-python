import pygame
from random import randrange
import sys

# Definição das cores utilizadas no jogo
branco = (255,255,255)
preto = (0,0,0)
vermelho = (255,0,0)
verde = (0,255,0)
azul = (0,0,255)
cinza = (90,90,90)

# Configurações da tela e do jogo
largura = 640
altura = 520
tamanho = 10  # Tamanho de cada segmento da cobra
placar = 40   # Altura do placar na parte inferior da tela

def text(fundo, msg, cor, tam, posx, posy):
    font = pygame.font.SysFont(None,tam)
    texto1 = font.render(msg, True, cor)
    fundo.blit(texto1,(posx,posy))

def cobra(fundo, CobraXY):
    for XY in CobraXY:
        pygame.draw.rect(fundo,branco,(XY[0],XY[1],tamanho,tamanho))

def maca(fundo, maca_x, maca_y):
    pygame.draw.rect(fundo,vermelho,(maca_x,maca_y,tamanho,tamanho))

def jogo():
    pygame.init()
    relogio = pygame.time.Clock()
    fundo = pygame.display.set_mode((largura,altura))
    pygame.display.set_caption("Jogo da cobrinha")

    # Inicialização das variáveis
    pos_x = randrange(0,largura - tamanho,10)
    pos_y = randrange(0,altura - tamanho - placar,10)
    maca_x = randrange(0,largura - tamanho ,10)
    maca_y = randrange(0,altura - tamanho - placar,10)
    vel_x = 0
    vel_y = 0     
    CobraXY = []
    CobraComp = 1
    Score = 0

    # Loop principal do jogo
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and vel_x != tamanho:
                    vel_y = 0
                    vel_x = -tamanho
                if event.key == pygame.K_RIGHT and vel_x != -tamanho:
                    vel_y = 0
                    vel_x = tamanho
                if event.key == pygame.K_UP and vel_y != tamanho:
                    vel_x = 0
                    vel_y = -tamanho
                if event.key == pygame.K_DOWN and vel_y != -tamanho:
                    vel_x = 0
                    vel_y = tamanho

        fundo.fill(preto)
        pos_x += vel_x
        pos_y += vel_y

        if pos_x == maca_x and pos_y == maca_y:
            maca_x = randrange(0,largura - tamanho,10)
            maca_y = randrange(0,altura - tamanho - placar,10)
            CobraComp += 1
            Score += 10

        # Verifica colisão com as bordas
        if pos_x < 0 or pos_x + tamanho > largura or pos_y < 0 or pos_y + tamanho > altura - placar:
            game_over(fundo, Score)

        CobraInicio = [pos_x, pos_y]
        CobraXY.append(CobraInicio)
        if len(CobraXY) > CobraComp:
            del CobraXY[0]
        
        # Verifica colisão com o próprio corpo
        if any(Bloco == CobraInicio for Bloco in CobraXY[:-1]):
            game_over(fundo, Score)

        cobra(fundo, CobraXY)
        maca(fundo, maca_x, maca_y)

        pygame.draw.rect(fundo,cinza,(0,altura-placar,largura,placar))
        text(fundo, f"Score : {Score}", branco, 40, 10, altura-30)

        pygame.display.update()
        relogio.tick(10)  # Controla a velocidade do jogo

def game_over(fundo, Score):
    while True:
        fundo.fill(preto)
        text(fundo, "GAME OVER", vermelho, 50, 205, 130)
        text(fundo, f"Pontuação final: {Score}", branco, 30, 200, 180)
        text(fundo, "Pressione R para jogar novamente", branco, 25, 160, 230)
        text(fundo, "Pressione ESC para sair", branco, 25, 190, 260)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    jogo()
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

if __name__ == "__main__":
    jogo()