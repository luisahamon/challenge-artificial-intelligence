import os
import py_compile
import sys

def verificar_sintaxe(diretorio):
    """Verifica a sintaxe de todos os arquivos Python em um diretório."""
    erros = []
    sucessos = []
    
    print(f"🔍 VERIFICANDO SINTAXE EM: {diretorio}")
    print("=" * 50)
    
    if not os.path.exists(diretorio):
        print(f"❌ Diretório não encontrado: {diretorio}")
        return erros, sucessos
    
    for arquivo in os.listdir(diretorio):
        if arquivo.endswith('.py'):
            caminho = os.path.join(diretorio, arquivo)
            print(f"📄 Testando: {arquivo}")
            
            try:
                py_compile.compile(caminho, doraise=True)
                print(f"   ✅ OK")
                sucessos.append(arquivo)
            except py_compile.PyCompileError as e:
                print(f"   ❌ ERRO DE SINTAXE: {e}")
                erros.append((arquivo, str(e)))
            except Exception as e:
                print(f"   ⚠️  OUTRO ERRO: {e}")
                erros.append((arquivo, str(e)))
    
    return erros, sucessos

def verificar_importacoes(diretorio):
    """Verifica se as importações funcionam."""
    print(f"\n🔗 VERIFICANDO IMPORTAÇÕES EM: {diretorio}")
    print("=" * 50)
    
    erros_import = []
    
    # Adiciona o diretório ao path temporariamente
    original_path = sys.path.copy()
    sys.path.insert(0, diretorio)
    
    try:
        for arquivo in os.listdir(diretorio):
            if arquivo.endswith('.py') and arquivo != '__init__.py':
                modulo = arquivo[:-3]  # Remove .py
                print(f"📦 Testando importação: {modulo}")
                
                try:
                    __import__(modulo)
                    print(f"   ✅ Importação OK")
                except ImportError as e:
                    print(f"   ❌ ERRO DE IMPORTAÇÃO: {e}")
                    erros_import.append((modulo, str(e)))
                except Exception as e:
                    print(f"   ⚠️  OUTRO ERRO: {e}")
                    erros_import.append((modulo, str(e)))
    finally:
        sys.path = original_path
    
    return erros_import

def main():
    print("🚀 VERIFICAÇÃO COMPLETA DE ERROS")
    print("=" * 60)
    
    # Diretórios para verificar
    diretorios = ['codificacao', 'testes']
    
    todos_erros_sintaxe = []
    todos_sucessos = []
    todos_erros_import = []
    
    for diretorio in diretorios:
        # Verificar sintaxe
        erros_sintaxe, sucessos = verificar_sintaxe(diretorio)
        todos_erros_sintaxe.extend([(diretorio, arquivo, erro) for arquivo, erro in erros_sintaxe])
        todos_sucessos.extend([(diretorio, arquivo) for arquivo in sucessos])
        
        # Verificar importações (apenas para codificacao)
        if diretorio == 'codificacao':
            erros_import = verificar_importacoes(diretorio)
            todos_erros_import.extend([(diretorio, modulo, erro) for modulo, erro in erros_import])
    
    # Relatório final
    print("\n" + "=" * 60)
    print("📊 RELATÓRIO FINAL")
    print("=" * 60)
    
    print(f"✅ Arquivos com sintaxe OK: {len(todos_sucessos)}")
    for diretorio, arquivo in todos_sucessos:
        print(f"   {diretorio}/{arquivo}")
    
    if todos_erros_sintaxe:
        print(f"\n❌ Erros de sintaxe encontrados: {len(todos_erros_sintaxe)}")
        for diretorio, arquivo, erro in todos_erros_sintaxe:
            print(f"   {diretorio}/{arquivo}: {erro}")
    else:
        print(f"\n🎉 Nenhum erro de sintaxe encontrado!")
    
    if todos_erros_import:
        print(f"\n🔗 Erros de importação encontrados: {len(todos_erros_import)}")
        for diretorio, modulo, erro in todos_erros_import:
            print(f"   {diretorio}/{modulo}: {erro}")
    else:
        print(f"\n🎉 Nenhum erro de importação encontrado!")

if __name__ == "__main__":
    main()
