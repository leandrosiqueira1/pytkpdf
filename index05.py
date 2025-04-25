import os
from pathlib import Path
from tkinter import filedialog, messagebox
from tkinterdnd2 import TkinterDnD, DND_FILES
import tkinter as tk
from pypdf import PdfReader, PdfWriter
from pdf2image import convert_from_path
from PIL import Image, ImageTk

class PDFMergerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Juntar PDFs com Drag and Drop")
        self.root.geometry("1000x800")
        self.pdf_files = []
        self.pdf_images = {}
        self.current_preview_pdf = None
        self.current_page_index = 0

        # Frame da lista
        left_frame = tk.Frame(root)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        tk.Label(left_frame, text="Arquivos PDF:").pack()

        # Listbox com suporte a drag and drop
        self.listbox = tk.Listbox(left_frame, width=50, height=25)
        self.listbox.pack()
        self.listbox.bind("<<ListboxSelect>>", self.show_preview)

        # Drag and Drop configurado aqui
        self.listbox.drop_target_register(DND_FILES)
        self.listbox.dnd_bind("<<Drop>>", self.drop_files)

        # Botões
        tk.Button(left_frame, text="Adicionar PDFs", command=self.add_pdfs).pack(pady=5)
        tk.Button(left_frame, text="Juntar PDFs", command=self.merge_pdfs).pack(pady=5)
        tk.Button(left_frame, text="Limpar Lista", command=self.clear_list).pack(pady=5)

        # Área de pré-visualização
        right_frame = tk.Frame(root)
        right_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH, padx=10, pady=10)

        self.preview_label = tk.Label(right_frame, text="Pré-visualização", font=("Arial", 14))
        self.preview_label.pack()

        self.image_label = tk.Label(right_frame)
        self.image_label.pack()

        nav_frame = tk.Frame(right_frame)
        nav_frame.pack()

        tk.Button(nav_frame, text="<< Anterior", command=self.prev_page).pack(side=tk.LEFT, padx=5)
        tk.Button(nav_frame, text="Próxima >>", command=self.next_page).pack(side=tk.LEFT, padx=5)

    def add_pdfs(self):
        files = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])
        self._add_files(files)

    def drop_files(self, event):
        files = self.root.tk.splitlist(event.data)
        pdfs = [f for f in files if f.lower().endswith(".pdf")]
        self._add_files(pdfs)

    def _add_files(self, files):
        for file in files:
            if file not in self.pdf_files:
                self.pdf_files.append(file)
                self.listbox.insert(tk.END, file)
                self.generate_thumbnails(file)

    def generate_thumbnails(self, file_path):
        try:
            images = convert_from_path(file_path, size=(400, 500))
            self.pdf_images[file_path] = [ImageTk.PhotoImage(img) for img in images]
        except Exception as e:
            print(f"Erro ao gerar prévia: {e}")
            self.pdf_images[file_path] = []

    def show_preview(self, event):
        selected = self.listbox.curselection()
        if selected:
            index = selected[0]
            self.current_preview_pdf = self.pdf_files[index]
            self.current_page_index = 0
            self.display_current_page()

    def display_current_page(self):
        images = self.pdf_images.get(self.current_preview_pdf, [])
        if images:
            image = images[self.current_page_index]
            self.image_label.config(image=image)
            self.image_label.image = image
        else:
            self.image_label.config(text="Prévia indisponível", image="")

    def next_page(self):
        if self.current_preview_pdf:
            images = self.pdf_images.get(self.current_preview_pdf, [])
            if self.current_page_index < len(images) - 1:
                self.current_page_index += 1
                self.display_current_page()

    def prev_page(self):
        if self.current_preview_pdf:
            if self.current_page_index > 0:
                self.current_page_index -= 1
                self.display_current_page()

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
            messagebox.showerror("Erro", f"Erro ao juntar os PDFs:\n{e}")

    def clear_list(self):
        self.pdf_files = []
        self.pdf_images = {}
        self.listbox.delete(0, tk.END)
        self.image_label.config(image='', text="")

if __name__ == "__main__":
    root = TkinterDnD.Tk()  # Importante para drag and drop
    app = PDFMergerApp(root)
    root.mainloop()
