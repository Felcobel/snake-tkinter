import os
import sys
import time
import random
from tkinter import *
import tkinter.font as font
from PIL import Image, ImageTk


class snake:
    def __init__(self, janela, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.janela = janela
        self.janela.title("Snake")

        # Inicializar variáveis
        self.reso_altura = 910
        self.reso_largura = 910
        self.tempo = 350
        self.velocidade = 30
        self.x = self.velocidade
        self.controle = 0
        self.y = 0
        self.pontos = 0
        self.rodando = False
        self.cont = []
        self.fim = False
        self.parte_corpo = None
        self.jog = None
        self.cogumeloItem = None
        self.coordenadax = (self.reso_altura/2)-50
        self.coordenaday = (self.reso_largura/2)-50
        self.direcao = None
        self.jogador = []
        self.corpo = []

        self.tamanho_fonte = font.Font(size=15)

        self.carrega_imagens()

        self.janela.geometry(f'{self.reso_altura}x{self.reso_largura}')

        self.canvas = Canvas(self.janela, width=self.reso_altura-10, height=self.reso_largura-10)

        self.bg = ImageTk.PhotoImage(Image.open('src/fundo.png').resize((910,910)))
        self.img_fundo = Label(self.canvas, image=self.bg)

        self.comecar = Button(self.canvas, text="Inciar", anchor=CENTER, width=20, height=3, command=self.iniciar, bg="white")  
        self.sair = Button(self.canvas, text="Sair", anchor=CENTER, width=20, height=3, command=self.fechar, bg="white")
        self.comecar['font'] = self.tamanho_fonte
        self.sair['font'] = self.tamanho_fonte
        
        self.canvas.pack(ipadx=self.reso_altura-10, ipady=self.reso_largura-10)

        self.canvas.create_image(0,0, image=self.bg, anchor=NW)

        self.botoes(self.rodando)


    def restart_programa(self):
        """Restarts the current program.
        Note: this function does not return. Any cleanup action (like
        saving data) must be done before calling this function."""
        python = sys.executable
        os.execl(python, python, * sys.argv)



    def carrega_imagens(self):
        self.jogador.append(ImageTk.PhotoImage(Image.open('src/pipe.png').resize((30,30))))
        self.jogador.append(ImageTk.PhotoImage(Image.open('src/pipeD.png').resize((30,30))))
        self.jogador.append(ImageTk.PhotoImage(Image.open('src/pipeE.png').resize((30,30))))
        self.jogador.append(ImageTk.PhotoImage(Image.open('src/pipeB.png').resize((30,30))))

        self.cogumelo = ImageTk.PhotoImage(Image.open('src/cogumelo.png').resize((20,20)))

        self.corpo.append(ImageTk.PhotoImage(Image.open('src/pipe_corpo.png').resize((30,30))))
        self.corpo.append(ImageTk.PhotoImage(Image.open('src/pipe_corpoD.png').resize((30,30))))
        self.corpo.append(ImageTk.PhotoImage(Image.open('src/pipe_corpoE.png').resize((30,30))))
        self.corpo.append(ImageTk.PhotoImage(Image.open('src/pipe_corpoB.png').resize((30,30))))


    def iniciar(self):
        self.rodando = True
        self.botoes(self.rodando)

        if self.jog not in self.canvas.find_all() or self.jog == None:
            self.jog = self.canvas.create_image(self.reso_largura/2, self.reso_altura/2, anchor=NW, image=self.jogador[1], tags='jogador')
            self.pontos_tela = self.canvas.create_text(self.reso_largura/2, 10, text=f'Pontuação: {self.pontos}', fill='white')
            self.retangulo = self.canvas.create_rectangle(0,0,self.reso_largura, self.reso_altura, tags="area")

        self.loop()


    def fechar(self):
        self.janela.destroy()

    
    def game_over(self):
        self.rodando = False
        self.canvas.delete(ALL)
        self.canvas.create_rectangle(0,0,self.reso_largura, self.reso_altura, fill="black")
        self.canvas.create_text(self.reso_largura/2, self.reso_altura/2, text=f'FIM\nPontuação Total: {self.pontos}', fill='white')
        self.recomecar = Button(self.canvas, text="Tentar Novamente", anchor=CENTER, width=20, height=3, command=self.restart_programa, bg="white")
        self.recomecar.place(relx=0.5, rely=0.4, anchor=CENTER)

    
    def score(self):
        self.pontos += 5
        self.canvas.itemconfig(self.pontos_tela, text=f'Pontuação: {self.pontos}')


    def mudar_direcao(self, x, y, direcao_press):
        if direcao_press == 'esquerda' and self.direcao != 'direita':
            self.canvas.itemconfig(self.jog, image=self.jogador[2])
        elif direcao_press == 'direita' and self.direcao != 'esquerda':
            self.canvas.itemconfig(self.jog, image=self.jogador[1])
        elif direcao_press == 'cima'and self.direcao != 'baixo':
            self.canvas.itemconfig(self.jog, image=self.jogador[0])
        elif direcao_press == 'baixo'and self.direcao != 'cima':
            self.canvas.itemconfig(self.jog, image=self.jogador[3])
        else:
            return 0

        self.direcao = direcao_press

        self.x = x
        self.y = y
      

    def movimento(self):
        self.coordenadax = self.canvas.coords(self.jog)[0]
        self.coordenaday = self.canvas.coords(self.jog)[1]

        self.parte_corpo = self.canvas.find_withtag('corpo') + self.canvas.find_withtag('jogador')

        temp = 0
        if len(self.parte_corpo) > 1:
            while temp < len(self.parte_corpo) - 1:
                c1 = self.canvas.coords(self.parte_corpo[temp])
                c2 = self.canvas.coords(self.parte_corpo[temp+1])
                self.canvas.move(self.parte_corpo[temp], c2[0] - c1[0], c2[1] - c1[1])
                self.girar(temp)
                temp+=1

        self.canvas.move(self.jog, self.x, self.y)


    def aumenta_velocidade(self):
        if self.controle <= 22:
            self.tempo -= 15
            self.controle +=1


    def girar(self, temp):
        if self.direcao == 'esquerda':
            self.canvas.itemconfig(self.parte_corpo[temp], image=self.corpo[2])
        if self.direcao == 'direita':
            self.canvas.itemconfig(self.parte_corpo[temp], image=self.corpo[1])
        if self.direcao == 'cima':
            self.canvas.itemconfig(self.parte_corpo[temp], image=self.corpo[0])
        if self.direcao == 'baixo':
            self.canvas.itemconfig(self.parte_corpo[temp], image=self.corpo[3])

    
    def colisao(self):
        self.col = self.canvas.bbox('jogador')
        self.parte_corpo = self.canvas.find_withtag('corpo')
        contato = self.canvas.find_overlapping(self.col[0],self.col[1],self.col[2],self.col[3])

        if self.cogumeloItem in contato:
            self.spawn_corpo()
            self.canvas.delete('cogumelo')
            self.score()
            self.aumenta_velocidade()

        for parte_corpos in self.parte_corpo:
            for contatos in contato:
                if parte_corpos == contatos:
                    self.game_over()

        if self.retangulo in contato:
            self.fim = True
            self.game_over()


    def loop(self):
        if self.rodando == True:
            if self.fim == False:
                self.spawn_cogumelo()
                self.colisao()
                self.movimento()

                self.canvas.after(self.tempo, self.loop)


    def spawn_corpo(self):
        if len(self.parte_corpo) == 0:
            x, y = self.canvas.coords(self.jog)
        else:
            x, y = self.canvas.coords(self.parte_corpo[len(self.parte_corpo)-1])
        
        if self.direcao == 'esquerda':
            self.canvas.create_image(x, y, anchor=NW, image=self.corpo[2], tags='corpo')
        if self.direcao == 'direita':
            self.canvas.create_image(x, y, anchor=NW, image=self.corpo[1], tags='corpo')
        if self.direcao == 'cima':
            self.canvas.create_image(x, y, anchor=NW, image=self.corpo[0], tags='corpo')
        if self.direcao == 'baixo':
            self.canvas.create_image(x, y, anchor=NW, image=self.corpo[3], tags='corpo')

    
    def spawn_cogumelo(self):
        if self.cogumeloItem not in self.canvas.find_all():
            x = random.randint(30,self.reso_altura-30)
            y = random.randint(30,self.reso_altura-30)
            
            if self.cogumeloItem == None:
                self.cogumeloItem = self.canvas.create_image(x, y, anchor=CENTER, image=self.cogumelo, tags='cogumelo')
            else:
                while (self.coordenadax <= x+60 and self.coordenaday <= y+60) and (self.coordenadax >= x-60 and self.coordenaday >= y-60):
                    x = random.randint(30,self.reso_altura-30)
                    y = random.randint(30,self.reso_altura-30)
                
                self.cogumeloItem = self.canvas.create_image(x, y, anchor=CENTER, image=self.cogumelo, tags='cogumelo')

            x = 0
            y = 0

    
    def botoes(self, rodando):
        self.rodando = rodando
        if self.rodando == True:
            #self.comecar.pack_forget()
            self.comecar.place(relx=10, rely=10, anchor=CENTER)
            self.sair.place(relx=10, rely=10, anchor=CENTER)
        elif self.rodando == False:
            self.comecar.place(relx=0.5, rely=0.4, anchor=CENTER)
            self.sair.place(relx=0.5, rely=0.5, anchor=CENTER)

    
    def pausa(self, pause):
        if pause == True:
            self.comecar.config(text='Continuar')
        self.botoes(rodando=False)


###########################################função inicial###########################################
def movimento(app):
    janela.bind("<KeyPress-Left>", lambda _: app.mudar_direcao(-app.velocidade, 0, 'esquerda'))
    janela.bind("<KeyPress-Right>", lambda _: app.mudar_direcao(app.velocidade, 0, 'direita'))
    janela.bind("<KeyPress-Up>", lambda _: app.mudar_direcao(0, -app.velocidade, 'cima'))
    janela.bind("<KeyPress-Down>", lambda _: app.mudar_direcao(0, app.velocidade, 'baixo'))
    janela.bind("<Escape>", lambda _: app.pausa(pause=True))


if __name__ == "__main__":
    janela = Tk()
    app = snake(janela)
    movimento(app)
    janela.mainloop()