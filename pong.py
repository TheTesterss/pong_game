import tkinter
from tkinter import messagebox
import time

canvasWidth =750
canvasHeight = 700
fenêtre = tkinter.Tk()
canvas = tkinter.Canvas(fenêtre, width=canvasWidth, height=canvasHeight, bg="dodgerblue4")
canvas.pack()
gaucheAppuyé = droiteAppuyé = 0
raquette = canvas.create_rectangle(0, 0, 40, 10, fill="dark turquoise")
raquette2 = canvas.create_rectangle(80, 20, 40, 10, fill="dark turquoise")
balle = canvas.create_oval(0, 0, 10, 10, fill="deep pink")
turn = 0
fenêtreOuverte = True

def boucle_principale():
    while fenêtreOuverte:
        déplacer_raquette()
        déplacer_balle()
        fenêtre.update()
        time.sleep(0.02)
        if fenêtreOuverte:
            vérifier_game_over()

def quand_touche_appuyée(event):
    global gaucheAppuyé,droiteAppuyé
    if turn % 2 == 0:
        if event.keysym == "q":
            gaucheAppuyé = 1
        elif event.keysym == "d":
            droiteAppuyé = 1
    else:
        if event.keysym == "Left":
            gaucheAppuyé = 1
        elif event.keysym == "Right":
            droiteAppuyé = 1
        
def quand_touche_relachée(event):
    global gaucheAppuyé, droiteAppuyé
    if turn % 2 == 0:
        if event.keysym == "q":
            gaucheAppuyé = 0
        elif event.keysym == "d":
            droiteAppuyé = 0
    else:
        if event.keysym == "Left":
            gaucheAppuyé = 0
        elif event.keysym == "Right":
            droiteAppuyé = 0

vitesseraquette = 50
def déplacer_raquette():
    if turn % 2 == 0:
        mouvRaquette2 = vitesseRaquette*droiteAppuyé - vitesseRaquette*gaucheAppuyé
        (gaucheRaquette2, hautRaquette2, basRaquette2, droiteRaquette2) = canvas.coords(raquette)
        if ((gaucheRaquette2> 0 or mouvRaquette2 > 0) and (droiteRaquette2 < canvasWidth or mouvRaquette2 < 0)):
            canvas.move(raquette2, mouvRaquette2, 0)
    else:
        mouvRaquette = vitesseRaquette*droiteAppuyé - vitesseRaquette*gaucheAppuyé
        (gaucheRaquette, hautRaquette, basRaquette, droiteRaquette) = canvas.coords(raquette)
        if ((gaucheRaquette> 0 or mouvRaquette > 0) and (droiteRaquette < canvasWidth or mouvRaquette < 0)):
            canvas.move(raquette, mouvRaquette, 0)
    
mouvBalleX = 4
mouvBalleY = -4
défHautRaquette = canvasHeight-40
défBasRaquette = canvasHeight-30

def déplacer_balle():
    global mouvBalleX, mouvBalleY, score, compteRebonds, vitesseRaquette, turn
    global gaucheAppuyé,droiteAppuyé
    (gaucheBalle, hautBalle, droiteBalle, basBalle) = canvas.coords(balle)
    
    if mouvBalleX > 0 and droiteBalle > canvasWidth:
        mouvBalleX = -mouvBalleX
    if mouvBalleX < 0 and gaucheBalle < 0:
        mouvBalleX = -mouvBalleX

    if (mouvBalleY > 0 and basBalle > défHautRaquette and basBalle < défBasRaquette and
            mouvBalleY > 0 and hautBalle > 0):
        gaucheRaquette, hautRaquette, droiteRaquette, basRaquette = canvas.coords(raquette)
        if (mouvBalleX > 0 and (droiteBalle + mouvBalleX > gaucheRaquette and gaucheBalle < droiteRaquette) or
                mouvBalleX < 0 and (droiteBalle > gaucheRaquette and gaucheBalle + mouvBalleX < droiteRaquette)):
            mouvBalleY = -mouvBalleY
            score += 1
            turn += 1
            gaucheAppuyé = 0
            droiteAppuyé = 0
            compteRebonds += 1
            if compteRebonds == 4:
                compteRebonds = 0
                vitesseRaquette += 1
                if mouvBalleX > 0:
                    mouvBalleX += 1
                else:
                    mouvBalleX -= 1
                mouvBalleY -= 1
    elif (mouvBalleY < 0 and hautBalle < 20 and hautBalle > 10 and mouvBalleY < 0 and basBalle < canvasHeight):
        gaucheRaquette2, hautRaquette2, droiteRaquette2, basRaquette2 = canvas.coords(raquette2)
        if (mouvBalleX > 0 and (droiteBalle + mouvBalleX > gaucheRaquette2 and gaucheBalle < droiteRaquette2) or
                mouvBalleX < 0 and (droiteBalle > gaucheRaquette2 and gaucheBalle + mouvBalleX < droiteRaquette2)):
            mouvBalleY = -mouvBalleY
            score += 1
            turn += 1
            gaucheAppuyé = 0
            droiteAppuyé = 0
            compteRebonds += 1
            if compteRebonds == 4:
                compteRebonds = 0
                vitesseRaquette += 1
                if mouvBalleX > 0:
                    mouvBalleX += 1
                else:
                    mouvBalleX -= 1
                mouvBalleY -= 1

    canvas.move(balle, mouvBalleX, mouvBalleY)

    
def vérifier_game_over():
    (gaucheBalle, hautBalle, droiteBalle, basBalle) = canvas.coords(balle)
    if hautBalle > canvasHeight or basBalle < 0:
        print("Ton score:" + str(score))
        rejouer = tkinter.messagebox.askyesno(message="Veux-tu rejouer ?")
        if rejouer:
            réinitialiser()
        else:
            fermer()

def fermer():
    global fenêtreOuverte
    fenêtreOuverte = False
    fenêtre.destroy()
    
def réinitialiser():
    global gaucheAppuyé, droiteAppuyé
    global mouvBalleX, mouvBalleY
    global score, compteRebonds, vitesseRaquette, turn
    score = 0
    gaucheAppuyé = 0
    droiteAppuyé = 0
    mouvBalleX = 4
    mouvBalleY = -4
    turn = 0
    canvas.coords(raquette, 10, défHautRaquette, 50, défBasRaquette)
    canvas.coords(raquette2, 80, 20, 40, 10)
    canvas.coords(balle, 20, défHautRaquette-10, 30, défHautRaquette)
    compteRebonds = 0
    vitesseRaquette = 6

fenêtre.protocol("WM_DELETE_WINDOW", fermer)
fenêtre.bind("<KeyPress>", quand_touche_appuyée)
fenêtre.bind("<KeyRelease>", quand_touche_relachée)

réinitialiser()
boucle_principale()
score = 0
compteRebonds = 0 
