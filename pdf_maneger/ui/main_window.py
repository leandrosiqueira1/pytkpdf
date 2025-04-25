import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, scrolledtext, messagebox
import pdfplumber
from PyPDF2 import PdfMerger 
import pandas as pd
import tabula 
from pdf2docx import Converter
import os



class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("PDF Manager - Projeto Profissional")
        self.root.geometry("900x600")
        self.root.resizable(False, False)

        # self.root.iconbitmap("assets/icon.ico")  # Ativar depois

        self._criar_menu()
        self._configurar_layout()

    def _criar_menu(self):
        """Cria a barra de menu superior"""
        barra_menu = tk.Menu(self.root)

        menu_arquivo = tk.Menu(barra_menu, tearoff=0)
        menu_arquivo.add_command(label="Sair", command=self.root.quit)

        menu_ajuda = tk.Menu(barra_menu, tearoff=0)
        menu_ajuda.add_command(label="Sobre", command=self._mostrar_sobre)

        barra_menu.add_cascade(label="Arquivo", menu=menu_arquivo)
        barra_menu.add_cascade(label="Ajuda", menu=menu_ajuda)

        self.root.config(menu=barra_menu)

    def _mostrar_sobre(self):
        """Abre uma janela de informação"""
        messagebox.showinfo("Sobre", "Projeto Gerenciador de PDFs\nCriado em Python com Tkinter.")

    def _configurar_layout(self):
        """Cria os frames e botões principais"""
        style = ttk.Style(self.root)
        style.theme_use("clam")

        self.frame_principal = ttk.Frame(self.root, padding=10)
        self.frame_principal.pack(expand=True, fill='both')

        self.label = ttk.Label(self.frame_principal, text="Escolha uma ação abaixo:", font=("Arial", 16))
        self.label.pack(pady=10)

        self.frame_botoes = ttk.Frame(self.frame_principal)
        self.frame_botoes.pack(pady=20)

        # Criando botões
        self._criar_botao("📎 Juntar PDFs", self._acao_juntar, 0, 0)
        self._criar_botao("✂️ Separar Páginas", self._acao_separar, 0, 1)
        self._criar_botao("📖 Ler PDF", self._acao_ler, 1, 0)
        self._criar_botao("📝 Converter para Word", self._acao_word, 1, 1)
        self._criar_botao("📊 Converter para Excel", self._acao_excel, 2, 0)

    def _criar_botao(self, texto, comando, linha, coluna):
        """Cria e posiciona um botão"""
        botao = ttk.Button(self.frame_botoes, text=texto, command=comando, width=30)
        botao.grid(row=linha, column=coluna, padx=10, pady=10)

    # Funções de exemplo para cada botão

    def _acao_juntar(self):
             """Seleciona multiplos PDFs e Junta  em um arquivo"""
        arquivos = filedialog.askopenfilename(title="Selecione os arquivos PDF", filetypes=[("*.pdf")], multiple=True)
        if not arquivos:
            return
        try:
            merger = PdfMerger()
            for pdf in arquivos:
                merger.append(pdf)
            salvar_como = filedialog.asksaveasfilename(title="Salvar PDF unificado",defaultextension=".pdf", filetypes=[("Arquivos PDF","*.pdf"),])
        messagebox.showinfo("Sucesso",f"PDF salvo com sucesso:\n"{salva_como})
        

        
    def _acao_separar(self):
        pass


    def _acao_ler(self):
        """Ler o texto de um PDF e mostrar na tela"""
        caminho_pdf = filedialog.askopenfilename(title="Selecione um arquivo em PDF",filetypes=[("Arquivo PDF", "*.pdf")])
        if not caminho_pdf:
            return 
        try:
            texto_extraido = ""
            with pdfplumber.open(caminho_pdf) as pdf:
                for pagina in pdf.pages:
                    texto = pagina.extract_text()
                    if texto:
                        texto_extraido += texto + "\n"
            self._mostrar_texto_pdf(texto_extraido)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao ler pdf: \n{e}")


    def _mostrar_texto_pdf(self,texto):
        """Criar uma nova janela com o texto lido"""
        janela_texto = tk.Toplevel(self.root)
        janela_texto.title("Texto do PDF")
        janela_texto.geometry("1050x920")
        
        area_texto = scrolledtext.ScrolledText(janela_texto, wrap='word', font=("Arial", 12))
        area_texto.pack(expand=True, fill='both' , padx=10, pady=10)
        area_texto.insert('1.0',texto)
        area_texto.config(state='disabled')


    def _acao_word(self):
        messagebox.showinfo("Ação", "Função de conversão para Word em construção.")

    def _acao_excel(self):
        messagebox.showinfo("Ação", "Função de conversão para Excel em construção.")

    def run(self):
        self.root.mainloop()
