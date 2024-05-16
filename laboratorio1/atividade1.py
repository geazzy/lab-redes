import random

def gerar_texto_puro(tamanho):
    alfabeto_portugues = 'abcdefghijklmnopqrstuvwxyz'
    frequencia_portugues = {
        'a': 0.1463, 'b': 0.0104, 'c': 0.0388, 'd': 0.0499,
        'e': 0.1257, 'f': 0.0102, 'g': 0.0130, 'h': 0.0078,
        'i': 0.0618, 'j': 0.0040, 'k': 0.0002, 'l': 0.0278,
        'm': 0.0474, 'n': 0.0505, 'o': 0.1073, 'p': 0.0252,
        'q': 0.0120, 'r': 0.0653, 's': 0.0781, 't': 0.0434,
        'u': 0.0463, 'v': 0.0167, 'w': 0.0001, 'x': 0.0021,
        'y': 0.0001, 'z': 0.0047
    }

    # Gera uma lista de letras ponderadas pela frequência
    letras_ponderadas = [letra for letra in alfabeto_portugues for _ in range(int(frequencia_portugues[letra] * 10000))]

    # Gera um texto puro aleatório com base nas letras ponderadas
    texto_puro = ''.join(random.choices(letras_ponderadas, k=tamanho))

    return texto_puro

def cifrar(texto_puro, deslocamento):
    alfabeto_portugues = 'abcdefghijklmnopqrstuvwxyz'
    alfabeto_cifrado = alfabeto_portugues[deslocamento:] + alfabeto_portugues[:deslocamento]
    chave_cifra = {alfabeto_portugues[i]: alfabeto_cifrado[i] for i in range(len(alfabeto_portugues))}
    
    texto_cifrado = ''
    for letra in texto_puro:
        if letra.isalpha():
            letra_min = letra.lower()
            if letra_min in chave_cifra:
                texto_cifrado += chave_cifra[letra_min]
            else:
                texto_cifrado += letra
        else:
            texto_cifrado += letra
    return texto_cifrado

def decifrar(texto_cifrado, deslocamento):
    alfabeto_portugues = 'abcdefghijklmnopqrstuvwxyz'
    alfabeto_cifrado = alfabeto_portugues[deslocamento:] + alfabeto_portugues[:deslocamento]
    chave_decifra = {alfabeto_cifrado[i]: alfabeto_portugues[i] for i in range(len(alfabeto_portugues))}
    
    texto_decifrado = ''
    for letra in texto_cifrado:
        if letra.isalpha():
            letra_min = letra.lower()
            if letra_min in chave_decifra:
                texto_decifrado += chave_decifra[letra_min]
            else:
                texto_decifrado += letra
        else:
            texto_decifrado += letra
    return texto_decifrado

# Exemplo de uso
tamanho = 100
texto_gerado = gerar_texto_puro(tamanho)
print("Texto puro gerado:", texto_gerado)

deslocamento = int(input("Informe o deslocamento da cifra de César: "))

# # Mapeamento do alfabeto
# alfabeto_portugues = 'abcdefghijklmnopqrstuvwxyz'
# alfabeto_cifrado = alfabeto_portugues[deslocamento:] + alfabeto_portugues[:deslocamento]
# print("Mapeamento do alfabeto:")
# for original, cifrado in zip(alfabeto_portugues, alfabeto_cifrado):
#     print(original, "->", cifrado)
    
# Texto cifrado
texto_cifrado = cifrar(texto_gerado, deslocamento)
print("Texto cifrado:", texto_cifrado)

# Decifrar texto cifrado
texto_decifrado = decifrar(texto_cifrado, deslocamento)
print("Texto decifrado:", texto_decifrado)

import string
from collections import Counter

def analisar_frequencia(texto):
    # Remover caracteres indesejados e normalizar para minúsculas
    texto = texto.lower()
    texto = ''.join(c for c in texto if c.isalnum() or c.isspace())

    # Contar a frequência de cada caractere
    frequencia_caracteres = Counter(texto)

    # Calcular o total de caracteres
    total_caracteres = sum(frequencia_caracteres.values())

    # Calcular a frequência relativa de cada caractere
    frequencia_relativa = {char: freq / total_caracteres for char, freq in frequencia_caracteres.items()}

    return frequencia_relativa

def analisar_bigramas_trigramas(texto):
    # Remover caracteres indesejados e normalizar para minúsculas
    texto = texto.lower()
    texto = ''.join(c for c in texto if c.isalnum() or c.isspace())

    # Gerar bigramas e trigramas
    bigramas = [texto[i:i+2] for i in range(len(texto) - 1)]
    trigramas = [texto[i:i+3] for i in range(len(texto) - 2)]

    # Contar a frequência de bigramas e trigramas
    frequencia_bigramas = Counter(bigramas)
    frequencia_trigramas = Counter(trigramas)

    # Calcular a frequência relativa de bigramas e trigramas
    total_bigramas = sum(frequencia_bigramas.values())
    total_trigramas = sum(frequencia_trigramas.values())

    frequencia_relativa_bigramas = {bg: freq / total_bigramas for bg, freq in frequencia_bigramas.items()}
    frequencia_relativa_trigramas = {tg: freq / total_trigramas for tg, freq in frequencia_trigramas.items()}

    return frequencia_relativa_bigramas, frequencia_relativa_trigramas

def analisar_texto(texto):
    frequencia_caracteres = analisar_frequencia(texto)
    frequencia_bigramas, frequencia_trigramas = analisar_bigramas_trigramas(texto)

    # Exibir resultados
    print("Frequência de caracteres:")
    print(frequencia_caracteres)

    print("\nFrequência de bigramas:")
    print(frequencia_bigramas)

    print("\nFrequência de trigramas:")
    print(frequencia_trigramas)

# Exemplo de uso
texto_exemplo = "Este é um exemplo de texto para análise de frequência de caracteres em português."
analisar_texto(texto_exemplo)
