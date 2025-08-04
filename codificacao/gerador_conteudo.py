import random
import re
from typing import Dict, List, Optional, Any, Union
from codificacao.utils import buscar_conteudo
from codificacao.config import Config
from codificacao.logger_config import setup_logger, log_performance
from codificacao.validation import validate_input_parameters, ValidationError

class GeradorConteudoDinamico:
    """
    Gerador de conteúdos dinâmicos personalizados baseado no nível do usuário,
    formato preferido, e histórico de dificuldades.
    """
    
    def __init__(self):
        """Inicializa o gerador com logger e templates."""
        self.logger = setup_logger(__name__)
        self.logger.info("GeradorConteudoDinamico inicializado")
        
        # Templates para diferentes níveis de conhecimento
        self.templates_iniciante = {
            'introducao': [
                "Vamos começar com o básico sobre {tema}.",
                "Primeiro, é importante entender o que é {tema}.",
                "Para começar, vamos entender os fundamentos de {tema}.",
                "Vou explicar {tema} de forma simples e clara."
            ],
            'explicacao': [
                "{tema} é {conceito_base}. Em outras palavras, {explicacao_simples}.",
                "Para entender {tema}, imagine que {analogia}. Isso significa que {conceito_base}.",
                "De forma simples, {tema} funciona assim: {explicacao_simples}."
            ],
            'exemplo': [
                "Por exemplo: {exemplo_pratico}",
                "Veja este exemplo prático: {exemplo_pratico}",
                "Um caso comum seria: {exemplo_pratico}"
            ]
        }
        
        self.templates_intermediario = {
            'introducao': [
                "Agora vamos aprofundar em {tema}.",
                "Como você já tem conhecimento básico, vamos explorar {tema} mais detalhadamente.",
                "Vamos expandir seu conhecimento sobre {tema}."
            ],
            'explicacao': [
                "{tema} envolve {conceitos_intermediarios}. Isso se relaciona com {conexoes}.",
                "Em {tema}, é importante considerar {aspectos_tecnicos} e como isso impacta {aplicacoes}.",
                "{tema} tem várias aplicações, incluindo {casos_uso}."
            ],
            'exemplo': [
                "Considere este cenário: {exemplo_intermediario}",
                "Na prática, isso significa: {aplicacao_pratica}",
                "Um exemplo mais complexo seria: {exemplo_avancado}"
            ]
        }
        
        self.templates_avancado = {
            'introducao': [
                "Vamos explorar aspectos avançados de {tema}.",
                "Para o seu nível, é interessante analisar {tema} sob a perspectiva de {aspecto_avancado}.",
                "Considerando sua experiência, vamos abordar {tema} de forma mais técnica."
            ],
            'explicacao': [
                "{tema} em nível avançado envolve {conceitos_complexos} e {implementacoes_tecnicas}.",
                "A arquitetura de {tema} considera {fatores_arquiteturais} e {otimizacoes}.",
                "Para dominar {tema}, é crucial entender {principios_avancados}."
            ],
            'exemplo': [
                "Em implementações enterprise: {exemplo_empresarial}",
                "Considerando performance e escalabilidade: {otimizacao}",
                "Em arquiteturas complexas: {arquitetura_avancada}"
            ]
        }
        
        # Palavras-chave por domínio para personalização
        self.dominios_conhecimento = {
            'html': {
                'conceito_base': 'uma linguagem de marcação para estruturar páginas web',
                'explicacao_simples': 'você usa tags para organizar o conteúdo de um site',
                'analogia': 'é como o esqueleto de uma casa - define onde cada coisa fica',
                'conceitos_intermediarios': 'semântica, acessibilidade e estruturas complexas',
                'aspectos_tecnicos': 'validação, compatibilidade entre navegadores',
                'aplicacoes': 'desenvolvimento web, criação de sites e aplicações',
                'casos_uso': 'páginas estáticas, formulários, estruturação de conteúdo',
                'conexoes': 'CSS para estilização e JavaScript para interatividade',
                'conceitos_complexos': 'Web Components, Shadow DOM, e performance optimization',
                'aspecto_avancado': 'arquitetura e performance',
                'fatores_arquiteturais': 'semântica, acessibilidade e SEO',
                'otimizacoes': 'minificação, lazy loading e cache',
                'principios_avancados': 'componentização, modularidade e reutilização',
                'implementacoes_tecnicas': 'Web Components e Custom Elements'
            },
            'programação': {
                'conceito_base': 'o processo de criar instruções para computadores',
                'explicacao_simples': 'você escreve código que diz ao computador o que fazer',
                'analogia': 'é como escrever uma receita muito detalhada',
                'conceitos_intermediarios': 'algoritmos, estruturas de dados e padrões',
                'aspectos_tecnicos': 'complexidade, manutenibilidade e testabilidade',
                'aplicacoes': 'desenvolvimento de software, automação e resolução de problemas',
                'casos_uso': 'aplicações web, mobile, desktop e sistemas embarcados',
                'conexoes': 'matemática, lógica e resolução de problemas',
                'conceitos_complexos': 'arquiteturas distribuídas, concorrência e otimização',
                'aspecto_avancado': 'arquitetura de software e escalabilidade',
                'fatores_arquiteturais': 'modularidade, extensibilidade e performance',
                'otimizacoes': 'algoritmos eficientes, estruturas de dados adequadas',
                'principios_avancados': 'SOLID, design patterns e clean architecture',
                'implementacoes_tecnicas': 'microserviços, containers e cloud computing'
            }
        }
    
    def extrair_conceitos_chave(self, conteudo_original: Optional[str]) -> Dict[str, Any]:
        """
        Extrai conceitos-chave do conteúdo original para usar nos templates.
        
        Args:
            conteudo_original (Optional[str]): Conteúdo de referência para extração
        Returns:
            Dict[str, Any]: Dicionário com conceitos extraídos (frases, exemplos, definições)
        """
        if not conteudo_original:
            return {}
        
        # Remove HTML tags se existirem
        texto_limpo = re.sub(r'<[^>]+>', '', conteudo_original)
        
        # Extrai frases importantes (simplificado)
        frases = [f.strip() for f in texto_limpo.split('.') if len(f.strip()) > 20]
        conceitos = {
            'frase_principal': frases[0] if frases else '',
            'exemplos_extraidos': [f for f in frases if 'exemplo' in f.lower() or 'por exemplo' in f.lower()],
            'definicoes': [f for f in frases if 'é' in f or 'são' in f]
        }
        
        return conceitos
    
    @log_performance
    def gerar_conteudo_personalizado(self, tema: str, nivel: str, formato: str, 
                                   historico_dificuldades: Optional[List[str]] = None) -> str:
        """
        Gera conteúdo educacional personalizado adaptado ao usuário.
        Args:
            tema (str): Tópico de aprendizagem (ex: 'HTML', 'programação')
            nivel (str): Nível de conhecimento ('iniciante', 'intermediário', 'avançado')
            formato (str): Formato de saída ('Texto', 'PDF', 'Vídeo', 'Exercício')
            historico_dificuldades (Optional[List[str]]): Lista de dificuldades anteriores do usuário
        Returns:
            str: Conteúdo formatado e personalizado
            
        Raises:
            ValidationError: Se parâmetros inválidos forem fornecidos
        """
        # Valida parâmetros de entrada
        try:
            tema, nivel, formato, historico_dificuldades = validate_input_parameters(
                tema, nivel, formato, historico_dificuldades
            )
            self.logger.info(f"Gerando conteúdo: tema={tema}, nivel={nivel}, formato={formato}")
        except ValidationError as e:
            self.logger.error(f"Erro de validação: {e}")
            raise
        
        # Busca conteúdo base existente
        conteudo_base = buscar_conteudo(tema, formato)
        
        # Extrai conceitos do conteúdo base
        conceitos = self.extrair_conceitos_chave(conteudo_base)
        
        # Seleciona templates baseado no nível
        if nivel == 'iniciante':
            templates = self.templates_iniciante
        elif nivel == 'intermediário':
            templates = self.templates_intermediario
        else:
            templates = self.templates_avancado
        
        # Identifica domínio do tema
        dominio = self.identificar_dominio(tema)
        dominio_info = self.dominios_conhecimento.get(dominio, self.dominios_conhecimento['programação'])
        
        # Gera conteúdo dinâmico
        conteudo_gerado = self.montar_conteudo_dinamico(
            tema, templates, dominio_info, conceitos, formato, historico_dificuldades
        )
        
        return conteudo_gerado
    
    def identificar_dominio(self, tema: str) -> str:
        """
        Identifica o domínio do conhecimento baseado no tema.
        
        Args:
            tema (str): Tema a ser classificado
        Returns:
            str: Domínio identificado ('html' ou 'programação')
        """
        tema_lower = tema.lower()
        if any(termo in tema_lower for termo in ['html', 'web', 'css', 'javascript']):
            return 'html'
        return 'programação'
    
    def montar_conteudo_dinamico(self, tema: str, templates: Dict[str, List[str]], 
                               dominio_info: Dict[str, str], conceitos: Dict[str, Any], 
                               formato: str, historico_dificuldades: Optional[List[str]]) -> str:
        """
        Monta o conteúdo dinâmico final combinando templates e informações personalizadas.
        
        Args:
            tema (str): Tema do conteúdo
            templates (Dict[str, List[str]]): Templates organizados por seção
            dominio_info (Dict[str, str]): Informações específicas do domínio
            conceitos (Dict[str, Any]): Conceitos extraídos do conteúdo base
            formato (str): Formato de saída desejado
            historico_dificuldades (Optional[List[str]]): Histórico de dificuldades do usuário
            
        Returns:
            str: Conteúdo dinâmico montado e formatado
        """
        # Seleciona templates aleatórios para variação
        intro_template = random.choice(templates['introducao'])
        explicacao_template = random.choice(templates['explicacao'])
        exemplo_template = random.choice(templates['exemplo'])
        
        # Preenche templates com informações personalizadas
        intro = intro_template.format(tema=tema, **dominio_info)
        
        # Personaliza explicação baseada no domínio
        explicacao = explicacao_template.format(
            tema=tema,
            **dominio_info
        )
        
        # Gera exemplo baseado no formato e conteúdo existente
        exemplo = self.gerar_exemplo_personalizado(tema, formato, conceitos, exemplo_template)
        
        # Adiciona dicas baseadas no histórico de dificuldades
        dica_personalizada = self.gerar_dica_personalizada(historico_dificuldades, tema)
        
        # Monta conteúdo final baseado no formato
        if formato == 'Texto':
            return self.formatar_como_texto(intro, explicacao, exemplo, dica_personalizada)
        elif formato == 'PDF':
            return self.formatar_como_pdf(intro, explicacao, exemplo, dica_personalizada)
        elif formato == 'Vídeo':
            return self.formatar_como_roteiro_video(intro, explicacao, exemplo, dica_personalizada)
        elif formato == 'Exercício':
            return self.gerar_exercicio_dinamico(tema, explicacao, exemplo)
        else:
            return self.formatar_como_texto(intro, explicacao, exemplo, dica_personalizada)
    
    def gerar_exemplo_personalizado(self, tema, formato, conceitos, template):
        """Gera exemplos personalizados baseados no tema e formato"""
        exemplos_por_tema = {
            'html': [
                'criar um cabeçalho com <h1>Meu Site</h1>',
                'fazer uma lista com <ul><li>Item 1</li><li>Item 2</li></ul>',
                'inserir um link com <a href="https://exemplo.com">Clique aqui</a>'
            ],
            'programação': [
                'um loop que conta de 1 a 10',
                'uma função que calcula a média de números',
                'um algoritmo que ordena uma lista'
            ]
        }
        
        dominio = self.identificar_dominio(tema)
        exemplos_disponiveis = exemplos_por_tema.get(dominio, exemplos_por_tema['programação'])
        exemplo_escolhido = random.choice(exemplos_disponiveis)
        
        # Usa as chaves disponíveis no template baseadas no que encontra
        if 'exemplo_pratico' in template:
            return template.format(exemplo_pratico=exemplo_escolhido)
        elif 'exemplo_intermediario' in template:
            return template.format(exemplo_intermediario=exemplo_escolhido)
        elif 'aplicacao_pratica' in template:
            return template.format(aplicacao_pratica=exemplo_escolhido)
        elif 'exemplo_avancado' in template:
            return template.format(exemplo_avancado=exemplo_escolhido)
        else:
            # Fallback simples
            return f"Por exemplo: {exemplo_escolhido}"
    
    def gerar_dica_personalizada(self, historico_dificuldades, tema):
        """Gera dicas baseadas no histórico de dificuldades do usuário"""
        if not historico_dificuldades:
            return f"\nDica: Pratique {tema} regularmente para fixar melhor o conhecimento!"
        
        dicas_genericas = [
            f"\nDica personalizada: Pratique {tema} criando pequenos projetos.",
            f"\nLembre-se: {tema} fica mais fácil com a prática constante.",
            f"\nSugestão: Tente explicar {tema} para alguém - isso ajuda a consolidar o aprendizado."
        ]
        
        return random.choice(dicas_genericas)
    
    def formatar_como_texto(self, intro, explicacao, exemplo, dica):
        """Formata o conteúdo como texto estruturado"""
        return f"""{intro}

{explicacao}

{exemplo}

{dica}

Continue praticando para dominar este conceito!"""
    
    def formatar_como_pdf(self, intro, explicacao, exemplo, dica):
        """Formata o conteúdo simulando um material PDF estruturado"""
        return f"""MATERIAL DE ESTUDO PERSONALIZADO

INTRODUÇÃO:
{intro}

CONCEITOS PRINCIPAIS:
{explicacao}

EXEMPLO PRÁTICO:
{exemplo}

{dica}

PRÓXIMOS PASSOS:
- Pratique os conceitos apresentados
- Busque exemplos adicionais
- Aplique em projetos próprios"""
    
    def formatar_como_roteiro_video(self, intro, explicacao, exemplo, dica):
        """Formata o conteúdo como roteiro de vídeo educativo"""
        return f"""ROTEIRO DE VÍDEO EDUCATIVO PERSONALIZADO

[ABERTURA]
{intro}

[DESENVOLVIMENTO]
{explicacao}

[DEMONSTRAÇÃO PRÁTICA]
{exemplo}

[DICA ESPECIAL]
{dica}

[ENCERRAMENTO]
Isso é tudo por hoje! Continue praticando e nos vemos no próximo conteúdo!"""
    
    def gerar_exercicio_dinamico(self, tema, explicacao, exemplo):
        """Gera exercícios dinâmicos baseados no tema"""
        exercicios_por_tema = {
            'html': [
                "Crie uma página HTML com um título e três parágrafos.",
                "Implemente uma lista não ordenada com 5 itens sobre HTML.",
                "Desenvolva um formulário simples com nome e email."
            ],
            'programação': [
                "Escreva um algoritmo que encontre o maior número em uma lista.",
                "Crie uma função que calcule o fatorial de um número.",
                "Implemente um contador que mostre números pares de 0 a 20."
            ]
        }
        
        dominio = self.identificar_dominio(tema)
        exercicios = exercicios_por_tema.get(dominio, exercicios_por_tema['programação'])
        exercicio_escolhido = random.choice(exercicios)
        return f"""EXERCÍCIO PRÁTICO PERSONALIZADO

CONCEITO:
{explicacao}

DESAFIO:
{exercicio_escolhido}

OBJETIVO:
Aplicar na prática os conceitos que você acabou de aprender sobre {tema}.

DICA:
Comece simples e vá aumentando a complexidade gradualmente!"""

# Instância global para uso no sistema
gerador_conteudo = GeradorConteudoDinamico()
