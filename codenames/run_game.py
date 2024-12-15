import sys
import importlib
import argparse
import time
import os

from game import Game
from players.guesser import *
from players.codemaster import *

class GameRun:
    """Class that builds and runs a Game based on command line arguments"""

    def __init__(self):
        parser = argparse.ArgumentParser(
            description="Run the Codenames AI competition game.",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        parser.add_argument("codemaster_red", help="import string of form A.B.C.MyClass or 'human'")
        parser.add_argument("guesser_red", help="import string of form A.B.C.MyClass or 'human'")
        parser.add_argument("codemaster_blue", help="import string of form A.B.C.MyClass or 'human'")
        parser.add_argument("guesser_blue", help="import string of form A.B.C.MyClass or 'human'")
        parser.add_argument("--seed", help="Random seed value for board state -- integer or 'time'", default='time')
        parser.add_argument("--single_team", default=False)

        parser.add_argument("--w2v", help="Path to w2v file or None", default=None)
        parser.add_argument("--glove", help="Path to glove file or None", default=None)
        parser.add_argument("--wordnet", help="Name of wordnet file or None, most like ic-brown.dat", default=None)
        parser.add_argument("--glove_cm", help="Path to glove file or None", default=None)
        parser.add_argument("--glove_guesser", help="Path to glove file or None", default=None)

        parser.add_argument("--no_log", help="Supress logging", action='store_true', default=False)
        parser.add_argument("--no_print", help="Supress printing", action='store_true', default=False)
        parser.add_argument("--game_name", help="Name of game in log", default="default")

        parser.add_argument("--cmr_model", default=None)
        parser.add_argument("--cmr_version", default=None)
        parser.add_argument("--gr_model", default=None)
        parser.add_argument("--gr_version", default=None)
        parser.add_argument("--cmb_model", default=None)
        parser.add_argument("--cmb_version", default=None)
        parser.add_argument("--gb_model", default=None)
        parser.add_argument("--gb_version", default=None)

        args = parser.parse_args()

        self.do_log = not args.no_log
        self.do_print = not args.no_print
        if not self.do_print:
            self._save_stdout = sys.stdout
            sys.stdout = open(os.devnull, 'w')
        self.game_name = args.game_name

        self.gr_kwargs = {}
        self.cmr_kwargs = {}
        self.gb_kwargs = {}
        self.cmb_kwargs = {}

        # load red codemaster class
        if args.codemaster_red == "human":
            self.codemaster_red = HumanCodemaster
            print('human codemaster')
        else:
            self.codemaster_red = self.import_string_to_class(args.codemaster_red)
            print('loaded codemaster class')

        # load red guesser class
        if args.guesser_red == "human":
            self.guesser_red = HumanGuesser
            print('human guesser')
        else:
            self.guesser_red = self.import_string_to_class(args.guesser_red)
            print('loaded guesser class')

        # load blue codemaster class
        if args.codemaster_blue == "human":
            self.codemaster_blue = HumanCodemaster
            print('human codemaster')
        else:
            self.codemaster_blue = self.import_string_to_class(args.codemaster_blue)
            print('loaded codemaster class')

        # load blue guesser class
        if args.guesser_blue == "human":
            self.guesser_blue = HumanGuesser
            print('human guesser')
        else:
            self.guesser_blue = self.import_string_to_class(args.guesser_blue)
            print('loaded guesser class')

        if args.single_team == "True":
            self.single_team = True
        else:
            self.single_team = False

        # if the game is going to have an ai, load up word vectors
        if sys.argv[1] != "human" or sys.argv[2] != "human":
            if args.wordnet is not None and args.wordnet != "":
                brown_ic = Game.load_wordnet(args.wordnet)
                self.gr_kwargs["brown_ic"] = brown_ic
                self.cmr_kwargs["brown_ic"] = brown_ic
                self.gb_kwargs["brown_ic"] = brown_ic
                self.cmb_kwargs["brown_ic"] = brown_ic
                print('loaded wordnet')

            if args.glove is not None and args.glove != "":
                glove_vectors = Game.load_glove_vecs(args.glove)
                self.gr_kwargs["glove_vecs"] = glove_vectors
                self.cmr_kwargs["glove_vecs"] = glove_vectors
                self.gb_kwargs["glove_vecs"] = glove_vectors
                self.cmb_kwargs["glove_vecs"] = glove_vectors
                print('loaded glove vectors')

            if args.w2v is not None and args.w2v != "":
                w2v_vectors = Game.load_w2v(args.w2v)
                self.gr_kwargs["word_vectors"] = w2v_vectors
                self.cmr_kwargs["word_vectors"] = w2v_vectors
                self.gb_kwargs["word_vectors"] = w2v_vectors
                self.cmb_kwargs["word_vectors"] = w2v_vectors
                print('loaded word vectors')

            if args.glove_cm is not None and args.glove_cm != "":
                glove_vectors = Game.load_glove_vecs(args.glove_cm)
                self.cmr_kwargs["glove_vecs"] = glove_vectors
                self.cmb_kwargs["glove_vecs"] = glove_vectors
                print('loaded glove vectors')

            if args.glove_guesser is not None and args.glove_guesser != "":
                glove_vectors = Game.load_glove_vecs(args.glove_guesser)
                self.gr_kwargs["glove_vecs"] = glove_vectors
                self.gb_kwargs["glove_vecs"] = glove_vectors
                print('loaded glove vectors')

            if args.cmr_model is not None and args.cmr_model != "":
                self.cmr_kwargs["model"] = args.cmr_model
                self.cmr_kwargs["version"] = args.cmr_version
            if args.gr_model is not None and args.gr_model != "":
                self.gr_kwargs["model"] = args.gr_model
                self.gr_kwargs["version"] = args.gr_version
            if args.cmb_model is not None and args.cmb_model != "":
                self.cmb_kwargs["model"] = args.cmb_model
                self.cmb_kwargs["version"] = args.cmb_version
            if args.gb_model is not None and args.gb_model != "":
                self.gb_kwargs["model"] = args.gb_model
                self.gb_kwargs["version"] = args.gb_version

        # set seed so that board/keygrid can be reloaded later
        if args.seed == 'time':
            self.seed = time.time()
        else:
            self.seed = int(args.seed)

        print("CMR=" + ":".join([args.cmr_model, args.cmr_version]) +
              " GR=" + ":".join([args.gr_model, args.gr_version]) +
              " CMB=" + ":".join([args.cmb_model, args.cmb_version]) +
              " GB=" + ":".join([args.gb_model, args.gb_version]))

    def __del__(self):
        """reset stdout if using the do_print==False option"""
        if not self.do_print:
            sys.stdout.close()
            sys.stdout = self._save_stdout

    def import_string_to_class(self, import_string):
        """Parse an import string and return the class"""
        parts = import_string.split('.')
        module_name = '.'.join(parts[:len(parts) - 1])
        class_name = parts[-1]

        module = importlib.import_module(module_name)
        my_class = getattr(module, class_name)

        return my_class


if __name__ == "__main__":
    game_setup = GameRun()

    game = Game(game_setup.codemaster_red,
                game_setup.guesser_red,
                game_setup.codemaster_blue,
                game_setup.guesser_blue,
                seed=game_setup.seed,
                do_print=game_setup.do_print,
                do_log=game_setup.do_log,
                game_name=game_setup.game_name,
                cmr_kwargs=game_setup.cmr_kwargs,
                gr_kwargs=game_setup.gr_kwargs,
                cmb_kwargs=game_setup.cmb_kwargs,
                gb_kwargs=game_setup.gb_kwargs,
                single_team=game_setup.single_team)

    game.run()
