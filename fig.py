import random

def a(ch):
	sp=[]
	for i in ch:
		if i==0:
			sp.append('')
		else:
			sp.append(i)
	return sp

def fig(r=0,c=0):
    #бомбы
    sp=[]#i for i in range(10)]
    while len(sp)<10:
        s=random.randint(0,100)
        if not s in sp:
            sp.append(s)
    #где бомбы
    spb=[]
    for i in range(10):
        spb.append([sp[i]//10, sp[i]%10])
    #цифры бомб
    spc=[]
    for r in range(10):
        line=[]
        for c in range(10):
            if [r,c] in spb:
                line.append('b')
                continue
            sp3=[]
            sp3=[
                   [r-1,c-1],[r-1,c], [r-1,c+1],
                   [r,c-1],                [r,c+1],
                   [r+1,c-1],[r+1,c],[r+1,c+1],
                   ]
            d1=0
            for d in sp3:
                if d in spb:
                    d1+=1
            line.append(d1)
        spc.append(line)
    return [list(map(a,spc)),spb]
            



fig()