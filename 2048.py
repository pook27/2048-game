import random
import tkinter as tk

class block:
    def __init__(self, value):
        self.value = value
        self.color = color_map[value]

    def __repr__(self):
        return f"[{self.value}])"

def start():
    lst = [""] * 16
    for i in range(4):
        for j in range(4):
            lst[j + i * 4] = block(0)
    return lst

def get_row(lst, row_index):
    return [lst[i] for i in range(row_index*4,row_index*4+4)]

def get_col(lst, col_index):
    return [lst[i] for i in range(col_index,col_index+16,4)]

def set_row(lst, row_index, row):
    for i in range(4):
        lst[4*row_index+i]=row[i]

def set_col(lst, col_index, col):
    for i in range(4):
        lst[col_index + 4*i]=col[i]

def show_board(lst):
    for i in range(4):
        for j in range(4):
            if lst[j+i*4].value==0:
                print(f"|  ", end="|")
            else:
                if len(str(lst[j + i * 4].value))<2:
                    print(f"|{lst[j + i * 4].value} ", end="|")
                else:
                    print(f"|{lst[j + i * 4].value}", end="|")
        print("")
    print("")

def generate_more(lst):
    poss=[]
    for i in range(4):
        for j in range(4):
            if lst[j+i*4].value==0:
                poss.append((i,j))
    chosen = random.choice(poss)
    val = 2*random.randint(1,2)
    bl = block(val)

    lst[chosen[0]*4+chosen[1]]=bl

def compress_and_merge(line):
    line = [i for i in line if i.value != 0]  # remove zeros
    merged = []
    i = 0
    while i < len(line):
        if i + 1 < len(line) and line[i].value == line[i + 1].value:
            merged.append(block(2 * line[i].value))
            i += 2  # skip the next one
        else:
            merged.append(block(line[i].value))
            i += 1
    while len(merged) < 4:
        merged.append(block(0))
    return merged


def update_gui():
    for i in range(4):
        for j in range(4):
            bl = block(lst[i * 4 + j].value)
            cells[i][j].config(text=str(bl.value) if bl.value != 0 else "", bg=bl.color)

def move(dir):
    moved = False
    if dir == 'Up':
        for i in range(4):
            old = get_col(lst, i)
            new = compress_and_merge(old)
            if [b.value for b in old] != [b.value for b in new]:
                moved = True
            set_col(lst, i, new)
    elif dir == 'Down':
        for i in range(4):
            old = get_col(lst, i)[::-1]
            new = compress_and_merge(old)
            new = new[::-1]
            if [b.value for b in get_col(lst, i)] != [b.value for b in new]:
                moved = True
            set_col(lst, i, new)
    elif dir == 'Left':
        for i in range(4):
            old = get_row(lst, i)
            new = compress_and_merge(old)
            if [b.value for b in old] != [b.value for b in new]:
                moved = True
            set_row(lst, i, new)
    elif dir == 'Right':
        for i in range(4):
            old = get_row(lst, i)[::-1]
            new = compress_and_merge(old)
            new = new[::-1]
            if [b.value for b in get_row(lst, i)] != [b.value for b in new]:
                moved = True
            set_row(lst, i, new)
    if moved:
        generate_more(lst)
        update_gui()

def on_key(event):
    if event.keysym in ['Up', 'Down', 'Left', 'Right']:
        move(event.keysym)

game = tk.Tk()
game.title("2048")
cells=[]

color_map = {
    0: "#cdc1b4", 2: "#eee4da", 4: "#ede0c8", 8: "#f2b179", 16: "#f59563",
    32: "#f67c5f", 64: "#f65e3b", 128: "#edcf72", 256: "#edcc61", 512: "#edc850",
    1024: "#edc53f", 2048: "#edc22e"
}

for i in range(4):
    row = []
    for j in range(4):
        frame = tk.Frame(game, width=100, height=100, bg='lightgrey', borderwidth=1, relief='solid')
        frame.grid(row=i, column=j)
        label = tk.Label(frame, text="", font=("Helvetica", 24), width=4, height=2, bg=color_map[0])
        label.pack(expand=True, fill="both")
        row.append(label)
    cells.append(row)

lst = start()
generate_more(lst)
update_gui()
game.bind("<Key>", on_key)
game.mainloop()
