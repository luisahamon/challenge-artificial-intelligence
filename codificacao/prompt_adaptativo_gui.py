import tkinter as tk
from tkinter import messagebox, filedialog
from sklearn.cluster import KMeans
import numpy as np
from sentence_transformers import SentenceTransformer
import warnings
from functools import lru_cache
from typing import Dict, List, Tuple, Optional

# Configuração única de warnings
warnings.filterwarnings("ignore", category=FutureWarning)

from .utils import buscar_conteudo
from .db import check_db_or_exit
from .gerador_conteudo import gerador_conteudo

check_db_or_exit()

class PromptAdaptativoGUI:
    """GUI otimizada para prompt adaptativo com IA e ML."""
    
    # Class variables otimizadas
    historico_respostas: List[List[float]] = []
    historico_textual: List[str] = []
    historico_dificuldades: List[str] = []
    trilhas_sugeridas: List[str] = []
    
    # Lazy loading do modelo
    _modelo_embedding: Optional[SentenceTransformer] = None
    
    # Configurações de tema otimizadas
    TEMAS = {
        'escuro': {'bg': '#222', 'fg': '#eee', 'entry_bg': '#333', 'entry_fg': '#fff'},
        'claro': {'bg': '#f5f5f5', 'fg': '#222', 'entry_bg': '#fff', 'entry_fg': '#222'}
    }
    
    # Constantes
    FORMATOS_VALIDOS = {'Texto', 'PDF', 'Vídeo', 'Imagem', 'Exercício'}
    NIVEIS_VALIDOS = {'iniciante', 'intermediário', 'avançado'}
    
    def __init__(self, master):
        self.master = master
        self.tema_escuro = False
        self.tamanho_fonte = 12
        self.estado = 'inicio'
        self.tema = ''
        self.nivel = ''
        self.formato = ''
        
        # Loading otimizado
        loading = self._show_loading('Carregando modelo de IA...')
        self._setup_gui()
        self._aplicar_tema()
        loading.destroy()
        self._iniciar_dialogo()
    
    @property
    def modelo_embedding(self) -> SentenceTransformer:
        """Lazy loading do modelo para otimizar inicialização."""
        if self._modelo_embedding is None:
            self._modelo_embedding = SentenceTransformer('all-MiniLM-L6-v2')
        return self._modelo_embedding
    
    def _setup_gui(self) -> None:
        """Setup otimizado da GUI com less code."""
        self.frame = tk.Frame(self.master)
        self.frame.pack(fill='both', expand=True)
        
        # Controles compactos
        self.controles_frame = tk.Frame(self.frame)
        self.controles_frame.pack(fill='x', padx=10, pady=(10,0))
        
        # Botões com dispatch otimizado
        botoes_config = [
            ('A+', self._aumentar_fonte, 'left', 3),
            ('A-', self._diminuir_fonte, 'left', 3),
            ('Conteúdo Dinâmico', self._gerar_conteudo_dinamico, 'left', None),
            ('Exportar', self._exportar_historico, 'left', None),
            ('Tema', self._trocar_tema, 'right', None)
        ]
        
        self.botoes = {}
        for texto, comando, lado, width in botoes_config:
            btn = tk.Button(self.controles_frame, text=texto, command=comando)
            if width: btn.config(width=width)
            btn.pack(side=lado, padx=2 if lado == 'left' else 8)
            self.botoes[texto.lower().replace(' ', '_')] = btn
        
        # Área de texto otimizada
        self.text_frame = tk.Frame(self.frame)
        self.text_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.scrollbar = tk.Scrollbar(self.text_frame)
        self.scrollbar.pack(side='right', fill='y')
        
        self.dialogo_text = tk.Text(
            self.text_frame, height=15, width=90, wrap='word', 
            state='disabled', yscrollcommand=self.scrollbar.set
        )
        self.dialogo_text.pack(side='left', fill='both', expand=True)
        self.scrollbar.config(command=self.dialogo_text.yview)
        
        # Input otimizado
        self.input_var = tk.StringVar()
        self.input_entry = tk.Entry(self.frame, textvariable=self.input_var, width=60)
        self.input_entry.pack(padx=10, pady=5, side='left')
        self.input_entry.bind('<Return>', lambda e: self._enviar())
        
        self.enviar_btn = tk.Button(self.frame, text='Enviar', command=self._enviar)
        self.enviar_btn.pack(padx=5, pady=5, side='left')
        
        self.sair_btn = tk.Button(self.frame, text='Sair', command=self.master.quit)
        self.sair_btn.pack(padx=10, pady=5, side='right')
    
    def _aplicar_tema(self) -> None:
        """Aplicação otimizada de tema com dispatch pattern."""
        tema_config = self.TEMAS['escuro' if self.tema_escuro else 'claro']
        fonte = ("Arial", self.tamanho_fonte)
        
        # Widgets principais com configuração batch
        widgets_principais = [
            (self.frame, {'bg': tema_config['bg']}),
            (self.dialogo_text, {
                'bg': tema_config['bg'], 'fg': tema_config['fg'], 
                'insertbackground': tema_config['fg'], 'font': fonte
            }),
            (self.input_entry, {
                'bg': tema_config['entry_bg'], 'fg': tema_config['entry_fg'],
                'insertbackground': tema_config['entry_fg'], 'font': fonte
            })
        ]
        
        # Botões com configuração uniforme
        config_botao = {
            'bg': tema_config['bg'], 'fg': tema_config['fg'],
            'activebackground': tema_config['entry_bg'], 'font': fonte
        }
        
        # Aplicação otimizada
        for widget, config in widgets_principais:
            widget.config(**config)
        
        # Todos os botões de uma vez
        for btn in [self.enviar_btn, self.sair_btn] + list(self.botoes.values()):
            btn.config(**config_botao)
    
    def _show_loading(self, msg: str = 'Carregando...') -> tk.Toplevel:
        """Loading dialog otimizado."""
        loading = tk.Toplevel(self.master)
        loading.title('Aguarde')
        loading.geometry('300x80')
        loading.transient(self.master)
        loading.grab_set()
        tk.Label(loading, text=msg, font=('Arial', 12)).pack(pady=20)
        self.master.update()
        return loading

    def _aumentar_fonte(self) -> None:
        """Aumenta fonte de forma otimizada."""
        if self.tamanho_fonte < 28:
            self.tamanho_fonte += 2
            self._aplicar_tema()

    def _diminuir_fonte(self) -> None:
        """Diminui fonte de forma otimizada."""
        if self.tamanho_fonte > 8:
            self.tamanho_fonte -= 2
            self._aplicar_tema()

    def _trocar_tema(self) -> None:
        """Troca tema de forma otimizada."""
        self.tema_escuro = not self.tema_escuro
        self._aplicar_tema()

    def _exportar_historico(self) -> None:
        """Exportação otimizada do histórico."""
        historico = self.dialogo_text.get('1.0', 'end').strip()
        if not historico:
            messagebox.showinfo('Exportar', 'Não há histórico para exportar.')
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension='.txt',
            filetypes=[('Arquivo de texto', '*.txt')],
            title='Salvar histórico'
        )
        
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(historico)
            messagebox.showinfo('Exportar', f'Histórico salvo em {file_path}')

    def _gerar_conteudo_dinamico(self) -> None:
        """Geração otimizada de conteúdo dinâmico."""
        if not self.tema:
            messagebox.showinfo(
                'Conteúdo Dinâmico', 
                'Primeiro, inicie uma conversa sobre um tema.'
            )
            return
        
        # Valores padrão otimizados
        nivel = self.nivel or 'intermediário'
        formato = self.formato or 'Texto'
        
        loading = self._show_loading('Gerando conteúdo personalizado...')
        
        try:
            conteudo = gerador_conteudo.gerar_conteudo_personalizado(
                self.tema, nivel, formato, self.historico_dificuldades
            )
            
            loading.destroy()
            self._inserir_dialogo(f'🤖 CONTEÚDO DINÂMICO:\n\n{conteudo}')
            self._inserir_dialogo('O que achou deste conteúdo personalizado?')
            self.estado = 'feedback'
            
        except Exception as e:
            loading.destroy()
            messagebox.showerror('Erro', f'Erro ao gerar conteúdo: {str(e)}')

    def _inserir_dialogo(self, texto: str, usuario: bool = False) -> None:
        """Inserção otimizada no diálogo."""
        self.dialogo_text.config(state='normal')
        prefix = 'Você: ' if usuario else 'Sistema: '
        self.dialogo_text.insert('end', f'{prefix}{texto}\n')
        self.dialogo_text.see('end')
        self.dialogo_text.config(state='disabled')
        
        # Feedback visual otimizado
        if not usuario:
            self.enviar_btn.config(relief='sunken')
            self.master.after(100, lambda: self.enviar_btn.config(relief='raised'))

    def _iniciar_dialogo(self) -> None:
        """Início otimizado do diálogo."""
        self._inserir_dialogo('Olá! Sobre qual tema você gostaria de aprender hoje?')
        self.estado = 'tema'

    @lru_cache(maxsize=32)
    def _detectar_nivel(self, resposta: str) -> str:
        """Detecção otimizada de nível com cache."""
        resposta = resposta.lower()
        
        # Palavras-chave otimizadas por nível
        palavras_iniciante = {'nada', 'não sei', 'nunca ouvi', 'não conheço', 'básico'}
        palavras_intermediario = {'sei', 'conheço', 'já estudei', 'experiência', 'uso'}
        palavras_avancado = {'implemento', 'domino', 'especialista', 'trabalho com'}
        
        # Análise rápida com sets (O(1) lookup)
        if any(palavra in resposta for palavra in palavras_avancado) or len(resposta.split()) > 25:
            return 'avançado'
        elif any(palavra in resposta for palavra in palavras_intermediario):
            return 'intermediário'
        elif any(palavra in resposta for palavra in palavras_iniciante) or len(resposta.split()) < 8:
            return 'iniciante'
        else:
            return 'intermediário'

    def _processar_diagnostico(self, resposta: str) -> None:
        """Processamento otimizado do diagnóstico."""
        self.historico_textual.append(resposta)
        
        # Encoding otimizado com lazy loading
        embeddings = self.modelo_embedding.encode(self.historico_textual)
        
        # Processamento de embeddings otimizado
        emb_media = embeddings.mean(axis=0) if len(embeddings.shape) == 2 else embeddings
        
        # Features otimizadas
        features = [
            float(len(resposta.split())),  # Convert to float
            float(sum(1 for w in ['não sei', 'nunca ouvi', 'básico'] if w in resposta.lower())),
            float(sum(1 for w in ['sei', 'conheço', 'intermediário'] if w in resposta.lower())),
            float(sum(1 for w in ['implemento', 'avançado', 'especialista'] if w in resposta.lower()))
        ] + list(emb_media[:8].astype(float))  # Ensure float type
        
        self.historico_respostas.append(features)
        
        # Detecção de nível otimizada
        if len(self.historico_respostas) >= 3:
            self.nivel = self._detectar_nivel_clustering()
        else:
            self.nivel = self._detectar_nivel(resposta)

    def _detectar_nivel_clustering(self) -> str:
        """Clustering otimizado para detecção de nível."""
        X = np.array(self.historico_respostas)
        kmeans = KMeans(n_clusters=3, n_init=10, random_state=42)
        labels = kmeans.fit_predict(X)
        
        user_label = labels[-1]
        cluster_sizes = [(i, X[labels==i, 0].mean()) for i in range(3)]
        cluster_sizes.sort(key=lambda x: x[1])
        
        cluster_to_nivel = {
            cluster_sizes[0][0]: 'iniciante',
            cluster_sizes[1][0]: 'intermediário', 
            cluster_sizes[2][0]: 'avançado'
        }
        
        return cluster_to_nivel[user_label]

    def _enviar(self) -> None:
        """Método de envio otimizado com dispatcher pattern."""
        entrada = self.input_var.get().strip()
        if not entrada:
            return
            
        self._inserir_dialogo(entrada, usuario=True)
        self.input_var.set('')

        # Dispatcher pattern para estados
        handlers = {
            'tema': self._handle_tema,
            'diagnostico': self._handle_diagnostico,
            'formato': self._handle_formato,
            'verificacao': self._handle_verificacao,
            'feedback': self._handle_feedback,
            'outro_conteudo': self._handle_outro_conteudo,
            'aprofundar': self._handle_aprofundar
        }
        
        handler = handlers.get(self.estado)
        if handler:
            handler(entrada)

    def _handle_tema(self, entrada: str) -> None:
        """Handler otimizado para tema."""
        self.tema = entrada
        self._inserir_dialogo(
            f'Para te ajudar melhor, me conte o que você já sabe sobre "{self.tema}". '
            'Pode ser uma explicação curta ou dizer se nunca ouviu falar.'
        )
        self.estado = 'diagnostico'

    def _handle_diagnostico(self, entrada: str) -> None:
        """Handler otimizado para diagnóstico."""
        self._processar_diagnostico(entrada)
        
        trilha = self._gerar_trilha_aprendizagem(self.nivel)
        if trilha:
            self.trilhas_sugeridas.append(trilha) 
            self._inserir_dialogo(f'Trilha sugerida: {trilha}')
            
        self._inserir_dialogo(
            'Qual formato de conteúdo prefere? (Texto, PDF, Vídeo, Imagem, Exercício)'
        )
        self.estado = 'formato'

    def _handle_formato(self, entrada: str) -> None:
        """Handler otimizado para formato."""
        formato = entrada.capitalize()
        
        # Normalização otimizada
        formato_map = {'Pdf': 'PDF', 'Video': 'Vídeo', 'Exercicio': 'Exercício'}
        formato = formato_map.get(formato, formato)
        
        if formato not in self.FORMATOS_VALIDOS:
            self._inserir_dialogo('Escolha: Texto, PDF, Vídeo, Imagem ou Exercício.')
            return
            
        self.formato = formato
        self._sugerir_conteudo()

    def _handle_verificacao(self, entrada: str) -> None:
        """Handler otimizado para verificação."""
        if entrada.lower() in {'não entendi', 'não sei', 'confuso'}:
            if self.tema not in self.historico_dificuldades:
                self.historico_dificuldades.append(self.tema)
            self._oferecer_conteudo_alternativo()
        else:
            self._inserir_dialogo(
                'Ótimo! Digite "aprofundar", "outro" ou um novo tema.'
            )
            self.estado = 'outro_conteudo'

    def _handle_feedback(self, entrada: str) -> None:
        """Handler otimizado para feedback."""
        if entrada.lower() in {'sim', 'entendi', 'ok', 'obrigado'}:
            self._inserir_dialogo(
                'Digite "outro" para mais conteúdo ou um novo tema para recomeçar.'
            )
            self.estado = 'outro_conteudo'
        else:
            self._inserir_dialogo('Deseja "formato" diferente ou "aprofundar"?')
            self.estado = 'aprofundar'

    def _handle_outro_conteudo(self, entrada: str) -> None:
        """Handler otimizado para outro conteúdo."""
        if entrada.lower() == 'outro':
            self._sugerir_conteudo(aprofundar=True)
        elif entrada.lower() == 'aprofundar':
            self._sugerir_conteudo(aprofundar=True)
            self.estado = 'feedback'
        else:
            self.tema = entrada
            self._inserir_dialogo(
                f'Agora sobre "{self.tema}". O que você já sabe sobre isso?'
            )
            self.estado = 'diagnostico'

    def _handle_aprofundar(self, entrada: str) -> None:
        """Handler otimizado para aprofundar."""
        if entrada.lower() == 'formato':
            self._inserir_dialogo('Qual formato prefere? (Texto, PDF, Vídeo, Imagem, Exercício)')
            self.estado = 'formato'
        elif entrada.lower() == 'aprofundar':
            self._sugerir_conteudo(aprofundar=True)
            self.estado = 'feedback'



    def _sugerir_conteudo(self, aprofundar: bool = False) -> None:
        """Sugestão otimizada de conteúdo."""
        if aprofundar:
            resultado = buscar_conteudo(self.tema, self.formato)
            if resultado and len(resultado) > 1000:
                resultado = resultado[500:2000] + ('...' if len(resultado) > 2000 else '')
            self._inserir_dialogo(f'Conteúdo aprofundado ({self.formato}):\n{resultado}')
            return

        resultado = buscar_conteudo(self.tema, self.formato)
        
        if not resultado or resultado.startswith('Nenhum conteúdo'):
            self._buscar_formatos_alternativos()
            return

        # Truncate otimizado por nível  
        tamanhos = {'iniciante': 1000, 'intermediário': 1500, 'avançado': 2000}
        tamanho = tamanhos.get(self.nivel, 1000)
        
        if len(resultado) > tamanho:
            resultado = resultado[:tamanho] + '...'

        self._inserir_dialogo(f'Conteúdo sugerido ({self.formato}):\n{resultado}')
        self._inserir_dialogo('Dica: Use "Conteúdo Dinâmico" para explicação personalizada!')
        self._inserir_dialogo(
            'Para verificar compreensão: qual o principal conceito acima? '
            '(Ou "não entendi" para explicação diferente)'
        )
        self.estado = 'verificacao'

    def _buscar_formatos_alternativos(self) -> None:
        """Busca otimizada de formatos alternativos."""
        formatos_disponiveis = []
        
        for formato in self.FORMATOS_VALIDOS:
            if formato == self.formato:
                continue
                
            resultado = buscar_conteudo(self.tema, formato)
            if resultado and not resultado.startswith('Nenhum conteúdo'):
                formatos_disponiveis.append(formato)

        if formatos_disponiveis:
            sugestao = ', '.join(formatos_disponiveis)
            self._inserir_dialogo(
                f'Não encontrei em {self.formato}. '
                f'Disponível em: {sugestao}. Qual deseja?'
            )
            self.estado = 'formato'
        else:
            self._inserir_dialogo('Não encontrei conteúdo para esse tema.')

    def _oferecer_conteudo_alternativo(self) -> None:
        """Oferece conteúdo alternativo otimizado."""
        self._inserir_dialogo('Vou gerar explicação dinâmica personalizada!')
        
        try:
            conteudo = gerador_conteudo.gerar_conteudo_personalizado(
                self.tema, self.nivel, 'Texto', self.historico_dificuldades
            )
            
            self._inserir_dialogo(f'🤖 EXPLICAÇÃO ALTERNATIVA:\n\n{conteudo}')
            
            # Busca formato alternativo
            for formato in self.FORMATOS_VALIDOS:
                if formato == self.formato:
                    continue
                    
                resultado = buscar_conteudo(self.tema, formato)
                if resultado and not resultado.startswith('Nenhum conteúdo'):
                    self.formato = formato
                    self._inserir_dialogo(f'Material em {formato}:\n{resultado[:500]}...')
                    break
            
            self._inserir_dialogo('Dúvida? Digite "não entendi". Senão, "ok".')
            
        except Exception as e:
            self._inserir_dialogo(f'Erro: {str(e)}')
            self._buscar_formatos_alternativos()

    @lru_cache(maxsize=16)
    def _gerar_trilha_aprendizagem(self, nivel: str) -> str:
        """Geração otimizada de trilha com cache."""
        trilhas = {
            'iniciante': 'Conceitos básicos → exemplos práticos → exercícios simples',
            'intermediário': 'Casos de uso → exercícios intermediários → vídeos explicativos',
            'avançado': 'Desafios avançados → projetos práticos → referências aprofundadas'
        }
        return trilhas.get(nivel, 'Trilha personalizada baseada no seu perfil')


def main() -> None:
    """Função principal otimizada."""
    root = tk.Tk()
    root.title("Prompt Adaptativo - IA Educacional")
    root.geometry("800x600")
    root.resizable(True, True)
    
    # Configurações de janela otimizadas
    root.minsize(600, 400)
    
    try:
        app = PromptAdaptativoGUI(root)
        root.mainloop()
    except KeyboardInterrupt:
        root.quit()
    except Exception as e:
        messagebox.showerror('Erro Fatal', f'Erro na inicialização: {str(e)}')


if __name__ == '__main__':
    main()
