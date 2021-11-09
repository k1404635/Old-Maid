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
    
        

def make_player1(code):
    info = requests.get("https://deckofcardsapi.com/api/deck/" + deck_id + "/pile/player1/add/?cards="+code) #replace ?cards=AS,2S with actual cards
    # we need to make this into something? to get the list of cards they have "https://deckofcardsapi.com/api/deck/"+deck_id+"/pile/player1/list/"


def make_player2(code):
    info = requests.get("https://deckofcardsapi.com/api/deck/" + deck_id + "/pile/player2/add/?cards="+code) #replace ?cards=AS,2S with actual cards
    # we need to make this into something? to get the list of cards they have "https://deckofcardsapi.com/api/deck/"+deck_id+"/pile/player2/list/"


def make_player3(code):
    info = requests.get("https://deckofcardsapi.com/api/deck/" + deck_id + "/pile/player3/add/?cards=" + code) #replace ?cards=AS,2S with actual cards
    # we need to make this into something? to get the list of cards they have "https://deckofcardsapi.com/api/deck/"+deck_id+"/pile/player3/list/"


def make_player4(code):
    info = requests.get("https://deckofcardsapi.com/api/deck/" + deck_id + "/pile/player4/add/?cards=" +code) #replace ?cards=AS,2S with actual cards
    # we need to make this into something? to get the list of cards they have "https://deckofcardsapi.com/api/deck/"+deck_id+"/pile/player4/list/"


def make_discard(code):
    dis = requests.get("https://deckofcardsapi.com/api/deck/" + deck_id + "/pile/discard/add/?cards="+code) #replace ?cards=AS,2S with actual cards
    # we need to make this into something? to get the list of cards they have "https://deckofcardsapi.com/api/deck/"+deck_id+"/pile/discard/list/"

def use_card():
  pass

def draw():
    stuff = requests.get("https://deckofcardsapi.com/api/deck/" + deck_id + "/draw/?count=1")
    result = stuff.json()
    
    
    imgr = requests.get(result['cards'][0]['image'])
    img_bytes = BytesIO(imgr.content)
    img = Image.open(img_bytes)
    img = img.resize((150, 200), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)
    panel = Button(root, image = img, command=lambda: use_card())
    panel.image = img
    panel.place(x=700,y=650)
    show_others_cards()
    
    return str(result['cards'][0]['code'])

def show_others_cards():
  c.create_rectangle(25, 325, 225, 475, fill="black")
  c.create_rectangle(1275, 325, 1475, 475, fill="black")
  c.create_rectangle(700, 25, 850, 225, fill="black")

def show_other_info():
  if p == 1:
    pass
  elif p == 2:
    pass
  elif p ==3:
    pass
  elif p == 4:
    pass

new_deck()
draw()
#pass_cards()

#app.run(host ='https://deckofcardsapi.com/api/deck')
root.mainloop()
