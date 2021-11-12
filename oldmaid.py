from tkinter import *
from PIL import ImageTk, Image
import flask
from flask.wrappers import Response
import requests
from io import BytesIO

app = flask.Flask(__name__)
global deck_id, c, p, cards
root = Tk()
root.title('Old Maid')
c = Canvas(root)
root.geometry('1500x900')
c.pack(fill=BOTH, expand=True)
p = 1
begin = True
cards = []

def new_deck():
    global deck_id

    response = requests.get("https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1")
    print(response.json()['deck_id'])
    deck_id = response.json()['deck_id']

    return deck_id

def pass_cards():
  count = 1
  a = draw()
  make_discard(a)
  for i in range(1, 52):
      b = draw()
      if count == 1:
          make_player1(b)
          count = 2
      elif count==2:
          make_player2(b)
          count = 3
      elif count == 3:
          make_player3(b)
          count = 4
      elif count == 4:
          make_player4(b)
          count = 1
  
  board()        

def make_player1(code):
    info = requests.get("https://deckofcardsapi.com/api/deck/" + deck_id + "/pile/player1/add/?cards="+code)
def get_player1():
    result = requests.get("https://deckofcardsapi.com/api/deck/"+deck_id+"/pile/player1/list/")
    result = result.json()
    result = result['piles']['player1']['cards']
    hand1 = []
    for x in result:
        hand1.append(x['code'])
    return hand1

def make_player2(code):
    info = requests.get("https://deckofcardsapi.com/api/deck/" + deck_id + "/pile/player2/add/?cards="+code) 
def get_player2():
    result = requests.get("https://deckofcardsapi.com/api/deck/"+deck_id+"/pile/player2/list/")
    result = result.json()
    result = result['piles']['player2']['cards']
    hand1 = []
    for x in result:
        hand1.append(x['code'])
    return hand1

def make_player3(code):
    info = requests.get("https://deckofcardsapi.com/api/deck/" + deck_id + "/pile/player3/add/?cards=" + code) 
def get_player3():
    result = requests.get("https://deckofcardsapi.com/api/deck/"+deck_id+"/pile/player3/list/")
    result = result.json()
    result = result['piles']['player3']['cards']
    hand1 = []
    for x in result:
        hand1.append(x['code'])
    return hand1

def make_player4(code):
    info = requests.get("https://deckofcardsapi.com/api/deck/" + deck_id + "/pile/player4/add/?cards=" +code)
def get_player4():
    result = requests.get("https://deckofcardsapi.com/api/deck/"+deck_id+"/pile/player4/list/")
    result = result.json()
    result = result['piles']['player4']['cards']
    hand1 = []
    for x in result:
        hand1.append(x['code'])
    return hand1

def make_discard(a):
    dis = requests.get("https://deckofcardsapi.com/api/deck/" + deck_id + "/pile/discard/add/?cards="+a)

def get_current_hand():
    global p
    if p == 1:
        return get_player1()
    elif p == 2:
        return get_player2()
    elif p == 3:
        return get_player3()
    elif p == 4:
        return get_player4()
    
def use_card(je):
    global cards
    chand = get_current_hand()
    cards.append(chand[je])
    print(je)
    
    if len(cards) == 1:
        select = Label(text="Select Another Card", fg="black", font=("Helvetica", 20))
        select.place(x=650, y=500)
    elif len(cards) == 2:
        card1 = str(cards[0])
        card1a = card1[0:1]
        card2 = cards[1]
        card2a = card2[0:1]
        print(card1a, card2a)
        if card1a == card2a:
            print("true")
        cards=[]
        
def board():
  global c
  hand = []
  if p == 1:
    res = requests.get("https://deckofcardsapi.com/api/deck/"+deck_id+"/pile/player1/list/")
    res = res.json()
    res = res['piles']['player1']['cards']
    for x in res:
      hand.append(x['image'])
  elif p == 2:
    res = requests.get("https://deckofcardsapi.com/api/deck/"+deck_id+"/pile/player2/list/")
    res = res.json()
    res = res['piles']['player2']['cards']
    for x in res:
      hand.append(x['image'])
  elif p == 3:
    res = requests.get("https://deckofcardsapi.com/api/deck/"+deck_id+"/pile/player3/list/")
    res = res.json()
    res = res['piles']['player3']['cards']
    for x in res:
      hand.append(x['image'])
  elif p == 4:
    res = requests.get("https://deckofcardsapi.com/api/deck/"+deck_id+"/pile/player4/list/")
    res = res.json()
    res = res['piles']['player4']['cards']
    for x in res:
      hand.append(x['image'])

  xvalue = 75
  yvalue = 650
  ia = 0
  for jjj in hand:
    imgr = requests.get(jjj)
    img_bytes = BytesIO(imgr.content)
    img = Image.open(img_bytes)
    img = img.resize((150, 200), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)
    panel = Button(root, image = img, command=lambda d = ia: use_card(d))
    panel.image = img
    panel.place(x=xvalue,y=yvalue)
    xvalue += 100
    ia+=1

  show_others_cards()

def draw():
  stuff = requests.get("https://deckofcardsapi.com/api/deck/" + deck_id + "/draw/?count=1")
  result = stuff.json()
  
  return str(result['cards'][0]['code'])

def show_others_cards():
  global c
  c.create_rectangle(25, 325, 225, 475, fill="black")
  c.create_rectangle(1275, 325, 1475, 475, fill="black")
  c.create_rectangle(700, 25, 850, 225, fill="black")
  show_other_info()

def show_other_info(): # make lists of hands global, then add to label to show number of cards
  global c
  if p == 1:
    current = Label(text="Player 1: Current player", fg="black", font=("Helvetica", 20))
    other1 = Label(text="Player 2: " + str(len(get_player2())), fg="black", font=("Helvetica", 20))
    other2 = Label(text="Player 3: " + str(len(get_player3())), fg="black", font=("Helvetica", 20))
    other3 = Label(text="Player 4: " + str(len(get_player4())), fg="black", font=("Helvetica", 20))
  elif p == 2:
    other1 = Label(text="Player 1: " + str(len(get_player1())), fg="black", font=("Helvetica", 20))
    current = Label(text="Player 2: Current player", fg="black", font=("Helvetica", 20))
    other2 = Label(text="Player 3: " + str(len(get_player3())), fg="black", font=("Helvetica", 20))
    other3 = Label(text="Player 4: " + str(len(get_player4())), fg="black", font=("Helvetica", 20))
  elif p == 3:
    other1 = Label(text="Player 1: " + str(len(get_player1())), fg="black", font=("Helvetica", 20))
    other2 = Label(text="Player 2: " + str(len(get_player2())), fg="black", font=("Helvetica", 20))
    current = Label(text="Player 3: Current player", fg="black", font=("Helvetica", 20))
    other3 = Label(text="Player 4: " + str(len(get_player4())), fg="black", font=("Helvetica", 20))
  elif p == 4:
    other1 = Label(text="Player 1: " + str(len(get_player1())), fg="black", font=("Helvetica", 20))
    other2 = Label(text="Player 2: " + str(len(get_player2())), fg="black", font=("Helvetica", 20))
    other3 = Label(text="Player 3: " + str(len(get_player3())), fg="black", font=("Helvetica", 20))
    current = Label(text="Player 4: Current player", fg="black", font=("Helvetica", 20))

  end = Button(root, text="End Turn", font=("Helvetica", 20), height = 1, width = 7, bg="SystemButtonFace", command=lambda: end_turn())

  end.place(x=700, y=550)
  current.place(x=650, y=300)
  other1.place(x=650, y=350)
  other2.place(x=650, y=400)
  other3.place(x=650, y=450)

def end_turn():
  global p, c
  if p < 4:
    p += 1
  else:
    p = 1
  c.delete('all')
  board()
  

new_deck()
#draw()
pass_cards()

root.mainloop()
