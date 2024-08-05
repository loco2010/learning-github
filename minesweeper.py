from tkinter import *
from tkinter import Variable, filedialog
from typing import Any 
import random

class Cell(Label):
    def __init__(self, master, row, col):
        self.isBomb = False
        self.isFlagged = False
        self.adjacentBombs = 0
        self.isRevealed = False
        self.master = master 
        self.row = row
        self.col = col
        self.colormap = ['','blue','darkgreen','#BD3648','purple','maroon','cyan','black','dim gray']
        Label.__init__(self, master, height=2, width=4, text='', bg='white', font=('Comic Sans MS', 24, 'bold'))

        # set up listeners.
        self.bind('<Button-1>', self.open)
        self.bind('<Button-2>', self.toggleFlag)
        self.updateCell()

    def updateCell(self):
        # set the background color
        if self.row%2 == self.col%2:
            if self.isRevealed:
                self.configure(bg='#A178AE')       
            else:
                self.configure(bg='#3F8FE9')        
        else:
            if self.isRevealed:
                self.configure(bg='#835990')                
            else:
                self.configure(bg='#3368A5')
        if self.isFlagged:
            self['text'] = '💀'
        else:
            self['text'] = ''

        # decide what you want to display
        if self.isRevealed:
            if self.isBomb:
                self['text'] = 'Bomb'  # display the number
                self['bg'] = 'skyblue'
                self['fg'] = 'red'
            else:
                # display number of adjacent bombs
                if self.adjacentBombs > 0:
                    self['text'] = str(self.adjacentBombs)  # display the number   
                    self['fg'] = self.colormap[self.adjacentBombs]

    def end(self):
        self.unbind('<Button-1>')
        self.unbind('<Button-2>')

    def toggleFlag(self, event):
        if self.isRevealed:
            return
        self.isFlagged = not self.isFlagged
        if not self.master.toggleFlag(self.isFlagged):
            self.isFlagged = not self.isFlagged
        self.updateCell()

    def open(self, event):
        if self.isFlagged:
            return
        if self.isRevealed:
            return
        
        self.isRevealed = True
        self.updateCell()
        self.master.cellOpened(self.row, self.col, 0)

    def makeBomb(self):
        self.isBomb = True

    def addBombCount(self):
        self.adjacentBombs += 1

            
class Minesweeper(Frame):
    def __init__(self, master, numColumns, numRows, numBombs):
        # places the lines in between the cells
        Frame.__init__(self, master, bg='black')
        self.grid()

        # makes the cells and places them
        self.cells = []
        for row in range(numRows):
            rowCells = []
            for col in range(numColumns):
                cell = Cell(self, row, col)
                cell.grid(row=row,column=col)
                rowCells.append(cell)
            self.cells.append(rowCells)

        # puts the amount of flags left at the bottom of the screen
        self.flagsLeft = numBombs
        self.flagCounter = Label(self, height=2, width=4,text=str(self.flagsLeft), bg='white', font=('Comic Sans MS', 24), fg='black')
        self.flagCounter.grid(row=numRows*2+1, column=int(numColumns/2))
        self.winLabel = Label(self, height=2, width=4,text='', bg='white', font=('Comic Sans MS', 24), fg='black')
        self.winLabel.grid(row=numRows*2+1, column=numColumns-3)

            # places random bombs
        while numBombs > 0:
            row = random.randrange(0, numRows)
            col = random.randrange(0, numColumns)
            if self.placeBomb(row, col):
                numBombs -= 1

        self.numBombs = numBombs

    def placeBomb(self, row, col):
        target = self.cells[row][col]
        if target.isBomb:
            return False
        target.makeBomb()
        self.addBombCount(row-1, col-1)
        self.addBombCount(row-1, col)
        self.addBombCount(row-1, col+1)
        self.addBombCount(row,   col-1)
        self.addBombCount(row,   col+1)
        self.addBombCount(row+1, col-1)
        self.addBombCount(row+1, col)
        self.addBombCount(row+1, col+1)
        return True

    def addBombCount(self, row, col):
        if row < 0 or col < 0:
            return
        if row >= len(self.cells) or col >= len(self.cells[0]):
            return
        self.cells[row][col].addBombCount()


    # return false if toggling is not allowed
    def toggleFlag(self, flag):
        if flag:
            if self.flagsLeft <= 0:
                return False
            self.flagsLeft -= 1
        else:
            self.flagsLeft += 1
        self.flagCounter['text'] = str(self.flagsLeft)
        return True

    def gameEnd(self, winFlag):
        if winFlag:
            self.winLabel['text'] = 'win'
        else:
            self.winLabel['text'] = 'lose'
        for row in self.cells:
            for cell in row:
                cell.end()

    def cellOpened(self, row, col, event):
        cellOpened = self.cells[row][col]

        if cellOpened.isBomb:
            self.gameEnd(False)
            return
    
        # if the cell opened had zero adjacent bombs, open all the neighbors
        if cellOpened.adjacentBombs == 0:
            for rowDelta in (-1,0,1):
                for colDelta in (-1,0,1):
                    self.openCell(row+rowDelta, col+colDelta)

        # check win
        allCellsOpen = True # check if all non-bombs are open
        for row in range(len(self.cells)):
            for col in range(len(self.cells[0])):
                cell = self.cells[row][col]
                if cell.isBomb == False and cell.isRevealed == False:
                    allCellsOpen = False
                    break
        if allCellsOpen:
            self.gameEnd(True)
    
    # helper function to call cell. check if row and col are valid
    def openCell(self, row, col):
        # check if row and col are valid
        if row < 0 or col < 0:
            return
        if row >= len(self.cells) or col >= len(self.cells[0]):
            return
        self.cells[row][col].open(1) # pass a dummy event





root = Tk()
root.title('Minesweeper')
mineGrid = Minesweeper(root, 15, 10, 2)
root.mainloop()