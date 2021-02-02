# -*- coding: utf-8 -*-
"""
Created on Sun Jan 17 23:37:38 2021

@author: Snorlax
"""

import tkinter as tk
import numpy as np
import sqlite3

#Connect to db
conn = sqlite3.connect("game1.db")
cur = conn.cursor()
#Create a table sqlite datatypes #NULL, #INTEGET, #REAL, #TEXT, #BLOB  IF NOT EXISTS
cur.execute("""CREATE TABLE IF NOT EXISTS old_game (
                game TEXT
                )""")
# Write changes
conn.commit()
conn.close()


class Counter(object):
    def __init__(self,txt_lbl):
        self.txt_lbl = txt_lbl
        self.value = 0
    def ContInc(self):
        self.value += 1
        self.txt_lbl.update_move(self.value)
    def CountReset(self):
        self.value = 0
        self.txt_lbl.update_move(self.value)
        self.txt_lbl.update_winner("            ")
        
class Board:
    def __init__(self, r, c, txt_lbl):
        self.list = ['white']*r*c
        self.status = False
        self.txt_lbl = txt_lbl
        
    def change(self,num, color, y, x):
        self.list[num] = color
        self.txt_lbl.update_x(x)
        self.txt_lbl.update_y(y)
        #print(self.list[num], num)
        
    def check_win(self):
        for i in range(n*n-5):
            if self.list[i] != 'white' and self.list[i] == self.list[i+1] and self.list[i+1] == self.list[i+2] \
                and self.list[i+2] == self.list[i+3] and self.list[i+3] == self.list[i+4]:
                self.status = True
            elif i < (n*n-4*n) and self.list[i] != 'white' and self.list[i] == self.list[i+n] \
                and self.list[i+n] == self.list[i+2*n] and self.list[i+2*n] == self.list[i+3*n]\
                    and self.list[i+3*n] == self.list[i+4*n]:
                self.status = True
            elif i < (n*n-(4*n+4)) and self.list[i] != 'white' and self.list[i] == self.list[i+n+1] and self.list[i+n+1] == self.list[i+2*n+2] \
                                   and self.list[i+2*n+2] == self.list[i+3*n+3] and self.list[i+3*n+3] == self.list[i+4*n+4]:
                self.status = True
            elif i < (n*n - (4*n-4)) and self.list[i] != 'white' and self.list[i] == self.list[i+n-1] \
                and self.list[i+n-1] == self.list[i+2*n-2] and self.list[i+2*n-2] == self.list[i+3*n-3]\
                    and self.list[i+3*n-3] == self.list[i+4*n-4]:
                self.status = True           
        return self.status
    
    def get_list_tuples(self): 
        res = [tuple(i.split(',')) for i in self.list]  
        res1 = range(n*n)
        res2 = tuple(zip(res1,self.list))
        return res
    
    def get_num_list_tuples(self): 
        res1 = range(n*n)
        res2 = tuple(zip(self.list,res1))
        return res2
        
    
    def write_old_game(self,new_list):
        self.list = new_list
        print("Updated")
        
    def BoardStatus(self):
        self.status = False

class ColorButton:
    def __init__(self,root, prow,pcol, counter, game_board,txt_lbl):
        self.txt_lbl = txt_lbl
        self.row = prow
        self.column = pcol
        self.root = root
        self.id = tk.Button(self.root, text='   ', bg='white', command=lambda: self.btncol(counter, game_board))
        self.id.grid(row=self.row, column=self.column)
        
    def btncol(self, counter, game_board):
        if counter.value%2:
            if self.id['bg'] == 'white':
                self.id.configure(bg='green')
                temp_num = int(self.row*n+self.column)
                game_board.change(temp_num, 'green', self.row, self.column)
            
                if game_board.check_win(): 
                    self.txt_lbl.update_winner("Winner Green") #print("Winner Green")
                else: pass
                counter.ContInc()
            else:
                pass
        else:
            if self.id['bg'] == 'white':
                self.id.configure(bg='red')
                temp_num = int(self.row*n+self.column)
                game_board.change(temp_num, 'red', self.row, self.column)
                
                if game_board.check_win(): 
                    self.txt_lbl.update_winner("Winner Red")#print("Winner Red")
                else: pass
                counter.ContInc()
            else:
                pass
 
    def btnUpdt(self,color):
        self.id.configure(bg=color)
    
class Labelz:
   def __init__(self,root,n):
       self.root = root
       self.xtxt = tk.Label(self.root, text="x-pos", anchor='w')
       self.xtxt.grid(row=2, column=n+1)
       self.xlbl = tk.Label(self.root, text=" ",anchor='w')
       self.xlbl.grid(row=3, column=n+1)
       self.ytxt = tk.Label(self.root, text="y-pos", anchor='w')
       self.ytxt.grid(row=2, column=n+2)
       self.ylbl = tk.Label(self.root, text=" ", anchor='w')
       self.ylbl.grid(row=3, column=n+2)
       self.ytxt = tk.Label(self.root, text="Moves", anchor='w')
       self.ytxt.grid(row=4, column=n+1)
       self.countlbl = tk.Label(self.root, text=" ", anchor='w')
       self.countlbl.grid(row=5, column=n+1)
       self.mess = tk.Label(self.root, text="           ", font=(None, 15),anchor='w')
       self.mess.grid(row=6, column=n+1, columnspan=2)
       
   def update_x(self,x):
       self.xlbl.configure(text=x)   
       
   def update_y(self,y):
       self.ylbl.configure(text=y)
       
   def update_move(self,move):
       self.countlbl.configure(text=move)
       
   def update_winner(self,winner):
       self.mess.configure(text=winner) 
     
class OtherButtons:
    def __init__(self,root,n,game_board, T, counter):
        self.root = root
        self.row = n+1
        self.btnexit = tk.Button(self.root, text='Exit', command=self.root.destroy)
        self.btnexit.grid(row=n, column=0, columnspan=4, ipadx=20)
        self.btnload = tk.Button(self.root, text='Load', command=lambda: self.DataLoad(n,game_board, T))
        self.btnload.grid(row=n, column=4, columnspan=4, ipadx=20)
        self.btnsave = tk.Button(self.root, text='Save', command=lambda: self.DataSave(n,game_board))
        self.btnsave.grid(row=n, column=8, columnspan=4, ipadx=20)
        self.btnclear = tk.Button(self.root, text='Clear', command=lambda: self.DataClear(n,T,counter,game_board))
        self.btnclear.grid(row=n, column=12, columnspan=4, ipadx=20)
   
    
    def DataSave(self,n,game_board): 
        #Connect to db
        conn = sqlite3.connect("game1.db")
        cur = conn.cursor()
        #Save satement
        cur.execute("SELECT COUNT(game) FROM old_game")
        row_count = cur.fetchone()[0]
        print(row_count)
        if row_count > 10:
            cur.executemany("UPDATE old_game SET game = ? WHERE oid=?", game_board.get_num_list_tuples())
        else:
            cur.executemany("INSERT INTO old_game VALUES (?)", game_board.get_list_tuples())        
        # Write changes
        conn.commit()
        conn.close()
        print("save successfull")
        
    def DataLoad(self,n,game_board, T):
        conn = sqlite3.connect("game1.db")
        cur = conn.cursor()
        #Load satement
        cur.execute("SELECT game FROM old_game")
        datas = cur.fetchall()           
        # Write changes
        conn.commit()
        conn.close()
        
        old_game_list = []
        for data in datas:
            old_game_list.append(data[0])
            
        game_board.write_old_game(old_game_list)
        for num,t in enumerate(T):
            t.btnUpdt(old_game_list[num])
            
    def DataClear(self,n,T,counter,game_board):
        clear_board_list = ['white']*n*n
        game_board.write_old_game(clear_board_list)
        for num,t in enumerate(T):
            t.btnUpdt(clear_board_list[num])
        counter.CountReset()
        game_board.BoardStatus()
        
       
root = tk.Tk()
root.title("Frame Viewer")
root.geometry("450x420")
n = 15       
txt_lbl = Labelz(root,n)
game_board = Board(n,n, txt_lbl)
counter = Counter(txt_lbl)
   
T = []
for i in range(n):
    for j in range(n):
       Btn = ColorButton(root, i,j, counter, game_board, txt_lbl) 
       T.append(Btn)

OtherButtons(root,n,game_board, T, counter)

root.mainloop()