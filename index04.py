import tkinter as tk
from tkinter import filedialog, messagebox
from pypdf import PdfWriter, PdfReader
from pdf2image import convert_from_path
from PIL import Image, ImageTk
from pathlib import Path
import os

class PDFMergerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Juntar PDFs com Prévia de Páginas")
        self.root.geometry("950x850")
        self.pdf_files = []
        self.pdf_images = {}  # Armazena imagens por PDF
        self.current_preview_pdf = None
        self.current_page_index = 0

        # Frame esquerdo (lista e botões)
        left_frame = tk.Frame(root)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        self.label = tk.Label(left_frame, text="Arquivos selecionados:")
        self.label.pack()

        self.listbox = tk.Listbox(left_frame, width=50, height=25)
        self.listbox.pack()
        self.listbox.bind("<<ListboxSelect>>", self.show_preview)

        self.add_button = tk.Button(left_frame, text="Adicionar PDFs", command=self.add_pdfs)
        self.add_button.pack(pady=5)

        self.merge_button = tk.Button(left_frame, text="Juntar PDFs", command=self.merge_pdfs)
        self.merge_button.pack(pady=5)

        self.clear_button = tk.Button(left_frame, text="Limpar Lista", command=self.clear_list)
        self.clear_button.pack(pady=5)

        # Frame direito (prévia do PDF)
        right_frame = tk.Frame(root)
        right_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH, padx=10, pady=10)

        self.preview_label = tk.Label(right_frame, text="Pré-visualização", font=("Arial", 14))
        self.preview_label.pack()

        self.image_label = tk.Label(right_frame)
        self.image_label.pack(pady=10)

        # Botões de navegação
        nav_frame = tk.Frame(right_frame)
        nav_frame.pack()

        self.prev_button = tk.Button(nav_frame, text="Anterior", command=self.show_previous_page)
        self.prev_button.grid(row=0, column=0, padx=5)

        self.page_info = tk.Label(nav_frame, text="Página 0 de 0")
        self.page_info.grid(row=0, column=1, padx=5)

        self.next_button = tk.Button(nav_frame, text="Próxima", command=self.show_next_page)
        self.next_button.grid(row=0, column=2, padx=5)

    def add_pdfs(self):
        files = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])
        for file in files:
            if file not in self.pdf_files:
                self.pdf_files.append(file)
                self.listbox.insert(tk.END, file)
                self.generate_thumbnails(file)

    def generate_thumbnails(self, file_path):
        try:
            images = convert_from_path(file_path, size=(500, 600))
            thumbnails = [ImageTk.PhotoImage(img) for img in images]
            self.pdf_images[file_path] = thumbnails
        except Exception as e:
            print(f"Erro ao gerar imagens: {e}")
            self.pdf_images[file_path] = []

    def show_preview(self, event):
        selected = self.listbox.curselection()
        if not selected:
            return
        index = selected[0]
        file_path = self.pdf_files[index]
        self.current_preview_pdf = file_path
        self.current_page_index = 0
        self.display_current_page()

    def display_current_page(self):
        if not self.current_preview_pdf:
            return
        images = self.pdf_images.get(self.current_preview_pdf, [])
        if images:
            img = images[self.current_page_index]
            self.image_label.config(image=img)
            self.image_label.image = img
            self.page_info.config(text=f"Página {self.current_page_index + 1} de {len(images)}")
        else:
            self.image_label.config(text="Prévia indisponível", image="")
            self.page_info.config(text="Página 0 de 0")

    def show_next_page(self):
        if not self.current_preview_pdf:
            return
        images = self.pdf_images.get(self.current_preview_pdf, [])
        if self.current_page_index < len(images) - 1:
            self.current_page_index += 1
            self.display_current_page()

    def show_previous_page(self):
        if not self.current_preview_pdf:
            return
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
            messagebox.showerror("Erro", f"Ocorreu um erro ao juntar os PDFs:\n{e}")

    def clear_list(self):
        self.pdf_files = []
        self.pdf_images = {}
        self.listbox.delete(0, tk.END)
        self.image_label.config(image='', text="")
        self.page_info.config(text="Página 0 de 0")
        self.current_preview_pdf = None
        self.current_page_index = 0

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFMergerApp(root)
    root.mainloop()
