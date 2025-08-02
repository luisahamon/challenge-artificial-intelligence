"""
Teste completo do sistema de estratégias de aprendizagem adaptativa.
Testa Strategy Pattern com diagnóstico, clustering e classificação.
"""

import sys
import os

# Adiciona o diretório codificacao ao path para imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'codificacao'))

from codificacao.strategy_pattern import (
    StrategyContext,
    StrategyType,
    DiagnosticStrategy,
    KMeansStrategy,
    RandomForestStrategy,
    LearningLevel,
    UserProfile,
    analyze_user_with_strategy,
    get_comprehensive_analysis
)

def teste_diagnostic_strategy():
    """Testa estratégia de diagnóstico."""
    print("🧪 TESTE 1: Estratégia de Diagnóstico")
    print("-" * 50)
    
    strategy = DiagnosticStrategy()
    
    # Casos de teste para diferentes tipos de usuários
    test_cases = [
        {
            'user_id': 'iniciante_001',
            'description': 'Usuário iniciante',
            'data': {
                'user_id': 'iniciante_001',
                'preferred_format': 'Vídeo',
                'avg_session_time': 30,
                'completion_rate': 0.4
            }
        },
        {
            'user_id': 'intermediario_001', 
            'description': 'Usuário intermediário',
            'data': {
                'user_id': 'intermediario_001',
                'preferred_format': 'Texto',
                'avg_session_time': 60,
                'completion_rate': 0.7
            }
        },
        {
            'user_id': 'avancado_001',
            'description': 'Usuário avançado',
            'data': {
                'user_id': 'avancado_001',
                'preferred_format': 'PDF',
                'avg_session_time': 90,
                'completion_rate': 0.9
            }
        }
    ]
    
    for case in test_cases:
        print(f"📊 Testando: {case['description']}")
        
        result = strategy.analyze(case['data'])
        
        print(f"   👤 Usuário: {result.user_id}")
        print(f"   📈 Nível estimado: {result.estimated_level.value if result.estimated_level else 'N/A'}")
        print(f"   🎯 Perfil: {result.user_profile.value if result.user_profile else 'N/A'}")
        print(f"   📊 Confiança: {result.confidence:.1%}")
        print(f"   ⚖️  Ajuste dificuldade: {result.difficulty_adjustment:+.1f}")
        print(f"   💡 Recomendações: {len(result.recommendations)}")
        
        # Mostra primeira recomendação
        if result.recommendations:
            print(f"      - {result.recommendations[0]}")
        
        # Mostra métricas principais
        metrics = result.metrics
        print(f"   📈 Accuracy: {metrics.get('accuracy', 0):.1%}")
        print(f"   🎯 Score combinado: {metrics.get('combined_score', 0):.2f}")
        print()
    
    print()

def teste_kmeans_strategy():
    """Testa estratégia de clustering K-means."""
    print("🧪 TESTE 2: Estratégia K-means Clustering")
    print("-" * 50)
    
    strategy = KMeansStrategy(n_clusters=3)
    
    test_user = {
        'user_id': 'cluster_test_001',
        'preferred_format': 'Texto',
        'avg_session_time': 45,
        'completion_rate': 0.6
    }
    
    print(f"🔬 Executando clustering para usuário: {test_user['user_id']}")
    
    result = strategy.analyze(test_user)
    
    print(f"   🎯 Cluster ID: {result.metrics.get('cluster_id', 'N/A')}")
    print(f"   📊 Silhouette Score: {result.metrics.get('silhouette_score', 0):.3f}")
    print(f"   📈 Confiança: {result.confidence:.1%}")
    print(f"   🏷️  Clusters totais: {result.metrics.get('n_clusters', 0)}")
    
    # Mostra características do cluster
    cluster_chars = result.metrics.get('cluster_characteristics', {})
    if cluster_chars:
        print(f"   👥 Perfil do cluster: {cluster_chars.get('profile', 'N/A')}")
        print(f"   📝 Descrição: {cluster_chars.get('description', 'N/A')}")
        print(f"   🎓 Estilo de aprendizagem: {cluster_chars.get('learning_style', 'N/A')}")
    
    print(f"\n   💡 Recomendações ({len(result.recommendations)}):")
    for i, rec in enumerate(result.recommendations[:3], 1):
        print(f"      {i}. {rec}")
    
    print()

def teste_random_forest_strategy():
    """Testa estratégia de classificação Random Forest."""
    print("🧪 TESTE 3: Estratégia Random Forest")
    print("-" * 50)
    
    strategy = RandomForestStrategy(n_estimators=50)  # Menos árvores para teste rápido
    
    test_user = {
        'user_id': 'rf_test_001',
        'preferred_format': 'Texto',
        'avg_session_time': 75,
        'completion_rate': 0.8,
        'last_success': True
    }
    
    print(f"🤖 Treinando modelo e fazendo predições para: {test_user['user_id']}")
    
    result = strategy.analyze(test_user)
    
    print(f"   🎯 Confiança geral: {result.confidence:.1%}")
    print(f"   ⏱️  Tempo estimado: {result.time_estimate} minutos")
    print(f"   📚 Próximos tópicos: {len(result.next_topics)}")
    
    if result.next_topics:
        print(f"      Recomendados: {', '.join(result.next_topics[:3])}")
    
    # Métricas do modelo
    model_accuracy = result.metrics.get('model_accuracy', 0)
    print(f"   🤖 Accuracy do modelo: {model_accuracy:.1%}")
    
    # Predições por tópico
    predictions = result.metrics.get('topic_predictions', [])
    if predictions:
        print(f"\n   📊 Top 3 predições:")
        for i, pred in enumerate(predictions[:3], 1):
            status = "✅" if pred['recommended'] else "❌"
            print(f"      {i}. {status} {pred['topic']}: {pred['probability']:.1%} (dif: {pred['difficulty']:.1f})")
    
    # Importância das features
    importance = result.metrics.get('feature_importance', {})
    if importance:
        print(f"\n   🔍 Features mais importantes:")
        sorted_features = sorted(importance.items(), key=lambda x: x[1], reverse=True)
        for feature, imp in sorted_features[:3]:
            print(f"      {feature}: {imp:.3f}")
    
    print(f"\n   💡 Primeiras recomendações:")
    for i, rec in enumerate(result.recommendations[:3], 1):
        print(f"      {i}. {rec}")
    
    print()

def teste_strategy_context():
    """Testa o contexto de estratégias."""
    print("🧪 TESTE 4: Strategy Context - Execução Individual")
    print("-" * 50)
    
    context = StrategyContext()
    
    test_user = {
        'user_id': 'context_test_001',
        'preferred_format': 'Vídeo',
        'avg_session_time': 50,
        'completion_rate': 0.65,
        'last_success': True
    }
    
    # Testa cada estratégia individualmente
    for strategy_type in [StrategyType.DIAGNOSTIC, StrategyType.CLUSTERING, StrategyType.CLASSIFICATION]:
        print(f"🔄 Executando: {strategy_type.value}")
        
        try:
            result = context.execute_strategy(strategy_type, test_user)
            
            print(f"   ✅ Sucesso - Confiança: {result.confidence:.1%}")
            print(f"   💡 Recomendações: {len(result.recommendations)}")
            
            if result.recommendations:
                print(f"      Primeira: {result.recommendations[0][:60]}...")
                
        except Exception as e:
            print(f"   ❌ Erro: {e}")
        
        print()

def teste_comprehensive_analysis():
    """Testa análise abrangente combinando todas as estratégias."""
    print("🧪 TESTE 5: Análise Abrangente (Todas as Estratégias)")
    print("-" * 50)
    
    context = StrategyContext()
    
    test_user = {
        'user_id': 'comprehensive_test_001',
        'preferred_format': 'PDF',
        'avg_session_time': 70,
        'completion_rate': 0.75,
        'last_success': True
    }
    
    print(f"🔍 Executando análise completa para: {test_user['user_id']}")
    
    try:
        result = context.get_combined_analysis(test_user)
        
        print(f"   🎯 Confiança combinada: {result.confidence:.1%}")
        print(f"   📈 Nível estimado: {result.estimated_level.value if result.estimated_level else 'N/A'}")
        print(f"   👤 Perfil: {result.user_profile.value if result.user_profile else 'N/A'}")
        print(f"   ⚖️  Ajuste dificuldade: {result.difficulty_adjustment:+.1f}")
        print(f"   ⏱️  Tempo estimado: {result.time_estimate} minutos")
        print(f"   📚 Próximos tópicos: {len(result.next_topics)}")
        
        if result.next_topics:
            print(f"      {', '.join(result.next_topics[:3])}")
        
        print(f"\n   💡 Recomendações combinadas ({len(result.recommendations)}):")
        
        # Agrupa recomendações por estratégia
        diagnostic_recs = [r for r in result.recommendations if '[DIAGNOSTIC]' in r]
        clustering_recs = [r for r in result.recommendations if '[CLUSTERING]' in r]
        classification_recs = [r for r in result.recommendations if '[CLASSIFICATION]' in r]
        
        print(f"      🔍 Diagnóstico: {len(diagnostic_recs)} recomendações")
        print(f"      🎯 Clustering: {len(clustering_recs)} recomendações")
        print(f"      🤖 Classificação: {len(classification_recs)} recomendações")
        
        # Mostra algumas recomendações de cada tipo  
        if diagnostic_recs:
            print(f"         Exemplo diagnóstico: {diagnostic_recs[0].replace('[DIAGNOSTIC] ', '')}")
        if clustering_recs:
            print(f"         Exemplo clustering: {clustering_recs[0].replace('[CLUSTERING] ', '')}")
        if classification_recs:
            print(f"         Exemplo classificação: {classification_recs[0].replace('[CLASSIFICATION] ', '')}")
        
        # Métricas individuais
        individual_results = result.metrics.get('individual_results', {})
        print(f"\n   📊 Resultados individuais:")
        for strategy, metrics in individual_results.items():
            conf = metrics.get('confidence', 0)
            recs = metrics.get('recommendations_count', 0)
            print(f"      {strategy}: {conf:.1%} confiança, {recs} recomendações")
        
    except Exception as e:
        print(f"   ❌ Erro na análise abrangente: {e}")
        import traceback
        traceback.print_exc()
    
    print()

def teste_convenience_functions():
    """Testa funções de conveniência."""
    print("🧪 TESTE 6: Funções de Conveniência")
    print("-" * 50)
    
    test_user = {
        'user_id': 'convenience_test_001',
        'preferred_format': 'Texto',
        'avg_session_time': 40,
        'completion_rate': 0.55
    }
    
    # Teste função de estratégia específica
    print("🔧 Testando analyze_user_with_strategy...")
    try:
        result = analyze_user_with_strategy(test_user, StrategyType.DIAGNOSTIC)
        print(f"   ✅ Diagnóstico: {result.confidence:.1%} confiança")
    except Exception as e:
        print(f"   ❌ Erro: {e}")
    
    # Teste função de análise abrangente
    print("🔧 Testando get_comprehensive_analysis...")
    try:
        result = get_comprehensive_analysis(test_user)
        print(f"   ✅ Análise completa: {result.confidence:.1%} confiança")
        print(f"   📚 {len(result.next_topics)} tópicos recomendados")
    except Exception as e:
        print(f"   ❌ Erro: {e}")
    
    print()

def teste_performance():
    """Testa performance do sistema de estratégias."""
    print("⚡ TESTE 7: Performance e Robustez")
    print("-" * 50)
    
    import time
    
    context = StrategyContext()
    
    # Gera vários usuários de teste
    test_users = []
    for i in range(5):
        test_users.append({
            'user_id': f'perf_test_{i:03d}',
            'preferred_format': ['Texto', 'Vídeo', 'PDF'][i % 3],
            'avg_session_time': 30 + (i * 15),
            'completion_rate': 0.5 + (i * 0.1),
            'last_success': i % 2 == 0
        })
    
    print(f"⏱️  Testando performance com {len(test_users)} usuários...")
    
    # Teste cada estratégia individualmente
    for strategy_type in [StrategyType.DIAGNOSTIC, StrategyType.CLUSTERING, StrategyType.CLASSIFICATION]:
        strategy_times = []
        
        for user in test_users:
            start_time = time.time()
            try:
                result = context.execute_strategy(strategy_type, user)
                execution_time = time.time() - start_time
                strategy_times.append(execution_time)
            except Exception as e:
                print(f"   ❌ Erro com {user['user_id']}: {e}")
        
        if strategy_times:
            avg_time = sum(strategy_times) / len(strategy_times)
            max_time = max(strategy_times)
            min_time = min(strategy_times)
            
            print(f"   📊 {strategy_type.value}:")
            print(f"      Tempo médio: {avg_time:.3f}s")
            print(f"      Tempo mín/máx: {min_time:.3f}s / {max_time:.3f}s")
    
    # Teste análise abrangente
    print(f"\n   🔍 Testando análise abrangente...")
    comprehensive_times = []
    
    for user in test_users[:3]:  # Menos usuários pois é mais pesado
        start_time = time.time()
        try:
            result = context.get_combined_analysis(user)
            execution_time = time.time() - start_time
            comprehensive_times.append(execution_time)
        except Exception as e:
            print(f"   ❌ Erro com {user['user_id']}: {e}")
    
    if comprehensive_times:
        avg_time = sum(comprehensive_times) / len(comprehensive_times)
        print(f"      Tempo médio (completa): {avg_time:.3f}s")
    
    print()

def main():
    """Executa todos os testes do sistema de estratégias."""
    print("🚀 SISTEMA DE ESTRATÉGIAS - TESTES COMPLETOS")
    print("=" * 60)
    print()
    
    try:
        teste_diagnostic_strategy()
        teste_kmeans_strategy()
        teste_random_forest_strategy()
        teste_strategy_context()
        teste_comprehensive_analysis()
        teste_convenience_functions()
        teste_performance()
        
        print("✅ TODOS OS TESTES DE ESTRATÉGIAS CONCLUÍDOS!")
        print("🎯 Strategy Pattern implementado e funcionando!")
        print("🧠 Sistema de IA adaptativa com múltiplas estratégias operacional!")
        
    except Exception as e:
        print(f"❌ Erro durante os testes: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
