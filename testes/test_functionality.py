# -*- coding: utf-8 -*-

import unittest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from codificacao.gerador_conteudo import GeradorConteudoDinamico
from codificacao.utils import buscar_conteudo

class TestCompleteSystem(unittest.TestCase):
    def setUp(self):
        """Configuração inicial para os testes."""
        self.gerador = GeradorConteudoDinamico()

    def test_geracao_conteudo_dinamico(self):
        """Testa a geração de conteúdo dinâmico."""
        conteudo = self.gerador.gerar_conteudo_personalizado('HTML', 'iniciante', 'Texto')
        self.assertIsInstance(conteudo, str)
        self.assertIn('HTML', conteudo)
        print('Teste de geração de conteúdo dinâmico: PASSOU')

    def test_busca_conteudo(self):
        """Testa a busca de conteúdo indexado."""
        resultado = buscar_conteudo('Python', 'Texto')
        self.assertIsNotNone(resultado)
        print('Teste de busca de conteúdo: PASSOU')

    def test_integracao_gerador_busca(self):
        """Testa a integração entre o gerador de conteúdo e a busca."""
        tema = 'Python'
        resultados_busca = buscar_conteudo(tema, 'Texto')
        conteudo_gerado = self.gerador.gerar_conteudo_personalizado(tema, 'intermediário', 'Texto')
        self.assertIsInstance(conteudo_gerado, str)
        self.assertIsNotNone(resultados_busca)
        print('Teste de integração gerador e busca: PASSOU')

    def test_erro_geracao_conteudo(self):
        """Testa o tratamento de erros na geração de conteúdo."""
        with self.assertRaises(Exception):
            self.gerador.gerar_conteudo_personalizado('', 'iniciante', 'Texto')
        print('Teste de tratamento de erro na geração de conteúdo: PASSOU')

    def test_indexacao_recursos(self):
        """Testa se os recursos foram indexados corretamente."""
        # Testa busca por diferentes tipos de conteúdo
        resultado_texto = buscar_conteudo('Apresentação', 'Texto')
        resultado_pdf = buscar_conteudo('Capítulo', 'PDF')
        resultado_video = buscar_conteudo('Dica', 'Vídeo')
        resultado_exercicios = buscar_conteudo('Exercícios', 'Texto')
        
        self.assertIsNotNone(resultado_texto)
        self.assertIsNotNone(resultado_pdf)
        self.assertIsNotNone(resultado_video)
        self.assertIsNotNone(resultado_exercicios)
        print('Teste de indexação de recursos: PASSOU')

    def test_sistema_completo(self):
        """Testa o sistema completo de geração e busca."""
        # Busca conteúdo sobre um tema
        tema = 'HTML'
        resultados = buscar_conteudo(tema, 'Texto')
        
        # Gera conteúdo baseado no tema
        conteudo_iniciante = self.gerador.gerar_conteudo_personalizado(tema, 'iniciante', 'Texto')
        conteudo_avancado = self.gerador.gerar_conteudo_personalizado(tema, 'avançado', 'Vídeo')
        
        # Verifica se o conteúdo foi gerado
        self.assertIsInstance(conteudo_iniciante, str)
        self.assertIsInstance(conteudo_avancado, str)
        print('Teste do sistema completo: PASSOU')

if __name__ == '__main__':
    unittest.main(verbosity=2)
