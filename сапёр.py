from tkinter import *
from PIL import Image, ImageTk
from fig import fig


def timelb(count,s):
    lb2['text'] = count
    if game and not s in spr:
        tk.after(1000, lambda count=count,s=s: timelb(count,s), count+1)

def prov():
    global game
    if sorted(spf)==sorted(spb):
        game=False
        bt1['image']=photow

def zan():
    global game,spc,spb,spf,ch,r,spr
    sp=fig()
    spc,spb=sp
    spf=[]
    game=True 
    q=r
    spr.append(q)
    r+=q
    timelb(0,r)
    lb['text']='10'
    bt1['image']=photon
    ch=10
    for i in range(10):
        for z in range(10):
            bts[i][z]['image']=''
            bts[i][z]['text']=' '
            bts[i][z]['relief']=RAISED

def razm(ev):
    new_width = ev.width//10
    new_height = ev.height//10
    if new_width>10 or new_height>10:
        
        image = copy_fl.resize((new_width, new_height))
        photo11 = ImageTk.PhotoImage(image) 
        
        image = copy_bom.resize((new_width, new_height))
        photo22 = ImageTk.PhotoImage(image)
        
        image = copy_nefl.resize((new_width, new_height))
        photo33 = ImageTk.PhotoImage(image) 
        
        for i in range(10):
            for z in range(10):
                if bts[i][z]['image'] !='':
                    
                    if [i,z] in spf:
                        bts[i][z].config(image = photo11)
                        bts[i][z].image = photo11 
                        if not game and not [i,z] in spb:
                            bts[i][z].config(image = photo33)
                            bts[i][z].image = photo33 
                    
                    else:
                        bts[i][z].config(image = photo22)
                        bts[i][z].image = photo22

                    

def ov():
    global game 
    game=False 
    bt1['image']=photoo 
    for i in range(10):
        for z in range(10):
            if [i,z] in spf:
                if not [i,z] in spb:
                    bts[i][z]['image']=photo3
            elif [i,z] in spb:
                bts[i][z]['image']=photo2

def cvet(a,b):
    if bts[a][b]['text']==1: bts[a][b]['fg']='#177fff'
    elif bts[a][b]['text']==2: bts[a][b]['fg']='#0a26c7'
    elif bts[a][b]['text']==3: bts[a][b]['fg']='#9018a8'
    elif bts[a][b]['text']==4: bts[a][b]['fg']='#c724c7'
    elif bts[a][b]['text']==5: bts[a][b]['fg']='#e31293'
    elif bts[a][b]['text']=='b':
        bts[a][b]['fg']='#ff0000'
        bts[a][b]['text']=''
        bts[a][b]['image']=photo2
        ov()

def otkr(r,c):
    bts[r][c]['text'] = spc[r][c]
    bts[r][c]['relief']= FLAT
    cvet(r,c)
    sp3=[
        [r-1,c-1],[r-1,c], [r-1,c+1],
        [r,c-1],                [r,c+1],
        [r+1,c-1],[r+1,c],[r+1,c+1],
    ]
    for i in sp3:
        if i[0]>9 or i[1]>9: continue
        if i[0]<0 or i[1]<0: continue
        if bts[i[0]][i[1]]['relief']== FLAT and bts[i[0]][i[1]]['image']=='': continue
        bts[i[0]][i[1]]['text'] = spc[i[0]][i[1]]
        cvet(i[0], i[1])
        bts[i[0]][i[1]]['relief']= FLAT
        if spc[i[0]][i[1]]=='': otkr(i[0],i[1])

def click(ro, co):
    if game and (not [ro,co] in spf):
        bts[ro][co]['text'] = spc[ro][co]
        bts[ro][co]['relief']= FLAT 
        if bts[ro][co]['text']=='': otkr(ro,co)
        else: cvet(ro,co)
    
def click1(row,col):
    global ch,game
    if ch==0 or bts[row][col]['relief']==FLAT:
        game=False
    if game and bts[row][col]['image']=='':
        bts[row][col]['image']= photo1
        ch-=1
        lb['text']=str(ch)
        spf.append([row,col])
    elif game or not bts[row][col]['image']=='' :
        bts[row][col]['image']= ''
        ch+=1
        lb['text']=str(ch)
        spf.remove([row,col])
    game=True
    prov()


#игра------------------------------------------------
tk=Tk()
tk.title('Сапёр')
sp=fig()
spc,spb=sp
spf=[]
game=True
tk.geometry('500x500')

# картинки-----------------------------------------
a=50
fl=Image.open("flag.png")
copy_fl=fl.copy()
copy_fl=copy_fl.resize((a,a))
photo1 = ImageTk.PhotoImage(copy_fl)

bom=Image.open("bomb.png")
copy_bom=bom.copy()
copy_bom=copy_bom.resize((a,a))
photo2 = ImageTk.PhotoImage(copy_bom)

nefl=Image.open("neflag.png")
copy_nefl=nefl.copy()
copy_nefl=copy_nefl.resize((a,a))
photo3 = ImageTk.PhotoImage(copy_nefl)
#смаилы
b=100
win=Image.open("win.png")
copy_win=win.copy()
copy_win=copy_win.resize((b,b))
photow = ImageTk.PhotoImage(copy_win)

norm=Image.open("norm.png")
copy_norm=norm.copy()
copy_norm=copy_norm.resize((b,b))
photon = ImageTk.PhotoImage(copy_norm)

over=Image.open("over.png")
copy_over=over.copy()
copy_over=copy_over.resize((b,b))
photoo = ImageTk.PhotoImage(copy_over)


bts=[]
tk.bind('<Configure>',razm)

# верх----------------------------------------------
fr1=Frame()
fr1.pack(fill=BOTH)
ch=10
r=1
spr=[]
lb=Label(fr1,font=('Verdana', 13, 'bold'),text="10",fg='red',bg='black')
lb.pack(anchor=SW)
bt1=Button(fr1,
command=zan,image=photon)
bt1.pack(anchor=S)
lb2=Label(fr1,font=('Verdana', 13, 'bold'),text='11',fg='red',bg='black')
lb2.pack(anchor=NE)


# низ-----------------------------------------------
fr=LabelFrame(bg='#7f7f7f')
fr.pack()
for row in range(10):
    fr.columnconfigure(row, weight=1,)
    fr.rowconfigure(row, weight=1, )
    line = []
    for col in range(10):
        bt = Button(fr, text=' ',width=100, height=100, 
                        font=('Verdana', 13, 'bold'),
                        command=lambda row=row, col=col: click(row,col)
                        )
        bt.bind('<Button-3>',lambda e, row=row, col=col: click1(row,col))
        bt.grid(
        row=row,
        column=col,
        ipadx=1,ipady=1,padx=1,pady=1
        )
        line.append(bt)
    bts.append(line)
timelb(0, r)
tk.mainloop()
