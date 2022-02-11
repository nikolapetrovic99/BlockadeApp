from typing import get_origin
from itertools import combinations
from itertools import *
from tkinter import *
from tkinter.font import Font
from tkinter import messagebox
from tkinter.ttk import Separator, Style
import queue
import pygame
import tkinter
import tkinter as tk
import time
import copy
 
m=11
n=14
greenwalls1=4
bluewalls1=4
greenwalls2=4
bluewalls2=4
fieldsaroundX=[]
fieldsaroundY=[]
zelenizid=Button
plavizid=Button
 
onmove=True
zid=False
 
firstclick=True
played=False
pawnorwall=True
 
pom=''
possiblemoves=list()
 
walls={
 
}
positions={}
 
pawn={
    "x1": (1,0),
    "x2": (4,1),
    "o1": (1,5),
    "o2": (3,5)
}
pawnstart={
    "x1": [(0,0), 'orange'],
    "x2": [(4,4), 'orange'],
    "o1": [(0,4), 'yellow'],
    "o2": [(4,0), 'yellow']
}
 
 
 
def FillGraphDefault(m, n):
    for i in range(0, m):
        for j in range(0, n):
            positions[(i,j)]=GetAllMoves(i, j)
def FillLists():
    for key,value in pawnstart.items():
        if key[0]=='x':
            for i in range(-1,2):
                for j in range(-1,2):
                    if (i == 0 or j == 0) and (i!=0 or j!=0):
                        fieldsaroundX.append((value[0][0]+i,value[0][1]+j))
        elif key[0]=='o':
                for i in range(-1,2):
                    for j in range(-1,2):
                        if (i == 0 or j == 0) and (i!=0 or j!=0):
                            fieldsaroundY.append((value[0][0]+i,value[0][1]+j))
 
 
 
def GetAllMoves(a, b):
    niz=list(map(lambda x, y: (x, y), list([a-1, a-1, a+1, a+1]), list([b-1, b+1, b-1, b+1])))
    niz1=list(map(lambda x, y: (x, y), list([a, a, a+2, a-2]), list([b-2, b+2, b, b])))
    niz2=[]
    for k in pawnstart.values():
        for i in range(-1,2):
            for j in range(-1,2):
                if (i == 0 or j == 0) and (i!=0 or j!=0):
                    if (k[0][0]+i,k[0][1]+j)==(a,b):
                        niz2.append(k[0])
                        #print(k[0]+(a,b))
    return list(x for x in niz1+niz+niz2 if valid_move(x, (m, n)))
 
 
def valid_move(move, size):
    if move[0]<size[0] and move[1]<size[1] and move[0]>=0 and move[1]>=0:
        return True
    return False
 
def GetPossibleMoves(positions,position,player,pawn): 
    lista=list(positions[position])
    if player:
        if position in fieldsaroundX:#u slucaju da se x nalazi polje od svoje baze onemogucava mu da skoci jednu kocku, posto su u listi dodati potezi za iks i oks za to
            if pawnstart["x1"][0] in lista:
                lista.remove(pawnstart["x1"][0])
            if pawnstart["x2"][0] in lista:
                lista.remove(pawnstart["x2"][0])
    else:
        if position in fieldsaroundY:
            if pawnstart["o1"][0] in lista:
                lista.remove(pawnstart["o1"][0])
            if pawnstart["o2"][0] in lista:
                lista.remove(pawnstart["o2"][0])
 
    for i in lista:#u slucaju da je pesak blokiran drugim pesakom u listu poteza mu se dodaje potez gde moze da skoci samo jedno polje
        if i in pawn.values() and i not in list(map(lambda x:x[0],pawnstart.values())):
            lista.remove(i)
            if position[0]==i[0]:
                if position[1]<i[1]:
                    lista.append((i[0],i[1]-1))
                else:
                    lista.append((i[0],i[1]+1))
            elif position[1]==i[1]:
                if position[0]<i[0]:
                    lista.append((i[0]-1,i[1]))
                else:
                    lista.append((i[0]+1,i[1]))
    return lista
def FindWallInfluence(c, type,walls):
    niz=list()
    if type=="green":#specijalni slucaj ako se zidovi stavljaju oko kuce, mora da izbaci ona polja koja ne postoje, spec dodata polja
        for k in pawnstart:
            for i in range(-1,1):
                for j in range(-1,1):
                    if (pawnstart[k][0][0]+i,pawnstart[k][0][1]+j)==c:
                        if j==-1:
                            niz.append([(pawnstart[k][0][0],pawnstart[k][0][1]-1), (pawnstart[k][0][0],pawnstart[k][0][1])])
                        else: 
                            niz.append([(pawnstart[k][0][0],pawnstart[k][0][1]+1), (pawnstart[k][0][0],pawnstart[k][0][1])])                        
        niz.append([(c[0]+1, c[1]), (c[0]+1, c[1]+2)])
        niz.append([(c[0]+1, c[1]), (c[0], c[1]+1)])
 
        niz.append([(c[0]+1, c[1]+1), (c[0], c[1])])
        niz.append([(c[0]+1, c[1]+1), (c[0]+1, c[1]-1)])
 
        niz.append([(c[0], c[1]), (c[0], c[1]+2)])
        niz.append([(c[0], c[1]-1), (c[0], c[1]+1)])
 
        if walls.get(((c[0], c[1]+1), 'blue')) is not None:#zidovi ne mogu da se preklapaju
            niz.append([(c[0], c[1]+1), (c[0]-1, c[1])])
        if walls.get(((c[0], c[1]-1), 'blue')) is not None:
            niz.append([(c[0]-1, c[1]+1), (c[0], c[1])])
 
        if walls.get(((c[0]+2, c[1]+1), 'blue')) is not None:
            niz.append([(c[0]+1, c[1]+1), (c[0]+2, c[1])])
        if walls.get(((c[0]+2, c[1]-1), 'blue')) is not None:
            niz.append([(c[0]+1, c[1]), (c[0]+2, c[1]+1)])
        #zeleni iznad ispod zelenog
        if walls.get(((c[0]-2, c[1]), 'green')) is not None:
            niz.append([(c[0], c[1]), (c[0]-1, c[1]+1)])
            niz.append([(c[0]-1, c[1]), (c[0], c[1]+1)])
        #zeleni zid ispod zelenog
        if walls.get(((c[0]+2, c[1]), 'green')) is not None:
            niz.append([(c[0]+1, c[1]), (c[0]+2, c[1]+1)])
            niz.append([(c[0]+2, c[1]), (c[0]+1, c[1]+1)])
 
    else:
        for k in pawnstart:
            for i in range(0,2):
                for j in range(-1,1):
                    if (pawnstart[k][0][0]+i,pawnstart[k][0][1]+j)==c:
                        if i==0:
                            niz.append([(pawnstart[k][0][0]-1,pawnstart[k][0][1]), (pawnstart[k][0][0],pawnstart[k][0][1])])
                        else: 
                            niz.append([(pawnstart[k][0][0]+1,pawnstart[k][0][1]), (pawnstart[k][0][0],pawnstart[k][0][1])])
        niz.append([(c[0]+1, c[1]), (c[0]-1, c[1])])
        niz.append([(c[0], c[1]+1), (c[0]-1, c[1])])
 
        niz.append([(c[0], c[1]), (c[0]-1, c[1]+1)])
        niz.append([(c[0]+1, c[1]+1), (c[0]-1, c[1]+1)])
 
        niz.append([(c[0], c[1]), (c[0]-2, c[1])])
        niz.append([(c[0], c[1]+1), (c[0]-2, c[1]+1)])
 
        if walls.get(((c[0], c[1]-1), 'green')) is not None:
            niz.append([(c[0], c[1]), (c[0]-1, c[1]-1)])
        if walls.get(((c[0], c[1]+1), 'green')) is not None:
            niz.append([(c[0], c[1]+1), (c[0]-1, c[1]+2)])
        if walls.get(((c[0]-2, c[1]-1), 'green')) is not None:
            niz.append([(c[0]-1, c[1]), (c[0], c[1]-1)])
        if walls.get(((c[0]-2, c[1]+1), 'green')) is not None:
            niz.append([(c[0]-1, c[1]+1), (c[0], c[1]+2)])
 
         #plavo desno 
        if walls.get(((c[0], c[1]+2), 'blue')) is not None:
            niz.append([(c[0], c[1]+1), (c[0]-1, c[1]+2)])
            niz.append([(c[0], c[1]+2), (c[0]-1, c[1]+1)])
        #plavi levo
        if walls.get(((c[0], c[1]-2), 'blue')) is not None:
            niz.append([(c[0], c[1]), (c[0]-1, c[1]-1)])
            niz.append([(c[0], c[1]-1), (c[0]-1, c[1])])
 
    return niz
 
 
def ClosedPath(positions,pawn):#provera da li je put od nekog pijuna do neke baze zatvoren
    if a_star(pawn["o1"],pawnstart["x1"][0],False,positions,pawn, False)==False  or a_star(pawn["o2"],pawnstart["x1"][0],False,positions,pawn, False)==False or a_star(pawn["o1"],pawnstart["x2"][0],False,positions,pawn, False)==False or a_star(pawn["o2"],pawnstart["x2"][0],False,positions,pawn, False)==False :
        return True
    elif a_star(pawn["x1"],pawnstart["o1"][0],True,positions,pawn, False)==False  or a_star(pawn["x2"],pawnstart["o1"][0],True,positions,pawn, False)==False or a_star(pawn["x1"],pawnstart["o2"][0],True,positions,pawn, False)==False or a_star(pawn["x2"],pawnstart["o2"][0],True,positions,pawn, False)==False :
        return True
 
def ValidWall(coords, type, walls):#da li se zid nalazi u opsegu table i da li se preklapa sa nekim zidovima
    if type=="green":
        if onmove ==True:
            if greenwalls1==0:
                return False
        else:
            if greenwalls2==0:
                return False
 
        if coords[0]>=m-1 or coords[1]>=n-1:
            return False
        if walls.get((coords, type)) or walls.get(((coords[0]-1, coords[1]), type)) or walls.get(((coords[0]+1, coords[1]), type)) or walls.get(((coords[0]+1, coords[1]), 'blue')):
            return False 
 
    else:
        if onmove ==True:
            if bluewalls1==0:
                    return False
        else:
            if bluewalls2==0:
                return False
 
        if coords[0]==0 or coords[1]>=n-1:
                return False
        if walls.get((coords, type)) or walls.get(((coords[0], coords[1]-1), type)) or walls.get(((coords[0], coords[1]+1), type)) or walls.get(((coords[0]-1, coords[1]), 'green')):
                return False 
 
    return True
 
def AddWall(coords, type, walls, greenwalls1, bluewalls1, greenwalls2, bluewalls2):
    walls[(coords, type)]=type
    if type=="green":
        if onmove is True:
            greenwalls1-=1
            zelenizid.config(text=greenwalls2)
        else:
            greenwalls2-=1
            zelenizid.config(text=greenwalls1)
 
    else: 
        if onmove is True:
            bluewalls1-=1
            plavizid.config(text=bluewalls2)
        else:
            bluewalls2-=1
            plavizid.config(text=bluewalls1)
    return [greenwalls1, bluewalls1, greenwalls2, bluewalls2]        
 
def IsEnd(p,pawn):
    if pawn["o1"] == pawnstart["x1"][0] or pawn["o1"] == pawnstart["x2"][0] or pawn["o2"] == pawnstart["x1"][0] or pawn["o2"] == pawnstart["x2"][0]:
        if p==True:
            msg=messagebox.showinfo( title="Kraj", message="Pobedio je O!" )
            window.quit()
        else:
            return True
    elif pawn["x1"] == pawnstart["o1"][0] or pawn["x1"] == pawnstart["o2"][0] or pawn["x2"]== pawnstart["o1"][0] or pawn["x2"] == pawnstart["o2"][0]:
        if p==True:
            msg=messagebox.showinfo( title="Kraj", message="Pobedio je X!" )
            window.quit()
        else:
            return True
 
def ProcessWall(coordinates, type,positions,walls,pawn):
    global greenwalls1, bluewalls1, greenwalls2, bluewalls2
    if ValidWall(coordinates, type,walls):
        ppp=copy.deepcopy(positions)
        niz=FindWallInfluence(coordinates, type,walls)
        for i in niz:
            try:
                positions[i[0]].remove(i[1])
            except:
                continue
            try:
                positions[i[1]].remove(i[0])
            except:
                continue
        if ClosedPath(positions,pawn):
            print("zatvoren put")
            return ppp
    else:
        print("nevalidan potez za zid")
        return False
    brojzidova= AddWall(coordinates, type ,walls, greenwalls1, bluewalls1, greenwalls2, bluewalls2)
    greenwalls1=brojzidova[0]
    bluewalls1=brojzidova[1]
    greenwalls2=brojzidova[2]
    bluewalls2=brojzidova[3]
    return True
listastanja=[]
def ComputerPlays(firstplayer, positions, walls, pawn):
        global firstclick, pawnorwall, onmove,greenwalls1, bluewalls1, greenwalls2, bluewalls2
        if (greenwalls1+bluewalls1+greenwalls2+bluewalls2)==0:
            minmax=alpha_beta([positions,walls,copy.deepcopy(pawn),onmove,firstplayer, greenwalls1, bluewalls1, greenwalls2, bluewalls2],3,-1000,1000)
        else:
             minmax=alpha_beta([positions,walls,copy.deepcopy(pawn),onmove,firstplayer, greenwalls1, bluewalls1, greenwalls2, bluewalls2],1,-1000,1000)
        for i,j in pawn.items():
            dugmici[j[0]*n+j[1]].config(text="")
        if len(minmax)>0:
            for k in minmax[1].keys():
                if k[1]=="green":
                    can=Canvas(width=7,height=40,bg="green",highlightthickness=0)
                    can.grid(column=int(k[0][1]*2)+1, row=int(k[0][0]*2),sticky="nesw")
                    can=Canvas(width=7,height=7,bg="green",highlightthickness=0)
                    can.grid(column=int(k[0][1]*2+1), row=int(k[0][0]*2+1),sticky="nesw")
                    can=Canvas(width=7,height=40,bg="green",highlightthickness=0)
                    can.grid(column=int(k[0][1]*2+1), row=int(k[0][0]*2+2),sticky="nesw")
                else:
                    can=Canvas(width=38,height=7,bg="blue",highlightthickness=0)
                    can.grid(column=int(k[0][1]*2), row=int(k[0][0]*2)-1,sticky="nesw")
                    can=Canvas(width=7,height=7,bg="blue",highlightthickness=0)
                    can.grid(column=int(k[0][1]*2)+1, row=int(k[0][0]*2)-1,sticky="nesw")
                    can=Canvas(width=38,height=7,bg="blue",highlightthickness=0)
                    can.grid(column=int(k[0][1]*2)+2, row=int(k[0][0]*2)-1,sticky="nesw")
        if len(minmax)>1:
            for i,j in minmax[2].items():
                dugmici[j[0]*n+j[1]].config(text=i)
        onmove=not onmove
        firstclick=True
        pawnorwall=True
        return minmax
 
 
def ProcessWallWithoutChanges(coordinates, type,positions,walls,pawn, greenwalls1, bluewalls1, greenwalls2, bluewalls2):
    if ValidWall(coordinates, type,walls):
        niz=FindWallInfluence(coordinates, type,walls)
        for i in niz:
            try:
                positions[i[0]].remove(i[1])
            except:
                continue
            try:
                positions[i[1]].remove(i[0])
            except:
                continue
        if ClosedPath(positions,pawn):
            return False
    else:
        return False
 
    return AddWall(coordinates, type, walls, greenwalls1, bluewalls1, greenwalls2, bluewalls2)
 
def Start():
    print("prvi igrac: ", str(firstplayer.get()))
    global m, n, greenwalls1, bluewalls1, greenwalls2, bluewalls2
    global firstclick, possiblemoves,positions, onmove, pawnorwall,pawn,walls, pomy
    m=int(spinboxm.get())
    n=int(spinboxn.get())
    greenwalls1=greenwalls2=int(spinboxgreen.get())
    bluewalls1=bluewalls2=int(spinboxblue.get())
    pawnstart["x1"][0]=pawn["x1"]=(3,3)#int(inputx1x.get("1.0",END)), int(inputx1y.get("1.0",END))
    pawnstart["x2"][0]=pawn["x2"]=(7,3)#int(inputx2x.get("1.0",END)), int(inputx2y.get("1.0",END))
    pawnstart["o1"][0]=pawn["o1"]=(3,10)#int(inputy1x.get("1.0",END)), int(inputy1y.get("1.0",END))
    pawnstart["o2"][0]=pawn["o2"]=(7,10)#int(inputy2x.get("1.0",END)), int(inputy2y.get("1.0",END))
    FillLists()
 
    for i in widgeti:
        i.destroy()
    DrawTable()
    for i, j in pawnstart.items():
        print(j[0])
        if i=="x1" or i=="x2":
            dugmici[j[0][0]*n+j[0][1]].config(bg="orange")
        else:
            dugmici[j[0][0]*n+j[0][1]].config(bg="yellow")
    FillGraphDefault(m, n)
    window.update()
    if str(firstplayer.get()) == "1":
        stanje=ComputerPlays("x1", positions, walls, pawn)
        positions=stanje[0]
        walls=stanje[1]
        pawn=stanje[2]
        greenwalls1=stanje[5]
        bluewalls1=stanje[6]
        greenwalls2=stanje[7]
        bluewalls2=stanje[8]
 
 
 
 
 
def DrawTable():
    for i in range(0,2*m,1):
        for j in range(0,2*n,1):
            if i%2==0:
                if j%2==0:
                    btn = Button(window, text="",width=4,height=2,command=lambda x=i,y=j:click(x,y))
                    btn.grid(column=j, row=i,padx=0,pady=0)
                    dugmici.append(btn)
                else:
                    window.rowconfigure(i,pad=0,minsize=7)
                    window.columnconfigure(j,pad=0,minsize=7)
            else:
                window.rowconfigure(i,pad=0,minsize=7)
                window.columnconfigure(j,pad=0,minsize=7)
    dugmici[pawn["x1"][0]*n+pawn["x1"][1]].config(text="x1")
    dugmici[pawn["x2"][0]*n+pawn["x2"][1]].config(text="x2")
    dugmici[pawn["o1"][0]*n+pawn["o1"][1]].config(text="o1")
    dugmici[pawn["o2"][0]*n+pawn["o2"][1]].config(text="o2")
    global zelenizid, plavizid
    zelenizid = Button(window, text=greenwalls1,width=4,height=2,command=zidzelen, bg="green")
    zelenizid.grid(column=2*m+6, row=6)
    plavizid = Button(window, text=bluewalls1,width=4,height=2,command=zidplav, bg="blue")
    plavizid.grid(column=2*m+6, row=4)
 
 
def h_function(start,end):
    return (abs(end[0]-start[0])+abs(end[1]-start[1]))
def a_star(start,end,player,positions,pawn, optimizacija):
    found_end = False
    open_set = set()
    closed_set = set()
    g = {}
    prev_nodes = {}
    g[start] = 0
    prev_nodes[start] = None
    open_set.add(start)
    while len(open_set) > 0 and (not found_end):
        node = None
        for next_node in open_set:
            if node is None or g[next_node] + h_function(next_node,end) < g[node] +h_function(node,end):
                node = next_node
        if node==end:
            found_end = True
            break
        for destination in GetPossibleMoves(positions,node,player,pawn):
            if destination not in open_set and destination not in closed_set:
                open_set.add(destination)
                prev_nodes[destination] = node
                g[destination] = g[node] + 1
            else:
                if g[destination] > g[node] + 1:
                    g[destination] = g[node] + 1
                    prev_nodes[destination] = node
                    if destination in closed_set:
                        closed_set.remove(destination)
                        open_set.add(destination)
        open_set.remove(node)
        closed_set.add(node)
    if optimizacija:
        path = []
        if found_end:
            prev = end
            while prev_nodes[prev] is not None:
                path.append(prev)
                prev = prev_nodes[prev]
            path.append(start)
            path.reverse()
        return path
    else:
        if found_end:
            br:int = 1
            while prev_nodes[node] is not None:
                br+=1
                node = prev_nodes[node]
            return br
        return False
 
 
 
 
 
window = Tk()
window.title("Blockade")
window.geometry("")
firstplayer=tk.IntVar()
def zidplav():
    global zid
    zid=True
def zidzelen():
    global zid
    zid=False
def click(i,j):
    print(i,j)
    global firstclick
    global possiblemoves,positions
    global pom
    global onmove, pawnorwall, pawn, walls, greenwalls1, bluewalls1, greenwalls2, bluewalls2
 
    if pawnorwall is True:
        if firstclick is True:
            pom=dugmici[int(i/2*n+j/2)]['text']
            if onmove is True:
                if pom=='x1' or pom=='x2':
                    firstclick=False
                    coord=pawn[pom]
                    possiblemoves=GetPossibleMoves(positions,coord,onmove,pawn)
                    for k in possiblemoves:
                        dugmici[int(k[0]*n+k[1])].config(bg="red")
            else:
                if pom=='o1' or pom=='o2':
                    firstclick=False
                    coord=pawn[pom]
                    possiblemoves=GetPossibleMoves(positions,coord,onmove, pawn)
                    for k in possiblemoves:
                        dugmici[int(k[0]*n+k[1])].config(bg="red")
 
        elif firstclick is False:
            firstclick=True
            for k in possiblemoves:
                    if (i/2, j/2)==k:
                        if (onmove and (greenwalls1==0 and bluewalls1==0)) or (onmove==False and (greenwalls2==0 and bluewalls2==0)):
                            onmove=not onmove
                        else:
                            pawnorwall=not pawnorwall
                        l=pawn[pom]
                        dugmici[l[0]*n+l[1]].config(text="")
                        pawn[pom]=k
                        dugmici[k[0]*n+k[1]].config(text=pom)
                        IsEnd(True,pawn)
                    if pawnstart['x1'][0]==k or pawnstart['x2'][0]==k:
                        dugmici[int(k[0]*n+k[1])].config(bg=pawnstart["x1"][1])
                    elif pawnstart['o1'][0]==k or pawnstart['o2'][0]==k:
                        dugmici[int(k[0]*n+k[1])].config(bg=pawnstart["o1"][1])
                    else:
                        dugmici[int(k[0]*n+k[1])].config(bg="SystemButtonFace")
    else:
        if zid==True:
            procWall=ProcessWall((i/2,j/2), "blue",positions,walls,pawn)
            if procWall==True:
                onmove=not onmove
                pawnorwall=True   
                can=Canvas(width=38,height=7,bg="blue",highlightthickness=0)
                can.grid(column=j, row=i-1,sticky="nesw")
                can=Canvas(width=7,height=7,bg="blue",highlightthickness=0)
                can.grid(column=j+1, row=i-1,sticky="nesw")
                can=Canvas(width=38,height=7,bg="blue",highlightthickness=0)
                can.grid(column=j+2, row=i-1,sticky="nesw")
            elif procWall!=False:
                positions=procWall
 
        else:
            procWall=ProcessWall((i/2,j/2), "green",positions,walls,pawn)
            if procWall==True:
                onmove=not onmove
                pawnorwall=True   
                can=Canvas(width=7,height=40,bg="green",highlightthickness=0)
                can.grid(column=j+1, row=i,sticky="nesw")
                can=Canvas(width=7,height=7,bg="green",highlightthickness=0)
                can.grid(column=j+1, row=i+1,sticky="nesw")
                can=Canvas(width=7,height=40,bg="green",highlightthickness=0)
                can.grid(column=j+1, row=i+2,sticky="nesw")
            elif procWall!=False:
                positions=procWall
    window.update()
    if onmove==False and pawnorwall==True and str(firstplayer.get())=="2":
        stanje=ComputerPlays("o1", positions, walls, pawn)
        positions=stanje[0]
        walls=stanje[1]
        pawn=stanje[2]
        greenwalls1=stanje[5]
        bluewalls1=stanje[6]
        greenwalls2=stanje[7]
        bluewalls2=stanje[8]
        IsEnd(True,pawn)
    elif onmove==True and pawnorwall==True and str(firstplayer.get())=="1":
        stanje=ComputerPlays("x1", positions, walls, pawn)
        positions=stanje[0]
        walls=stanje[1]
        pawn=stanje[2]
        greenwalls1=stanje[5]
        bluewalls1=stanje[6]
        greenwalls2=stanje[7]
        bluewalls2=stanje[8]
        IsEnd(True,pawn)
 
 
 
dugmici=list()
widgeti=list()
label=tk.Label(window, text="m:", font=Font(family='Helvetica', size=20))
label.grid(column=0,row=0)
widgeti.append(label)
spinboxm = Spinbox(window, from_=11, to=22, font=Font(family='Helvetica', size=20), width=2)
spinboxm.grid(row=0, column=1)
widgeti.append(spinboxm)
label1=tk.Label(window, text="n:", font=Font(family='Helvetica', size=20))
label1.grid(row=1, column=0)
widgeti.append(label1)
 
spinboxn = Spinbox(window, from_=14, to=28, width=2, font=Font(family='Helvetica', size=20))
spinboxn.grid(row=1, column=1)
widgeti.append(spinboxn)
 
 
#broj zidova
label2=tk.Label(window, text="Blue:", font=Font(family='Helvetica', size=20))
label2.grid(row=0, column=3)
widgeti.append(label2)
 
spinboxblue = Spinbox(window, from_=1, to=18, width=2, font=Font(family='Helvetica', size=20))
spinboxblue.grid(row=0, column=4)
widgeti.append(spinboxblue)
 
label3=tk.Label(window, text="Green:", font=Font(family='Helvetica', size=20))
label3.grid(row=1, column=3)
widgeti.append(label3)
 
spinboxgreen = Spinbox(window, from_=1, to=18, width=2, font=Font(family='Helvetica', size=20))
spinboxgreen.grid(row=1, column=4)
widgeti.append(spinboxgreen)
 
#pozicijax
label4=tk.Label(window, text="x1(x):", font=Font(family='Helvetica', size=20))
label4.grid(row=2, column=0)
widgeti.append(label4)
 
inputx1x=tk.Text(window, height=1, width=2, font=Font(family='Helvetica', size=20))
inputx1x.grid(row=2, column=1)
widgeti.append(inputx1x)
 
label5=tk.Label(window, text="x1(y):", font=Font(family='Helvetica', size=20))
label5.grid(row=2, column=3)
widgeti.append(label5)
 
inputx1y=tk.Text(window, height=1, width=2, font=Font(family='Helvetica', size=20))
inputx1y.grid(row=2, column=4)
widgeti.append(inputx1y)
 
label5=tk.Label(window, text="x2(x):", font=Font(family='Helvetica', size=20))
label5.grid(row=3, column=0)
widgeti.append(label5)
 
inputx2x=tk.Text(window, height=1, width=2, font=Font(family='Helvetica', size=20))
inputx2x.grid(row=3, column=1)
widgeti.append(inputx2x)
 
label5=tk.Label(window, text="x2(y):", font=Font(family='Helvetica', size=20))
label5.grid(row=3, column=3)
widgeti.append(label5)
 
inputx2y=tk.Text(window, height=1, width=2, font=Font(family='Helvetica', size=20))
inputx2y.grid(row=3, column=4)
widgeti.append(inputx2y)
 
#pozicijay
label6=tk.Label(window, text="o1(x):", font=Font(family='Helvetica', size=20))
label6.grid(row=4, column=0)
widgeti.append(label6)
 
inputy1x=tk.Text(window, height=1, width=2, font=Font(family='Helvetica', size=20))
inputy1x.grid(row=4, column=1)
widgeti.append(inputy1x)
 
label7=tk.Label(window, text="o1(y):", font=Font(family='Helvetica', size=20))
label7.grid(row=4, column=3)
widgeti.append(label7)
 
inputy1y=tk.Text(window, height=1, width=2, font=Font(family='Helvetica', size=20))
inputy1y.grid(row=4, column=4)
widgeti.append(inputy1y)
 
label8=tk.Label(window, text="o2(x):", font=Font(family='Helvetica', size=20))
label8.grid(row=5, column=0)
widgeti.append(label8)
 
inputy2x=tk.Text(window, height=1, width=2, font=Font(family='Helvetica', size=20))
inputy2x.grid(row=5, column=1)
widgeti.append(inputy2x)
 
label9=tk.Label(window, text="o2(y):", font=Font(family='Helvetica', size=20))
label9.grid(row=5, column=3)
widgeti.append(label9)
 
inputy2y=tk.Text(window, height=1, width=2, font=Font(family='Helvetica', size=20))
inputy2y.grid(row=5, column=4)
widgeti.append(inputy2y)
 
 
radio1=tk.Radiobutton(window, text="X", value=1, variable=firstplayer)
radio1.grid(row=6, column=0)
widgeti.append(radio1)
radio2=tk.Radiobutton(window, text="O", value=2, variable=firstplayer)
radio2.grid(row=7, column=0)
widgeti.append(radio2)
 
 
#startbutton
 
buttonstart=tk.Button(window,text="Start",font=Font(family='Helvetica', size=10), width=8, command=Start)
buttonstart.grid(row=8, column=0, columnspan=6)
widgeti.append(buttonstart)
#inputtxt.destroy()
 
def best_move(stanje, iksoks):#trazi najkraci put i vraca minimalni put i putanju, mi uzimamo orvi element iz lista, to je najbolji potez
    a="x"
    if iksoks=="x":
        a="o"
    niz=list();
    niz.append(a_star(stanje[2][iksoks+"1"],pawnstart[a+"1"][0],True if a=="o" else False,stanje[0],stanje[2], True))
    niz.append(a_star(stanje[2][iksoks+"2"],pawnstart[a+"2"][0],True if a=="o" else False,stanje[0],stanje[2], True))
    niz.append(a_star(stanje[2][iksoks+"1"],pawnstart[a+"2"][0],True if a=="o" else False,stanje[0],stanje[2], True))
    niz.append(a_star(stanje[2][iksoks+"2"],pawnstart[a+"1"][0],True if a=="o" else False,stanje[0],stanje[2], True))
    min=niz[0]
    for i in niz:
        if len(min)>len(i):
            min=i
 
    for key, value in stanje[2].items():
        if value==min[0]:
            return (key, min[1])
 
 
def nova_stanja(stanje):
    listaa=[]
    if stanje[3]:
        stanje[3]=False
        if (greenwalls1+bluewalls1+greenwalls2+bluewalls2)==0:
            for i in GetPossibleMoves(stanje[0],stanje[2]["x1"],True,stanje[2]):#uzimamo sve mogucnosti za x1 i igramo ih
                stanjepom=copy.deepcopy(stanje)
                stanjepom[2]["x1"]=i
                listaa.append(stanjepom)
            for i in GetPossibleMoves(stanje[0],stanje[2]["x2"],True,stanje[2]):#uzimamo sve mog za x2 i ihramo ih, odlazimo u dubinu
                stanjepom=copy.deepcopy(stanje)
                stanjepom[2]["x2"]=i
                listaa.append(stanjepom)
            return listaa
 
        stanjepom=copy.deepcopy(stanje)  #u slucaju da ima zidova, sad posto ima zidova uzimamo samo 1 najbolji kako bi izvrsili optimizaciju    
        best=best_move(stanje, "x")#ako nema zidova uzima sve poteze, a ako ima onda samo najbolji(optimizacija), taj najbolji uparujemo sa svim zidovima
        stanjepom[2][best[0]]=best[1]
        for j in range(0,n):
            for k in range(0,m):
                for tip in ["blue","green"]:
                    stanjepom1=copy.deepcopy(stanjepom)
                    zidovipom=ProcessWallWithoutChanges((j,k),tip,stanjepom1[0],stanjepom1[1],stanjepom1[2], stanjepom1[5],  stanjepom1[6],  stanjepom1[7],  stanjepom1[8])
                    if zidovipom!=False:
                        for i in range(0,4):
                            stanjepom1[i+5]=zidovipom[i]
                        listaa.append(stanjepom1)   
    else:
        stanje[3]=True
        stanjepom=copy.deepcopy(stanje)
        best=best_move(stanje, "o")
        stanjepom[2][best[0]]=best[1]
        if (greenwalls1+bluewalls1+greenwalls2+bluewalls2)==0:
            listaa.append(stanjepom)
        else:
            for j in range(0,n):
                for k in range(0,m):
                    for tip in ["blue","green"]:
                        stanjepom1=copy.deepcopy(stanjepom)
                        zidovipom=ProcessWallWithoutChanges((j,k),tip,stanjepom1[0],stanjepom1[1],stanjepom1[2], stanjepom1[5],  stanjepom1[6],  stanjepom1[7],  stanjepom1[8])
                        if zidovipom!=False:
                            for i in range(0,4):
                                stanjepom1[i+5]=zidovipom[i]
                            listaa.append(stanjepom1)        
 
    return listaa
 
def udaljenost(stanje,xo,player):
    if xo=="x":
        o="o";
    else:
        o="x"
    a=a_star(stanje[2][xo+"1"],pawnstart[o+"1"][0],player,stanje[0],stanje[2], False)
    b=a_star(stanje[2][xo+"1"],pawnstart[o+"2"][0],player,stanje[0],stanje[2], False)
    c=a_star(stanje[2][xo+"2"],pawnstart[o+"1"][0],player,stanje[0],stanje[2], False)
    d=a_star(stanje[2][xo+"2"],pawnstart[o+"2"][0],player,stanje[0],stanje[2], False)
    return(a,b,c,d)
 
 
 
 
 
 
# 0-positions 1-walls 2-pawn 3-onmove 
def proceni_stanje(stanje):
    if stanje[3]==False:
        u=udaljenost(stanje,"x",True)
        x=min(u[3],min(u[2],min(u[0],u[1])))
        if (greenwalls1+bluewalls1+greenwalls2+bluewalls2)==0:
            return x
        else:
            u=udaljenost(stanje,"o",False)#slucaj kada imamo zidove
            x1=min(min(u[0],u[2]),min(u[1],u[3]))#proverava minimalni put za protivnika, 
            x2=u[0]+u[1]+u[2]+u[3];#zbir svih protivnika
            return x-(x1*2+x2)#prioritet ima najkraci put da se poveca
    else: 
        u=udaljenost(stanje,"o",False)
        x=min(u[3],min(u[2],min(u[0],u[1])))
        if (greenwalls1+bluewalls1+greenwalls2+bluewalls2)==0:
            return x
        else:
            u=udaljenost(stanje,"x",True)
            x1=min(min(u[0],u[2]),min(u[1],u[3]))
            x2=u[0]+u[1]+u[2]+u[3];
            return x-(x1*2+x2)
 
 
"""def min_value(stanje, dubina, alpha, beta):
    if dubina == 0:
        return (stanje, proceni_stanje(stanje))
    else:
        for s in nova_stanja(stanje):
            beta = min(beta,max_value(copy.deepcopy(s), dubina - 1, alpha, beta),key=lambda x: x[1])
            if beta[1] <= alpha[1]:
                return alpha
    return beta
brojac=0
def max_value(stanje, dubina, alpha, beta):
    global brojac
    brojac+=1
    if dubina == 0:
        return (stanje, proceni_stanje(stanje))
    else:
        for s in nova_stanja(stanje):
            alpha = max(alpha,min_value(copy.deepcopy(s), dubina - 1, alpha, beta),key=lambda x: x[1])
            if alpha[1] >= beta[1]:
               return beta
    return alpha"""
 
 
"""def minimax(stanje, dubina, moj_potez, alpha = (pawn["x1"], -999), beta = (pawn["x1"],999)):
    if moj_potez:
        return max_value(stanje, dubina, alpha, beta)
    else:
        return min_value(stanje, dubina, alpha, beta)"""
 
 
 
def minimax(stanje,minmax,depth,alpha,beta):
    if IsEnd(False,stanje[2]):
        if minmax==True:
            return (proceni_stanje(stanje))-depth
        else:
            return (proceni_stanje(stanje))+depth
    if depth == 0 :
        return (proceni_stanje(stanje))
    if minmax:
        best=-1000
        for i in nova_stanja(stanje):
            val=minimax(i,False,depth-1,alpha,beta)
            best=max(best,val)
            alpha=max(alpha,best)
 
            if beta<=alpha:
                break
        return best
    else:
        best=1000
        for i in nova_stanja(stanje):
            val=minimax(i,True,depth-1,alpha,beta)
            best=min(best,val)
            beta=min(beta,best)
            if beta<=alpha:
                break
        return best
 
 
 
 
def alpha_beta(stanje,depth,alpha,beta):
    best=1000
    if firstplayer.get()==1:
        player=True
    else:
        player=False
    najbolje_stanje=list()
    for i in nova_stanja(stanje):
        b=minimax(i,player,depth-1,alpha,beta)
        if b<best:
            best=b
            najbolje_stanje=i
    return najbolje_stanje
 
 
 
window.mainloop()