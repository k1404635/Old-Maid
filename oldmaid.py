from tkinter import *
from PIL import ImageTk, Image
import flask
from flask.wrappers import Response
import requests
from io import BytesIO

app = flask.Flask(__name__)
global deck_id, c, p
root = Tk()
root.title('Old Maid')
c = Canvas(root)
root.geometry('1500x900')
c.pack(fill=BOTH, expand=True)
p = 1
begin = True

def new_deck():
    global deck_id

    response = requests.get("https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1") #don't need ?deck_count=1 bc thats what is requested
    print(response.json()['deck_id'])
    deck_id = response.json()['deck_id']

    return deck_id

def pass_cards():
  a = draw()
  make_discard(a)
  for i in range(1, 52):
      b = draw()
      if i%4 == 1:
          make_player1(b)
      elif i%4==2:
          make_player2(b)
      elif i%4 == 3:
          make_player3(b)
      elif i%4 == 0:
          make_player4(b)
  board()
    
        

def make_player1(code):
  info = requests.get("https://deckofcardsapi.com/api/deck/" + deck_id + "/pile/player1/add/?cards="+code)
  result = requests.get("https://deckofcardsapi.com/api/deck/"+deck_id+"/pile/player1/list/")
  result = result.json()
  result = result['piles']['player1']['cards']
  hand1 = []
  for x in result:
    hand1.append(x['code'])

def make_player2(code):
    info = requests.get("https://deckofcardsapi.com/api/deck/" + deck_id + "/pile/player2/add/?cards="+code) #replace ?cards=AS,2S with actual cards
    # we need to make this into something? to get the list of cards they have "https://deckofcardsapi.com/api/deck/"+deck_id+"/pile/player2/list/"


def make_player3(code):
    info = requests.get("https://deckofcardsapi.com/api/deck/" + deck_id + "/pile/player3/add/?cards=" + code) #replace ?cards=AS,2S with actual cards
    # we need to make this into something? to get the list of cards they have "https://deckofcardsapi.com/api/deck/"+deck_id+"/pile/player3/list/"


def make_player4(code):
    info = requests.get("https://deckofcardsapi.com/api/deck/" + deck_id + "/pile/player4/add/?cards=" +code) #replace ?cards=AS,2S with actual cards
    # we need to make this into something? to get the list of cards they have "https://deckofcardsapi.com/api/deck/"+deck_id+"/pile/player4/list/"


def make_discard(a):
    dis = requests.get("https://deckofcardsapi.com/api/deck/" + deck_id + "/pile/discard/add/?cards="+a) #replace ?cards=AS,2S with actual cards
    # we need to make this into something? to get the list of cards they have "https://deckofcardsapi.com/api/deck/"+deck_id+"/pile/discard/list/"
    
def use_card():
  pass

def board():
  hand = []
  if p == 1:
    res = requests.get("https://deckofcardsapi.com/api/deck/"+deck_id+"/pile/player1/list/")
    res = res.json()
    res = res['piles']['player1']['cards']
    for x in res:
      hand.append(x['image'])
  elif p == 2:
    pass
  elif p == 3:
    pass
  elif p == 4:
    pass

  xvalue = 75
  yvalue = 650
  for jjj in hand:
    imgr = requests.get(jjj)
    img_bytes = BytesIO(imgr.content)
    img = Image.open(img_bytes)
    img = img.resize((150, 200), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)
    panel = Button(root, image = img, command=lambda: use_card())
    panel.image = img
    panel.place(x=xvalue,y=yvalue)
    xvalue += 100

  show_others_cards()

def draw():
  stuff = requests.get("https://deckofcardsapi.com/api/deck/" + deck_id + "/draw/?count=1")
  result = stuff.json()
  
  return str(result['cards'][0]['code'])

def show_others_cards():
  c.create_rectangle(25, 325, 225, 475, fill="black")
  c.create_rectangle(1275, 325, 1475, 475, fill="black")
  c.create_rectangle(700, 25, 850, 225, fill="black")
  show_other_info()

def show_other_info(): # make lists of hands global, then add to label to show number of cards
  if p == 1:
    current = Label(text="Player 1: Current player", fg="black", font=("Helvetica", 20))
    other1 = Label(text="Player 2: ", fg="black", font=("Helvetica", 20))
    other2 = Label(text="Player 3: ", fg="black", font=("Helvetica", 20))
    other3 = Label(text="Player 4: ", fg="black", font=("Helvetica", 20))
  elif p == 2:
    other1 = Label(text="Player 1: ", fg="black", font=("Helvetica", 20))
    current = Label(text="Player 2: Current player", fg="black", font=("Helvetica", 20))
    other2 = Label(text="Player 3: ", fg="black", font=("Helvetica", 20))
    other3 = Label(text="Player 4: ", fg="black", font=("Helvetica", 20))
  elif p ==3:
    other1 = Label(text="Player 1: ", fg="black", font=("Helvetica", 20))
    other2 = Label(text="Player 2: ", fg="black", font=("Helvetica", 20))
    current = Label(text="Player 3: Current player", fg="black", font=("Helvetica", 20))
    other3 = Label(text="Player 4: ", fg="black", font=("Helvetica", 20))
  elif p == 4:
    other1 = Label(text="Player 1: ", fg="black", font=("Helvetica", 20))
    other2 = Label(text="Player 2: ", fg="black", font=("Helvetica", 20))
    other3 = Label(text="Player 3: ", fg="black", font=("Helvetica", 20))
    current = Label(text="Player 4: Current player", fg="black", font=("Helvetica", 20))

  current.place(x=650, y=350)
  other1.place(x=650, y=400)
  other2.place(x=650, y=450)
  other3.place(x=650, y=500)

new_deck()
#draw()
pass_cards()

#app.run(host ='https://deckofcardsapi.com/api/deck')
root.mainloop()
