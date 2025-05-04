import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, scrolledtext, messagebox,simpledialog,BitmapImage,PhotoImage
import pandas as pd
import tabula 
from pdf2docx import Converter
from pdf2image import convert_from_path
import os
import io 
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.lib.colors import black
from reportlab.lib.pagesizes import A4
from PyPDF2 import PageObject
import fitz
from PIL import Image


class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("PDF Manager - Projeto Profissional")
        self.root.geometry("900x600")
        self.root.resizable(False, False)


        icon_path = os.path.join(os.path.dirname(__file__), "assets", "lelerpdf.png")
        if os.path.exists(icon_path):
            icon = PhotoImage(file=icon_path)
            self.root.iconphoto(False, icon)
        else:
            print(f"[ERRO] Ícone não encontrado em: {icon_path}")


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

        self.frame_principal = ttk.Frame(self.root, padding=12)
        self.frame_principal.pack(expand=True, fill='both')

        self.label = ttk.Label(self.frame_principal, text="Escolha uma ação abaixo:", font=("Arial", 25),padding=15)
        self.label.pack(pady=12)

        self.frame_botoes = ttk.Frame(self.frame_principal)
        self.frame_botoes.pack(pady=20)

        # Criando botões
        self._criar_botao("➕ Juntar PDFs", self._acao_juntar, 0, 0)                 
        self._criar_botao("🧩 Separar Páginas", self._acao_separar, 0, 1)         
        self._criar_botao("📖 Ler PDF", self._acao_ler, 1, 0)                     
        self._criar_botao("📝 PDF para Word", self._acao_word, 1, 1)                
        self._criar_botao("📊 PDF para Excel", self._acao_excel, 2, 0)             
        self._criar_botao("🖼️ Extrair imagem do PDF", self._acao_extrair_imagem, 2, 1)                 
        self._criar_botao("🔢 Enumerar Páginas", self.adiciona_numeros_pdf, 3, 0)  
        self._criar_botao("📤 Extrair Páginas", self._acao_extrair_paginas, 3, 1)          

    def _criar_botao(self, texto, comando, linha, coluna):
        """Cria e posiciona um botão"""
        botao = tk.Button(self.frame_botoes, text=texto, command=comando, width=30,height=2,
                  bg="#4CAF50", fg="white", activebackground="#45a049",
                  font=("Arial", 16, "bold"))
        botao.grid(row=linha, column=coluna, padx=10, pady=10)
        

    # Funções de exemplo para cada botão

    def _acao_juntar(self):
        """Seleciona multiplos PDFs e Junta  em um arquivo"""
        arquivos = filedialog.askopenfilenames(title="Selecione os arquivos PDF", filetypes=[("Arquivos PDF","*.pdf")], multiple=True)
        if not arquivos:
            return
        try:
            merger = PdfMerger()
            for pdf in arquivos:
                merger.append(pdf)
            salvar_como = filedialog.asksaveasfilename(title="Salvar PDF unificado",defaultextension=".pdf", filetypes=[("Arquivos PDF","*.pdf"),])
            if salvar_como:
                merger.write(salvar_como)
                merger.close()
            messagebox.showinfo("Sucesso",f"PDF salvo com sucesso:\n{salvar_como}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao juntar PDFs:\n{e}")
        
    def _acao_separar(self):
        """Separar cada página do PDF de um arquivo"""
        caminho_pdf = filedialog.askopenfilename(title="Selecione o arquivo PDF",filetypes=[("Arquivos PDF", "*.pdf")])
        if not caminho_pdf:
            return
        pasta_destino = filedialog.askdirectory(title="Selecione a pasta para salvar as páginas.")
        if not pasta_destino:
            return
        
        try:
            leitor = PdfReader(caminho_pdf)
            for i, pagina in enumerate(leitor.pages):
                escritor = PdfWriter()
                escritor.add_page(pagina)
                nome_arquivo = f"página_{i}.pdf"
                caminho_completo = f"{pasta_destino}/{nome_arquivo}"
                with open(caminho_completo,"wb") as arquivo_saida:
                    escritor.write(arquivo_saida)
            messagebox.showinfo("Sucesso", f"PDF separado com sucesso!\nPaginas salvas{pasta_destino}")
        except Exception as e:
            messagebox.showerror("Erro as separar PDF:\n{e}")



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
        """Converte PDF para word (.docx)"""
        caminho_pdf = filedialog.askopenfilename(title="Selecione o PDF", filetypes=[("Arquivos PDF", "*.pdf")])
        if not caminho_pdf:
            return
        salvar_como = filedialog.asksaveasfilename(title="Salva como word", defaultextension=".docx",filetypes=[("Documento WOrd", "*.docx")])
        if not salvar_como:
            return 
        try:
            converter = Converter(caminho_pdf)
            converter.convert(salvar_como,start=0,end=None)
            converter.close()
            messagebox.showinfo("SUcesso", f"PDF convertido com sucesso para:\n{salvar_como}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao converte PDF para word: \n{e}")
           


    def _acao_excel(self):
        """Extrai tabelas do PDF e salva como Excel (.xlsx)"""
        caminho_pdf = filedialog.askopenfilename(
            title="Selecione o PDF com tabelas",
            filetypes=[("Arquivos PDF", "*.pdf")]
        )

        if not caminho_pdf:
            return

        salvar_como = filedialog.asksaveasfilename(
            title="Salvar como Excel",
            defaultextension=".xlsx",
            filetypes=[("Planilha Excel", "*.xlsx")]
        )

        if not salvar_como:
            return

        try:
            # extração de todas as tabelas
            tabelas = tabula.read_pdf(caminho_pdf, pages='all', multiple_tables=True)

            if not tabelas:
                messagebox.showwarning("Aviso", "Nenhuma tabela encontrada no PDF.")
                return

            with pd.ExcelWriter(salvar_como, engine='openpyxl') as writer:
                for i, tabela in enumerate(tabelas):
                    tabela.to_excel(writer, sheet_name=f'Tabela_{i+1}', index=False)

            messagebox.showinfo("Sucesso", f"Tabelas salvas em:\n{salvar_como}")

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao converter PDF para Excel:\n{e}")
                                    
    def _acao_extrair_imagem(self):
        """Extrai imagens JPG de um PDF e salva em uma pasta"""
        arquivo_pdf = filedialog.askopenfilename(title="Selecione o PDF",filetypes=[("Arquivos PDF", "*.pdf")])

        if not arquivo_pdf:
            return

        pasta_destino = filedialog.askdirectory(title="Escolha a pasta para salvar as imagens")
        if not pasta_destino:
            return

        try:
            doc = fitz.open(arquivo_pdf)
            count = 0

            for i, pagina in enumerate(doc):
                imagens = pagina.get_images(full=True)
                for img_index, img in enumerate(imagens):
                    xref = img[0]
                    base_image = doc.extract_image(xref)
                    imagem_bytes = base_image["image"]
                    imagem_pil = Image.open(io.BytesIO(imagem_bytes))

                    nome_arquivo = f"pagina{i+1}_img{img_index+1}.jpg"
                    caminho_completo = os.path.join(pasta_destino, nome_arquivo)
                    imagem_pil.save(caminho_completo, "JPEG")
                    count += 1

            if count == 0:
                messagebox.showinfo("Resultado", "Nenhuma imagem encontrada no PDF.")
            else:
                messagebox.showinfo("Sucesso", f"{count} imagens salvas com sucesso em:\n{pasta_destino}")

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao extrair imagens:\n{e}")



    def adiciona_numeros_pdf(self):
        """adiciona numeração de página em pdf"""
        caminho_pdf = filedialog.askopenfilename(title="Selecione o arquivo", filetypes=[("Arquivo PDF", "*.pdf")])
        if not caminho_pdf:
            return
        
        salvar_pdf = filedialog.asksaveasfilename(defaultextension=".pdf",filetypes=[("Arquivo PDF","*.pdf")],title="Salvar PDF com numeração")
        if not salvar_pdf:
            return
        
        try:   
            leitor = PdfReader(caminho_pdf)
            escritor = PdfWriter()
            total_paginas = len(leitor.pages)

            for numero, pagina in enumerate(leitor.pages, start=1):
                largura = float(pagina.mediabox.width)
                altura = float(pagina.mediabox.height)
                                
                packet = io.BytesIO()
                can = canvas.Canvas(packet, pagesize=(largura,altura))
                can.setFont("Helvetica", 12)
                can.setFillColor(black)

                texto = f"{numero} / {total_paginas}"
                can.drawString(largura-100, 20,texto)
                can.save()

                packet.seek(0)
                overlay= PdfReader(packet).pages[0]
                pagina.merge_page(overlay)

                escritor.add_page(pagina)

            with open(salvar_pdf,"wb") as saida:
                escritor.write(saida)
            messagebox.showinfo("Sucesso", "PDF numeração com sucesso!")

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao adicionar numeração:\n {e}")
    

    def _acao_extrair_paginas(self):
        """Extrai páginas específicas de um PDF"""
        caminho_pdf = filedialog.askopenfilename(title="Selecione o PDF",filetypes=[("Arquivos PDF", "*.pdf")])
        if not caminho_pdf:
            return

        entrada = simpledialog.askstring("Páginas","Digite as páginas que deseja extrair (ex: 1,3,5-7):")
        if not entrada:
            return

        salvar_pdf = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("Arquivos PDF", "*.pdf")],
            title="Salvar páginas extraídas"
        )
        if not salvar_pdf:
            return

        try:
            leitor = PdfReader(caminho_pdf)
            escritor = PdfWriter()
            total_paginas = len(leitor.pages)

            # Processar entrada do usuário
            paginas = set()
            for parte in entrada.split(','):
                if '-' in parte:
                    inicio, fim = map(int, parte.split('-'))
                    paginas.update(range(inicio, fim + 1))
                else:
                    paginas.add(int(parte))

            paginas_validas = [p for p in paginas if 1 <= p <= total_paginas]
            if not paginas_validas:
                messagebox.showwarning("Aviso", "Nenhuma página válida foi informada.")
                return

            for i in sorted(paginas_validas):
                escritor.add_page(leitor.pages[i - 1])

            with open(salvar_pdf, "wb") as saida:
                escritor.write(saida)

            messagebox.showinfo("Sucesso", f"Páginas extraídas e salvas em:\n{salvar_pdf}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao extrair páginas:\n{e}")  
        

    def run(self):
        self.root.mainloop()
