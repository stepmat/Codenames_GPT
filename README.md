# Codenames AI Competition Framework

This is the main repository for the (new and revised) Codenames AI Competition Framework, focussed on the development of LLM powered agents to play the word association game "Codenames" by Vlaada Chvatil. The purpose of this competition is to test AI in a framework that:

* Requires the understanding of language
* Requires communication, in a semantically meaningful way, with players of unknown provenance --  the player on the other side of the table may be a human or it may be another, unaffiliated, bot
* Requires understanding words with multiple meanings

This competition and the code in this repository are based on the original Codenames AI competition (https://github.com/CodenamesAICompetition/Game), but with the following major modifications:

* The game rules have been altered to more closely represent those of the original game, with the largest modification being that the two teams now compete against each other, with each team consisting of a Codemaster and Guesser agent.
* A renewed emphasis on utilising the capabilities of LLMs (such as GPT-4, Gemini, Claude or Llama) to identify suitable clues and guesses. More traditional Codenames game-playing techniques (such as utilising word vector embeddings) are also applicable, either alongside LLM models or as a stand-alone techniques. However, the emphasis with this new competition will be on agents that are able to handle new and previously unseen wordsets, and agents who are able to play effectively alongside wide range of potential teammates.
  
**Further installation requirements are found below.**

## Submissions

Competition entrants will need to submit two agents, one Codemaster and one Guesser.

Entrants will need to provide complete instructions for how to run their agents on the following hardware:
* **Operating System:** Windows 11 or Ubuntu 24.04
* **Processor:** AMD Ryzen Threadripper PRO 5955WX (64 MB cache, 16 cores, 32 threads, 4.0GHz to 4.5GHz)
* **Memory:** 256GB, 4x64GB, DDR4, 3200MHz, RDIMM ECC Memory
* **Video Card:** NVIDIA® RTX™ A6000, 48 GB GDDR6, 4 DP
* **Storage:** 100GB

Entrants must ensure that both the submitted Codemaster and Guesser agent can run concurrently on the above hardware (i.e., available VRAM must be shared by both Codemaster and Guesser at the same time).

Submitted agents may utilise external services (such as the openAI API utilised by the provided GPT agent) but entrants will need to ensure that any necessary keys and funds required for these services are provided for. 

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
```

## Codemaster Class
Any Codemaster bot is a python 3 class that derives from the supplied abstract base class Codemaster in `codemaster.py`.  The bot must implement three functions:
```
__init__(self)
set_game_state(words_on_board : List[str], key_grid : List[str]) -> None
get_clue() -> Tuple[str,int]
```
#### *details*

'__init__' **kwargs are passed through.  These arguments are not currently used by the default GPT agents, but the option to use them for developing your own agents is still provided.

`set_game_state` is passed the list of words on the board, as well as the key grid provided to spymasters (codemasters).  The `words` are either: an upper-case word found in the English language or one of 4 special tokens: `'*Red*', '*Blue*', '*Civilian*', '*Assassin*'` indicating that the word that was originally at that location has been guessed and been found to be of that type.  The `key_grid` is a list of `'*Red*', '*Blue*', '*Civilian*', '*Assassin*'` indicating whether a spot on the board is on the team of the codemaster (`'*Red*'`), the opposing team (`'*Blue*'`), a civilian (`'*Civilian*'`), or the assassin (`'*Assassin*'`).


`get_clue` returns a tuple containing the clue, a single English word, and the number of words the Codemaster intends it to cover.

## Guesser Class

Any Guesser bot is a python 3 class that derives from the supplied abstract base class Guesser in `guesser.py`.  The bot must implement four functions:

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

At the start of each team's turn, the Codemaster supplies a clue and a number (the number of words related to that clue).

e.g., `('pebble',2)`

The clue must:
* Be semantically related to what the Codemaster wants their guesser to guess -- i.e. no using words to tell the position of the words
* Be a single English word
* NOT be derived from or derive one of the words on the board -- i.e. days or cloaked are not valid clues. *Note, in our code we enforce through a strict string sub-word check. However, this can be circumnavigated by providing words that are spelt incorrectly or contain additional characters. For competition purposes, human judges will be used to ensure that provided clues stick to this rule, and repeated violations will result in disqualification.*

The Guesser then selects from the remaining words on he board, based on the which words are most associated with the Codemaster's clue.

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

## Prerequisite: Installation and Downloads (LLMs)
Note: The installation of the [Anaconda Distribution](https://www.anaconda.com/distribution/) should be used for certain dependencies to work without issues.

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

## Prerequisite: Installation and Downloads (word vector agents)
Note: The installation of the [Anaconda Distribution](https://www.anaconda.com/distribution/) should be used for certain dependencies to work without issues. Also installing NLTK and gensim through conda is much simpler and less time consuming than the below alternatives.

Example installation order:
```
(base) conda create --name codenames python=3.6
(base) conda activate codenames
(codenames) conda install gensim
(codenames) pip install -U gensim
(codenames) pip install -U nltk
(codenames) python
>>> import nltk
>>> nltk.download('all')
>>> exit()
(codenames) pip install -U colorama
(codenames) git clone https://github.com/CodenamesAICompetition/Game.git
(codenames) cd codenames
```

Alternatively you can use your system's packaging system. (*apt-get* on Debian, or *MacPorts/Homebrew* on macOS)
Or just use Python's packaging system, pip3, which is included by default from the Python binary installer.

To check that everything is installed without error type in a terminal:  
`$ python3 -c "import scipy, numpy, gensim.models.keyedvectors, argparse, importlib, nltk, nltk.corpus, nltk.stem"`

Installing Gensim:

* Using Anaconda:
```conda install gensim```

* For Windows User using Conda Prompt(as well as the command on top):
```pip install -U gensim```

* For macOS, using Anaconda(same as above) or easy_install:
```sudo easy_install --upgrade gensim```

Installation of NLTK on macOS/linux:
* Install python3 on your operation system. If python 2 and python 3 coexists in your Operating System than you must specify `python3` for your commands.
* For macOS users, who don't have `pip3` or `python3` recognized in terminal, simply open terminal and type in `brew install python3` and check to see if `pip3` is a recognized command. If it is move on to the next step, if not type `brew postinstall python3`, or alternatively visit the [Python](https://python.org) website.
* Type in `sudo pip3 install -U nltk`
* Finally type in terminal (this installs all nltk packages, as opposed to a select few):
```
python
>>> import nltk
>>> nltk.download('all')
```

*Note for Windows user: Use the conda bash prompt for general purpose testing/running (as opposed to git bash)*

Installation of NLTK on Windows:
```pip install -U nltk```
```
python
>>> import nltk
>>> nltk.download('all')
```

Install colorama for colored console output:
```pip install -U colorama```

### These files can optionally be installed as well, provide path through command arguments:
* [Glove Vectors](https://nlp.stanford.edu/data/glove.6B.zip) (~2.25 GB)
* [Google News Vectors](https://drive.google.com/file/d/0B7XkCwpI5KDYNlNUTTlSS21pQmM/edit) (~3.5 GB)

## LLM Agents (Replicate Experiments from "Codenames as a Benchmark for Large Language Models")

* Open llm_manager.py and add your API keys near the top of the file where it says, "ENTER YOUR API KEY HERE".
  * This needs to be done for each api key requested.
  
* Experiment results can be replicated by running "round_robin_script.py"
  * Note, you will need to comment or uncomment the desired models in the all_codemasters and all_guessers arrays.

