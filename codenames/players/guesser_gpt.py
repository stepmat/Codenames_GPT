from copy import deepcopy
from gpt_manager import talk_to_ai, game_rules
from players.guesser import Guesser


class AIGuesser(Guesser):

    def __init__(self):
        super().__init__()
        self.num = 0
        self.conversation_history = [{"role": "system", "content": game_rules},
                                     {"role": "system", "content": "You are playing the association game 'Codenames' as the red guesser"}]

    def set_board(self, words):
        self.words = words

    def set_clue(self, clue, num):
        self.clue = clue
        self.num = num
        print("The clue is:", clue, num)
        li = [clue, num]
        return li

    def keep_guessing(self):
        return self.num > 0

    def get_remaining_options(self):
        remaining_options = []
        for i in range(len(self.words)):
            if self.words[i][0] == '*':
                continue
            remaining_options.append(self.words[i])
        return remaining_options

    def get_answer(self):
        guess = None
        remaining_options = self.get_remaining_options()
        while guess is None:
            conversation_history_copy = deepcopy(self.conversation_history)
            prompt = "The remaining words are: " + str(remaining_options) + ". \n"
            prompt += "The following is the codemaster's clue: " + str(self.clue) + ". \n"
            prompt += "Provide a guess for one of the remaining words associated with this clue. \n"
            prompt += "Provide no additional text. \n"
            # Bonus Prompts
            # prompt += "Think very carefully about your guess before responding. \n"
            response = talk_to_ai(conversation_history_copy, prompt)
            if response in self.words:
                guess = response
            else:
                print("Warning! Invalid guess: " + response)
        self.num -= 1
        return guess
