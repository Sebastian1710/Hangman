import pygame
import math
import tkinter
from tkinter import messagebox
from tkinter import simpledialog
import os


#Setup display
pygame.init()
WIDTH, HEIGHT = 1920, 1020 #Asigning the dimensions of the game
win = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Hangman Game") #Asigning the game's name
Icon = pygame.image.load("Icon.png")
pygame.display.set_icon(Icon)

#Load images
images = []
for i in range(7):
    image = pygame.image.load("Hangman_" + str(i) + ".png")
    images.append(image)



#Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

#Fonts
LETTER_FONT = pygame.font.SysFont('comic-sans', 45)
WORD_FONT = pygame.font.SysFont('Verdana', 60)
TITLE_FONT = pygame.font.SysFont('Verdana', 80)

#Drawing
def draw():
    win.fill(WHITE) #Background Color
    win.blit(images[hangman_status], (50, 70)) # Hangman drawn onto the window

    #Draw Title
    win.blit(Icon, (1720, 10))
    text = TITLE_FONT.render("HANGMAN GAME", 1, BLACK)
    win.blit(text, (WIDTH/2 - text.get_width()/2, 10))

    #Draw Word
    display_word_1 = ""
    if " " not in word:
        for letter in word:
            if letter in guessed:
                display_word_1 += letter + " "
            else:
                display_word_1 += "_ "
        text = WORD_FONT.render(display_word_1, 1, BLACK)
        win.blit(text, (550, 385))

    elif " " in word:
        splits = word.count(" ")
        word_1 = word.split(" ")
        splitsn = word.count(" ")
        while (splitsn-1) != -1:
            for letter in word_1[splits-splitsn]:
                if letter in guessed:
                    display_word_1 += letter + " "
                else:
                    display_word_1 += "_ "
            display_word_1+= "    "
            splitsn = splitsn-1
        for letter in word_1[splits]:
                if letter in guessed:
                    display_word_1 += letter + " "
                else:
                    display_word_1 += "_ "
        text = WORD_FONT.render(display_word_1, 1, BLACK)
        win.blit(text, (550, 385))


    #Draw letter buttons
    for letter in letters:
        x, y, ltr, visible = letter
        if visible:
            pygame.draw.circle(win, BLACK, (x, y), RADIUS, 3) #Draws 1 circle per letter
            text = LETTER_FONT.render(ltr, 1, BLACK)  #Draws the letter inside the button
            win.blit(text, (x - text.get_width()/2, y - text.get_height()/2))
    pygame.display.update()

#Establish an alert for the results
def display_results(results):
    win.fill(WHITE)
    pygame.display.update()
    root = tkinter.Tk()
    root.withdraw()
    messagebox.showinfo("Game Over", results)

def main():
    win.fill(WHITE)
    #Game variables
    ROOT = tkinter.Tk()
    ROOT.withdraw()
    global word
    global hangman_status
    global guessed
    word = simpledialog.askstring(title="Hangman", prompt="Input the word you want to play with:")
    word = word.upper()
    hangman_status = 0
    guessed = []
    
    #Letter buttons (2 rows of 13 letters)
    global letters
    global RADIUS
    global GAP
    RADIUS = 30
    GAP = 20
    letters = []
    startx = round((WIDTH-(RADIUS * 2 + GAP) * 13) / 2)
    starty = 750
    A = 65 #Number that represents A, the rest of the alfabet is 66 = B, 67 = C, etc.
    for i in range(26):
        x = startx + GAP * 2 + ((RADIUS * 2 + GAP) * (i % 13))
        y = starty + ((i // 13) * (GAP + RADIUS * 2))
        letters.append([x, y, chr(A+i), True]) #For every loop, it writes the proper letter

    #Setup game loop
    FPS = 60 #Setting the refresh rate for the game
    clock = pygame.time.Clock()
    run = True
    while run: #Making the game be constantly refreshing
        clock.tick(FPS)

        draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT: #Making the loop end when quitting the game
                run = False
                break
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                m_x, m_y = pygame.mouse.get_pos() #Letting us know where the mouse is on the screen
                for letter in letters:
                    x, y, ltr, visible = letter
                    if visible:
                        dis = math.sqrt((x - m_x)**2 + (y - m_y)**2)
                        if dis < RADIUS:
                            letter[3] = False
                            guessed.append(ltr)
                            if ltr not in word:
                                hangman_status += 1
        draw()

        won = True
        for letter in word:
            if letter not in guessed:
                won = False
                break
        if won:
            pygame.time.delay(2000)
            display_results("Congratulations!   You Won!")
            break
        if hangman_status == 6:
            pygame.time.delay(2000)
            display_results("Sorry,  You Lost.  The correct word was:  "+word)
            break
    if event.type == pygame.QUIT: #Making the loop end when quitting the game
                run = False
                pygame.quit()
    else:
        ROOT = tkinter.Tk()
        ROOT.withdraw()
        if (messagebox.askyesno(message="Do yo want to restart ?", title="Game Over")) == True:
            main()
main()
    

pygame.quit()   