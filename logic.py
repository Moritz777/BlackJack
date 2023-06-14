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

import time
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
                self.deck.append(Card(suit, rank))  # build Card objects and add them to the list

    def __str__(self):
        deck_comp = ''  # start with an empty string
        for card in self.deck:
            deck_comp += '\n '+card.__str__()  # add each Card object's print string
        return 'Das Deck hat:' + deck_comp

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

    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.rank]

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

    while True:
        player_input = input("Hit (weitere Karte) oder Stand (Halten)? '<Eingabe>' oder 's'? ")

        if player_input == '':
            hit(deck, hand)

        elif player_input[0].lower() == 's':
            print("Du nimmst keine weitere Karte. Der Dealer spielt.")
            playing = False
            time.sleep(1)

        elif player_input[0].lower() == 'q':
            exit(0)
        break


def show_some(player, dealer):
    """
    function to display some cards (keep the dealers second card hidden)
    :param player: the player
    :param dealer: the dealer
    """
    print("\nHand des Dealers:")
    print(" <Karte versteckt>")
    print('', dealer.cards[1])
    print("\nSpieler Hand:", *player.cards, sep='\n ')
    print(f"Dein bisheriger Score: {player.value}")


def show_all(player, dealer):
    """
    function to display all cards
    :param player: the player
    :param dealer: the dealer
    """
    print("\nHand des Dealers:", *dealer.cards, sep='\n ')
    print("Dealer finaler Score:", dealer.value)
    print("\nSpieler Hand:", *player.cards, sep='\n ')
    print(f"Dein finaler Score: {player.value}")


# functions to handle end of game scenarios

def player_busts(player, dealer, chips):
    print("Spieler hat über 21!")
    chips.lose_bet()


def player_wins(player, dealer, chips):
    print("Spieler gewinnt!")
    chips.win_bet()


def dealer_busts(player, dealer, chips):
    print("Dealer hat über 21!")
    chips.win_bet()


def dealer_wins(player, dealer, chips):
    print("Dealer gewinnt!")
    chips.lose_bet()


def push(player, dealer):
    print("Dealer und Spieler haben gleich viel! Unentschieden.")


# Spielablauf

while True:
    # greeting the player
    print(logo)
    print('Willkommen zu Blackjack! Komm so nah wie möglich an 21 ohne darüber zu kommen! \n\
          Der Dealer zieht Karten bis er 17 erreicht. Asse zählen als 1 oder 11.')

    # Create & shuffle the deck, dealing two cards to each player (dealer & player)
    deck = Deck()
    deck.shuffle()

    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())

    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())

    # Set up the Player's chips
    player_chips = Chips()

    # Prompt the Player for their bet
    take_bet(player_chips)

    # Show cards (but keep one dealer card hidden)
    show_some(player_hand, dealer_hand)
    time.sleep(1)

    while playing:

        # Prompt the Player to Hit or Stand
        hit_or_stand(deck, player_hand)

        # Show cards (but keep one dealer card hidden)
        show_some(player_hand, dealer_hand)
        print("Der Dealer zieht noch eine Karte")
        time.sleep(5)

        # If Player's hand exceeds 21, run player_busts() and break out of loop
        if player_hand.value > 21:
            player_busts(player_hand, dealer_hand, player_chips)
            break

        # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
        if player_hand.value <= 21:
            while dealer_hand.value < 17:
                hit(deck, dealer_hand)

            # Show all cards
            show_all(player_hand, dealer_hand)

            # Run different winning scenarios
            if dealer_hand.value > 21:
                dealer_busts(player_hand, dealer_hand, player_chips)

            elif dealer_hand.value > player_hand.value:
                player_wins(player_hand, dealer_hand, player_chips)

            else:
                push(player_hand, dealer_hand)

    print("\nSpielgewinn ist bei", player_chips.total)

    # Ask to play again
    new_game = input("Möchtest du noch eine Runde spielen? Gib 'j' oder 'n' ein. ")

    if new_game[0].lower() == 'j':
        playing = True
        continue
    else:
        print("Danke für's spielen!")
        break
