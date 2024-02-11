from wordle_words import wordle_answers
from wordle_words import wordle_possible
from random import randrange
from time import sleep

# Pick random word from all possible wordle answers
mystery_word = wordle_answers[randrange(0, len(wordle_answers))]
wordle_printable = []   # store printable color blocks to be displayed in terminal
is_solved = False  # Boolean to check whether the mystery word has been guessed

# Variable to store the tiles
white_tile = ':white_large_square:'
green_tile = ':green_square:'
yellow_tile = ':yellow_square:'

def check_input_validity() -> str:
    while True:
        error_msg = ''
        guess = input('Word input: ').strip().lower()
        if guess not in wordle_possible:
            error_msg += 'Invalid word. '

        if len(guess) != 5:
            error_msg += 'Word must be 5 characters long. '

        if len(guess) == 5 and guess in wordle_possible:
            return guess

        print(error_msg + 'Try again!')

def count_letters(word) -> dict:
    # Create a dictionary to store the count of each letter
    letter_count = {}

    # Iterate over each letter in the word
    for letter in word:
        # Increment the count of the current letter in the dictionary
        letter_count[letter] = letter_count.get(letter, 0) + 1

    return letter_count

def wordle() -> bool:
    is_word_correct = False
    temp_wordle_printable = []  # List to store current wordle output (printed block by block)
    green_list = []

    # Check whether input is valid or not
    guess = check_input_validity()

    # Main wordle game
    temp_printable = '' # Output of the current guess
    correct_letters = 0

    # debug
    # mystery_word = 'spell'

    # returns a dict of each letter count in the word
    guess_letter_count = count_letters(guess)
    mystery_word_letter_count = count_letters(mystery_word)

    # iterates 5 times
    for index in range(len(guess)):
        # Green tile
        if guess[index] == mystery_word[index]:
            correct_letters += 1
            temp_printable += green_tile

            #updating the letter count
            green_list.append(guess[index])
            guess_letter_count[guess[index]] -= 1
            mystery_word_letter_count[mystery_word[index]] -= 1

        # Yellow tile
        elif guess[index] in mystery_word and guess[index] != mystery_word[index]:
            green_tileable = False

            # this for loop prioritizes green tile over yellow tile
            for j in range(5):
                if guess[j] == mystery_word[j] and guess[j] == guess[index]:
                    green_tileable = True

            if green_tileable and (guess[index] not in green_list) and mystery_word_letter_count[guess[index]] == 1:
                temp_printable += white_tile
                guess_letter_count[guess[index]] -= 1

            else:
                # this if statement ensures the case of duplicate letters in the mystery word
                if mystery_word_letter_count[guess[index]] > 0 and guess_letter_count[guess[index]] > 0:
                    temp_printable += yellow_tile

                    # updating the letter count
                    guess_letter_count[guess[index]] -= 1
                    mystery_word_letter_count[guess[index]] -= 1

                else:
                    temp_printable += white_tile

                    # updating the letter count
                    guess_letter_count[guess[index]] -= 1

        # White tile
        else:
            temp_printable += white_tile

            # updating the letter count, ONLY the guess letter count is updated SINCE the guess letter is NOT in the mystery word
            guess_letter_count[guess[index]] -= 1

        if correct_letters == 5:    # Word is guessed
            is_word_correct = True

    # appending the output to be printed
    temp_wordle_printable.append(f'{guess[0].upper()} {guess[1].upper()} {guess[2].upper()} '
                                 f'{guess[3].upper()} {guess[4].upper()}')
    temp_wordle_printable.append(temp_printable)

    print('======================')

    # printing the past attempts
    for printable in wordle_printable:
        print(printable)

    # printing the current attempt
    print(temp_wordle_printable[0])

    for tile in temp_wordle_printable[1]:
        print(tile, end='')
        sleep(0.4)

    print('\n======================')

    # appending the current attempt to the wordle printable list to be printed in the next attempt as past attempt
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