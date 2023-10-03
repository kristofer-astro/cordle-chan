from wordle_words import wordle_answers
from wordle_words import wordle_possible
from random import randrange
from time import sleep

# Pick random word from all possible wordle answers
mystery_word = wordle_answers[randrange(0, len(wordle_answers))]
wordle_printable = []   # store printable color blocks to be displayed in terminal
is_solved = False  # Boolean to check whether the mystery word has been guessed

# Variable to store the tiles
white_tile = '⬜'
green_tile = '🟩'
yellow_tile = '🟨'

def wordle():
    is_word_correct = False
    temp_wordle_printable = []  # List to store current wordle output (printed block by block)

    # Check whether input is valid or not
    is_guess_valid = False
    while not is_guess_valid:
        error_msg = ''
        guess = input('Word input: ')
        if guess not in wordle_possible:
            error_msg += 'Invalid word. '

        if len(guess) != 5:
            error_msg += 'Word must be 5 characters long. '

        if len(guess) == 5 and guess in wordle_possible:
            is_guess_valid = True
            break

        print(error_msg + 'Try again!')

    # Main wordle game
    temp_printable = '' # Output of the current guess
    correct_letters = 0

    for index in range(len(guess)):
        # Green tile
        if guess[index] == mystery_word[index]:
            correct_letters += 1
            temp_printable += green_tile

        # Yellow tile
        elif guess[index] in mystery_word and guess[index] != mystery_word[index]:
            temp_printable += yellow_tile

        # White tile
        else:
            temp_printable += white_tile

        if correct_letters == 5:    # Word is guessed
            is_word_correct = True

    # Printing the output
    temp_wordle_printable.append(f'{guess[0].upper()} {guess[1].upper()} {guess[2].upper()} '
                                 f'{guess[3].upper()} {guess[4].upper()}')
    temp_wordle_printable.append(temp_printable)

    print('======================')

    for printable in wordle_printable:
        print(printable)

    print(temp_wordle_printable[0])

    for tile in temp_wordle_printable[1]:
        print(tile, end='')
        sleep(0.4)

    print('\n======================')
    wordle_printable.append(temp_wordle_printable[0])
    wordle_printable.append(temp_wordle_printable[1])

    if is_word_correct:
        return True

tries = 1
while tries <= 6:
    print(f'Attempt #{tries}:')
    is_solved = wordle()

    if is_solved:
        print('Congratulations!! 🎉🎉🎉 You have guessed the right word 🙂')
        break

    tries += 1

if not is_solved:
    print(f'The correct answer is {mystery_word}!')