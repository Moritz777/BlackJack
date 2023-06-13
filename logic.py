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


class Card:

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.rank + ' of ' + self.suit



def main():
    """
    Ask the user for their name. Start the game.
    """
    print(logo)
    name = ''
    while name == '':
        name = input('Wie heißt du? ')

    blackjack()


def blackjack():
    """
    Implement the game "Blackjack".
    """
    # Initialize starting scores for all the players to avoid
    # KeyErrors
    player_hand = []
    can_continue = True
    while True:
        player_input = get_player_input()
        if player_input == '':
            player_hand.append(deal_card())
            print(player_hand)
        elif player_input == 's':
            print(f"Your final hand: {player_hand}, final score: {calculate_score(player_hand)}")
            continue
        # elif player_input == 'r':
        #    blackjack()
        elif player_input == 'q':
            exit(0)


def deal_card():
    """
    Let the player draw a card.
    :return: value of the card which was drawn
    """
    cards = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]
    card = random.choice(cards)
    return card


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
    user_input = input()
    while user_input not in ['', 's', 'q', 'r']:
        print('Bitte wähle ein gültige Option aus.')
        user_input = input()
    return user_input


if __name__ == '__main__':
    main()
