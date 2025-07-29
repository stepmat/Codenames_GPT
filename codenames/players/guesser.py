from abc import ABC, abstractmethod


class Guesser(ABC):
    """guesser abstract class that mimics a field operative in the codenames game"""

    def __init__(self):
        """Handle pretrained vectors and declare instance vars"""
        self.move_history = []
        pass

    def set_move_history(self, move_history):
        """Called periodically by the Game to update the current move history"""
        self.move_history = move_history

    def get_move_history(self):
        """Called to access the current move history"""
        return self.move_history

    @abstractmethod
    def set_board(self, words_on_board):
        """Set function for the current game board"""
        pass

    @abstractmethod
    def set_clue(self, clue, num_guesses):
        """Set function for current clue and number of guesses this class should attempt"""
        pass

    @abstractmethod
    def keep_guessing(self):
        """Return True if guess attempts remaining otherwise False"""
        pass

    @abstractmethod
    def get_answer(self):
        """Return the guessed word based on the clue and current game board"""
        pass


class HumanGuesser(Guesser):
    """Guesser derived class for human interaction"""

    def __init__(self):
        super().__init__()
        self.team = team
        pass

    def set_clue(self, clue, num):
        print("The clue is:", clue, num)

    def set_board(self, words):
        self.words = words

    def get_answer(self):
        answer_input = input("Guesser makes turn.\nPlease enter a valid Word >> ")
        type(answer_input)

        while not self._is_valid(answer_input):
            print("Input Invalid")
            print(self.words)
            answer_input = input("Please enter a valid Word >> ")
            type(answer_input)
        return answer_input

    def keep_guessing(self):
        guess_again = False
        response = input("Answer only 'y' (yes) or 'n' (no). Other answers will be considered as n. >> ")
        if "y" in response:
            guess_again = True
        elif "n" in response:
            guess_again = False
        return guess_again

    def _is_valid(self, result):
        if result.upper() in self.words:
            return True
        else:
            return False
