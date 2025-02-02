from tkinter import Tk, Frame, Label, Button, LabelFrame
from tkinter import constants as const
from PIL import Image
from PIL.ImageTk import PhotoImage as PhImg
import random

EMOJI_SIZE = 100

COLOR = {
    "": "#ffffff",
    1: "#177fff",
    2: "#0a26c7",
    3: "#9018a8",
    4: "#c724c7",
    5: "#e31293",
    'b': "#ff0000",
}


class Box:
    is_bomb = False
    is_flag = False
    is_un_flag = False

    is_open = False

    def __init__(self, fr: LabelFrame, r: int, c: int):
        self.__col = c
        self.__row = r
        self.__bt = Button(fr, text=' ', width=100, height=100,
                           font=('Verdana', 13, 'bold'),
                           command=self.open_box
                           )
        self.__bt.bind('<Button-3>', self.__put_flag)
        self.__bt.grid(
            row=r, column=c,
            ipadx=1, ipady=1, padx=1, pady=1
        )

    def open_box(self):
        if self.is_flag or not game:
            return
        if self.is_open:
            sp_around = get_arround(self.__row, self.__col)
            count = 0
            for r, c in sp_around:
                count += 1 if btns[r][c].is_flag else 0

            if str(self.__bt["text"]) != str(count):
                return
            for r, c in sp_around:
                if not btns[r][c].is_open:
                    btns[r][c].open_box()
            return
        self.is_open = True
        box = [self.__row, self.__col]
        if not game or box in spf:
            return
        self.__bt["text"] = spc[self.__row][self.__col]
        self.__bt["relief"] = const.FLAT
        self.__coloring()
        if self.__bt['text'] == '':
            opening_space(self.__row, self.__col)

    def __put_flag(self, e):
        global spf
        if self.is_open or not game:
            return
        box = [self.__row, self.__col]

        if self.is_flag:  # remove
            self.__bt["image"] = ""
            self.is_flag = False
            lb_flags.plus()
            spf.remove(box)
        elif not lb_flags.is_empty:  # add
            self.flag()
            lb_flags.minus()
            spf.append(box)

        check()

    def __coloring(self):
        bt = self.__bt
        bt["fg"] = COLOR[bt["text"]]
        if bt["text"] == 'b':
            bt['text'] = ''
            bt['image'] = bomb
            game_over()

    def restart(self):
        self.__bt["text"] = ""
        self.__bt["image"] = ""
        self.__bt["relief"] = const.RAISED

        self.is_bomb = False
        self.is_flag = False
        self.is_un_flag = False
        self.is_open = False

    def un_flag(self):
        self.__bt["image"] = un_flag
        self.is_un_flag = True

    def bomb(self):
        self.__bt["image"] = bomb
        self.is_bomb = True

    def flag(self):
        self.__bt["image"] = flag
        self.is_flag = True


class MainButton:
    def __init__(self, fr: Frame):
        self.bt = Button(fr, command=restart, image=norm)
        self.bt.pack(anchor=const.S)

    def win(self):
        self.bt["image"] = win

    def norm(self):
        self.bt["image"] = norm

    def over(self):
        self.bt["image"] = over


class BombCounter:
    __bombs = 10
    _is_empty = False

    def __init__(self, fr: Frame):
        self.__lb = Label(fr, font=('Verdana', 13, 'bold'), text="10", fg='red', bg='black')
        self.__lb.pack(anchor=const.SW)

    def __updt(self):
        self.__lb["text"] = str(self.__bombs)

    def minus(self):
        self.__bombs -= 1
        self.__updt()

    def plus(self):
        self.__bombs += 1
        self.__updt()

    def restart(self):
        self.__bombs = 10
        self.__updt()

    @property
    def is_empty(self):
        return self.__bombs == 0


class Timer:
    __count = 0

    def __init__(self, fr: Frame):
        self.__lb = Label(fr, font=('Verdana', 13, 'bold'), text='0', fg='red', bg='black')
        self.__lb.pack(anchor=const.NE)
        self.restart()
        tk.after(1000, self.__timer)

    def restart(self):
        self.__count = 0
        self.__lb['text'] = self.__count
        tk.after(1000, self.__timer)

    def __timer(self):
        self.__lb['text'] = self.__count
        self.__count += 1
        if not game:
            return
        tk.after(1000, self.__timer)


def get_arround(row: int, col: int):
    # @formatter:off
    return [
        [row - 1, col - 1], [row - 1, col], [row - 1, col + 1],
        [row,     col - 1],                 [row,     col + 1],
        [row + 1, col - 1], [row + 1, col], [row + 1, col + 1],
    ]
    # @formatter:on


def check():
    global game
    if sorted(spf) == sorted(spb):
        game = False
        bt_main.win()


def randomizer():
    # бомбы
    sp = set()
    while len(sp) < 10:
        s = random.randint(0, 100)
        sp.add(s)

    # где бомбы
    spb = []
    for i in sp:
        spb.append([i // 10, i % 10])

    # цифры бомб
    spc = []
    for r in range(10):
        line = []
        for c in range(10):
            if [r, c] in spb:
                line.append('b')
                continue
            sp_around = get_arround(r, c)
            d1 = 0
            for d in sp_around:
                if d in spb:
                    d1 += 1
            if d1 == 0:
                d1 = ""
            line.append(d1)
        spc.append(line)
    return spc, spb


def opening_space(r, c):
    sp_around = get_arround(r, c)
    for r, c in sp_around:
        if not (0 <= r <= 9) or not (0 <= c <= 9): continue

        bt = btns[r][c]
        if bt.is_open: continue

        bt.open_box()


def restart():
    global spc, spb, spf, game
    spc, spb = randomizer()
    spf = []
    game = True
    lb_timer.restart()
    lb_flags.restart()
    bt_main.norm()
    for r in range(10):
        for c in range(10):
            btns[r][c].restart()


def game_over():
    global game
    game = False
    bt_main.over()

    for r, c in spb:
        if [r, c] not in spf:
            btns[r][c].bomb()

    for r, c in spf:
        if [r, c] not in spb:
            btns[r][c].un_flag()


def window_size(ev):
    global flag, un_flag, bomb
    new_width = ev.width // 10
    new_height = (ev.height - 188) // 10
    if new_width > 10 and new_height > 10:

        flag = create_img_tk("imgs/flag.png", new_height, new_width)
        bomb = create_img_tk("imgs/bomb.png", new_height, new_width)
        un_flag = create_img_tk("imgs/neflag.png", new_height, new_width)

        for r in range(10):
            for c in range(10):
                bt = btns[r][c]

                if bt.is_flag:
                    bt.flag()
                elif bt.is_bomb:
                    bt.bomb()
                elif bt.is_un_flag:
                    bt.un_flag()


# region window -------------------------
tk = Tk()
tk.title('Сапёр')
spc, spb = randomizer()
spf = []
game = True
cur_sess = 1
tk.geometry('500x688')
tk.bind('<Configure>', window_size)
tk.iconbitmap("imgs/sapper.ico")


# endregion


# region img ----------------------------
def create_img_tk(path: str, hieght: int, width: int = 0):
    if width == 0:
        width = hieght
    img = Image.open(path).resize((width, hieght))
    return PhImg(img)


# bomb = create_img_tk("imgs/bomb.png", 50)
# un_flag = create_img_tk("imgs/neflag.png", 50)
# flag = create_img_tk("imgs/flag.png", 50)

win = create_img_tk("imgs/win.png", EMOJI_SIZE)
norm = create_img_tk("imgs/norm.png", EMOJI_SIZE)
over = create_img_tk("imgs/over.png", EMOJI_SIZE)
# endregion
# region top ----------------------------
fr_top = Frame()
fr_top.pack(fill=const.BOTH)

lb_flags = BombCounter(fr_top)
bt_main = MainButton(fr_top)
lb_timer = Timer(fr_top)
# endregion
# region body ---------------------------
fr_body = LabelFrame(bg='#7f7f7f')
fr_body.pack()
btns = []

for row in range(10):
    fr_body.columnconfigure(row, weight=1, )
    fr_body.rowconfigure(row, weight=1, )
    line = []
    for col in range(10):
        bt = Box(fr_body, row, col)
        line.append(bt)
    btns.append(line)

# endregion

tk.mainloop()
