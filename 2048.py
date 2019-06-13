from tkinter import Button, Frame, Label, Tk, messagebox, IntVar
from random import choice, randint
import numpy as np

n = 4
previous_state = False
colors = {
    '':'#b2bec3',
    2:'#fdcb6e',
    4: '#ffeaa7',
    8: '#fab1a0',
    16: '#e17055',
    32: '#ff7675',
    64: '#d63031',
    128: '#55efc4',
    256: '#00b894',
    512: '#81ecec',
    1024: '#00cec9',
    2048: '#74b9ff',
    4096: '#0984e3',
    8192: '#a29bfe',
    16384: '#6c5ce7',
    32768: '#fd79a8',
    65536: '#e84393'
}

total_score = None

class matrix:
    def __init__(self, n):
        self.n = n
        self.matrix = []
        self.reset()

    def __getitem__(self, item):
        return self.matrix[item]

    def __str__(self):
        s = str(self.matrix[0])
        for i in range(self.n-1):
            s += f'\n{str(self.matrix[i+1])}'
        return s

    def reset(self):
        '''
        Resets all the value of matrix with None
        :return:
        '''
        self.matrix=[]
        x0, y0, x1, y1 = randint(0, self.n-1),randint(0, self.n-1),randint(0, self.n-1),randint(0, self.n-1)
        while x1 == x0:
            x1 = randint(0, self.n-1)
        while y1 == y0:
            y1 = randint(0, self.n-1)
        
        for i in range(self.n):
            self.matrix.append([''] * self.n)

        self.matrix[x0][y0] = 2
        self.matrix[x1][y1] = 2

    def available_positions(self):
        positions = []
        for i in range(self.n):
            for j in range(self.n):
                if self.matrix[i][j] == '':
                    positions.append((i,j))
        return positions

    def give_position(self):
        '''
        This function will provide an empty random position alaliable
        :return: tuple of cordinate x,y in matrix
        '''
        pos = self.available_positions()
        if pos == []:
            return None
        return choice(self.available_positions())

def update(root, grid):
    '''
    This function creates buttons on tk
    :param root: tk
    :param grid: game object
    :return: none
    '''
    for i in range(grid.n):
        for j in range(grid.n):
            val = grid[i][j]
            l = Label(root, text = val, height = 3, width = 6, relief= 'flat', fg='white', bg=colors[val])
            l.grid(row= i, column=j, padx=1, pady=1)
            l.config(font=('bold', 24))




def buclick(root, grid, bu):

    global previous_state
    previous_state = grid.matrix

    if bu == 'l':
        l_move(grid)
    if bu == 'r':
        r_move(grid)
    if bu == 'u':
        u_move(grid)
    if bu == 'd':
        d_move(grid)

    new = randint(1,10)
    if new == 1:
        new = 4
    else:
        new = 2

    pos = grid.give_position()
    if pos is None:
        messagebox.showwarning('Game Over', 'You filled all empty cell....\nGame Over....\nTry Again....')
        reset_bu(root, grid)
    else:
        grid.matrix[pos[0]][pos[1]] = new
        update(root, grid)

def previous(root, grid):
    if previous_state:
        grid.matrix = previous_state
        update(root, grid)

def reset_bu(root, grid):
    grid.reset()
    update(root, grid)
    total_score.set(0)

def l_move(grid):
    for row in grid.matrix:
        for i in range(1, grid.n):
            if isinstance(row[i], int):
                while i != 0 and row[i-1] == '':
                    row[i-1], row[i] = row[i], row[i-1]
                    i -= 1
                if i != 0:
                    if row[i] == row[i-1]:
                        row[i-1] = row[i]*2
                        total_score.set(total_score.get()+row[i]*2)
                        row[i] = ''

def r_move(grid):
    for row in grid.matrix:
        for i in range(grid.n-2, -1, -1):
            if isinstance(row[i], int):
                while i != grid.n-1 and row[i + 1] == '':
                    row[i + 1], row[i] = row[i], row[i + 1]
                    i += 1
                if i != grid.n-1:
                    if row[i] == row[i + 1]:
                        row[i + 1] = row[i] * 2
                        total_score.set(total_score.get()+row[i]*2)
                        row[i] = ''

def u_move(grid):

    for j in range(grid.n):
        row = []
        for r in grid.matrix:
            row.append(r[j])

        for i in range(1, grid.n):
            if isinstance(row[i], int):
                while i != 0 and row[i - 1] == '':
                    row[i - 1], row[i] = row[i], row[i - 1]
                    i -= 1
                if i != 0:
                    if row[i] == row[i - 1]:
                        row[i - 1] = row[i] * 2
                        total_score.set(total_score.get() + row[i] * 2)
                        row[i] = ''

        for i in range(grid.n):
            grid.matrix[i][j] = row[i]

def d_move(grid):
    for j in range(grid.n):
        row = []
        for r in grid.matrix:
            row.append(r[j])

        for i in range(grid.n-2, -1, -1):
            if isinstance(row[i], int):
                while i != grid.n-1 and row[i + 1] == '':
                    row[i + 1], row[i] = row[i], row[i + 1]
                    i += 1
                if i != grid.n-1:
                    if row[i] == row[i + 1]:
                        row[i + 1] = row[i] * 2
                        total_score.set(total_score.get()+row[i]*2)
                        row[i] = ''

        for i in range(grid.n):
            grid.matrix[i][j] = row[i]

def gui(grid):
    '''
    This function will handle gui part
    :param grid: game grid object
    :return: none
    '''
    global total_score
    root = Tk()
    root.title("2048 game")

    for i in range(grid.n):
        root.rowconfigure(i,weight=1) #for changing size label with window increase
        root.columnconfigure(i,weigh=1)

    total_score = IntVar()
    root.config(background='#bdc3c7')
    ###########################################
    #putting initial position of all labels
    update(root, grid)
    ###########################################
    #keybinds
    root.bind('<Left>', lambda event: buclick(root, grid,'l'))
    root.bind('<Right>', lambda event: buclick(root, grid,'r'))
    root.bind('<Up>', lambda event: buclick(root, grid,'u'))
    root.bind('<Down>', lambda event: buclick(root, grid,'d'))
    root.bind('<Delete>', lambda event: reset_bu(root, grid))
    root.bind('<End>', lambda event: previous(root, grid))


    ###########################################
    #reset button
    reset = Button(root,text = "Reset", height = 2, width =11, bg='#273c75', fg='white')
    reset.grid(row = grid.n, column = 0)
    reset.config(command= lambda : reset_bu(root, grid))

    ###########################################
    #back button
    back = Button(root, text='Back', heigh=2, width= 11, bg='#0097e6', fg='white')
    back.grid(row = grid.n, column=1)
    back.config(command= lambda : previous(root, grid))

    ###########################################
    #score
    score = Frame(root)
    score.grid(row= grid.n, column = n-2, columnspan =2)

    score_label = Label(score, text= 'Score', bg='#dcdde1', height=2, width=11)
    score_label.grid(row=0, column= 0, sticky='e')


    score_entry = Label(score, textvariable=total_score, height=2 , width=13, bg='#dcdde1')
    score_entry.grid(row=0, column=1)
    ###########################################

    root.mainloop()

def main():
    game = matrix(n)
    gui(game)


if __name__ == '__main__':
    main()
