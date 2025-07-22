import math
import random
import tkinter as tk
import colorsys

def start():
    return [0] * size**2

def get_row(lst, row_index):
    return [lst[i] for i in range(row_index*size,row_index*size+size)]

def get_col(lst, col_index):
    return [lst[i] for i in range(col_index,col_index+size**2,size)]

def set_row(lst, row_index, row):
    for i in range(size):
        lst[size*row_index+i]=row[i]

def set_col(lst, col_index, col):
    for i in range(size):
        lst[col_index + size*i]=col[i]

def generate_more(lst):
    poss=[]
    for i in range(size):
        for j in range(size):
            if lst[j+i*size]==0:
                poss.append((i,j))
    chosen = random.choice(poss)
    val = 2*random.randint(1,2)

    lst[chosen[0]*size+chosen[1]]=val

def compress_and_merge(line):
    line = [i for i in line if i != 0]  # remove zeros
    merged = []
    i = 0
    while i < len(line):
        if i + 1 < len(line) and line[i] == line[i + 1] and line[i]< 2**num_of_cubes:
            merged.append(2 * line[i])
            i += 2  # skip the next one
        else:
            merged.append(line[i])
            i += 1
    while len(merged) < size:
        merged.append(0)
    return merged


def update_gui(lst, size):
    for i in range(size):
        for j in range(size):
            val = lst[i * size + j]
            cells[i][j].config(text=str(val) if val != 0 else "", bg=color_map[val])

def move(dir):
    moved = False
    if dir == 'Up':
        for i in range(size):
            old = get_col(lst, i)
            new = compress_and_merge(old)
            if old != new:
                moved = True
            set_col(lst, i, new)
    elif dir == 'Down':
        for i in range(size):
            old = get_col(lst, i)[::-1]
            new = compress_and_merge(old)
            new = new[::-1]
            if old[::-1]!=new:
                moved = True
            set_col(lst, i, new)
    elif dir == 'Left':
        for i in range(size):
            old = get_row(lst, i)
            new = compress_and_merge(old)
            if old != new:
                moved = True
            set_row(lst, i, new)
    elif dir == 'Right':
        for i in range(size):
            old = get_row(lst, i)[::-1]
            new = compress_and_merge(old)
            new = new[::-1]
            if old[::-1]!=new:
                moved = True
            set_row(lst, i, new)
    if moved:
        generate_more(lst)
        update_gui(lst, size)

def on_key(event):
    if event.keysym in ['Up', 'Down', 'Left', 'Right']:
        move(event.keysym)
        if winning(lst):
            game.unbind("<Key>")
            game_over_label = tk.Label(game, text="You're a winner!", font=("Calibri", 32), fg="green")
            game_over_label.grid(row=0, column=0, columnspan=size)
        elif not possible_next(lst):
            game.unbind("<Key>")
            game_over_label = tk.Label(game, text="Game Over!", font=("Calibri", 32), fg="red")
            game_over_label.grid(row=0, column=0, columnspan=size)

def map_colors(num):
    max_num = 2 ** num
    arr = [j for j in range(int(math.log2(max_num)) + 1)]
    values = [0]
    values.extend(list(map(lambda x: 2 ** x, arr)))

    cmap = {}
    for i,val in enumerate(values):
        h = i/len(values)
        r, g, b = colorsys.hsv_to_rgb(h,1,1)
        color = "#{:02x}{:02x}{:02x}".format(int(r*255), int(g*255), int(b*255))
        cmap[val] = color
    cmap[0]="#ffffff"
    return cmap

def possible_next(lst):
    for i in range(size):
        row = get_row(lst,i)
        col = get_col(lst,i)
        for j in range(size):
            if row[j]==0 or col[j]==0:
                return True
            if j < size - 1:
                if row[j] == row[j+1] and row[j]<2**num_of_cubes:
                    return True
                if col[j] == col[j+1] and col[j]<2**num_of_cubes:
                    return True
    return False

def winning(lst):
    return 2**num_of_cubes in lst



size = 4
num_of_cubes = 11
color_map = map_colors(num_of_cubes)

game = tk.Tk()
game.title("2048")
cells=[]

for i in range(size):
    row = []
    for j in range(size):
        frame = tk.Frame(game, width=100, height=100, bg='lightgrey', borderwidth=1, relief='solid')
        frame.grid(row=i, column=j)
        label = tk.Label(frame, text="", font=("Helvetica", 24), width=4, height=2, bg=color_map[0])
        label.pack(expand=True, fill="both")
        row.append(label)
    cells.append(row)

lst = start()
generate_more(lst)
update_gui(lst, size)
game.bind("<Key>", on_key)
game.mainloop()
