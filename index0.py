import tkinter as tk
from tkinter import filedialog, messagebox
from pypdf import PdfWriter, PdfReader


class juntaPDF:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Abrir arquivo")
        self.root.geometry("500x500")
        self.label = tk.Label(self.root,text="Olá mundo!")
        self.label.pack()

        self.botao = tk.Button(self.root,text="Clique aqui",command=self.botao_clicado)
        self.botao.pack()

        btsalvar = tk.Button(self.root,text="Salvar arquivo",command=self.salvar_arquivo)
        btsalvar.pack()


    def botao_clicado(self):
        self.label.config(text="Botão clicado!")

    def salvar_arquivo(self):
        arquivo = filedialog.asksaveasfile(mode="w", defaultextension=".txt",filetypes=[("Arquivo txt","*.txt")])
        if arquivo:
            arquivo.write("Conteudo do arquivo")
            arquivo.close()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = juntaPDF()
    app.run()
