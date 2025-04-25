from tkinterdnd2 import DND_FILES, TkinterDnD
import tkinter as tk
from tkinter import filedialog, messagebox
from pypdf import PdfReader, PdfWriter
from pdf2image import convert_from_path
from PIL import Image, ImageTk
from pathlib import Path
import os

class PDFMergerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Juntar PDFs com Prévia e Arrastar")
        self.root.geometry("1000x800")
        self.pdf_files = []
        self.thumbnails = {}
        self.current_page = {}

        # Frame esquerdo
        left_frame = tk.Frame(root)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        self.label = tk.Label(left_frame, text="Arquivos selecionados:")
        self.label.pack()

        self.listbox = tk.Listbox(left_frame, width=50, height=25)
        self.listbox.pack()
        self.listbox.bind("<<ListboxSelect>>", self.show_preview)

        # Habilitar arrastar e soltar
        self.root.drop_target_register(DND_FILES)
        self.root.dnd_bind('<<Drop>>', self.drop_files)

        self.add_button = tk.Button(left_frame, text="Adicionar PDFs", command=self.add_pdfs)
        self.add_button.pack(pady=5)

        self.merge_button = tk.Button(left_frame, text="Juntar PDFs", command=self.merge_pdfs)
        self.merge_button.pack(pady=5)

        self.clear_button = tk.Button(left_frame, text="Limpar Lista", command=self.clear_list)
        self.clear_button.pack(pady=5)

        # Frame direito
        right_frame = tk.Frame(root)
        right_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH, padx=10, pady=10)

        self.preview_label = tk.Label(right_frame, text="Pré-visualização", font=("Arial", 14))
        self.preview_label.pack()

        self.image_label = tk.Label(right_frame)
        self.image_label.pack()

        # Navegação entre páginas
        nav_frame = tk.Frame(right_frame)
        nav_frame.pack(pady=5)

        self.prev_button = tk.Button(nav_frame, text="Página Anterior", command=self.prev_preview_page)
        self.prev_button.grid(row=0, column=0, padx=5)

        self.next_button = tk.Button(nav_frame, text="Próxima Página", command=self.next_preview_page)
        self.next_button.grid(row=0, column=1, padx=5)

    def add_pdfs(self):
        files = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])
        self.process_files(files)

    def drop_files(self, event):
        files = self.root.tk.splitlist(event.data)
        self.process_files(files)

    def process_files(self, files):
        for file in files:
            if file not in self.pdf_files and file.lower().endswith('.pdf'):
                self.pdf_files.append(file)
                self.listbox.insert(tk.END, file)
                self.generate_thumbnails(file)

    def generate_thumbnails(self, file_path):
        try:
            images = convert_from_path(file_path, size=(400, 500))
            thumbs = [ImageTk.PhotoImage(img) for img in images]
            self.thumbnails[file_path] = thumbs
            self.current_page[file_path] = 0
        except Exception as e:
            print(f"Erro ao gerar pré-visualização: {e}")
            self.thumbnails[file_path] = []
            self.current_page[file_path] = 0

    def show_preview(self, event=None):
        selected = self.listbox.curselection()
        if selected:
            index = selected[0]
            file_path = self.pdf_files[index]
            thumbs = self.thumbnails.get(file_path, [])
            current = self.current_page.get(file_path, 0)
            if thumbs:
                current = max(0, min(current, len(thumbs) - 1))
                self.image_label.config(image=thumbs[current])
                self.image_label.image = thumbs[current]
            else:
                self.image_label.config(text="Prévia indisponível", image='')

    def next_preview_page(self):
        selected = self.listbox.curselection()
        if selected:
            index = selected[0]
            file_path = self.pdf_files[index]
            thumbs = self.thumbnails.get(file_path, [])
            if not thumbs:
                return
            self.current_page[file_path] = (self.current_page[file_path] + 1) % len(thumbs)
            self.show_preview()

    def prev_preview_page(self):
        selected = self.listbox.curselection()
        if selected:
            index = selected[0]
            file_path = self.pdf_files[index]
            thumbs = self.thumbnails.get(file_path, [])
            if not thumbs:
                return
            self.current_page[file_path] = (self.current_page[file_path] - 1) % len(thumbs)
            self.show_preview()

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

    def clear_list(self):
        self.pdf_files = []
        self.thumbnails = {}
        self.current_page = {}
        self.listbox.delete(0, tk.END)
        self.image_label.config(image='', text="")

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = PDFMergerApp(root)
    root.mainloop()
