import tkinter as tk
from tkinter import filedialog, messagebox
from pypdf import PdfWriter, PdfReader


class juntaPDF:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Abrir arquivo")
        self.root.geometry("500x500")

        #Botão com nome ola mundo!
        self.label = tk.Label(self.root,text="Olá mundo!")
        self.label.pack()

        #Botão com nome Clique aqui
        self.botao = tk.Button(self.root,text="Clique aqui",command=self.botao_clicado)
        self.botao.pack()

        #BOtão com nome Salvar arquivo
        btsalvar = tk.Button(self.root,text="Salvar arquivo",command=self.salvar_arquivo)
        btsalvar.pack()

    #FUnção que muda o conteudo do botão ola mundo!
    def botao_clicado(self):
        self.label.config(text="Botão clicado!")
        self.botao.config(text="Botão clicado")
    

    #Função que salva o arquivo em formato txt
    def salvar_arquivo(self):
        #variavel arquivo recebe o arquivo como os parametros que dever ser criado.
        arquivo = filedialog.asksaveasfile(defaultextension=".txt",filetypes=[("Arquivo txt","*.txt")])
        if arquivo:
            arquivo.write("Conteudo do arquivo")
            arquivo.close()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = juntaPDF()
    app.run()
