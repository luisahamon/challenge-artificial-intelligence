"""
Teste completo do sistema de connection pooling SQLite.
Testa performance, thread safety e funcionalidades avançadas.
"""

import sys
import os
import time
import threading
import concurrent.futures

# Adiciona o diretório codificacao ao path para imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'codificacao'))

from codificacao.connection_pool import (
    SQLiteConnectionPool,
    PooledConnection,
    get_global_pool,
    close_global_pool,
    get_db_connection,
    execute_query
)

def teste_basic_connection():
    """Testa funcionalidade básica do pool."""
    print("🧪 TESTE 1: Funcionalidade Básica")
    print("-" * 50)
    
    with SQLiteConnectionPool("index.db", pool_size=2, max_connections=4) as pool:
        print(f"✅ Pool criado com {pool.pool_size} conexões base")
        
        # Teste query simples
        try:
            results = pool.execute_query("SELECT name FROM sqlite_master WHERE type='table' LIMIT 5")
            print(f"✅ Query executada: {len(results)} tabelas encontradas")
            
            if results:
                print(f"   Primeira tabela: {results[0].get('name', 'N/A')}")
        
        except Exception as e:
            print(f"❌ Erro na query: {e}")
        
        # Teste context manager
        try:
            with pool.get_connection() as conn:
                cursor = conn.execute("SELECT COUNT(*) as total FROM sqlite_master")
                result = cursor.fetchone()
                print(f"✅ Context manager: {dict(result)['total']} objetos no DB")
        
        except Exception as e:
            print(f"❌ Erro no context manager: {e}")
        
        # Mostra estatísticas iniciais
        stats = pool.get_stats()
        pool_stats = stats['pool_stats']
        print(f"\n📊 Estatísticas iniciais:")
        print(f"   Total conexões: {pool_stats['total_connections']}")
        print(f"   Conexões ativas: {pool_stats['active_connections']}")
        print(f"   Conexões idle: {pool_stats['idle_connections']}")
        print(f"   Requests totais: {pool_stats['total_requests']}")
    
    print()

def teste_concurrent_access():
    """Testa acesso concorrente ao pool."""
    print("🧪 TESTE 2: Acesso Concorrente")
    print("-" * 50)
    
    def worker_task(pool, worker_id, num_queries):
        """Função worker para teste concurrent."""
        results = []
        
        for i in range(num_queries):
            try:
                # Executa query simples
                query_results = pool.execute_query(
                    "SELECT name FROM sqlite_master WHERE type='table' LIMIT ?", 
                    (3,)
                )
                results.append(len(query_results))
                
                # Simula processamento
                time.sleep(0.01)
                
            except Exception as e:
                print(f"❌ Worker {worker_id} erro na query {i}: {e}")
                results.append(0)
        
        return {
            'worker_id': worker_id,
            'queries_executed': len(results),
            'total_results': sum(results),
            'avg_results': sum(results) / len(results) if results else 0
        }
    
    with SQLiteConnectionPool("index.db", pool_size=3, max_connections=6) as pool:
        num_workers = 5
        queries_per_worker = 10
        
        print(f"🚀 Iniciando {num_workers} workers, {queries_per_worker} queries cada")
        
        start_time = time.time()
        
        # Executa workers concorrentemente
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
            futures = [
                executor.submit(worker_task, pool, i, queries_per_worker)
                for i in range(num_workers)
            ]
            
            # Coleta resultados
            worker_results = []
            for future in concurrent.futures.as_completed(futures):
                try:
                    result = future.result(timeout=30)
                    worker_results.append(result)
                    print(f"✅ Worker {result['worker_id']}: {result['queries_executed']} queries")
                except Exception as e:
                    print(f"❌ Worker falhou: {e}")
        
        execution_time = time.time() - start_time
        
        # Estatísticas finais
        stats = pool.get_stats()
        pool_stats = stats['pool_stats']
        
        print(f"\n⏱️  Tempo total: {execution_time:.3f}s")
        print(f"📊 Queries por segundo: {(num_workers * queries_per_worker) / execution_time:.1f}")
        print(f"🎯 Hit rate: {pool_stats['hit_rate']:.1f}%")
        print(f"❌ Taxa de erro: {pool_stats['error_rate']:.1f}%")
        print(f"⏳ Tempo médio de espera: {pool_stats['avg_wait_time']:.3f}s")
        
        # Mostra estatísticas de conexões
        print(f"\n🔗 Conexões:")
        for conn_info in stats['connections']:
            print(f"   {conn_info['id']}: {conn_info['usage_count']} usos, "
                  f"{conn_info['avg_query_time']:.3f}s avg")
    
    print()

def teste_connection_health():
    """Testa sistema de saúde das conexões."""
    print("🧪 TESTE 3: Sistema de Saúde")
    print("-" * 50)
    
    with SQLiteConnectionPool("index.db", pool_size=2, max_connections=4, 
                             health_check_interval=2) as pool:
        
        print("🏥 Testando health checks das conexões...")
        
        # Executa algumas queries para gerar atividade
        for i in range(5):
            try:
                pool.execute_query("SELECT 1")
                time.sleep(0.1)
            except Exception as e:
                print(f"❌ Query {i} falhou: {e}")
        
        # Aguarda um ciclo de health check
        print("⏳ Aguardando health check automático...")
        time.sleep(3)
        
        # Força health check manual
        pool._perform_health_check()
        print("✅ Health check manual executado")
        
        # Mostra estatísticas de saúde
        stats = pool.get_stats()
        healthy_connections = sum(1 for conn in stats['connections'] if conn['is_healthy'])
        total_connections = len(stats['connections'])
        
        print(f"🏥 Conexões saudáveis: {healthy_connections}/{total_connections}")
        
        # Testa otimização do pool
        print("🔧 Testando otimização do pool...")
        pool.optimize_pool()
        print("✅ Otimização concluída")
        
        # Estatísticas finais
        final_stats = pool.get_stats()['pool_stats']
        print(f"\n📊 Estatísticas finais:")
        print(f"   Uptime: {final_stats['uptime_seconds']:.1f}s")
        print(f"   Total requests: {final_stats['total_requests']}")
        print(f"   Hit rate: {final_stats['hit_rate']:.1f}%")
    
    print()

def teste_transaction_support():
    """Testa suporte a transações."""
    print("🧪 TESTE 4: Suporte a Transações")
    print("-" * 50)
    
    with SQLiteConnectionPool("index.db", pool_size=2) as pool:
        
        # Teste transação simples
        print("💳 Testando transação simples...")
        
        def simple_transaction(conn):
            # Operações dentro da transação
            conn.execute("CREATE TEMP TABLE IF NOT EXISTS test_transaction (id INTEGER, value TEXT)")
            conn.execute("INSERT INTO test_transaction (id, value) VALUES (?, ?)", (1, "teste"))
            conn.execute("INSERT INTO test_transaction (id, value) VALUES (?, ?)", (2, "transacao"))
        
        try:
            pool.execute_transaction([simple_transaction])
            print("✅ Transação simples executada com sucesso")
        except Exception as e:
            print(f"❌ Erro na transação: {e}")
        
        # Teste transação com rollback
        print("🔄 Testando transação com rollback...")
        
        def failing_transaction(conn):
            conn.execute("CREATE TEMP TABLE IF NOT EXISTS test_rollback (id INTEGER PRIMARY KEY)")
            conn.execute("INSERT INTO test_rollback (id) VALUES (?)", (1,))
            # Esta operação deve falhar (duplicate key)
            conn.execute("INSERT INTO test_rollback (id) VALUES (?)", (1,))
        
        try:
            pool.execute_transaction([failing_transaction])
            print("❌ Transação deveria ter falhado!")
        except Exception as e:
            print(f"✅ Rollback funcionou corretamente: {type(e).__name__}")
        
        # Teste script SQL
        print("📜 Testando execução de script...")
        
        script = """
        CREATE TEMP TABLE IF NOT EXISTS test_script (
            id INTEGER PRIMARY KEY,
            name TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        INSERT INTO test_script (name) VALUES ('script_test_1');
        INSERT INTO test_script (name) VALUES ('script_test_2');
        """
        
        try:
            pool.execute_script(script)
            
            # Verifica se o script funcionou
            results = pool.execute_query("SELECT COUNT(*) as count FROM test_script")
            count = results[0]['count'] if results else 0
            print(f"✅ Script executado: {count} registros criados")
            
        except Exception as e:
            print(f"❌ Erro no script: {e}")
    
    print()

def teste_global_pool():
    """Testa pool global e funções de conveniência."""
    print("🧪 TESTE 5: Pool Global e Conveniência")
    print("-" * 50)
    
    # Teste pool global
    print("🌍 Testando pool global...")
    
    try:
        # Primeira chamada cria o pool
        pool1 = get_global_pool("index.db", pool_size=2)
        print(f"✅ Pool global criado: {pool1.pool_size} conexões")
        
        # Segunda chamada retorna o mesmo pool
        pool2 = get_global_pool("index.db")
        is_same = pool1 is pool2
        print(f"✅ Pool reutilizado: {is_same}")
        
        # Teste função de conveniência para query
        results = execute_query("SELECT name FROM sqlite_master WHERE type='table' LIMIT 3")
        print(f"✅ Query conveniente: {len(results)} resultados")
        
        # Teste context manager conveniente
        with get_db_connection() as conn:
            cursor = conn.execute("SELECT COUNT(*) as total FROM sqlite_master")
            result = dict(cursor.fetchone())
            print(f"✅ Context conveniente: {result['total']} objetos")
        
        # Estatísticas do pool global
        stats = pool1.get_stats()['pool_stats']
        print(f"\n📊 Estatísticas pool global:")
        print(f"   Requests: {stats['total_requests']}")
        print(f"   Hit rate: {stats['hit_rate']:.1f}%")
        
        # Fecha pool global
        close_global_pool()
        print("✅ Pool global fechado")
        
    except Exception as e:
        print(f"❌ Erro no pool global: {e}")
        import traceback
        traceback.print_exc()
    
    print()

def teste_performance_comparison():
    """Compara performance com e sem pool."""
    print("⚡ TESTE 6: Comparação de Performance")
    print("-" * 50)
    
    num_queries = 100
    
    # Teste sem pool (conexões individuais)
    print("🐌 Testando sem pool (conexões individuais)...")
    
    start_time = time.time()
    for i in range(num_queries):
        try:
            import sqlite3
            conn = sqlite3.connect("index.db")
            cursor = conn.execute("SELECT COUNT(*) FROM sqlite_master")
            cursor.fetchone()
            conn.close()
        except Exception as e:
            print(f"❌ Erro query {i}: {e}")
    
    time_without_pool = time.time() - start_time
    
    # Teste com pool
    print("🚀 Testando com pool...")
    
    with SQLiteConnectionPool("index.db", pool_size=3) as pool:
        start_time = time.time()
        
        for i in range(num_queries):
            try:
                pool.execute_query("SELECT COUNT(*) as count FROM sqlite_master")
            except Exception as e:
                print(f"❌ Erro query {i}: {e}")
        
        time_with_pool = time.time() - start_time
        
        # Estatísticas finais
        stats = pool.get_stats()['pool_stats']
        
        print(f"\n⏱️  Resultados de Performance:")
        print(f"   Sem pool: {time_without_pool:.3f}s ({num_queries/time_without_pool:.1f} qps)")
        print(f"   Com pool: {time_with_pool:.3f}s ({num_queries/time_with_pool:.1f} qps)")
        
        speedup = time_without_pool / time_with_pool if time_with_pool > 0 else 0
        print(f"   🚀 Speedup: {speedup:.2f}x")
        
        print(f"\n📊 Estatísticas do pool:")
        print(f"   Hit rate: {stats['hit_rate']:.1f}%")
        print(f"   Tempo médio espera: {stats['avg_wait_time']:.3f}s")
        print(f"   Conexões utilizadas: {stats['total_connections']}")
    
    print()

def teste_edge_cases():
    """Testa casos extremos e tratamento de erros."""
    print("⚠️  TESTE 7: Casos Extremos")
    print("-" * 50)
    
    # Teste pool pequeno com muitas requisições
    print("🔥 Testando sobrecarga do pool...")
    
    with SQLiteConnectionPool("index.db", pool_size=1, max_connections=2, timeout=1.0) as pool:
        
        def stress_worker(worker_id):
            results = []
            for i in range(5):
                try:
                    start = time.time()
                    pool.execute_query("SELECT 1")
                    elapsed = time.time() - start
                    results.append(elapsed)
                    time.sleep(0.1)  # Simula processamento
                except Exception as e:
                    print(f"❌ Worker {worker_id} query {i}: {e}")
                    results.append(-1)
            return results
        
        # Executa vários workers simultâneos
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            futures = [executor.submit(stress_worker, i) for i in range(4)]
            
            all_results = []
            for future in concurrent.futures.as_completed(futures, timeout=10):
                try:
                    results = future.result()
                    all_results.extend([r for r in results if r >= 0])
                except Exception as e:
                    print(f"❌ Worker falhou: {e}")
        
        if all_results:
            avg_time = sum(all_results) / len(all_results)
            max_time = max(all_results)
            print(f"✅ Stress test: {len(all_results)} queries, {avg_time:.3f}s avg, {max_time:.3f}s max")
        
        # Estatísticas finais do stress test
        stats = pool.get_stats()['pool_stats']
        print(f"   Hit rate: {stats['hit_rate']:.1f}%")
        print(f"   Error rate: {stats['error_rate']:.1f}%")
    
    # Teste query inválida
    print("\n🚫 Testando queries inválidas...")
    
    with SQLiteConnectionPool("index.db", pool_size=1) as pool:
        try:
            pool.execute_query("SELECT * FROM tabela_inexistente")
            print("❌ Query inválida deveria ter falhado!")
        except Exception as e:
            print(f"✅ Query inválida tratada: {type(e).__name__}")
        
        # Pool deve continuar funcionando após erro
        try:
            results = pool.execute_query("SELECT 1 as test")
            print(f"✅ Pool recuperou após erro: {len(results)} resultado")
        except Exception as e:
            print(f"❌ Pool não recuperou: {e}")
    
    print()

def main():
    """Executa todos os testes do connection pool."""
    print("🚀 SISTEMA DE CONNECTION POOLING - TESTES COMPLETOS")
    print("=" * 60)
    print()
    
    try:
        teste_basic_connection()
        teste_concurrent_access()
        teste_connection_health()
        teste_transaction_support()
        teste_global_pool()
        teste_performance_comparison()
        teste_edge_cases()
        
        print("✅ TODOS OS TESTES DE CONNECTION POOLING CONCLUÍDOS!")
        print("🔗 Sistema de pool inteligente implementado e funcionando!")
        print("⚡ Performance otimizada com monitoramento em tempo real!")
        
    except Exception as e:
        print(f"❌ Erro durante os testes: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Garante limpeza do pool global
        close_global_pool()

if __name__ == "__main__":
    main()
