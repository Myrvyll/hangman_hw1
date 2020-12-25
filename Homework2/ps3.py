# 6.0001 Problem Set 3
#
# The 6.0001 Word Game
# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>
#
# Name          : Babych Iryna (Myrvyll)
# Collaborators : --
# Time spent    : <total time>

import math
import random
import string

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
LETTERS = 'aeioubcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7
WILDCARD = '*'

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10, '*': 0
}

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq
	

# (end of helper code)
# -----------------------------------

#
# Problem #1: Scoring a word
#
def get_word_score(word, n):
    """
    Returns the score for a word. Assumes the word is a
    valid word.

    word: string
    n: int >= 0
    returns: int >= 0
    """
    wordlen = len(word)
    word = word.lower()

    sum_of_letters = 0
    for el in word:
        sum_of_letters += SCRABBLE_LETTER_VALUES[el]

    coefficient = 7*wordlen - 3*(n-wordlen)
    if coefficient < 1:
        coefficient = 1

    return sum_of_letters*coefficient


def display_hand(hand):
    """
    Displays the letters currently in the hand.

    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """
    print('Current hand: ', end='')
    for letter in hand.keys():
        for _ in range(hand[letter]):
             print(letter, end=' ')      # print all on the same line
    print()                              # print an empty line


def enter_natnumbers(comment):
    '''
    Takes input from user and checks whether it is integer number 
    which is more than 0. Lets user input more than 1 time.

    comment: string that is outputted when function is called
    return: integer
    '''

    wrong = True
    while wrong:
        number = input(comment)

        try:
            number = int(number)
            if number <= 0:
                raise TypeError
            wrong = False

        except ValueError:
            print('It is not a number. Try again.')
        except TypeError:
            print('Number of hands must be more or equal to 1.')

    return int(number)


def yes_no(comment):
    '''
    Takes input from user and checks whether it is string containing 
    one word "yes" or "no". Lets user input more than 1 time.
    
    comment: string that is outputted when function is called
    return: string "yes" or "no"
    '''
    wrong = True
    while wrong:
        line = input(comment)

        if line.lower() == 'yes' or line.lower() == 'no':
            wrong = False
        else:
            print('It is not a possible answer.')

    return line


def latin_letters(comment):
    '''
    Takes input from user and checks whether it is string containing 
    one letter from latin alphabet. Lets user input more than 1 time.
    
    comment: string that is outputted when function is called
    return: string with one letter
    '''    

    wrong = True
    while wrong:
        line = input(comment)
        if len(line) == 1 and line in LETTERS:
            wrong = False
        else:
            print('It must be one latin letter.')
    
    return line



def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    ceil(n/3) letters in the hand should be VOWELS (note,
    ceil(n/3) means the smallest integer not less than n/3).

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """
    
    hand = {}
    num_vowels = int(math.ceil(n / 3))

    for _ in range(num_vowels-1):
        x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1
    
    for _ in range(num_vowels, n):    
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1

    hand[WILDCARD] = 1
    
    return hand


def update_hand(hand, word):
    """
    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not modify hand.

    word: string
    hand: dictionary (string -> int)    
    returns: dictionary (string -> int)
    """

    hand2 = hand.copy()
    word = word.lower()

    for el in word:
        if not hand2.get(el, 0):
            pass
        else:
            hand2[el] -= 1
            
    return hand2


def is_valid_word(word, hand, word_list):
    """
    Returns True if word is in the word_list and is entirely
    composed of letters in the hand. Otherwise, returns False.
    Does not mutate hand or word_list.
   
    word: string
    hand: dictionary (string -> int)
    word_list: list of lowercase strings
    returns: boolean
    """
    hand2 = hand.copy()
    word = word.lower()

    #checks whether word with wildcard exists
    if word.find(WILDCARD) != -1:

        found = False                           
        for element in VOWELS:
            word2 = word.replace(WILDCARD, element)

            if word2 in word_list:
                found = True
        
        if not found:
            return False

    #checks whether common word exist
    elif word not in word_list:
        return False

    #checks whether there are enough letters in hand
    for letter in word:

        if hand.get(letter) == None:
            return False
        if not hand2[letter]:
            return False
        else:
            hand2[letter] -= 1

    return True


def calculate_handlen(hand):
    """ 
    Returns the length (number of letters) in the current hand.
    
    hand: dictionary (string-> int)
    returns: integer
    """
    summa = 0
    for item in hand.values():
        summa += item

    return summa



def play_hand(hand, word_list):

    """
    Allows the user to play the given hand, as follows:

      hand: dictionary (string -> int)
      word_list: list of lowercase strings
      returns: the total score for the hand
      
    """
    total_score = 0

    playing = True
    while playing:

        display_hand(hand)
        handlen = calculate_handlen(hand)
        
        word = input('Enter word, or “!!” to indicate that you are finished: ')
        
        #stops function if !! is inputted
        if word == '!!':
            playing = False
            continue

        #processes situation when the word is inputted in a right way
        if is_valid_word(word, hand, word_list):
            score = get_word_score(word, handlen)
            total_score += score
            print(f'"{word}" earned {score} points. Total: {total_score} points\n')
      
        else:
            print('This is not a valid word. Please choose another word.\n')

        hand = update_hand(hand, word)
        
        #stops function if there are no letters left
        if not calculate_handlen(hand):
            print(f'Ran out of letters. ', end='')
            playing = False

    print(f'Total score: {total_score} points')        
    return total_score


def substitute_hand(hand, letter):
    """ 
    Allow the user to replace all copies of one letter in the hand (chosen by user)
    with a new letter chosen from the VOWELS and CONSONANTS at random. The new letter
    should be different from user's choice, and should not be any of the letters
    already in the hand.

    If user provide a letter not in the hand, the hand should be the same.

    Has no side effects: does not mutate hand.

    For example:
        substitute_hand({'h':1, 'e':1, 'l':2, 'o':1}, 'l')
    might return:
        {'h':1, 'e':1, 'o':1, 'x':2} -> if the new letter is 'x'
    The new letter should not be 'h', 'e', 'l', or 'o' since those letters were
    already in the hand.
    
    hand: dictionary (string -> int)
    letter: string
    returns: dictionary (string -> int)
    """
    hand2 = hand.copy()

    past_letters = hand2.keys()
    available_letters = list(LETTERS - past_letters)
    
    #if letter in hand replaces it
    if letter in hand.keys():
        new_letter = random.choice(available_letters)
        hand2[new_letter] = hand2.pop(letter)

    return hand2
       
    
def play_game(word_list):
    """
    Allow the user to play a series of hands
      
    word_list: list of lowercase strings
    Return: the total score for the series of hands
    """

    number_of_hands = enter_natnumbers('Enter total number of hands: ')

    overall_score = 0

    while number_of_hands:

        start_hand = deal_hand(HAND_SIZE)
        display_hand(start_hand)
        
        substitute = yes_no('Would you like to substitute a letter? ')

        #processes substitude if user answered yes
        if substitute.lower() == 'yes':
            letter_to_change = latin_letters('Which letter would you like to replace: ')
            hand = substitute_hand(start_hand, letter_to_change)
        else:
            hand = start_hand
        #counts score and plays hand
        score_for_hand = play_hand(hand, word_list)

        #processes replay
        print('--------')
        replay = yes_no('Would you like to replay the hand? ')
        if replay.lower() == 'yes':
            score_for_hand_try2 = play_hand(hand, word_list)
        else:
            score_for_hand_try2 = 0
        #updates overall score
        overall_score += max(score_for_hand, score_for_hand_try2)

        number_of_hands -= 1

    print('--------')
    print('Total score over all hands:', overall_score)

    return overall_score
    

if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)
