
import customtkinter as ctk
from tkinter import *
import sqlite3
from tkinter import messagebox



class BackEnd():
    def conecta_db(self):
        self.conn = sqlite3.connect("Sistema_cadastros.db")
        self.cursor = self.conn.cursor()
        print('Banco de dados conectado')

    def desconecta_db(self):
        self.conn.close()
        print('Banco de dados desconectado')

    def cria_tabela(self):
        self.conecta_db()

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Usuarios(
                Id INTEGER PRIMARY KEY AUTOINCREMENT, 
                Username TEXT NOT NULL,
                Email TEXT NOT NULL,
                Senha TEXT NOT NULL,
                Confirma_senha TEXT NOT NULL            
            );            
        ''')
        self.conn.commit()
        print('Tabela criada com sucesso')
        self.desconecta_db()  

    def cadastrar_usuario(self):
        self.user_cadastro = self.user_cadastro_entry.get()
        self.email_cadastro = self.email_cadastro_entry.get()
        self.senha_cadastro = self.senha_cadastro_entry.get()
        self.confirma_senha_cadastro = self.confirma_senha_entry.get()


        self.conecta_db()

        #Mandar dados para o db
        self.cursor.execute("""
            INSERT INTO Usuarios (Username, Email, Senha, Confirma_Senha)
            VALUES (?, ?, ?, ?)""", (self.user_cadastro, self.email_cadastro, self.senha_cadastro, self.confirma_senha_cadastro))
        
    
        try:
            if(self.user_cadastro == "" or self.email_cadastro == "" or self.senha_cadastro == "" or self.confirma_senha_cadastro == ""):
                messagebox.showerror(title="Sistema de login", message="ERRO!\nPor favor, preencha todos os campos")

                #len serve para contar o numero de caracteres que estao dentro do input
            elif(len(self.user_cadastro) < 8):
                messagebox.showwarning(title="Sistema de login", message="O nome de usuário deve conter pelo menos 8 caracteres")

            elif(len(self.senha_cadastro) < 8):
                messagebox.showwarning(title="A senha deve conter pelo menos 8 caracteres")

            elif(self.senha_cadastro != self.confirma_senha_cadastro):
                messagebox.showerror(title="Sistema de login", message="ERRO!\nAs senhas não coincidem")

            else:
                self.conn.commit() #enviar para o banco de dados
                messagebox.showinfo(title="Sistema de login", message=f"Parabéns {self.user_cadastro}\n Os seus dados foram cadastrados com sucesso!")
                self.desconecta_db()
                self.limpa_entry_cadastro()
        except:
            messagebox.showerror(title="Sistema de login", message="Erro no processamento do seu cadastro\nPor favor tente novamente.")
            self.desconecta_db()
            

    def verifica_login(self):
        self.user_login = self.user_login_entry.get()
        self.senha_login = self.senha_login_entry.get()

        print(self.user_login, self.senha_login)
        self.limpa_entry_login()

        self.conecta_db()

        self.cursor.execute("""SELECT * FROM Usuarios WHERE (Username = ? AND Senha = ?)""", (self.user_login, self.senha_login))

        self.verifica_dados = self.cursor.fetchone() #Percorrendo na tabela Usuarios

        try:
            if (self.user_login in self.verifica_dados and self.senha_login in self.verifica_dados):
                messagebox.showinfo(title="Sistema de login", message=f"Parabéns, {self.user_login}\nlogin feito com sucesso")
                self.desconecta_db()
                self.limpa_entry_login()
        except:
            messagebox.showerror(title="Sistema de login", message="ERRO!\nDados não encontrados em sistema. \nPor favor, verifique os seus dados ou cadastre-se")
            self.desconecta_db()
                


        


class App(ctk.CTk, BackEnd):
    def __init__(self):
        super().__init__()
        self.config_janela_ini()
        self.tela_login()
        self.cria_tabela()


    #configurando a janela principal
    def config_janela_ini(self):
        self.geometry("700x400")
        self.title("Sistema de login")
        self.resizable(False, False)

    def tela_login(self):


        #Trabalhando com as imagens
        self.img = PhotoImage(file="canva.png")
        self.lb_img = ctk.CTkLabel(self, text=None, image=self.img)
        self.lb_img.grid(row=3, column=0, padx=30, pady=40) #linha e coluna

        #Titulo da anossa plataforma
        self.title = ctk.CTkLabel(self, text="Faça o seu login ou cadastre-se\nna nossa plataforma para acessar\nos nossos serviços!",font=("Century Gothic bold", 17))
        self.title.grid(row=2, column=0, padx=30, pady=40)

        #Criar a frame do formulario de login 
        self.frame_login = ctk.CTkFrame(self, width=350, height=380)
        self.frame_login.place(x=350, y=10)

        #Colocando widgets dentro do frame - formulario de login
        self.lb_title = ctk.CTkLabel(self.frame_login, text="Faça o seu login", font=("Century Gothic bold", 22))
        self.lb_title.grid(row=0, column=0, padx=65, pady=10)

        
        self.user_login_entry = ctk.CTkEntry(self.frame_login, width=300, placeholder_text="Seu nome de usuário", font=("Century Gothic bold", 16), corner_radius=15, border_color='#529eeb')
        self.user_login_entry.grid(row=1, column=0, padx=10, pady=10)
       
        self.senha_login_entry = ctk.CTkEntry(self.frame_login, width=300, placeholder_text="Sua senha", font=("Century Gothic bold", 16), show='*', corner_radius=15, border_color='#529eeb')
        self.senha_login_entry.grid(row=2, column=0, padx=10, pady=10)

        self.ver_senha = ctk.CTkCheckBox(self.frame_login, text="Clique para ver sua senha", font=("Century Gothic bold", 14), corner_radius=20)
        self.ver_senha.grid(row=3, column=0, padx=10, pady=10)

        self.botao_login = ctk.CTkButton(self.frame_login, width=300, text="LOGIN", font=("Century Gothic bold", 16, 'bold'), corner_radius=15, command=self.verifica_login)
        self.botao_login.grid(row=4, column=0, padx=10, pady=10)

        self.span = ctk.CTkLabel(self.frame_login, text='Se não tem uma conta, clique no botão abaixo para se cadastrar', font=('Century Gothic', 10))
        self.span.grid(row=5, column=0, padx=10, pady=10)

        self.botao_cadastro = ctk.CTkButton(self.frame_login, width=300, text="CADASTRE-SE", font=("Century Gothic bold", 16, 'bold'), command=self.tela_cadastro, corner_radius=15, fg_color='green', hover_color='#2D9334')
        self.botao_cadastro.grid(row=6, column=0, padx=10, pady=10)

    def tela_cadastro(self):
        #Remover o formulario de login
        self.frame_login.place_forget()

        #Criar a frame do formulario de cadastro 
        self.frame_cadastro = ctk.CTkFrame(self, width=350, height=380)
        self.frame_cadastro.place(x=350, y=10)

        #Criando o nosso titulo
        self.lb_title_cadastro = ctk.CTkLabel(self.frame_cadastro, text="Faça o seu cadastro!", font=("Century Gothic bold", 22))
        self.lb_title_cadastro.grid(row=0, column=0, padx=65, pady=5)

        #Criar os nossos widgets da tela de cadastro 
        self.user_cadastro_entry = ctk.CTkEntry(self.frame_cadastro, width=300, placeholder_text="Seu nome de usuário", font=("Century Gothic bold", 16), corner_radius=15, border_color='#529eeb')
        self.user_cadastro_entry.grid(row=1, column=0, padx=10, pady=7)

        self.email_cadastro_entry = ctk.CTkEntry(self.frame_cadastro, width=300, placeholder_text="Seu email", font=("Century Gothic bold", 16), corner_radius=15, border_color='#529eeb')
        self.email_cadastro_entry.grid(row=2, column=0, padx=10, pady=7)
       
        self.senha_cadastro_entry = ctk.CTkEntry(self.frame_cadastro, width=300, placeholder_text="Sua senha", font=("Century Gothic bold", 16), show='*', corner_radius=15, border_color='#529eeb')
        self.senha_cadastro_entry.grid(row=3, column=0, padx=10, pady=7)

        self.confirma_senha_entry = ctk.CTkEntry(self.frame_cadastro, width=300, placeholder_text="Confirme sua senha", font=("Century Gothic bold", 16), show='*', corner_radius=15, border_color='#529eeb')
        self.confirma_senha_entry.grid(row=4, column=0, padx=10, pady=7)

        self.ver_senha = ctk.CTkCheckBox(self.frame_cadastro, text="Clique para ver sua senha", font=("Century Gothic bold", 14), corner_radius=20)
        self.ver_senha.grid(row=5, column=0, pady=7)

        self.botao_cadastrar = ctk.CTkButton(self.frame_cadastro, width=300, text="CADASTRAR", font=("Century Gothic bold", 16, 'bold'), corner_radius=15, fg_color='green', hover_color='#2D9334', command=self.cadastrar_usuario)
        self.botao_cadastrar.grid(row=6, column=0, padx=10, pady=7)

        self.botao_back = ctk.CTkButton(self.frame_cadastro, width=300, text="VOLTAR", font=("Century Gothic bold", 16, 'bold'), corner_radius=15, fg_color='#444', hover_color='#333', command=self.tela_login)
        self.botao_back.grid(row=7, column=0, padx=10, pady=7)

    def limpa_entry_cadastro(self):
        self.user_cadastro_entry.delete(0, END)
        self.email_cadastro_entry.delete(0, END)
        self.senha_cadastro_entry.delete(0, END)
        self.confirma_senha_entry.delete(0, END)

    def limpa_entry_login(self):
        self.user_login_entry.delete(0, END)
        self.senha_login_entry.delete(0, END)







if __name__=="__main__":
    app = App()
    app.mainloop()