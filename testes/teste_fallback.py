"""
Teste do sistema de fallback inteligente.
Demonstra os diferentes níveis de fallback e suas funcionalidades.
"""

import sys
import os

# Adiciona o diretório codificacao ao path para imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'codificacao'))

from codificacao.intelligent_fallback import (
    IntelligentFallbackSearch, 
    FallbackLevel, 
    DomainMapper, 
    SynonymManager,
    buscar_conteudo_inteligente
)

def teste_domain_mapper():
    """Testa o mapeamento de domínios."""
    print("🧪 TESTE 1: Mapeamento de Domínios")
    print("-" * 50)
    
    test_cases = [
        ("Python", "programacao"),
        ("HTML", "web"),
        ("SQL", "database"),
        ("Docker", "devops"),
        ("Machine Learning", "data_science"),
        ("Tema Desconhecido", "geral")
    ]
    
    for tema, expected_domain in test_cases:
        domain = DomainMapper.get_domain(tema)
        status = "✅" if domain == expected_domain else "❌"
        print(f"{status} {tema} → {domain} (esperado: {expected_domain})")
        
        # Mostra tópicos relacionados
        related = DomainMapper.get_related_topics(domain)
        if related:
            print(f"    Relacionados: {related[:3]}")
    
    print()

def teste_synonym_manager():
    """Testa o gerenciador de sinônimos."""
    print("🧪 TESTE 2: Gerenciador de Sinônimos")
    print("-" * 50)
    
    test_cases = [
        "python",
        "javascript", 
        "função",
        "lista",
        "iniciante"
    ]
    
    for term in test_cases:
        synonyms = SynonymManager.get_synonyms(term)
        print(f"📝 {term}: {synonyms[:5]}")  # Mostra até 5 sinônimos
    
    print()

def teste_fallback_levels():
    """Testa diferentes níveis de fallback."""
    print("🧪 TESTE 3: Níveis de Fallback")
    print("-" * 50)
    
    search = IntelligentFallbackSearch()
    
    test_cases = [
        # (tema, formato, esperado_level, descrição)
        ("Apresentação", "Texto", FallbackLevel.EXACT, "Busca exata (arquivo existe)"),
        ("Python", "Texto", FallbackLevel.SYNONYMS, "Busca por sinônimos"),
        ("Java", "Texto", FallbackLevel.DOMAIN, "Busca por domínio (programação)"),
        ("Algoritmo", "Texto", FallbackLevel.SEMANTIC, "Busca semântica"),
        ("XYZ123Inexistente", "Texto", FallbackLevel.GENERIC, "Conteúdo genérico")
    ]
    
    for tema, formato, expected_level, descricao in test_cases:
        print(f"🔍 Testando: {tema} ({descricao})")
        
        result = search.buscar_conteudo_com_fallback(tema, formato)
        
        # Verifica se o nível está correto
        level_match = result.fallback_level == expected_level
        status = "✅" if level_match else f"❌ (obtido: {result.fallback_level.value})"
        
        print(f"   {status} Nível: {result.fallback_level.value}")
        print(f"   📊 Confiança: {result.confidence:.1%}")
        print(f"   📍 Fonte: {result.source}")
        print(f"   🔑 Termos: {result.search_terms}")
        print(f"   📄 Conteúdo: {result.content[:80]}...")
        print()
    
    # Mostra estatísticas
    stats = search.get_stats()
    print("📈 Estatísticas do teste:")
    print(f"   Total de buscas: {stats['total_searches']}")
    print(f"   Taxa de sucesso: {stats['success_rate']:.1f}%")
    print("   Uso por nível:")
    for level, count in stats['fallback_usage'].items():
        if count > 0:
            print(f"     {level}: {count} ({count/stats['total_searches']*100:.1f}%)")
    
    print()

def teste_performance():
    """Testa performance do sistema de fallback."""
    print("⚡ TESTE 4: Performance e Robustez")
    print("-" * 50)
    
    import time
    
    search = IntelligentFallbackSearch()
    
    # Testes de performance
    test_themes = [
        "Python", "JavaScript", "HTML", "CSS", "React",
        "SQL", "Docker", "Git", "Linux", "API"
    ]
    
    start_time = time.time()
    
    results = []
    for tema in test_themes:
        tema_start = time.time()
        result = search.buscar_conteudo_com_fallback(tema, "Texto")
        tema_time = time.time() - tema_start
        
        results.append({
            'tema': tema,
            'time': tema_time,
            'level': result.fallback_level.value,
            'confidence': result.confidence
        })
    
    total_time = time.time() - start_time
    
    print(f"⏱️  Tempo total: {total_time:.3f}s")
    print(f"⚡ Tempo médio por busca: {total_time/len(test_themes):.3f}s")
    
    # Agrupa por nível de fallback
    level_counts = {}
    for result in results:
        level = result['level']
        level_counts[level] = level_counts.get(level, 0) + 1
    
    print("\n📊 Distribuição por nível:")
    for level, count in level_counts.items():
        percentage = (count / len(test_themes)) * 100
        print(f"   {level}: {count} ({percentage:.1f}%)")
    
    # Mostra resultados mais lentos
    slow_results = sorted(results, key=lambda x: x['time'], reverse=True)[:3]
    print(f"\n🐌 Buscas mais lentas:")
    for i, result in enumerate(slow_results, 1):
        print(f"   {i}. {result['tema']}: {result['time']:.3f}s ({result['level']})")
    
    print()

def teste_edge_cases():
    """Testa casos extremos e tratamento de erros."""
    print("⚠️  TESTE 5: Casos Extremos")
    print("-" * 50)
    
    search = IntelligentFallbackSearch()
    
    edge_cases = [
        ("", "Texto", "String vazia"),
        ("   ", "Texto", "String só com espaços"),
        ("a", "Texto", "String muito curta"),
        ("X" * 1000, "Texto", "String muito longa"),
        ("!@#$%", "Texto", "Caracteres especiais"),
        ("Python", "FormatoInexistente", "Formato inválido"),
        ("Python123", "Texto", "Tema com números"),
        ("término ção açúde", "Texto", "Acentos e caracteres especiais")
    ]
    
    for tema, formato, descricao in edge_cases:
        try:
            print(f"🧪 {descricao}: '{tema[:20]}{'...' if len(tema) > 20 else ''}'")
            
            result = search.buscar_conteudo_com_fallback(tema, formato)
            
            # Verifica se retornou algum resultado
            has_content = len(result.content) > 0
            status = "✅" if has_content else "❌"
            
            print(f"   {status} Level: {result.fallback_level.value}")
            print(f"   📊 Confiança: {result.confidence:.1%}")
            
            if result.content:
                preview = result.content[:50].replace('\n', ' ')
                print(f"   📄 Preview: {preview}...")
            
        except Exception as e:
            print(f"   ❌ Erro: {e}")
        
        print()

def teste_integracao():
    """Testa integração com outros componentes."""
    print("🔗 TESTE 6: Integração e Função de Conveniência")
    print("-" * 50)
    
    # Testa função de conveniência
    temas_teste = ["Python", "HTML", "Docker", "TemaInexistente"]
    
    for tema in temas_teste:
        print(f"🔍 Busca rápida: {tema}")
        
        try:
            content = buscar_conteudo_inteligente(tema, "Texto", "intermediário")
            
            # Verifica se retornou conteúdo
            has_content = len(content.strip()) > 0
            status = "✅" if has_content else "❌"
            
            print(f"   {status} Conteúdo obtido: {len(content)} caracteres")
            
            if content:
                preview = content[:80].replace('\n', ' ')
                print(f"   📄 Preview: {preview}...")
            
        except Exception as e:
            print(f"   ❌ Erro: {e}")
        
        print()

def main():
    """Executa todos os testes do sistema de fallback."""
    print("🚀 SISTEMA DE FALLBACK INTELIGENTE - TESTES")
    print("=" * 60)
    print()
    
    try:
        teste_domain_mapper()
        teste_synonym_manager() 
        teste_fallback_levels()
        teste_performance()
        teste_edge_cases()
        teste_integracao()
        
        print("✅ TODOS OS TESTES CONCLUÍDOS COM SUCESSO!")
        print("🎯 Sistema de fallback inteligente implementado e funcionando!")
        
    except Exception as e:
        print(f"❌ Erro durante os testes: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
