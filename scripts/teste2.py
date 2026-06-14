NOTAS_MAPA = [
    (1000, 0), (1500, 1), (2000, 2), (2500, 3),
    (3000, 0), (3200, 1), (3400, 2), (3600, 3),
    (5000, 1), (5500, 2), (6000, 0), (7000, 3)
]


for nota in NOTAS_MAPA[:]:  # Cópia da lista para poder remover itens
    tempo_nota, faixa_nota = nota
    print(tempo_nota, faixa_nota)
    print(nota)

