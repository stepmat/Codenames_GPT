# Codenames AI Competition (2025)

![image](https://github.com/user-attachments/assets/510cbaa5-a579-46a3-94c6-2cee11f60a7c)

This is the main repository for the (new and revised) Codenames AI Competition Framework, focussed on the development of LLM powered agents to play the word association game "Codenames" by Vlaada Chvatil. The purpose of this competition is to develop an AI benchmark that:

* Requires an understanding of natural language.
* Requires communication, in a semantically meaningful way, with players of unknown provenance - the player on the other side of the table may be a human or it may be another agent.
* Requires an understanding of the multiple meanings and associations that words may have.

This competition and the code framework provided in this repository are based on the original Codenames AI competition (https://github.com/CodenamesAICompetition/Game), but with the following major modifications:

* The game rules have been altered to more closely represent those of the original game, with the largest modification being that it is now possible for two teams to compete against each other, with each team consisting of a Codemaster and Guesser agent.
* A renewed emphasis on utilising the capabilities of LLMs (such as GPT-4, Gemini, Claude or Llama) to identify suitable clues and guesses. More traditional Codenames game-playing techniques (such as utilising word vector embeddings) are also applicable, either alongside LLM models or as a stand-alone technique. However, the emphasis with this new competition will be on agents that are able to handle new and previously unseen wordsets, and agents who are able to play effectively alongside wide range of potential teammates.
  
**Further installation requirements are found below.**

## Registration

To register for this competition, please post a message on the following discord group stating your team name, along with details of the members and their affiliations:
* [Discord](https://discord.gg/uHUynQJp6r)

A separate private channel for your team will then be created for you to ask private questions to the organisers.
Public questions or troubleshooting requests should be posted on the main general channel.

## Submissions

Competition entrants will need to submit two agents, one Codemaster and one Guesser.

We strongly encourage teams to submit these agents as single python files whenever possible, mimicking the layout and structure of the example codemaster_GPT.py and guesser_GPT.py files.
The exact functions that submitted Codemaster and Guesser Classes much provide in order to function are specified in the **Codenames AI Framework** section below.
Entrants may submit additional files if they are required, but should provide complete instructions / documentation for their usage.
Entrants should not modify any of the other files provided as part of this framework.

Entrants will need to provide complete instructions for how to run their agents on the following hardware:
* **Operating System:** Windows 11 or Ubuntu 24.04
* **Processor:** AMD Ryzen Threadripper PRO 5955WX (64 MB cache, 16 cores, 32 threads, 4.0GHz to 4.5GHz)
* **Memory:** 256GB, 4x64GB, DDR4, 3200MHz, RDIMM ECC Memory
* **Video Card:** NVIDIA® RTX™ A6000, 48 GB GDDR6, 4 DP
* **Storage:** 100GB

Entrants must ensure that both the submitted Codemaster and Guesser agent can run concurrently on the above hardware (i.e., available VRAM must be shared by both Codemaster and Guesser at the same time).
Agents also need to provide a response when requested in a timely fashion, with a soft time limit of 60 seconds being imposed. Agents that repeatedly or egregiously breach this time limit when requested by the framework for a clue or guess response, will be disqualified.

Submitted agents may utilise external services (such as the OpenAI API utilised by the provided GPT agent) but entrants will need to ensure that any necessary keys and funds required for these services are provided for. 
To encourage the use of open-source models, and to allow those who cannot afford external API services to still compete, we will award an additional special prize to the entrant that develops a solution that does not rely on external services.

## Competition Format

The competition will consist of two separate tracks:

* **Single Team:** Played using the same scoring system as the previous Codenames AI framework, where a single team (red codemaster/guesser) attempts to identify all red words in as few turns as possible. Teams are awarded a score at the end of the game based on the number of turns taken (lower score is better). The only exception to this is if the guesser selects all blue words or the assassin word, which results in a maximum score of 25 points.
* **Two Teams:** Played using the full set of rules from the original Codenames game, where two teams (red codemaster/guesser and blue codemaster/guesser) attempt to identify all words of their team’s colour first. Selecting the assassin word results in an immediate win for the other team. Guessers can also inadvertently help the opposing team win if they accidentally select any words of their colour. Rather than using a scoring system, this version measures success in terms of overall win-rate.

Each submission will (unless otherwise requested by the entrants) be automatically included in both tracks, with the entrant evaluation process for both tracks being as follows:

* **First Round:** The first round will consist of a round robin style tournament to evaluate the performance of each entrant team. For the Single Team track, performance will be determined based on the average score over all games. For the Two Teams track, performance will be determined based on the average win-rate over all games. The top performing four teams from each track will then progress to the second round. In the event of a tie, a single additional game will be played to break the split.
* **Second Round:** The second round will consist of a single elimination style knockout tournament between the top four teams. Pair-ups will be determined by standard seeding (i.e., highest paired with lowest) and matches will be a best of three games.

## Prize Money

This competition is supported by the IEEE Computational Intelligence Society (CIS) who have provided prize money for the successful winners of each track (single and two teams). Prize money will be allocated for the 1st, 2nd and 3rd place winners of each track as follows:

* **First Place:** $500 USD
* **Second Place:** $300 USD
* **Third Place:** $200 USD

Please note, these prizes must be awarded in accordance with the [IEEE CIS prize distribution policy](https://cis.ieee.org/images/files/Documents/competitions/prize-dist-policy.pdf). This means that competition entrants who wish to be eligible for this prize money must be involved in a maximum of one submission team.

## Additional Rules

### Clue Requirements

Competition agents must abide the rules of Codenames regarding valid clues, and not attempt to manipulate the limitations of this framework in order to gain an unfair advantage. This includes, but is not limited to:
* Using their clue to indicate the position of words to select rather than by language association (e.g., using the clue "Four-Two" to indicate the position of word(s)).
* Using compound or misspelled words in their clue to provide additional information (e.g., using the clue "Bearbirdfox" to indicate multiple words).
* Using non-English or foreign words for their clues.

Full rules on valid clues can be found in the official game rulebook (https://czechgames.com/files/rules/codenames-rules-en.pdf). Agent clues will be reviewed by the competition organisers and any agents repeatedly breaking these rules or otherwise violating the spirit of the game will be disqualified.

It is also the entrant's responsibility to make sure that their submitted agents provide their responses in a valid format (e.g., the codemaster's clue contains both a word and a number, and the guesser selects a valid word on the board). Any agent that violates the required response format or causes an exception in the framework code will be disqualified.

### Word Pool

Whilst the framework provided uses the original pool of 395 possible words from Codenames, the competition will use an alternative pool of words. These words will not be provided to entrants beforehand and may potentially contain slang or other pop-culture terms that are not considered standard English words (e.g., "Hogwarts" or "Xenomorph"). This uncertainty in the set of final possible words will help ensure that agents have a sufficiently diverse understanding of language and are not merely memorising associations between a smaller set of known words.

## Key Dates

Please take note of the following deadlines:

**Registration Deadline:** 31 July 2025
* Date to register your interest in the competition.
  
**Submission for Testing Deadline:** 4 August 2025
* Date to submit your files for testing purposes, the competition organisers will check that the code can be run successfully and provide feedback if not.
* Entrants are not required to submit their files by this date, but will not receive any testing feedback if they do not.
  
**Final Submission Deadline:** 11 August 2025
* Date to submit final code / files for the competition.
  
**Result Presentation:** 26-29 August 2025
* Results will be presented during the CoG 2025 conference.

&nbsp;

# Codenames AI Framework

## Running the game from terminal instructions

To run the game, the terminal will require a certain number of arguments.
Where the order is:
* args[0] = run_game.py
* args[1] = package.MyCodemasterRedClass
* args[2] = package.MyGuesserRedClass
* args[3] = package.MyCodemasterBlueClass
* args[4] = package.MyGuesserBlueClass

**run_game.py simply handles system arguments then called game.Game().
See below for more details about calling game.Game() directly.**

An optional seed argument can be used for the purpose of consistency against the random library.
* --seed *Integer value* or "time"
  * ("time" uses Time.time() as the seed)

An optional single_team argument can be used to decide whether to play the single team or two teams rules.
* --single_team *Boolean*
  * (by default this will be False, playing the two teams setup)
 
A set of optional version arguments can be used to specify an exact LLM version for each codemaster and guesser agent.
* --cmr_version *String*
* --gr_version *String*
* --cmb_version *String*
* --gb_version *String*

Other optional arguments include:
* --no_log
  * raise flag for suppressing logging
* --no_print
  * raise flag for suppressing printing to std out
* --game_name *String*
  * game_name in logfile

An example simulation of a game between two teams of GPT-4 Codemasters and Guessers in the terminal from codenames/:  
`$ python run_game.py players.codemaster_GPT.AICodemaster players.guesser_GPT.AIGuesser players.codemaster_GPT.AICodemaster players.guesser_GPT.AIGuesser --seed 3442

## Running the game from calling Game(...).run()

The class Game() that can be imported from game.Game is the main framework class.

An example of calling generalized vector Codemaster and guesser from python code rather than command line
```
    Game(AICodemaster, AIGuesser, AICodemaster, AIGuesser, seed=seed, do_print=True, game_name="GPT-GPT").run()
```

See simple_example.py for an example of calling Game.run() directly.
Arguments for custom Codemaster and Guesser classes can be provided using the cmr_kwargs, gr_kwargs, cmb_kwargs and gb_kwargs parameters.

## Game Class

The main framework class that calls your AI bots.

As mentioned above, a Game can be created/played directly by importing game.Game,
initializing with the args below, and calling the run() method.

```
Class that setups up game details and 
calls Guesser/Codemaster pair to play the game

Args:
    codemaster_red (:class:`Codemaster`):
        Codemaster for red team (spymaster in Codenames' rules) class that provides a clue.
    guesser_red (:class:`Guesser`):
        Guesser for red team (field operative in Codenames' rules) class that guesses based on clue.
    codemaster_blue (:class:`Codemaster`):
        Codemaster for blue team (spymaster in Codenames' rules) class that provides a clue.
    guesser_blue (:class:`Guesser`):
        Guesser for blue team (field operative in Codenames' rules) class that guesses based on clue.
    seed (int or str, optional): 
        Value used to init random, "time" for time.time(). 
        Defaults to "time".
    do_print (bool, optional): 
        Whether to keep on sys.stdout or turn off. 
        Defaults to True.
    do_log (bool, optional): 
        Whether to append to log file or not. 
        Defaults to True.
    game_name (str, optional): 
        game name used in log file. Defaults to "default".
    cmr_kwargs (dict, optional):
        kwargs passed to red Codemaster.
    gr_kwargs (dict, optional):
        kwargs passed to red Guesser.
    cmb_kwargs (dict, optional):
        kwargs passed to blue Codemaster.
    gb_kwargs (dict, optional):
        kwargs passed to blue Guesser.
    single_team (bool, optional): 
        Whether to play the single team track version. 
        Defaults to False.
```

## Codemaster Class
Any Codemaster bot is a python 3 class that derives from the supplied abstract base class Codemaster in `codemaster.py`.  The bot must implement three functions:
```
__init__(self)
set_game_state(words_on_board : List[str], key_grid : List[str]) -> None
get_clue() -> Tuple[str,int]
```
#### *details*

`__init__` **kwargs are passed through.  These arguments are not currently used by the default GPT agents, but the option to use them for developing your own agents is still provided.

`set_game_state` is passed the list of words on the board, as well as the key grid provided to spymasters (codemasters).  The `words` are either: an upper-case word found in the English language or one of 4 special tokens: `'*Red*', '*Blue*', '*Civilian*', '*Assassin*'` indicating that the word that was originally at that location has been guessed and been found to be of that type.  The `key_grid` is a list of `'*Red*', '*Blue*', '*Civilian*', '*Assassin*'` indicating whether a spot on the board is on the team of the codemaster (`'*Red*'`), the opposing team (`'*Blue*'`), a civilian (`'*Civilian*'`), or the assassin (`'*Assassin*'`).


`get_clue` returns a tuple containing the clue, a single English word, and the number of words the Codemaster intends it to cover.

## Guesser Class

Any Guesser bot is a python 3 class that derives from the supplied abstract base class Guesser in `guesser.py`.  The bot must implement five functions:

```
__init__(self)
set_board(words: List[str]) -> None
set_clue(clue: str, num_guesses: int) -> None
keep_guessing -> bool
get_answer() -> Str
```

#### *details*

`__init__` is as above with the Codemaster.

`set_board` is passed the list of words on the board.  The `words` are either: an all upper case word found in the English language or one of 4 special tokens: `'*Red*', '*Blue*', '*Civilian*', '*Assassin*'` indicating that the word that was originally at that location has been guessed and been found to be of that type.

`set_clue` is passed the clue and the number of guesses it covers, as supplied by the `get_clue` of the Codemaster through the Game class.

`keep_guessing` is a function that the game engine checks to see if the bot chooses to keep guessing, as the bot must only make at least one guess, but may choose to guess until it has gone to the number supplied by get_clue + 1.

`get_answer` returns the current guess of the Guesser, given the state of the board and the previous clue.

## Move History
UPDATED (14/05/2025)

A shared move history has been added into the game framework, that both the Codemaster and Guesser base classes can access.
To access this move history from inside your Codemaster or Guesser bot, simply call `super().get_move_history()`.
This will return a list of all previous moves made for the game so far, from both the Red and Blue teams.
* Codemaster moves are formatted as ["Colour_Codemaster", "Clue", "Number"], for example ['Red_Codemaster', 'TABLEWARE', 2].
* Guesser moves are formatted as ["Colour_Guesser", "Answer", "Tile Identity", "Continue Guessing"], for example ['Red_Guesser', 'PLATE', '\*Red\*', True].


## Rules of the Game

Codenames is a word-based game of language understanding and communication.
Players are split into two teams (red and blue), with each team consisting of a Codemaster and Guesser. Each team's goal is to discover their colour words as quickly as possible, while minimizing the number of incorrect guesses.

### Setup:

At the start of the game, the board consists of 25 English words:

DAY SLIP SPINE WAR CHICK\
FALL HAND WALL AMAZON DEGREE\
GIANT CENTAUR CLOAK STREAM CHEST\
HAM DOG EMBASSY GRASS FLY\
CAPITAL OIL COLD HOSPITAL MARBLE

The Codemasters on each team has access to a hidden map that tells them the identity of all of the words (Red, Blue, Civilian or Assassin).

*Red* *Red* *Civilian* *Assassin* *Red*\
*Red* *Civilian* *Red* *Blue* *Civilian*\
*Blue* *Civilian* *Civilian* *Red* *Civilian*\
*Blue* *Blue* *Civilian* *Blue* *Red*\
*Red* *Civilian* *Red* *Blue* *Red*

The Guessers on each team do not have access to this map, and so do not know the identity of any words.
Players need to work as a team to select their words as quickly as possible, while minimizing the number of incorrect guesses.
For example, the red team's guesser needs to select the following words:

DAY, SLIP, CHICK, FALL, WALL, STREAM, FLY, CAPITAL, MARBLE

### Turns:

At the start of each team's turn, the Codemaster supplies a clue and a number (the number of words related to that clue). Note that Codemasters can give "0" as their number, which allows guessers an unlimited number of guesses. 

e.g., `('pebble',2)`

The clue must:
* Be semantically related to what the Codemaster wants their guesser to guess -- i.e. no using words to tell the position of the words
* Be a single English word
* NOT be derived from or derive one of the words on the board -- i.e. days or cloaked are not valid clues. *Note, in our code we enforce through a strict string sub-word check. However, this can be circumnavigated by providing words that are spelt incorrectly or  additional characters. For competition purposes, human judges will be used to ensure that provided clues stick to this rule, and repeated violations will result in disqualification.*

The Guesser then selects from the remaining words on the board, based on which words are most associated with the Codemaster's clue.

e.g. `'MARBLE'`

The identity of the selected word is then revealed to all players.
If the Guesser selected a word that is their team's colour, then they may get to pick another word.
The Guesser must always make at least one guess each turn, and can guess up to one word more than the number provided in the Codemaster's clue.
If a Guesser selects a word that is not their team's colour, their turn ends.
The Guesser can choose to stop selecting words (ending their turn) any time after the first guess.

###Ending:

Play proceeds, passing back and forth, until one of three outcomes is achieved:

* All of the words of your team's colour have been selected -- you win
* All of the words of the other team's colour have been selected -- you lose
* You select the assassin tile -- you lose

## Prerequisite: Installation and Downloads
Note: The installation of the [Anaconda Distribution](https://www.anaconda.com/download) should be used for certain dependencies to work without issues.

Example installation order:
```
(base) conda create --name codenames python=3.9
(base) conda activate codenames
(codenames) pip install -U colorama
(codenames) pip install -U openai
(codenames) git clone https://github.com/stepmat/Codenames_GPT.git
(codenames) cd Codenames_GPT
```

Alternatively, you can use your system's packaging system. (*apt-get* on Debian, or *MacPorts/Homebrew* on macOS)
Or just use Python's packaging system, pip3, which is included by default from the Python binary installer.


## OpenAI GPT Agent

* Open gpt_manager.py and add your OpenAI API key near the top of the file where it says, "ENTER YOUR API KEY HERE".
* After this, you should be able to use the codemaster_GPT and guesser_GPT agents.
* For example, running "python simple_example.py" will perform a single game between both GPT agents.
