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

class Nave:
    def __init__(self):
        self.largura = 50
        self.altura = 45
        self.x = LARGURA // 2 - self.largura // 2
        self.y = ALTURA - 90
        self.velocidade = 6
        self.vidas = 3
        self.invencivel = 0
        self.cooldown_tiro = 0

    def mover(self):
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] and self.x > 0:
            self.x -= self.velocidade
        if teclas[pygame.K_RIGHT] and self.x + self.largura < LARGURA:
            self.x += self.velocidade
        if teclas[pygame.K_UP] and self.y > ALTURA // 2:
            self.y -= self.velocidade
        if teclas[pygame.K_DOWN] and self.y + self.altura < ALTURA:
            self.y += self.velocidade

        if self.invencivel > 0:
            self.invencivel -= 1
        if self.cooldown_tiro > 0:
            self.cooldown_tiro -= 1

    def atirar(self):
        if self.cooldown_tiro == 0:
            self.cooldown_tiro = 12
            cx = self.x + self.largura // 2
            return Tiro(cx, self.y)
        return None

    def levar_dano(self):
        if self.invencivel == 0:
            self.vidas -= 1
            self.invencivel = 90
            return True
        return False

    def rect(self):
        return pygame.Rect(self.x + 8, self.y + 8, self.largura - 16, self.altura - 8)

    def desenhar(self, tela):
        if self.invencivel > 0 and (self.invencivel // 6) % 2 == 0:
            return

        cx = self.x + self.largura // 2
        # corpo principal nave
        pygame.draw.polygon(tela, AZUL_NAVE, [
            (cx, self.y),
            (self.x + 5, self.y + self.altura),
            (self.x + self.largura - 5, self.y + self.altura),
        ])
        # cockpit
        pygame.draw.polygon(tela, BRANCO, [
            (cx, self.y + 8),
            (cx - 10, self.y + 28),
            (cx + 10, self.y + 28),
        ])

        # propulsores
        pygame.draw.rect(tela, LARANJA, 
                         (self.x + 5, self.y + self.altura - 5, 12, 8))
        pygame.draw.rect(tela, LARANJA,
                         (self.x + self.largura - 17, self.y + self.altura - 5, 12, 8))

        # chamas
        pygame.draw.polygon(tela, AMARELO, [
            (self.x + self.largura - 11, self.y + self.altura + 3),
            (self.x + self.largura - 5, self.y + self.altura + random.randint(8, 16)),
            (self.x + self.largura - 17, self.y + self.altura + 3),
        ])
        pygame.draw.polygon(tela, AMARELO, [
            (self.x + self.largura - 11, self.y + self.altura + 3),
            (self.x + self.largura - 5, self.y + self.altura + random.randint(8, 16)),
            (self.x + self.largura - 17, self.y + self.altura + 3),
        ])

class Tiro:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocidade = 10
        self.largura = 4
        self.altura = 14

    def mover(self):
        self.y -= self.velocidade

    def rect(self):
        return pygame.draw.Rect(self.x - self.largura // 2, self.y, self.largura, self.altura)

    def desenhar(self, tela):
        pygame.draw.rect(tela, AMARELO, self.rect(), border_radius=2)
        pygame.draw.rect(tela, BRANCO, (self.x - 1, self.y, 2, 6), border_radius=1)

class Inimigo:
    def __init__(self, nivel=1):
        self.largura = 44
        self.altura = 38
        self.x = random.randint(10, LARGURA - 54)
        self.y = random.randint(-120, -40)
        self.velocidade = random.uniform(1.5 + nivel * 0.3, 2.5 + nivel * 0.4)
        self.vida = 1 + (nivel // 3)
        self.cooldown_tiro = random.randint(60, 180)
        self.cor = random.choice([VERMELHO, ROXO, LARANJA])

