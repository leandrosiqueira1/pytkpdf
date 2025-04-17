import tkinter as tk
from tkinter import filedialog, messagebox
from pypdf import PdfWriter, PdfReader

class PDFMergerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Juntar PDFs")
        self.root.geometry("500x500")
        self.pdf_files = []

        self.label = tk.Label(root, text="Arquivos selecionados:")
        self.label.pack(pady=5)

        self.listbox = tk.Listbox(root, width=50)
        self.listbox.pack(pady=5)

        self.add_button = tk.Button(root, text="Adicionar PDFs", command=self.add_pdfs)
        self.add_button.pack(pady=5)

        self.merge_button = tk.Button(root, text="Juntar PDFs", command=self.merge_pdfs)
        self.merge_button.pack(pady=5)

        self.clear_button = tk.Button(root, text="Limpar Lista", command=self.clear_list)
        self.clear_button.pack(pady=5)

    def add_pdfs(self):
        arquivos = filedialog.askopenfilenames(filetypes=[("Arquivos pdf", "*.pdf")])
        for arquivo in arquivos:
            if arquivo not in self.pdf_files:
                self.pdf_files.append(arquivo)
                self.listbox.insert(tk.END, arquivo)

    def merge_pdfs(self):
        if len(self.pdf_files) < 2:
            messagebox.showwarning("Aviso", "Adicione pelo menos dois arquivos PDF.")
            return

        output_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("Arquivos pdf", "*.pdf")],
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

            messagebox.showinfo("Sucesso", f"PDF criado com sucesso: {output_path}")
            self.clear_list()
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao juntar os PDFs:\n{e}")

    def clear_list(self):
        self.pdf_files = []
        self.listbox.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFMergerApp(root)
    root.mainloop()
