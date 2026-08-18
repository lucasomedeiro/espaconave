import pygame
import sys
import random

pygame.init()
pygame.mixer.init()

# CONFIGURAÇÕES
LARGURA, ALTURA = 800, 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("NAVE ESPACIAL")

clock = pygame.time.Clock()
FPS = 60

PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
AZUL_NAVE = (0, 200, 255)
AMARELO = (255, 230, 0)
VERMELHO = (255, 50, 50)
LARANJA = (255, 140, 0)
VERDE = (0, 255, 100)
CINZA = (180, 180, 180)
ROXO = (180, 0, 255)

# ESTRELAS DE FUNDO
class Estrela:
    def __init__(self):
        self.reiniciar()

    def reiniciar(self, y_inicial=None):
        self.x = random.randint(0, LARGURA)
        self.y = y_inicial if y_inicial is not None else random.randint(0, ALTURA)
        self.velocidade = random.uniform(0.5, 2.0)
        self.brilho = random.randint(100, 255)
        self.tamanho = random.randint(1, 3)

    def mover(self):
        self.y += self.velocidade
        if self.y > ALTURA:
            self.reiniciar(y_inicial=0)

    def desenhar(self, tela):
        cor = (self.brilho, self.brilho, self.brilho)
        pygame.draw.circle(tela, cor, (int(self.x), int(self.y)), self.tamanho)

# Explosão
class Particula:
    def __init__(self, x, y, cor):
        self.x = x
        self.y = y
        self.cor = cor
        self.vx = random.uniform(-3, 3)
        self.vy = random.uniform(-3, 3)
        self.vida = random.randint(15, 30)
        self.raio = random.randint(2, 5)

    def atualizar(self):
        self.x += self.vx
        self.y += self.vy
        self.vida -= 1
        self.raio = max(0, self.raio - 0.1)

    def desenhar(self, tela):
        if self.vida > 0:
            pygame.draw.circle(tela, self.cor, (int(self.x), int(self.y)), int(self.raio))