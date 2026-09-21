import pygame
import random

pygame.init()


# Configurações da tela
LARGURA, ALTURA = 1200, 800
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Desvie das Canetas")

imagem_fundo = pygame.image.load("fundo_manoel_1200x800.png").convert()
fundo_x = (LARGURA - imagem_fundo.get_width()) // 2
fundo_y = (ALTURA - imagem_fundo.get_height()) // 2

# Cores
BRANCO = (255, 255, 255)
AZUL = (50, 150, 255)
VERMELHO = (255, 60, 60)
PRETO = (0, 0, 0)
ROSA = (255, 20, 147)

# Jogador
jogador_largura, jogador_altura = 100, 100
velocidade_jogador_inicial = 15

imagem_jogador = pygame.image.load("manoel_sem_fundo.png").convert_alpha()
imagem_jogador = pygame.transform.scale(imagem_jogador, (jogador_largura, jogador_altura))

# Bloco inimigo
bloco_largura, bloco_altura = 110, 110
velocidade_bloco_inicial = 10

imagem_bloco = pygame.image.load("pngwing.com.png").convert_alpha()
imagem_bloco = pygame.transform.scale(imagem_bloco, (bloco_largura, bloco_altura))

clock = pygame.time.Clock()
fonte = pygame.font.SysFont(None, 36)
fonte_grande = pygame.font.SysFont(None, 90)
fonte_media = pygame.font.SysFont(None, 48)


def tela_game_over(pontos):
    #Mostra a tela de Game Over e espera o jogador decidir o que fazer.
    #Retorna True se o jogador quiser reiniciar, False se quiser sair.
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:
                    return True
                if evento.key == pygame.K_ESCAPE:
                    return False

        # fundo escurecido
        tela.blit(imagem_fundo, (fundo_x, fundo_y))
        overlay = pygame.Surface((LARGURA, ALTURA))
        overlay.set_alpha(180)
        overlay.fill(PRETO)
        tela.blit(overlay, (0, 0))

        texto_go = fonte_grande.render("GAME OVER", True, VERMELHO)
        texto_go_rect = texto_go.get_rect(center=(LARGURA // 2, ALTURA // 2 - 80))
        tela.blit(texto_go, texto_go_rect)

        texto_pontos = fonte_media.render(f"Pontuação final: {pontos}", True, BRANCO)
        texto_pontos_rect = texto_pontos.get_rect(center=(LARGURA // 2, ALTURA // 2))
        tela.blit(texto_pontos, texto_pontos_rect)

        texto_instrucao = fonte.render("Pressione R para reiniciar ou ESC para sair", True, BRANCO)
        texto_instrucao_rect = texto_instrucao.get_rect(center=(LARGURA // 2, ALTURA // 2 + 70))
        tela.blit(texto_instrucao, texto_instrucao_rect)

        pygame.display.flip()
        clock.tick(30)

    return False


def jogar():
    #Roda uma partida. Retorna a pontuação final ao colidir.
    jogador_x = LARGURA // 2 - jogador_largura // 2
    jogador_y = ALTURA - jogador_altura - 10
    velocidade_jogador = velocidade_jogador_inicial

    bloco_x = random.randint(0, LARGURA - bloco_largura)
    bloco_y = -bloco_altura
    velocidade_bloco = velocidade_bloco_inicial

    pontos = 0
    rodando = True

    while rodando:
        clock.tick(100)  # 60 FPS

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()

        # Movimento do jogador
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] and jogador_x > 0:
            jogador_x -= velocidade_jogador
        if teclas[pygame.K_RIGHT] and jogador_x < LARGURA - jogador_largura:
            jogador_x += velocidade_jogador


        # Movimento do bloco
        bloco_y += velocidade_bloco
        if bloco_y > ALTURA:
            bloco_y = -bloco_altura
            bloco_x = random.randint(0, LARGURA - bloco_largura)
            pontos += 1
            velocidade_bloco += 0.5  # aumenta a dificuldade aos poucos
            velocidade_jogador += 0.5

        # Verifica colisão (game over)
        jogador_rect = pygame.Rect(jogador_x, jogador_y, jogador_largura, jogador_altura)
        bloco_rect = pygame.Rect(bloco_x, bloco_y, bloco_largura, bloco_altura)

        if jogador_rect.colliderect(bloco_rect):
            rodando = False

        # Desenho
        tela.fill(BRANCO)
        tela.blit(imagem_fundo, (fundo_x, fundo_y))

        tela.blit(imagem_jogador, (jogador_x, jogador_y))
        tela.blit(imagem_bloco, (bloco_x, bloco_y))

        texto = fonte.render(f"Pontos: {pontos}", True, (0, 0, 0))
        tela.blit(texto, (10, 10))

        pygame.display.flip()

    return pontos


# Loop principal do jogo, permitindo reiniciar após o Game Over
continuar = True
while continuar:
    pontos_finais = jogar()
    continuar = tela_game_over(pontos_finais)

pygame.quit()