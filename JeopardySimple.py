# -*- coding: utf-8 -*-
"""
Created on Mon Feb 14 12:24:43 2022

@author: user190344
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Feb  7 12:08:39 2022

@author: user190344
"""
import tkinter as tk
#import random
import ctypes

ctypes.windll.shcore.SetProcessDpiAwareness(1)

class InvalidGameFile(Exception):
    pass



class IllegalCategoryCount(Exception):
    pass


class IllegalPointsCount(Exception):
    pass

class GameTile:
    def __init__(self, category='', points=0, question='', answer=''):
        self.category = category  # The question category
        self.points = points  # The point value of this question
        self.question = question  # The question
        self.answer = answer  # The answer

    def __str__(self):  # This method creates a string representation of this object
        # Let's store all of our properties in a dict object
        result = {'category': self.category,
                  'points': self.points,
                  'question': self.question,
                  'answer': self.answer}

        # Now we can convert the dict to a string which will give us friendly formatting
        return str(result)

    def __repr__(self):
        # This method also creates a String representation of a Python object
        # The Python debugger calls this method rather than __str__
        # But we can just reuse our code by calling __str__
        return self.__str__()
    

    
    
def readGameBoard(gameFile):
    # Read the entire file into memory
    rawLines = open(gameFile, 'r', encoding='utf-8').readlines()
    
    fileLines = []
    for line in rawLines:
        # remove any '\n' characters and store them in fileLines
        fileLines.append(line.strip())

   
    #split by ::
    #[0] holds topics
    categories = fileLines[0].split('::')
    
    
    
    #[1] holds points
    points = []  
    pointValues = fileLines[1].split('::')
    
    # change str to int
    for pv in pointValues:
       
        points.append(int(pv))
        
    qsttile = {}  # Store all of the questions here
    
    # Read the rest of the file
    for line in fileLines[2:]:  # Ignore categories and points in file
        #split
        parts = line.split('::')
        #Check categories and points against cat/pt list
        if parts[0] in categories and int(parts[1]) in points:
            # Make Gametiles
            gameTile = GameTile(category=parts[0],
                                points=int(parts[1]),
                                question=parts[2],
                                answer=parts[3])
            # Make a new list for a new category in nested list
            if parts[0] not in qsttile:
                qsttile[parts[0]] = []
                qsttile[parts[0]].append(gameTile)
            else:
                # or add to existing list
                qsttile[parts[0]].append(gameTile)
                
    return qsttile, categories # Return dictionary and category list


        
        
def Gamescreen():
        
        
        
    root = tk.Tk()
    root.state('zoomed') #Windows
    #root.attributes('-zoomed', True) #Linux
    root.configure(bg='dodgerblue')
    root.title('English Jeopardy')
    
                
    #split root into different sections rows and columns
    root.rowconfigure([0,1,2,3,4,5,6], weight=1,pad=2)
    root.columnconfigure([0,1,2,3,4], weight=1, pad=2)
    #Category frame for holding section titles
    catfrm = tk.Frame(root, bg='dodgerblue') 
    catfrm.grid(row=1, column=0, columnspan=5, sticky='news',pady=0, padx=0 )
    catfrm.columnconfigure([0,1,2,3,4], weight=1)
    catx=0
        
    #initialize lists to hold buttons and qsttile
    qbtns= []
    qsttiletlist = []
    qbtncnt=0
        
        
            
    #Read file with questions
    qsttile, categories = readGameBoard('questionsactive.txt')
    for k in categories:
        catlbl = tk.Label(catfrm, text=k)
        catlbl.grid(row=1, column=catx, sticky='nsew',pady=0, padx=0)
        btnrow=2
        for j in qsttile[k]:
            qsttiletlist.append(j)
            #create button that calls btnclick when pressed
            qbtns.append(tk.Button(root, text=j.points, 
                            command=lambda c=qbtncnt: btnclick(qsttiletlist[c],qbtns[c])))
            qbtns[qbtncnt].grid(row=btnrow, column=catx, sticky='news',
                                    pady=0, padx=0)
            btnrow=btnrow+1
            qbtncnt=qbtncnt+1
        catx+=1
        
       
       
    def btnclick(btncall, qbtns):
        #print(btncall.question)
        qbtns.destroy()
        qstmenu=tk.Tk()
        qstmenu.configure(bg='dodgerblue')
        qstmenu.title(btncall.category)
        qstmenu.state('zoomed') #windows
        qstbtn = tk.Button(qstmenu, text='Question:' + btncall.question, font=("Helvetica",50), 
                          wraplength= qstmenu.winfo_screenwidth(), bg='dodgerblue',
                          command=lambda :QuestionClick(btncall, qstmenu) )
        qstbtn.grid(row=0, column=0)
        
        extbtn = tk.Button(qstmenu, text='exit', bg='white', 
                           command= qstmenu.destroy) #windows, test on linux
        extbtn.grid(row=2)
        
    def QuestionClick(btncall, qstmenu):
        anslbl= tk.Label(qstmenu, text='Answer:' + btncall.answer, 
                         font=("Helvetica",50), bg='dodgerblue',
                         wraplength= qstmenu.winfo_screenwidth())
        anslbl.grid(row=1)
    return root
        #qstmenu.attributes('-zoomed', True) #linux
        
# =============================================================================
#    start startmenu()    
# =============================================================================
    
        
# =============================================================================
# end def
# =============================================================================

root = Gamescreen()

root.mainloop()
