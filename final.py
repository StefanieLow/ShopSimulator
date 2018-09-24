#---------------------------------------------------------------------
#Program Name: ??? - final.py
#Programmers: Stefanie Low and Pearl Kong
#Date: June 22, 2017
#Input: Name, difficulty, pricing, and amount of products to buy
#Processing: Stores name for ranking, sets different seasons and
#    difficulties (starting balance, items that will be bought,
#    number of customers that come in), keeps track of account
#    (balance, money spent, money earnt), creates random list of
#    stock items and customers (demographic, time they will spend
#    in store, whether or not they will buy an object), allows
#    customers to purchase items depending on their demographic
#    and the price, keeps track of time (1 hour = 15 seconds) and
#    days (game lasts for 10 days), calculates and updates scores
#Output: Prints screens for different parts of the game, a
#    window with a sun/moon and tree depending on time and season,
#    buttons that change screens, labels, blits necessary information
#    (account info, customers in store,items in catalogue, items in
#    store, prices, scores, etc.)
#---------------------------------------------------------------------
#import necessary modules
import random
import time
import tkinter as tk
from tkinter import *
import pygame
import os
import random
import sky

#colours for the sky
night = (0,24,72)
day = (139,201,236)
moon = [(252,251,227),(252,251,227),(252,251,227),(240,240,216),(240,240,216),(205,215,182),(250,242,248),(250,242,248),(235,239,201),(235,239,201)]
sun = [(230,230,0),(255,173,51),(255,215,0),(255,255,0),(250,250,210),(218,165,32),(255,204,0),(240,230,140),(255,250,205),(255,228,181)]

#general variables
difficulty = 0
cList = []
cInStore = []
user = ""
i = False
inPlay = True
dayNum = 0
drawB = True
yes = False
sellItems = []

#Customer class stores an agegroup, whether or not a purchase will be made, the time they will spend in store, and the time they entered the store
class Customer(object):
#class constructor
    def __init__(self, demographic, timeIn = 0):
        self.ageGroup = demographic
        self.timeIn = timeIn
        if self.ageGroup == 'Child': #chance that they will buy something varies depending on age
            chance = [0,0,0,1]
        elif self.ageGroup == 'Adult':
            chance = [0,1,1]
        else:
            chance = [0,1]
        self.buyChance = random.choice(chance)
        self.timeInStore = random.randrange(5,31) #can spend 5 to 30 seconds(20 minutes to 2 hours in-game) in the store
#SaleItem class stores an item's name, image, stock price, ideal price, stock quantity, demographic, season, if it's on sale, its sale price, and sale quantity
class SaleItem:
#class constructor
    def __init__ (self, name, imagePath, stockPrice, idealPrice, quantity, demographic, season):
        self.n = name
        self.imgPath = imagePath 
        self.stock = float(stockPrice)
        self.stockQuan = int(quantity)
        self.ideal = float(idealPrice)
        if demographic == " ": #File input for demographics is "all" as default
            self.demo = "All"
        else:
            self.demo = demographic
        self.onShelf = False 
        self.season = season
        self.sale = 0
        self.quan = 0
#function to pudate an item's sale price
    def changePrice(self, new):
        self.sale = new
#function to put an item on sale
    def putOnShelf(self):
        self.onShelf = True
#function to stop selling an item
    def outOfStock(self):
        self.onShelf = False
#function to load in an item's image
    def getImage(self):
        self.img = pygame.image.load(self.imgPath)
#Account class stores the balance, the money spent, and the money earned
class Account:
#class constructer 
    def __init__ (self, balance):
        self.balance = balance
        self.spent = 0
        self.earn = 0
#function to record amount spent when buying stock items 
    def Use(self, spent): 
        self.spent += spent
#function to record amount earned when selling items
    def Make(self, earned): 
        self.earn += earned
#function to update balance depending on money made and spent 
    def updateBalance(self): 
        self.balance -= self.spent
        self.balance += self.earn
        self.spent = 0
        self.earn = 0

#function to create list of customers
def createCust():
    global cList, num 
    num = random.choice(range(5-(difficulty)))#less customers can be created as difficulty increases
    for x in range(num):
        dem = random.choice(['Child','Adult','Senior'])
        cList.append(Customer(dem))
#function to have customers walk into the store
def walkIn():
    global cInStore, cList
    if len(cList) > 0:#only run if customers exist that haven't gone in yet
        for x in range(random.choice(range(len(cList)+1))):#random amount can go in at the same time
            cInStore.append(cList.pop())
            cInStore[-1].timeIn = time.time()
            doorbell.play()
#function to have customers walk out of the store
def walkOut():
    global cInStore, hour, account
    for x in cInStore: 
        if time.time() >= x.timeIn + x.timeInStore or hour == 17:#remove customers if their time limit is up or if the day is over
            if x.buyChance == 1:
                account = Buy(x, sellItems, season, account)
            cInStore.remove(x)
            doorbell.play()
#function to put item info into list
def createItems(fileName, catalogue): 
    file = open(fileName, "r") #open file, read info into catalogue, and return that list
    name = ""
    place = ""
    SP = 0
    IP = 0
    quan = 0
    demo = ""
    season = ""
    for item in range(58):
        item = file.readline().strip()
        name, place, SP, IP, quan, demo, season = item.split(",")
        temp = SaleItem(name, "Images/" + place, SP, IP, quan, demo, season)
        temp.getImage()
        catalogue.append(temp)
    file.close()
    return catalogue
#function to decide which item(s) a customer will buy depending on demographic, price, season, and availability
def Buy(customer, itemsOnShelf, gameSeason, account):
    for x in itemsOnShelf:
        if (customer.ageGroup == x.demo or x.demo == "All") and (x.quan > 0 and x.onShelf): 
            if x.sale < x.ideal: #less than ideal, (x.sale/x.ideal) < 1
                custPurchase(x, customer, account)
                bought.play()
            elif 1 <= (x.sale/x.ideal) <= 1.5: #ideal, 1.2, or 1.5 times
                if random.randint(1,10) > 2: #80% chance
                    custPurchase(x, customer, account)
                    bought.play()
                elif x.season == gameSeason: #when seasons matter
                    custPurchase(x, customer, account)
                    bought.play()
            elif 1.5 <= (x.sale/x.ideal) <= 2.5:
                if random.randint(1,10) > 7: # 20% chance
                    custPurchase(x, customer, account)
                    bought.play()   
            else:
                if random.randint(1,100) == 1: # severely overpriced
                    custPurchase(x, customer, account)
                    bought.play()
    return account
#function to change quantities, make money, and record the most recent purchase
def custPurchase(item, customer, account):
    global yes, cust, itm
    yes = False
    account.Make(item.sale)
    item.quan -= 1
    if item.quan == 0:
        item.outOfStock()
    yes = True
    cust = customer.ageGroup
    itm = item.n
#function to remove items that are sold out
def checkShelf(itemsOnShelf):
    temp = []
    for x in itemsOnShelf:
        if x.quan != 0:
            temp.append(x)
        else:
            x.onShelf = False
    if len(temp) != 0:
        return temp
    else:
        return []
#function to remove items that have been fully bought by user
def checkQuan(itemList):
    temp = []
    for x in itemList:
        if x.stockQuan != 0:
            temp.append(x)
    return temp
#function to select items that will be shown on catalogue
def catSelection(itemList):
    possible = []
    canOrder = []
    possible = checkQuan(itemList) #make sure they're in stock
    for x in range(6):
        y = random.randint(0, len(possible) -1)
        if possible[y] not in canOrder:#don't append it more than once
            canOrder.append(possible[y])
    return canOrder          
#function to display numbers as currency
def displayCurrency(value):
    currency = "${:,.2f}".format(value)
    return currency
#function to write on pygame screen
def write(canvas, font, text, colour, coordinates, rotate=0):                                               
    tSurface = font.render(text, False, colour)                                                   
    tSurface = pygame.transform.rotate(tSurface, rotate)
    canvas.blit(tSurface, coordinates)      
#function to write account information onto screen
def writeStats():
    global account
    f = open('clipboard.txt')
    write(screen, cFont, f.readline().strip()+displayCurrency(account.balance), (0,15,130), (130,150), -7.5)
    write(screen, cFont, f.readline().strip()+displayCurrency(account.spent), (0,15,130), (124,200), -7.5)
    write(screen, cFont, f.readline().strip()+displayCurrency(account.earn), (0,15,130), (118,250), -7.5)
    write(screen, cFont, f.readline().strip()+displayCurrency(account.earn-account.spent), (0,15,130), (112,300), -7.5)
    account.updateBalance()
    write(screen, cFont, f.readline().strip()+displayCurrency(account.balance), (0,15,130), (106,350), -7.5)
    write(screen, cFont, f.readline().strip(), (0,15,130), (100,350), -7.5)
    write(screen, cFont, f.readline().strip(), (0,15,130), (94,400), -7.5)
    f.close()
#function to update the scores at the end of the game
def updateScores():                                                                             
    global account, hsLines, difficulty, user
    if difficulty == 0: #set starting balance
        start = 50
    elif difficulty == 1:
        start = 30
    else:
        start = 20
    score = account.balance-start #set score
    for x in range(10):#add in score if in the top ten                                                                       
        if hsLines[x].strip() == '':#if the score is empty, set it to large negative number(to compare)
            num = -100000000000000000
        else:
            num = int(hsLines[x].strip()[-1])
        if score > num:                                         
            score = round(score,2)
            hsLines.insert(x+1,user+" "+str(score) + "\n")
            break
    hs = open('highscores.txt', 'w')                                                                  
    hs.writelines([item for item in hsLines[:10]])#write in new top scores
    hs.close()
#function to draw right tree picture depending on season 
def drawTree():
    global season
    if season == 'winter':
        photo = wTree
    elif season == 'fall':
        photo = fTree
    elif season == 'spring':
        photo  = spTree
    else:
        photo = suTree
    screen.blit(photo, (273,278))

#button function to get name and set up Difficulty window
def startGame():
    global user, winNum, name, inst, en, start
    user = name.get()
    if user != "":
        en.destroy()
        name.destroy()
        start.destroy()
        inst.destroy()
        redrawDiffWin()
#button function to show instructions if they haven't already been shown        
def instructions():
    global i
    if not i:
        screen.blit(paper, (700,140))
        f = open('instructions.txt')
        y=240
        for line in f:
            write(screen, pFont, line.strip(), (0,0,0), (800,y))
            y+=30
        f.close()
        i = True
        pygame.display.update()
#button functions to set difficulty, season, account, and set up Buy window
def easy():
    global difficulty, account, season, c
    difficulty = 0
    season = 'winter'
    account = Account(50)
    c = catSelection(items)
    redrawBuyWin()
def medium():
    global difficulty, account, season, c
    difficulty = 1
    season = 'summer'
    account = Account(30)
    c = catSelection(items)
    redrawBuyWin()
def hard():
    global difficulty, account, season, c
    difficulty = 2
    season = random.choice(['fall','spring'])
    account = Account(20)
    c = catSelection(items)
    redrawBuyWin()
#button function to set up Catalogue window
def setUpCat():
    global nd, cat, e1,e2,e3,e4,e5,e6
    nd.destroy()
    cat.destroy()
    e1.destroy()
    e2.destroy()
    e3.destroy()
    e4.destroy()
    e5.destroy()
    e6.destroy()
    pageflip.play()
    redrawCatWin()
#button function to buy items from stock(change stock quantity, send money, add to items to be sold, put on sale)
def buyFromStock(item, itemList, account):
    global drawB, sellItems
    itemQ = checkQuan(itemList)
    if item in itemQ:
        item.stockQuan -= 1
        account.Use(item.stock)
        item.quan += 1
        item.putOnShelf()
        if item not in sellItems:
            sellItems.append(item)
        bought.play()
        drawB = False
        redrawCatWin()
#button function to set up Buy window from Catalogue window
def goBack():
    global bb, buyB, drawB
    bb.destroy()
    for x in buyB:
        x.destroy()
    drawB = True
    pageflip.play()
    redrawBuyWin()
#button function to set up Sell window
def setUpDay():
    global nd, cat, dayNum, price, sellItems, itemImg, e1,e2,e3,e4,e5,e6
    price = []
    try:#get item prices
        price.append(e1.get())
        price.append(e2.get())
        price.append(e3.get())
        price.append(e4.get())
        price.append(e5.get())
        price.append(e6.get())
    except NameError:
        pass
    price = [value for value in price if value != ""]
    itemImg = []#get item images
    for x in range(10):
        itemImg.append(lock)
    for x in range(len(sellItems)):
        sellItems[x].changePrice(float(price[x]))
        itemImg[x] = sellItems[x].img
    nd.destroy()
    cat.destroy()
    e1.destroy()
    e2.destroy()
    e3.destroy()
    e4.destroy()
    e5.destroy()
    e6.destroy()
    dayNum += 1
    redrawSellWin()
#button function to end day and set up Buy window
def tearDownDay():
    global ed, c, cList
    ed.destroy()
    c = catSelection(items)
    cList = []
    redrawBuyWin()
#button function to set up high scores window
def setUpScores():
    global eg, e1,e2,e3,e4,e5,e6
    e1.destroy()
    e2.destroy()
    e3.destroy()
    e4.destroy()
    e5.destroy()
    e6.destroy()
    eg.destroy()
    updateScores()
    redrawEndWin()
#button function to quit game
def quitGame():
    win.destroy()
    
#code to draw the Start window
def redrawStartWin():
    global en, name, start, inst
    screen.blit(back, (0,0))
    sky.draw(moon,night,screen)
    en = Label(win,text="Enter Name",bg='#DFE0D2',font=helv36)
    en.place(x=220,y=650) 
    name = Entry(win)
    name.config(width=15,font=helv36)
    name.place(x=150,y=720)
    start = Button(win,text = 'Start',command=startGame,font=helv36)#code example for buttons
    start.place(x=100,y=800)
    inst = Button(win,text = 'Instructions',command=instructions,font=helv36)
    inst.place(x=290,y=800)
#code to draw the Difficulty window
def redrawDiffWin():
    global cd, diff
    screen.blit(back, (0,0))
    sky.redraw(moon,night,screen)
    cd = Label(win,text="Choose Difficulty",bg='#DFE0D2',font=helv36)
    cd.place(x=150,y=650)
    diff = []
    diff.append(Button(win,text='Easy',command=easy,font=helv28))
    diff.append(Button(win,text='Medium',command=medium,font=helv28))
    diff.append(Button(win,text='Hard',command=hard,font=helv28))
    X = 120
    for num,b in enumerate(diff):
        b.place(x=X,y=750)
        if num == 0:
            X += 150
        else:
            X += 200
#code to draw the Buy window
def redrawBuyWin():
    global cd, diff, nd, cat, ed, dayNum, eg, prices, sellItems, e1,e2,e3,e4,e5,e6
    prices = []
    if dayNum < 10: #put in right buttons depending on day
        nd = Button(win, text='New Day', command=setUpDay, font=helv28)
        nd.place(x=840,y=600)
        cat = Button(win,text="Catalogue", font=helv28, command=setUpCat)
        cat.place(x=968,y=190)
    else: #game end here 
        eg = Button(win, text='End Game', command=setUpScores, font=helv28)
        eg.place(x=840,y=600) 
    screen.blit(nback, (0,0))
    cd.destroy()
    for x in diff:
        x.destroy()
    writeStats()#get info and entry boxes for prices
    e1 = Entry(win)
    e1.config(width=6,font=helv15)
    e2 = Entry(win)
    e2.config(width=6,font=helv15)
    e3 = Entry(win)
    e3.config(width=6,font=helv15)
    e4 = Entry(win)
    e4.config(width=6,font=helv15)
    e5 = Entry(win)
    e5.config(width=6,font=helv15)
    e6 = Entry(win)
    e6.config(width=6,font=helv15)
    X = 94
    Y = 400
    sellItems = checkShelf(sellItems)#write in items to be sold (6 max)
    for i,item in enumerate(sellItems):
        write(screen, cFont, str(item.quan)+"x "+item.n + " " +displayCurrency(item.stock), (0,15,130), (X-6, Y+50), -7.5)
        X -= 6
        Y += 50
        if i == 0: 
            e1.insert(0,item.sale)
            e1.place(x=X-6+405,y=Y+50)
        elif i == 1:
            e2.insert(0,item.sale)
            e2.place(x=X-6+405,y=Y+50)
        elif i == 2:
            e3.insert(0,item.sale)
            e3.place(x=X-6+405,y=Y+50)
        elif i == 3:
            e4.insert(0,item.sale)
            e4.place(x=X-6+405,y=Y+50)
        elif i == 4:
            e5.insert(0,item.sale)
            e5.place(x=X-6+405,y=Y+50)
        elif i == 5:
            e6.insert(0,item.sale)
            e6.place(x=X-6+405,y=Y+50)
    pygame.display.update()
#code to draw the Catalogue window
def redrawCatWin():
    global c, account, buyB, bb, drawB
    if drawB: #draw buy buttons once
        bb = Button(win, text='Back',command=goBack,font=helv28)
        bb.place(x=1000,y=800)
        buyB = []
        b1 = Button(win, text="Buy", font=helv15, command=lambda:buyFromStock(c[0], c, account))
        buyB.append(b1)
        b2 = Button(win, text="Buy", font=helv15, command=lambda:buyFromStock(c[1], c, account))
        buyB.append(b2)
        b3 = Button(win, text="Buy", font=helv15, command=lambda:buyFromStock(c[2], c, account))
        buyB.append(b3)
        b4 = Button(win, text="Buy", font=helv15, command=lambda:buyFromStock(c[3], c, account))
        buyB.append(b4)
        b5 = Button(win, text="Buy", font=helv15, command=lambda:buyFromStock(c[4], c, account))
        buyB.append(b5)
        b6 = Button(win, text="Buy", font=helv15, command=lambda:buyFromStock(c[5], c, account))
        buyB.append(b6)
    screen.blit(cback, (0,0))
    X = 675
    Y = 100
    for i,x in enumerate(c):#write in the items in the catalogue and place buttons 
        write(screen, catFont, str(x.stockQuan) +"x " + x.n, (0,15,130), (X, Y))
        write(screen, catFont, displayCurrency(x.stock), (0,15,130), (X+300, Y))
        if drawB:
            buyB[i].place(x=X+450, y=Y-3)
        Y += 50
    write(screen, cFont, "Balance: " + displayCurrency(account.balance-account.spent), (0,0,0), (100,800))#write balance
    pygame.display.update()
#code to draw Sell window
def redrawSellWin():
    global ed, hour, account, dayNum, sellItems, seasons, yes, cust, itm
    yes = False
    inPlay = True #set initial screen and variables
    sky.draw(sun,day,screen)
    ed = Button(win, text="End Day", font=helv28, command=tearDownDay)
    ed.place(x=800,y=800)
    curT = time.time()
    hour = 9
    createCust()
    while inPlay:#main loop while day is in progress
        screen.blit(back, (0,0))
        sky.redraw(sun,day,screen)
        drawTree()
        numC = 0 #track numbers of customers
        numA = 0
        numS = 0
        X = 600
        Y = 180
        walkIn()
        for x in range(6):#draw items
            screen.blit(itemImg[x],(X,Y))
            if x < len(sellItems):
                screen.blit(tag, (X+50, Y+100))
                write(screen,catFont, "x" + str(sellItems[x].quan), (0,0,0), (X+130,Y))
                write(screen,catFont, displayCurrency(sellItems[x].sale), (0,15,130), (X+85,Y+110))
            X += 200
            if x == 2:
                X = 600
                Y += 170
        for x in cInStore:#update clipboard stats
            if x.ageGroup == 'Child':
                numC += 1
            elif x.ageGroup == 'Adult':
                numA += 1
            else:
                numS += 1    
        if hour == 17:#end day
            sky.draw(moon,night,screen)
            numC = 0
            numA = 0
            numS = 0
            inPlay = False
        if time.time()-curT >= 15:#change time at every hour
            curT = time.time()
            hour += 1
            createCust()
        walkOut()
        write(screen, cFont, "Amount sold:" + displayCurrency(account.earn),(0,15,130),(100,650))#write clipboard stats
        write(screen, cFont, "Children: " + str(numC),(0,15,130),(100,700))
        write(screen, cFont, "Adults: " + str(numA),(0,15,130),(100,750))
        write(screen, cFont, "Seniors: " + str(numS),(0,15,130),(100,800))
        write(screen, tFont, str(hour)+":00", (0,0,0), (3,2))#write day stats
        write(screen, tFont, "Day " + str(dayNum), (0,0,0), (3,35))
        write(screen, tFont, "Season: " + season, (0,0,0), (3,68))
        if yes:#write most recent purchase
            write(screen, catFont, "A "+ cust+" has purchased " + itm,(0,0,0), (750,700))
        pygame.display.update()
#code to write high scores on last window
def redrawEndWin():
    screen.blit(nback, (0,0))
    write(screen, cFont, 'High Scores', (0,15,130), (130,150), -7.5)
    hs = open('highscores.txt')
    X = 124
    Y = 200
    for x in range(10):#write in top ten scores
        line = hs.readline().strip()
        if line != '':
            name,score = line.split()
            write(screen, cFont, name, (0,15,130), (X,Y), -7.5)
            write(screen, cFont, displayCurrency(float(score)), (0,15,130), (X+300,Y+55), -7.5)
            X -= 6
            Y += 50
        else:
            write(screen, cFont, line, (0,15,130), (X,Y), -7.5)
    hs.close()
    q = Button(win, text="Quit", font=helv28, command=quitGame)
    q.place(x=840,y=600)
    pygame.display.update()
    
#main setup
#start tkinter
win = tk.Tk()
#create window
win.title("Shop Simulator 2.0")
win.configure(background = "pale turquoise")
#creates embed frame for pygame window
embed = tk.Frame(win, width = 1200, height = 900) 
embed.grid(columnspan = (600), rowspan = 500) 
embed.pack(side = BOTTOM) 
#code to merge pygame and tkinter (pygame as video window)
os.environ['SDL_WINDOWID'] = str(embed.winfo_id())
os.environ['SDL_VIDEODRIVER'] = 'windib'
#code to initialize pygame window
screen = pygame.display.set_mode((1200,900))
screen.fill(pygame.Color(255,255,255))
pygame.init()
#code to load sounds
pageflip = pygame.mixer.Sound('pageflip.wav')
bought = pygame.mixer.Sound('bought.wav')
doorbell = pygame.mixer.Sound('doorbell.wav')
#code to load pictures
back = pygame.image.load('BackDrop.jpg') 
nback = pygame.image.load('NightScene.jpg')
cback = pygame.image.load('Catalogue1.jpg')
paper = pygame.image.load('paper.jpg')
lock = pygame.image.load('lock.png')
fTree = pygame.image.load('fTree.png')
wTree = pygame.image.load('wTree.png')
spTree = pygame.image.load('spTree.png')
suTree = pygame.image.load('sTree.png')
tag = pygame.image.load('tag.png')
itemImg = []
items = []
for x in range(10):
    itemImg.append(lock)
#code to load fonts (both tkinter and pygame)
helv36 = tk.font.Font(family='Helvetica', size=36, weight='bold')
helv28 = tk.font.Font(family='Helvetica', size=28, weight='bold')
helv15 = tk.font.Font(family='Helvetica', size=15, weight='bold')
pFont = pygame.font.SysFont("helvetica", 24, True)
tFont = pygame.font.SysFont("helvetica", 28, True)
cFont = pygame.font.SysFont("comic sans ms", 28, True)
catFont = pygame.font.SysFont("comic sans ms", 20, True)
#code to get current high scores
hs = open('highscores.txt')
hsLines = hs.readlines()
hs.close()
#code to load in items
items = createItems('items.txt', items)
#start the game
redrawStartWin()
pygame.display.update()
win.mainloop()

