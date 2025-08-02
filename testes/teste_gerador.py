#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de teste para verificar a funcionalidade de geração dinâmica de conteúdo
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from gerador_conteudo import gerador_conteudo

def teste_gerador_conteudo():
    """Testa o gerador de conteúdo dinâmico"""
    print("=== TESTE DO GERADOR DE CONTEÚDO DINÂMICO ===\n")
    
    # Teste 1: Conteúdo para iniciante sobre HTML
    print("TESTE 1: Conteúdo para INICIANTE sobre HTML (formato Texto)")
    print("-" * 60)
    conteudo1 = gerador_conteudo.gerar_conteudo_personalizado(
        tema="HTML", 
        nivel="iniciante", 
        formato="Texto"
    )
    print(conteudo1)
    print("\n")
    
    # Teste 2: Conteúdo para intermediário sobre programação
    print("TESTE 2: Conteúdo para INTERMEDIÁRIO sobre programação (formato PDF)")
    print("-" * 60)
    conteudo2 = gerador_conteudo.gerar_conteudo_personalizado(
        tema="programação", 
        nivel="intermediário", 
        formato="PDF"
    )
    print(conteudo2)
    print("\n")
    
    # Teste 3: Conteúdo para avançado sobre HTML
    print("TESTE 3: Conteúdo AVANÇADO sobre HTML (formato Vídeo)")
    print("-" * 60)
    conteudo3 = gerador_conteudo.gerar_conteudo_personalizado(
        tema="HTML", 
        nivel="avançado", 
        formato="Vídeo"
    )
    print(conteudo3)
    print("\n")
    
    # Teste 4: Exercício para intermediário
    print("TESTE 4: Exercício INTERMEDIÁRIO sobre programação")
    print("-" * 60)
    conteudo4 = gerador_conteudo.gerar_conteudo_personalizado(
        tema="programação", 
        nivel="intermediário", 
        formato="Exercício"
    )
    print(conteudo4)
    print("\n")
    
    # Teste 5: Com histórico de dificuldades
    print("TESTE 5: Conteúdo com histórico de dificuldades")
    print("-" * 60)
    historico_dificuldades = ["HTML", "CSS"]
    conteudo5 = gerador_conteudo.gerar_conteudo_personalizado(
        tema="JavaScript", 
        nivel="iniciante", 
        formato="Texto",
        historico_dificuldades=historico_dificuldades
    )
    print(conteudo5)
    print("\n")
    
    print("=== TESTES CONCLUÍDOS ===")

if __name__ == "__main__":
    teste_gerador_conteudo()
