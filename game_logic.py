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
    Create six decks from the given cards
    """
    def __init__(self):
        self.deck = []  # start with an empty list
        for i3 in range(6):
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
        if card.rank == 'Ace':
            self.aces += 1

    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1


class Chips:
    """
    keep track of the players capital, bets and ongoing winnings.
    """
    def __init__(self):
        self.total = 100000  # Can be set to default value or supplied by database, user capital in cents (e.g. 100€)
        self.bet = 0  # the amount the player bets for one round
        self.win = 0  # win from one round

    def win_bet(self):
        self.win += self.bet
        self.total += self.win

    def lose_bet(self):
        self.win -= self.bet
        self.total += self.win

    def win_blackjack(self):
        self.win += self.bet
        self.win += self.bet * 0.5
        self.total += self.win


# Functions start here

def take_bet(chips):
    """
    take bets from the player
    :param chips: the players chips as given below
    """
    while True:
        print(f"Dein Kontostand beträgt: {player_chips.total / 100}€")
        try:
            chips.bet = int(input('Wie viel Geld möchtest du setzen? '))*100
        except ValueError:
            print('Bitte eine Zahl eingeben!')
        else:
            if chips.bet > chips.total:
                print(f"Sorry, du kannst nicht mehr als {chips.total/100}€ setzen")
            elif chips.bet <= 500:
                print('Sorry, du musst mehr als 5€ setzen.')
            elif chips.bet > 2000:
                print('Sorry, es dürfen maximal 20€ gesetzt werden.')
            else:
                break


def hit(decks, hand):
    """
    Let the player draw a card.
    """
    hand.add_card(decks.deal())
    hand.adjust_for_ace()


def hit_or_stand(decks, hand):
    """
    Prompt the player to hit or stand.
    """
    global playing  # for use in an upcoming while loop

    while True:
        player_input = input("Hit (weitere Karte) oder Stand (Halten)? '<Eingabe>' oder 's'? ")

        if player_input == '':
            hit(decks, hand)
            return True

        elif player_input[0].lower() == 's':
            print("Du nimmst keine weitere Karte.")
            playing = False
            time.sleep(1)
            return False

        elif player_input[0].lower() == 'q':
            exit(0)
        break


def show_cards(player, dealer):
    """
    function to display all cards
    :param player: the player
    :param dealer: the dealer
    """
    print("\nHand des Dealers:", *dealer.cards, sep='\n ')
    print("Dealer Score:", dealer.value)
    print("\nSpieler Hand:", *player.cards, sep='\n ')
    print(f"Dein Score: {player.value}")


# functions to handle end of game scenarios
def player_busts(chips):
    print("Spieler hat über 21! Verloren!")
    chips.lose_bet()


def player_wins(chips):
    print("Spieler gewinnt!")
    chips.win_bet()


def player_wins_blackjack(chips):
    print("Blackjack! Spieler gewinnt!")
    chips.win_blackjack()


def player_wins_tripple_seven(chips):
    print("Tripple Seven! Spieler gewinnt!")
    chips.win_blackjack()


def dealer_busts(chips):
    print("Der Dealer hat über 21! Spieler gewinnt!")
    chips.win_bet()


def dealer_wins(chips):
    print("Dealer gewinnt! Spieler hat verloren!")
    chips.lose_bet()


def dealer_wins_blackjack(chips):
    print("Dealer hat Blackjack und gewinnt! Spieler hat verloren!")


def push():
    print("Dealer und Spieler haben gleich viel! Unentschieden.")


def greet_player():
    print(logo)
    print('Willkommen zu Blackjack! Komm so nah wie möglich an 21 ohne darüber zu kommen! \n\
              Der Dealer zieht Karten bis er 17 erreicht. Asse zählen als 1 oder 11.')


# Spielablauf
while True:

    # greeting the player
    greet_player()

    # Create & shuffle the deck, dealing two cards to the player
    deck = Deck()
    deck.shuffle()

    # deal one card to the dealer
    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    i2 = 0

    # deal two cards to the player
    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())
    i = 1

    # Set up the Player's chips
    player_chips = Chips()

    # Prompt the Player for their bet
    take_bet(player_chips)

    # Show cards
    show_cards(player_hand, dealer_hand)
    time.sleep(1)

    if player_hand.value == 21:
        player_wins_blackjack(player_chips)
        playing = False

    while playing:

        # Prompt the Player to Hit or Stand
        if hit_or_stand(deck, player_hand):
            i += 1
            print('Du ziehst eine:', player_hand.cards[i])
            time.sleep(1)

        # Show cards
        show_cards(player_hand, dealer_hand)
        time.sleep(1)

        if player_hand.value == 21:  # and player_hand.cards[card].rank == 'Seven':
            i7 = 0
            for card in range(0, len(player_hand.cards)):
                if player_hand.cards[card].rank == 'Seven':
                    i7 += 1
                    print(f"Der Spieler hat {i7} Sieben(en) auf der Hand.")
                    if i7 == 3:
                        player_wins_tripple_seven(player_chips)
                        playing = False

        # If Player's hand exceeds 21, run player_busts() and break out of loop
        if player_hand.value > 21:
            player_busts(player_chips)
            time.sleep(2)
            break

        if player_hand.value == 21:
            pass  # TODO: don't ask the player again if he wants to hit, let him stand automatically

    # If Player hasn't busted or tripple seven, play Dealer's hand until Dealer reaches 17
    if player_hand.value <= 21:
        '''
        # prompt the player to hit or stand again
        if playing is True and hit_or_stand(deck, player_hand):
            i += 1
            print('Du ziehst eine:', player_hand.cards[i])
            time.sleep(2)
        '''

        while dealer_hand.value < 17:
            print('Der Dealer zieht eine Karte.')
            hit(deck, dealer_hand)
            i2 += 1
            print('Der Dealer hat gezogen:', dealer_hand.cards[i2])
            time.sleep(2)

        if dealer_hand.value == 21 and len(dealer_hand.cards) == 2:
            print('Der Dealer hat Blackjack!')

        # Show all cards
        show_cards(player_hand, dealer_hand)
        time.sleep(2)

        # Run different winning scenarios
        if dealer_hand.value > 21:
            dealer_busts(player_chips)
            time.sleep(2)

        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_chips)
            time.sleep(2)

        elif dealer_hand.value < player_hand.value:
            player_wins(player_chips)
            time.sleep(2)

        elif dealer_hand.value == 21:  # TODO: Separate Blackjack and just having 21
            print('Dealer und Spieler haben Blackjack!')
            push()
            time.sleep(2)

        else:
            push()
            time.sleep(2)

    print(f"\nSpielgewinn ist bei: {player_chips.win/100}€")
    print(f"Kontostand ist bei: {player_chips.total/100}€")

    # Ask to play again
    new_game = input("Möchtest du noch eine Runde spielen? Gib 'j' oder 'n' ein. ")

    if new_game[0].lower() == 'j':
        playing = True
        continue
    else:
        print("Danke für's spielen!")
        break
