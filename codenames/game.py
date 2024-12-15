import random
import time
import json
import enum
import os
import shutil
import sys

import colorama
import gensim.models.keyedvectors as word2vec
import numpy as np
from nltk.corpus import wordnet_ic


class GameCondition(enum.Enum):
    """Enumeration that represents the different states of the game"""
    RED_TURN = 0
    BLUE_TURN = 1
    RED_WIN = 2
    BLUE_WIN = 3


class Game:
    """Class that setups up game details and calls Codemaster/Guesser pairs to play the game
    """

    def __init__(self, codemaster_red, guesser_red, codemaster_blue, guesser_blue,
                 seed="time", do_print=True, do_log=True, game_name="default",
                 cmr_kwargs={}, gr_kwargs={}, cmb_kwargs={}, gb_kwargs={},
                 single_team=False):
        """ Setup Game details

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
        """

        self.game_winner = None
        self.game_start_time = time.time()
        self.game_end_time = None
        colorama.init()

        self.do_print = do_print
        if not self.do_print:
            self._save_stdout = sys.stdout
            sys.stdout = open(os.devnull, 'w')

        self.codemaster_red = codemaster_red("Red", **cmr_kwargs)
        self.guesser_red = guesser_red("Red", **gr_kwargs)
        self.codemaster_blue = codemaster_blue("Blue", **cmb_kwargs)
        self.guesser_blue = guesser_blue("Blue", **gb_kwargs)

        self.cmr_kwargs = cmr_kwargs
        self.gr_kwargs = gr_kwargs
        self.cmb_kwargs = cmb_kwargs
        self.gb_kwargs = gb_kwargs
        self.do_log = do_log
        self.game_name = game_name
        self.single_team = single_team

        self.num_red_words = 9
        self.num_blue_words = 8
        self.num_civilian_words = 7
        self.num_assassin_words = 1

        self.recorded_moves = {}

        # set seed so that board/keygrid can be reloaded later
        if seed == 'time':
            self.seed = time.time()
            random.seed(self.seed)
        else:
            self.seed = seed
            random.seed(int(seed))

        print("seed:", self.seed)

        # load board words
        with open("wordpools/codenames_original_wordpool.txt", "r") as f:
            temp = f.read().splitlines()
            assert len(temp) == len(set(temp)), "game wordpool should not have duplicates"
            random.shuffle(temp)
            self.words_on_board = temp[:25]

        # set grid key for codemaster (spymaster)
        self.key_grid = ["Red"] * self.num_red_words + ["Blue"] * self.num_blue_words + \
                        ["Civilian"] * self.num_civilian_words + ["Assassin"] * self.num_assassin_words
        random.shuffle(self.key_grid)

    def __del__(self):
        """reset stdout if using the do_print==False option"""
        if not self.do_print:
            sys.stdout.close()
            sys.stdout = self._save_stdout

    @staticmethod
    def load_glove_vecs(glove_file_path):
        """Load stanford nlp glove vectors
        Original source that matches the function: https://nlp.stanford.edu/data/glove.6B.zip
        """
        with open(glove_file_path, encoding="utf-8") as infile:
            glove_vecs = {}
            for line in infile:
                line = line.rstrip().split(' ')
                glove_vecs[line[0]] = np.array([float(n) for n in line[1:]])
            return glove_vecs

    @staticmethod
    def load_wordnet(wordnet_file):
        """Function that loads wordnet from nltk.corpus"""
        return wordnet_ic.ic(wordnet_file)

    @staticmethod
    def load_w2v(w2v_file_path):
        """Function to initalize gensim w2v object from Google News w2v Vectors
        Vectors Source: https://drive.google.com/file/d/0B7XkCwpI5KDYNlNUTTlSS21pQmM/edit
        """
        return word2vec.KeyedVectors.load_word2vec_format(w2v_file_path, binary=True, unicode_errors='ignore')

    def _display_board_codemaster(self):
        """prints out board with color-paired words, only for codemaster, color && stylistic"""
        print(str.center("___________________________BOARD___________________________\n", 60))
        counter = 0
        for i in range(len(self.words_on_board)):
            if counter >= 1 and i % 5 == 0:
                print("\n")
            if self.key_grid[i] == 'Red':
                print(str.center(colorama.Fore.RED + self.words_on_board[i], 15), " ", end='')
                counter += 1
            elif self.key_grid[i] == 'Blue':
                print(str.center(colorama.Fore.BLUE + self.words_on_board[i], 15), " ", end='')
                counter += 1
            elif self.key_grid[i] == 'Civilian':
                print(str.center(colorama.Fore.RESET + self.words_on_board[i], 15), " ", end='')
                counter += 1
            else:
                print(str.center(colorama.Fore.MAGENTA + self.words_on_board[i], 15), " ", end='')
                counter += 1
        print(str.center(colorama.Fore.RESET +
                         "\n___________________________________________________________", 60))
        print("\n")

    def _display_board(self):
        """prints the list of words in a board like fashion (5x5)"""
        print(colorama.Style.RESET_ALL)
        print(str.center("___________________________BOARD___________________________", 60))
        for i in range(len(self.words_on_board)):
            if i % 5 == 0:
                print("\n")
            print(str.center(self.words_on_board[i], 10), " ", end='')

        print(str.center("\n___________________________________________________________", 60))
        print("\n")

    def _display_key_grid(self):
        """ Print the key grid to stdout  """
        print("\n")
        print(str.center(colorama.Fore.RESET +
                         "____________________________KEY____________________________\n", 55))
        counter = 0
        for i in range(len(self.key_grid)):
            if counter >= 1 and i % 5 == 0:
                print("\n")
            if self.key_grid[i] == 'Red':
                print(str.center(colorama.Fore.RED + self.key_grid[i], 15), " ", end='')
                counter += 1
            elif self.key_grid[i] == 'Blue':
                print(str.center(colorama.Fore.BLUE + self.key_grid[i], 15), " ", end='')
                counter += 1
            elif self.key_grid[i] == 'Civilian':
                print(str.center(colorama.Fore.RESET + self.key_grid[i], 15), " ", end='')
                counter += 1
            else:
                print(str.center(colorama.Fore.MAGENTA + self.key_grid[i], 15), " ", end='')
                counter += 1
        print(str.center(colorama.Fore.RESET +
                         "\n___________________________________________________________", 55))
        print("\n")

    def get_words_on_board(self):
        """Return the list of words that represent the board state"""
        return self.words_on_board

    def get_key_grid(self):
        """Return the codemaster's key"""
        return self.key_grid

    def _accept_guess(self, guess_index, game_condition):
        """Function that takes in an int index called guess to compare with the key grid
        """

        if self.key_grid[guess_index] == "Red":
            self.words_on_board[guess_index] = "*Red*"
            if self.words_on_board.count("*Red*") >= self.num_red_words:
                return GameCondition.RED_WIN
            return GameCondition.RED_TURN

        elif self.key_grid[guess_index] == "Blue":
            self.words_on_board[guess_index] = "*Blue*"
            if self.words_on_board.count("*Blue*") >= self.num_blue_words:
                return GameCondition.BLUE_WIN
            return GameCondition.BLUE_TURN

        elif self.key_grid[guess_index] == "Assassin":
            self.words_on_board[guess_index] = "*Assassin*"
            if game_condition == GameCondition.RED_TURN:
                return GameCondition.BLUE_WIN
            else:
                return GameCondition.RED_WIN

        else:
            self.words_on_board[guess_index] = "*Civilian*"
            if game_condition == GameCondition.RED_TURN:
                return GameCondition.BLUE_TURN
            else:
                return GameCondition.RED_TURN

    def write_results(self, num_of_turns):
        """Logging function
        writes in both the original and a more detailed new style
        """
        red_result = 0
        blue_result = 0
        civ_result = 0
        assa_result = 0

        for i in range(len(self.words_on_board)):
            if self.words_on_board[i] == "*Red*":
                red_result += 1
            elif self.words_on_board[i] == "*Blue*":
                blue_result += 1
            elif self.words_on_board[i] == "*Civilian*":
                civ_result += 1
            elif self.words_on_board[i] == "*Assassin*":
                assa_result += 1
        total = red_result + blue_result + civ_result + assa_result

        if not os.path.exists("results"):
            os.mkdir("results")

        with open("results/bot_results.txt", "a") as f:
            f.write(
                f'TOTAL:{num_of_turns} B:{blue_result} C:{civ_result} A:{assa_result} '
                f'R:{red_result} CODEMASTER_R:{self.codemaster_red.name} '
                f'GUESSER_R:{self.guesser_red.name} '
                f'CODEMASTER_B:{self.codemaster_blue.name} '
                f'GUESSER_B:{self.guesser_blue.name} '
                f'SEED:{self.seed} WINNER:{self.game_winner}\n'
            )

        with open("results/bot_results_new_style.txt", "a") as f:
            results = {"game_name": self.game_name,
                       "total_turns": num_of_turns,
                       "R": red_result, "B": blue_result, "C": civ_result, "A": assa_result,
                       "codemaster_red": self.codemaster_red.name,
                       "guesser_red": self.guesser_red.name,
                       "codemaster_blue": self.codemaster_blue.name,
                       "guesser_blue": self.guesser_blue.name,
                       "seed": self.seed,
                       "winner": self.game_winner,
                       "time_s": (self.game_end_time - self.game_start_time),
                       "cmr_kwargs": {k: v if isinstance(v, float) or isinstance(v, int) or isinstance(v, str) else None
                                      for k, v in self.cmr_kwargs.items()},
                       "gr_kwargs": {k: v if isinstance(v, float) or isinstance(v, int) or isinstance(v, str) else None
                                     for k, v in self.gr_kwargs.items()},
                       "cmb_kwargs": {k: v if isinstance(v, float) or isinstance(v, int) or isinstance(v, str) else None
                                      for k, v in self.cmb_kwargs.items()},
                       "gb_kwargs": {k: v if isinstance(v, float) or isinstance(v, int) or isinstance(v, str) else None
                                     for k, v in self.gb_kwargs.items()},
                       }
            f.write(json.dumps(results))
            f.write('\n')

        with open("results/move_log.txt", "a") as f:
            f.write(json.dumps(self.recorded_moves))
            f.write('\n')

    @staticmethod
    def clear_results():
        """Delete results folder"""
        if os.path.exists("results") and os.path.isdir("results"):
            shutil.rmtree("results")

    def run(self):
        """Function that runs the codenames game between codemaster and guesser"""
        game_condition = GameCondition.RED_TURN
        turn_counter = 0

        while game_condition != GameCondition.BLUE_WIN and game_condition != GameCondition.RED_WIN:

            if game_condition == GameCondition.RED_TURN:
                codemaster = self.codemaster_red
                guesser = self.guesser_red
                print("RED TEAM TURN")
            else:
                codemaster = self.codemaster_blue
                guesser = self.guesser_blue
                print("BLUE TEAM TURN")

            # board setup and display
            print('\n' * 2)
            words_in_play = self.get_words_on_board()
            current_key_grid = self.get_key_grid()
            codemaster.set_game_state(words_in_play, current_key_grid)
            self._display_key_grid()
            self._display_board_codemaster()

            # codemaster gives clue & number here
            clue, clue_num = codemaster.get_clue()
            turn_counter += 1
            keep_guessing = True
            clue_num = int(clue_num)

            # update log of game states and moves made.
            self.recorded_moves["clue_" + str(len(self.recorded_moves))] = {
                "team":str(game_condition),
                "red_words":str(self.key_grid.count('Red')-self.words_on_board.count('*Red*')),
                "blue_words": str(self.key_grid.count('Blue')-self.words_on_board.count('*Blue*')),
                "civillian_words": str(self.key_grid.count('Civilian')-self.words_on_board.count('*Civilian*')),
                "assassin_words": str(self.key_grid.count('Assassin')-self.words_on_board.count('*Assassin*')),
                "turn_counter": str(turn_counter),
                "clue": clue,
                "clue_num": str(clue_num)
            }

            print('\n' * 2)
            guesser.set_clue(clue, clue_num)

            while keep_guessing:

                guesser.set_board(words_in_play)
                guess_answer = guesser.get_answer()

                # if no comparisons were made/found than retry input from codemaster
                if guess_answer is None or guess_answer == "no comparisons":
                    break
                guess_answer_index = words_in_play.index(guess_answer.upper().strip())
                game_condition_result = self._accept_guess(guess_answer_index, game_condition)

                # print(game_condition)
                # print(game_condition_result)

                if game_condition == game_condition_result:
                    print('\n' * 2)
                    self._display_board_codemaster()
                    print("Keep Guessing? the clue is ", clue, clue_num)
                    keep_guessing = guesser.keep_guessing()
                    if not keep_guessing:
                        if game_condition == GameCondition.RED_TURN:
                            game_condition = GameCondition.BLUE_TURN
                        elif game_condition == GameCondition.BLUE_TURN:
                            game_condition = GameCondition.RED_TURN
                else:
                    keep_guessing = False
                    game_condition = game_condition_result

                # update log of game states and moves made.
                self.recorded_moves["guess_" + str(len(self.recorded_moves))] = {
                    "guess_answer": str(guess_answer),
                    "keep_guessing": str(keep_guessing),
                    "game_condition": str(game_condition),
                    "game_condition_result": str(game_condition_result)
                }

                # if playing single team version, then it is always the red team's turn.
                if self.single_team and game_condition == GameCondition.BLUE_TURN:
                    game_condition = GameCondition.RED_TURN

        if game_condition == GameCondition.RED_WIN:
            self.game_winner = "R"
            print("Red Team Wins!")
        else:
            self.game_winner = "B"
            print("Blue Team Wins!")

        self.game_end_time = time.time()
        self._display_board_codemaster()
        if self.do_log:
            self.write_results(turn_counter)
        print("Game Over")
