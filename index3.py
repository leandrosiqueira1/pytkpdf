# === IMPORTAÇÃO DE BIBLIOTECAS ===
import tkinter as tk  # Interface gráfica com Tkinter
from tkinter import filedialog, messagebox  # Diálogos de arquivos e mensagens
from pypdf import PdfWriter, PdfReader  # Leitura e escrita de arquivos PDF
from pdf2image import convert_from_path  # Conversão de PDF em imagem (usada para pré-visualização)
from PIL import Image, ImageTk  # Manipulação e exibição de imagens no Tkinter
from pathlib import Path  # Trabalhar com caminhos de arquivos de forma segura
import os  # Interações com o sistema de arquivos

# === CLASSE PRINCIPAL DO APLICATIVO ===
class PDFMergerApp:
    def __init__(self, root):
        # Configuração da janela principal
        self.root = root
        self.root.title("Juntar PDFs com Prévia")
        self.root.geometry("900x800")

        # Armazenamento interno dos arquivos PDF e suas miniaturas
        self.pdf_files = []         # Lista dos PDFs adicionados
        self.thumbnails = {}        # Dicionário com pré-visualizações (miniaturas)

        # === FRAME ESQUERDO ===
        left_frame = tk.Frame(root)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        self.label = tk.Label(left_frame, text="Arquivos selecionados:")
        self.label.pack()

        self.listbox = tk.Listbox(left_frame, width=50, height=25)
        self.listbox.pack()
        self.listbox.bind("<<ListboxSelect>>", self.show_preview)

        self.add_button = tk.Button(left_frame, text="Adicionar PDFs", command=self.add_pdfs)
        self.add_button.pack(pady=5)

        self.sort_button = tk.Button(left_frame, text="Ordenar (A-Z)", command=self.sort_pdfs)
        self.sort_button.pack(pady=5)

        self.merge_button = tk.Button(left_frame, text="Juntar PDFs", command=self.merge_pdfs)
        self.merge_button.pack(pady=5)

        self.clear_button = tk.Button(left_frame, text="Limpar Lista", command=self.clear_list)
        self.clear_button.pack(pady=5)

        # === FRAME DIREITO ===
        right_frame = tk.Frame(root)
        right_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH, padx=10, pady=10)

        self.preview_label = tk.Label(right_frame, text="Pré-visualização", font=("Arial", 14))
        self.preview_label.pack()

        self.image_label = tk.Label(right_frame)
        self.image_label.pack()

    # === FUNÇÃO PARA ADICIONAR PDFs ===
    def add_pdfs(self):
        files = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])
        for file in files:
            if file not in self.pdf_files:
                self.pdf_files.append(file)
                self.listbox.insert(tk.END, file)
                self.generate_thumbnail(file)

    # === GERAR MINIATURA DA PRIMEIRA PÁGINA DO PDF ===
    def generate_thumbnail(self, file_path):
        try:
            images = convert_from_path(file_path, first_page=1, last_page=1, size=(400, 500))
            img = images[0]
            thumb = ImageTk.PhotoImage(img)
            self.thumbnails[file_path] = thumb
        except Exception as e:
            print(f"Erro ao gerar imagem de prévia: {e}")
            self.thumbnails[file_path] = None

    # === MOSTRAR MINIATURA AO SELECIONAR PDF NA LISTA ===
    def show_preview(self, event):
        selected = self.listbox.curselection()
        if selected:
            index = selected[0]
            file_path = self.pdf_files[index]
            thumb = self.thumbnails.get(file_path)
            if thumb:
                self.image_label.config(image=thumb)
                self.image_label.image = thumb
            else:
                self.image_label.config(text="Prévia indisponível", image="")

    # === ORDENAR OS PDFs POR NOME (A-Z) ===
    def sort_pdfs(self):
        self.pdf_files.sort(key=lambda x: os.path.basename(x).lower())
        self.refresh_listbox()

    # === ATUALIZAR LISTA VISUAL APÓS ORDENAR ===
    def refresh_listbox(self):
        self.listbox.delete(0, tk.END)
        for file in self.pdf_files:
            self.listbox.insert(tk.END, file)

    # === JUNTAR PDFs SELECIONADOS EM UM ÚNICO PDF ===
    def merge_pdfs(self):
        if len(self.pdf_files) < 2:
            messagebox.showwarning("Aviso", "Adicione pelo menos dois arquivos PDF.")
            return

        output_path = filedialog.asksaveasfilename(
            initialdir=str(Path.home() / "Documentos"),
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            title="Salvar PDF combinado como"
        )
        if not output_path:
            return

        writer = PdfWriter()

        try:
            for pdf in self.pdf_files:
                reader = PdfReader(pdf)
                for page in reader.pages:
                    writer.add_page(page)

            with open(output_path, "wb") as out_file:
                writer.write(out_file)

            messagebox.showinfo("Sucesso", f"PDF criado com sucesso:\n{output_path}")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao juntar os PDFs:\n{e}")

    # === LIMPAR LISTA DE PDFs E MINIATURAS ===
    def clear_list(self):
        self.pdf_files = []
        self.thumbnails = {}
        self.listbox.delete(0, tk.END)
        self.image_label.config(image='', text="")

# === EXECUTAR O APP ===
if __name__ == "__main__":
    root = tk.Tk()
    app = PDFMergerApp(root)
    root.mainloop()
