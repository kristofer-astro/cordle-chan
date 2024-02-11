import nextcord
from nextcord import Intents
from nextcord.ext import commands

# IMPORT WORDLE
from wordle_words import wordle_answers
from wordle_words import wordle_possible
from random import randrange
from time import sleep

# Load TOKEN
TOKEN = ''

# BOT SETUP
intents = Intents.default()
intents.message_content = True
cordle = commands.Bot(command_prefix=">", intents=intents)


# MAIN BOT FUNCTIONALITY
cordle.remove_command('help')

@cordle.slash_command(name='ping')
async def ping(interaction: nextcord.Interaction):
    await interaction.response.send_message(f'Pong :ping_pong:: {round(cordle.latency * 1000)} ms ')

@cordle.slash_command(name='help', description='List of commands')
async def help(interaction: nextcord.Interaction):

    help_embed = nextcord.Embed(
        title='Hi~!! Cordle-chan here >w<',
        description='Cordle-chan is a Wordle discord bot ! OwO',
        colour=nextcord.Colour.yellow()
    )

    help_embed.add_field(name=':wrench: Utility Commands', value='`/help` - Displays this message \n'
                                                                 '`/ping` - Returns the latency of the bot',
                         inline=False)
    help_embed.add_field(name=':jigsaw: Wordle Commands', value='`/wordle` - Initiates a Wordle game \n'
                                                                '`>input (word)` - Guessing a word for the puzzle',
                         inline=False)
    help_embed.add_field(name=':bulb: More Features Coming Soon!', value='', inline=False)

    await interaction.response.send_message(embed=help_embed)



'''
=================================================== WORDLE GAME ========================================================
'''

# initializing global variables
player = ''
game_over = True
is_solved = False
all_printable = []
attempts = 0
white = ':white_large_square:'
green = ':green_square:'
yellow = ':yellow_square:'
mystery_word = ''

@cordle.slash_command(name='wordle', description='Play Wordle game on Discord!', dm_permission=True)
async def wordle(interaction: nextcord.Interaction):
    embed = nextcord.Embed(
        title='test title',
        description='this is the description',
        color=nextcord.Colour.green()
    )

    global player, game_over, attempts, mystery_word

    if game_over:
        global printable
        game_over = False
        player = interaction.user
        attempts = 0

        # Pick random word from all possible wordle answers
        mystery_word = wordle_answers[randrange(0, len(wordle_answers))]

        await interaction.response.send_message(f'Please enter a 5-letter word, {player.mention}!\n'
                                                f'Type `>input (word)` !!')

    else:
        await interaction.response.send_message('A game is currently in progress!')



@cordle.command(name='input')
async def wordle_input(ctx, guess : str):
    global player, game_over, all_printable, attempts, mystery_word, white, green, yellow, is_solved

    # checks if a game is currently running or not
    if not game_over:

        # ensures that the game is unique for each player
        if player == ctx.author:

            # CHECK FOR INPUT VALIDATION
            error_msg = ''
            guess = guess.strip().lower()

            if guess not in wordle_possible:
                error_msg += 'Invalid word. '

            if len(guess) != 5:
                error_msg += 'Word must be 5 characters long. '

            if error_msg != '':
                await ctx.send(error_msg + 'Try again!')

            # IF INPUT IS VALID, STARTS AN ATTEMPT
            if len(guess) == 5 and guess in wordle_possible:
                await ctx.send(f'Your input "{guess}" is VALID !')

                attempt_printable = [f'`  {guess[0].upper()}     {guess[1].upper()}      {guess[2].upper()}      '
                                 f'{guess[3].upper()}     {guess[4].upper()}  `'] # List to store current wordle output (printed block by block)
                green_list = []
                block_printable = ''
                correct_letters = 0

                guess_count = {letter: guess.count(letter) for letter in guess}
                mystery_count = {letter: mystery_word.count(letter) for letter in mystery_word}

                # MAIN WORDLE GAME
                for index in range(len(guess)):
                    # Green tile
                    if guess[index] == mystery_word[index]:
                        correct_letters += 1
                        block_printable += green

                        # updating the letter count
                        green_list.append(guess[index])
                        guess_count[guess[index]] -= 1
                        mystery_count[mystery_word[index]] -= 1

                    # Yellow tile
                    elif guess[index] in mystery_word and guess[index] != mystery_word[index]:
                        green_tileable = False

                        # this for loop prioritizes green tile over yellow tile
                        for j in range(5):
                            if guess[j] == mystery_word[j] and guess[j] == guess[index]:
                                green_tileable = True

                        if green_tileable and (guess[index] not in green_list) and mystery_count[
                            guess[index]] == 1:
                            block_printable += white
                            guess_count[guess[index]] -= 1

                        else:
                            # this if statement ensures the case of duplicate letters in the mystery word
                            if mystery_count[guess[index]] > 0 and guess_count[guess[index]] > 0:
                                block_printable += yellow

                                # updating the letter count
                                guess_count[guess[index]] -= 1
                                mystery_count[guess[index]] -= 1

                            else:
                                block_printable += white

                                # updating the letter count
                                guess_count[guess[index]] -= 1

                    # White tile
                    else:
                        block_printable += white

                        # updating the letter count, ONLY the guess letter count is updated SINCE the guess letter is NOT in the mystery word
                        guess_count[guess[index]] -= 1

                    if correct_letters == 5:
                        is_solved = True

                # APPENDING OUTPUT TO CURRENT ATTEMPT OUTCOME
                attempt_printable.append(block_printable)

                # PRINTING THE MAIN OUTPUT

                for attempt in all_printable:
                    await ctx.send(attempt)

                await ctx.send(attempt_printable[0])
                await ctx.send(attempt_printable[1])    # can be improved(?) add delay for every block printed -> edit message


                # END OF AN ATTEMPT
                attempts += 1;
                all_printable.append(attempt_printable[0])
                all_printable.append(attempt_printable[1])

                # CHECKS IF PUZZLE IS SOLVED OR USER FINISHES THEIR 6TH ATTEMPT BUT NOT SOLVED -> ENDS THE GAME
                if is_solved:
                    await ctx.send('Congratulations!! 🎉🎉🎉 You have guessed the right word 🙂')
                    game_over = True
                    all_printable = []
                    attempts = 0

                if attempts == 6 and not is_solved:
                    await ctx.send(f'The correct answer is {mystery_word}!')
                    game_over = True
                    all_printable = []
                    attempts = 0

        else:
            await ctx.send('Please start a new Wordle game using `/wordle` !')
    else:
        await ctx.send('Please start a new Wordle game using `/wordle` !')


@cordle.command(name='exit')
async def exit_game(ctx):
    global game_over, all_printable, attempts, mystery_word

    if not game_over:
        game_over = True
        all_printable = []
        attempts = 0

        await ctx.send(f'You have forcibly end the game! The answer is {mystery_word}!')
    else:
        await ctx.send('There is no game currently running!')

'''
=================================================== WORDLE GAME ========================================================
'''


# BOT STARTUP
@cordle.event
async def on_ready() -> None:
    print(f'{cordle.user.name} is online!')

# LOGGING INCOMING MESSAGES
'''
@bot.event
async def on_message(message) -> None:
    if message.author == bot.user:
        return

    print(f'[{message.channel}] {message.author}: "{message.content}"')
'''

# MAIN ENTRY POINT
cordle.run(token=TOKEN)



'''
========================================================================================================================
FEATURES TO BE ADDED

- EMBEDS EMBEDS EMBEDS
- PING COMMAND
- WORDLE PRINTABLE EMBED INSTANT THEN CURRENT ATTEMPT PRINT BLOCK BY BLOCK EDIT WITH TIME DELAY?
- RNG THINGS
- END GAME EARLY FEATURE






========================================================================================================================
'''
