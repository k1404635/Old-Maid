from tkinter import *
from PIL import ImageTk, Image
import flask
from flask.wrappers import Response
import requests
from io import BytesIO

app = flask.Flask(__name__)

root = Tk()
root.title('Old Maid')
c = Canvas(root)
root.geometry('846x669')
#c.pack(fill=BOTH, expand=True)
    
global deck_id

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

def board(cards):
    card1 = cards[0]
    card1a = card1[0:1]
    card2 = cards[1]
    card2a = card2[0:1]
    if card1a == card2a:
        pass #add to discard pile and remove from the player's hand

def random():
    pass


def draw():
    stuff = requests.get("https://deckofcardsapi.com/api/deck/" + deck_id + "/draw/?count=1")
    result = stuff.json()
    print(result['cards'][0]['code'])
    imgr = requests.get(result['cards'][0]['image'])
    img_bytes = BytesIO(imgr.content)
    img = Image.open(img_bytes)
    img = img.resize((150, 200), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)
    panel = Label(root, image = img)
    panel.image = img
    panel.grid(row = 2)

    
    return str(result['cards'][0]['code'])


new_deck()
draw()
#pass_cards()

#app.run(host ='https://deckofcardsapi.com/api/deck')
root.mainloop()
