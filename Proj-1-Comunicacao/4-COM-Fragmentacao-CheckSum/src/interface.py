import tkinter as tk
from tkinter import filedialog
import client
import server
from PIL import ImageTk, Image

class Janela_Principal():

    def __init__(self):

        self.window = tk.Tk()
        self.window.geometry("250x400+100+100")
        self.window.title("LMMF Protocol")
        self.window.configure(background = 'white')
        self.window.resizable(False, False)

        # Geometria da pagina
        self.window.rowconfigure(0, minsize = 100)
        self.window.rowconfigure(1, minsize = 100)
        self.window.rowconfigure(2, minsize = 100)
        self.window.rowconfigure(3, minsize = 100)
        self.window.columnconfigure(0, minsize = 250)

        #Label
        self.Logo = ImageTk.PhotoImage(Image.open("./interface_imgs/python_logo.jpeg"))
        self.Logo_label = tk.Label(self.window, image = self.Logo, height = 1, width = 1)
        self.Logo_label.grid(row = 0, column = 0, sticky = "nsew")

        #Botoes
        self.button_client = tk.Button(self.window, text = "Client", height = 3, width = 30)
        self.button_client.grid(row = 1, column = 0)
        self.button_client.configure(command = self.conectarClient)

        self.button_server = tk.Button(self.window, text = "Server", height = 3, width = 30)
        self.button_server.grid(row = 2, column = 0)
        self.button_server.configure(command = self.conectarServer)
        
        self.button_Reconhecimento = tk.Button(self.window, text = "Sair", height = 3, width = 30)
        self.button_Reconhecimento.grid(row   = 3, column = 0)
        self.button_Reconhecimento.configure(command = self.sair)
        
    #Loop do codigo
    def iniciar(self):
        self.window.mainloop()

    #Acoes dos botoes
    def conectarClient(self):
        self.window.filename = filedialog.askopenfilename()
        client.main(self.window.filename)

    def conectarServer(self):
        server.main()

    def sair(self):
        self.window.destroy()


#Loop do codigo
app = Janela_Principal()
app.iniciar()