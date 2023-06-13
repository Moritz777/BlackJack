"""
Implementation of the game "Blackjack".

The game rules are outlined in the guide issued by Provadis.

Functions:
    main: Ask the user for their name and start the game
    blackjack: Implement the main game logic
    deal_card: Let the Croupier deal cards
    get_player_input:
    print_winner:
"""

# importing random to get random cards later on

import random

logo = '''
    .------.            _     _            _    _            _    
    |A_  _ |.          | |   | |          | |  (_)          | |   
    |( \/ ).-----.     | |__ | | __ _  ___| | ___  __ _  ___| | __
    | \  /|K /\  |     | '_ \| |/ _` |/ __| |/ / |/ _` |/ __| |/ /
    |  \/ | /  \ |     | |_) | | (_| | (__|   <| | (_| | (__|   < 
    `-----| \  / |     |_.__/|_|\__,_|\___|_|\_\ |\__,_|\___|_|\_\\
          |  \/ K|                            _/ |                
          `------'                           |__/           
    '''

# initialise the cards suits, ranks and values

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10,
          'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}

# setting the players ability to play to true

playing = True

# defining classes


class Card:
    """
    initialise a card with the given suit and rank
    """
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.rank + ' of ' + self.suit


class Deck:
    """
    Create a deck from the given cards
    """
    def __init__(self):
        self.deck = []  # start with an empty list
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit,rank))  # build Card objects and add them to the list

    def __str__(self):
        deck_comp = ''  # start with an empty string
        for card in self.deck:
            deck_comp += '\n '+card.__str__() # add each Card object's print string
        return 'The deck has:' + deck_comp

    def shuffle(self):          # shuffle function will shuffle the whole deck
        random.shuffle(self.deck)

    def deal(self):             # deal function will take one card from the deck
        single_card = self.deck.pop()
        return single_card


class Hand:
    """
    Add the cards from the deck class to the player's hand
    """
    def __init__(self):
        self.cards = []  # start with an empty list as we did in the Deck class
        self.value = 0   # start with zero value
        self.aces = 0    # add an attribute to keep track of aces

    # now let's add cards

    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.rank]

    # adjusting the value of ace

    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1


class Chips:
    """
    keep track of the players chips, bets and ongoing winnings.
    """
    def __init__(self):
        self.total = 50  # This can be set to a default value or supplied by a user input
        self.bet = 0

    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet


# Functions start here

def take_bet(chips):
    """
    take bets from the player
    :param chips: the players chips as given below
    """
    while True:
        try:
            chips.bet = int(input('Wie viel Geld möchtest du setzen? '))
        except ValueError:
            print('Bitte eine Zahl eingeben!')
        else:
            if chips.bet > chips.total:
                print(f"Sorry, du kannst nicht mehr als {chips.total}€ setzen")
            else:
                break


def hit(deck, hand):
    """
    Let the player draw a card.
    """
    hand.add_card(deck.deal())
    hand.adjust_for_ace()


def hit_or_stand(deck, hand):
    """
    Prompt the player to hit or stand.
    """
    global playing  # for use in an upcoming while loop
    # player_hand = []

    while True:
        player_input = get_player_input()

        if player_input == '':
            hit(deck, hand)
            # player_hand.append(cards)
            # print(player_hand)

        elif player_input[0].lower() == 's':
            print("Du nimmst keine weitere Karte. Der Dealer spielt.")
            # print(f"Deine finale Hand: {player_hand}, Finaler Score: {calculate_score(player_hand)}")
            playing = False

        elif player_input[0].lower() == 'q':
            exit(0)
        break


def calculate_score(cards):
    if sum(cards) == 21 and len(cards) == 2:
        return 0
    if 11 in cards and sum(cards) > 21:
        cards.remove(11)
        cards.append(1)

    return sum(cards)


def print_winner(score):
    """
    Decide who won the game based on the scoreboard and print it out.

    Args:
         score: The final scoreboard
    """
    current_winner_score = 0
    # z.B.: [('Janine', 9), ('Gabriele', 9), ('Bot', 3)]
    scores = score.items()
    for score in scores:
        if score[1] >= 16:
            continue
        if score[1] > current_winner_score:
            current_winner_score = score[1]

    for score in scores:
        if score[1] == current_winner_score:
            print(score[0], 'hat mit', score[1], 'Punkten gewonnen!')


def get_player_input():
    """
    Print the user interface, accept their input and return it.

    This function asks the user for their input until they give
    us a valid option.

    Return:
        user_input: A string of the user input (one of '', 's', 'q' or 'r')
    """
    print('\nWas möchtest du als nächstes tun?')
    print('1. [<Eingabe>]: Weitere Karte ziehen')
    print('2. [s]: stand - Keine weitere Karte')
    print('3. [q]: Spiel verlassen')
    # print('4. [r]: Spiel zurücksetzen')
    user_input = input().lower()
    while user_input not in ['', 's', 'q', 'r']:
        print('Bitte wähle ein gültige Option aus.')
        user_input = input()
    return user_input


while True:
    print(logo)
    print('Willkommen zu Blackjack! Komm so nah wie möglich an 21 ohne darüber zu kommen! \n\
          Der Dealer nimmt Karten bis er 17 erreicht. Asse zählen als 1 oder 11.')
    deck = Deck()
    deck.shuffle()

    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())

    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())

    player_chips = Chips()

    take_bet(player_chips)

    while playing:
        hit_or_stand(deck, player_hand)
