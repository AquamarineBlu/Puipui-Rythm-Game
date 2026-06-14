import pygame
import sys

# Inicialização
pygame.init()
pygame.mixer.init()

# Configurações da Tela
LARGURA, ALTURA = 800, 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Meu Jogo de Ritmo")
relogio = pygame.time.Clock()

# Cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
CINZA = (50, 50, 50)
CORES_FAIXAS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)] # Vermelho, Verde, Azul, Amarelo

# Configurações do Jogo
TECLAS = [pygame.K_d, pygame.K_f, pygame.K_j, pygame.K_k] # Teclas para as 4 faixas
POS_Y_ALVO = 500  # Onde o jogador deve apertar a nota
VELOCIDADE = 0.1  # Pixels por milissegundo

# --- MAPEAMENTO DAS NOTAS (Mapeamento/Beatmap) ---
# Cada tupla é: (tempo_em_milissegundos, indice_da_faixa)
NOTAS_MAPA = [
    (1000, 0), (1500, 1), (2000, 2), (2500, 3),
    (3000, 0), (3200, 1), (3400, 2), (3600, 3),
    (5000, 1), (5500, 2), (6000, 0), (7000, 3)
]

# Carregar música (Substitua por um arquivo real)
# pygame.mixer.music.load("musica.mp3")
# pygame.mixer.music.play()

# Marcar o tempo de início do jogo
tempo_inicial = pygame.time.get_ticks()
pontuacao = 0
fonte = pygame.font.SysFont(None, 40)

# Loop Principal
rodando = True
while rodando:
    tela.fill(PRETO)
    
    # Calcular tempo atual da música
    tempo_atual = pygame.time.get_ticks() - tempo_inicial

    # 1. Captura de Eventos (Input do Jogador)
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
            
        if evento.type == pygame.KEYDOWN:
            if evento.key in TECLAS:
                faixa_pressionada = TECLAS.index(evento.key)
                
                # Verificar se acertou alguma nota nessa faixa
                for nota in NOTAS_MAPA[:]:  # Cópia da lista para poder remover itens
                    tempo_nota, faixa_nota = nota
                    if faixa_nota == faixa_pressionada:
                        # Margem de erro de 100 milissegundos para mais ou para menos
                        if abs(tempo_atual-tempo_nota) < 100:
                            pontuacao += 100
                            NOTAS_MAPA.remove(nota)
                            break

    # 2. Desenhar o Cenário (As 4 faixas e a linha de batida)
    for i in range(4):
        x = 200 + i * 100
        pygame.draw.rect(tela, CINZA, (x, 0, 80, ALTURA), 1)
        pygame.draw.rect(tela, BRANCO, (x, POS_Y_ALVO, 80, 10), 2) # Linha alvo

    # 3. Atualizar e Desenhar as Notas
    for nota in NOTAS_MAPA[:]:
        tempo_nota, faixa_nota = nota
        
        # Calcular posição Y com base no tempo
        # Distância = Velocidade * Tempo restante até o momento do acerto
        tempo_restante = tempo_nota - tempo_atual
        pos_y = POS_Y_ALVO - (tempo_restante * VELOCIDADE)
        
        # Desenhar a nota se ela estiver na tela
        if pos_y > -50 and pos_y < ALTURA:
            pos_x = 200 + faixa_nota * 100
            pygame.draw.rect(tela, CORES_FAIXAS[faixa_nota], (pos_x, pos_y, 80, 20))
        
        # Se a nota passou direto e o jogador perdeu
        if pos_y > POS_Y_ALVO + 50:
            NOTAS_MAPA.remove(nota)

    # 4. Mostrar Pontuação
    texto_score = fonte.render(f"Pontos: {pontuacao}", True, BRANCO)
    tela.blit(texto_score, (20, 20))

    pygame.display.flip()
    relogio.tick(60) # Mantém o jogo visualmente fluido, mas não afeta a física das notas

pygame.quit()
sys.exit()