# Problem Set 2, hangman.py
# Name: 
# Collaborators:
# Time spent:

# Hangman Game
# -----------------------------------

import random
import string


WORDLIST_FILENAME = "words.txt"
VOWELS = {"a", "e", "i", "o", "u"}
UNDERSCORE = "_"
GUESSES_START = 6
WARNINGS_START = 3


def load_words():
    '''
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, "r")
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist


def choose_word(wordlist):
    '''
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    '''
    return random.choice(wordlist)

# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
     lowercase
    letters_guessed: set (of letters), which letters have been guessed so far;
     assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
    False otherwise
    '''
    if set(secret_word) <= letters_guessed:
        return True
    else:
        return False


def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: set (of letters), which letters have been guessed so far
        returns string, comprised of letters, underscores (_), and spaces that represents
        which letters in secret_word have been guessed so far.
    '''
    result = []
    for letter in list(secret_word):
        if letter in letters_guessed:
            result.append(letter)
        else:
            result.append("_ ")
    string = "".join(result)
    return string.rstrip()


def get_available_letters(letters_guessed):
    '''
    letters_guessed: set (of letters), which letters have been guessed so far
      returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    universum = string.ascii_lowercase
    result = []
    for elem in universum:
        if elem not in letters_guessed:
            result.append(elem)
    return "".join(result)


def input_hint():
    wrong = True
    while wrong:
        hint = input()
        if hint.lower() == 'yes':
            return True
        elif hint.lower() == 'no':
            return False
        else:
            print('Your input does not match any possible answer.')
            print('Try again. Would you like to play with hints? Yes/No')
    

def validate_input(letter, letters_guessed):
    '''
    letter: strind with user`s input
    letters_guessed: set of already tried letters
    return: tuple which consists of 2 elements, True/False and string with message according to
    the problem found (if there are no problem the string is empty)
        It checks whether letter is only one symbol long, whether it belongs to ACSII, and
        whether this letter had already been guessed.
    '''
    
    if len(letter) != 1:
        return (False, "You can't guess more than one symbol per a try")
    elif letter not in set(string.ascii_letters):
        return (False, "This is not a valid letter")
    elif letter in letters_guessed:
        return (False, "You've already guessed that letter")
    else:
        return (True, "")


def warning_calculate(guesses, warnings, letter, secret_word, letters_guessed):
    '''
    guesses: integer number showing how much guesses left
    warnings: integer number showing how much warnings left
    letter: string with user`s input
    secret_word: word randomly chosen from all possible ones at the game start
    letters_guessed: set of already guessed letters
      returns: tuple made of number of warnings and guesses left according to the input mistake
      and outputs messages about incorret input.
    '''
    if warnings > 0:
        warnings = warnings - 1
        text = f"You have {warnings} warnings left"
    else:
        text = f"You have no warnings left so you lose one guess"
        guesses = guesses - 1
    _, comment = validate_input(letter, letters_guessed)
    print(f"Oops! {comment}. {text}: {get_guessed_word(secret_word, letters_guessed)}")
    return (warnings, guesses)


def processing_mistake(letter, letters_guessed, guesses, secret_word):
    '''
    letter: string of user`s input (object for checking)
    letters_guessed: set (of letters), which letters have been guessed so far
    guesses: integer number showing how much guesses left
    secret_word: word randomly chosen from all possible ones at the game start

      returns number of guesses after taking player`s inkling depending on whether it 
      was right and what type of letter it was (consonant or vowel)
    '''

    if letter not in set(secret_word):
        print("Oops! That letter is not in my word: ", get_guessed_word(secret_word, letters_guessed))
        if letter in VOWELS:
            guesses = guesses - 2
        else:
            guesses = guesses - 1
    else:
        print("Good guess:", get_guessed_word(secret_word, letters_guessed))
    return guesses


def is_it_end(secret_word, letters_guessed, guesses):
    '''
    letters_guessed: set (of letters), shows which letters have been guessed so far
    guesses: integer number showing how much guesses left
    secret_word: word randomly chosen from all possible ones at the game start
      return: True if game must end, False otherwise
      It checkes whether it is time to finish the game after every player`s step
    '''
    if is_word_guessed(secret_word, letters_guessed):
        return True
    elif guesses <= 0:
        return True
    else:
        return False


def beginning(secret_word, warnings):
    print("Welcome to the game Hangman!")
    print(f"I am thinking of the word that is {len(secret_word)} letters long.")
    print(f"You have {warnings} warnings left.")
    print("Would you like to play with hints? Yes/No")
    hints = input_hint()
    return hints


def ending(secret_word, guesses):
    '''
    secret_word: word chosen for guessing in the beginning of the game
    guesses: number of guesses left
     returns nothing, only print message about end of the game, one for winning
     other for losing
    '''
    print("------------------")
    if guesses <= 0:
        print(f"Sorry, you ran out of guesses. The word was '{secret_word}'.")
    else:
        print("Congratulations, you won!")
        print(f"Your total score for this game is: {guesses * len(set(secret_word))}")


def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
        returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise
    '''
    # gets set of letters which are already known
    letters = set(my_word)
    letters.remove(UNDERSCORE)

    # checks whether length of both words is equal
    if len(my_word) != len(other_word):
        return False
    
    # checks whether letters in both words are equal and if in 
    # first it is underscore whether conforming letter in other one
    # is not in already known ones
    for i, item in enumerate(my_word):
        if item == UNDERSCORE:
            if other_word[i] in letters:
                return False
        else:
            if item != other_word[i]:
                return False
    return True


def show_possible_matches(secret_word, letters_guessed):
    '''
    secret_word: string, the secret word to guess.
    letters_guessed: set of letters were used before.
        returns nothing but prints string with suitable words divided with spaces
    '''
    my_clear_word = get_guessed_word(secret_word, letters_guessed).replace(" ", "")

    matched_words = [x for x in wordlist if match_with_gaps(my_clear_word, x)]
    matched_words = " ".join(matched_words)
    if not matched_words:
        print("No matches found.")
    else:
        print(f"Possible word matches are: \n{matched_words}")

# -----------------------------------

def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    '''
    guesses = GUESSES_START
    warnings = WARNINGS_START
    guessed_letters = set()

    hints = beginning(secret_word, warnings)

    game = True
    while game:
        print("------------------")
        print(f"You have {guesses} guesses left.")
        print("Available letters: ", get_available_letters(guessed_letters))
        inkling = input("Please guess a letter: ")

        #cheking whether user wants hint to be shown
        if hints and inkling == "*":
            show_possible_matches(secret_word, guessed_letters)
            continue

        #cheking whether input is in appropriate format and taking away warnings/guesses in case of
        # mistake, also updating list of already guessed letters. 
        if validate_input(inkling, guessed_letters)[0]:
            inkling = inkling.lower()
            guessed_letters.add(inkling)
        else:
            warnings, guesses = warning_calculate(guesses, warnings, inkling, secret_word, guessed_letters)
            continue
        
        #function that updates number of guesses left.
        guesses = processing_mistake(inkling, guessed_letters, guesses, secret_word)

        #checks whether it is time to end a game
        if is_it_end(secret_word, guessed_letters, guesses):
            game = False
            
    ending(secret_word, guesses)

# -----------------------------------

if __name__ == "__main__":
    
    secret_word = choose_word(wordlist)
    hangman(secret_word)