from gpt_manager import game_rules, GPT
from players.guesser import Guesser
import random


class AIGuesser(Guesser):

    def __init__(self, team="Red"):
        super().__init__()
        self.team = team
        self.num = 0
        self.guesses = 0
        system_prompt = game_rules + "You are playing the game Codenames as the " + team + " Guesser. "
        self.manager = GPT(system_prompt=system_prompt, version="gpt-4o-2024-05-13")

    def set_board(self, words):
        self.words = words

    def set_clue(self, clue, num):
        self.clue = clue
        self.num = num
        print("The clue is:", clue, num)
        li = [clue, num]
        return li

    def keep_guessing(self):
        invalid_timer = 0
        response = None
        prompt = ""
        guess_again = False
        while response is None and (self.guesses <= self.num or self.num == 0):
            prompt += "The remaining words are: " + str(self.get_remaining_options()) + ". "
            prompt += "The following is the Codemaster's clue: (" + str(self.clue) + ", " + str(self.num) + "). "
            prompt += "You have picked " + str(self.guesses) + " words this turn. "
            prompt += "Would you like to keep guessing? Answer only 'yes' or 'no'. "
            response = self.manager.talk_to_ai(prompt)
            if "yes" in response.lower():
                guess_again = True
            elif "no" in response.lower():
                guess_again = False
            elif invalid_timer > 10:
                guess_again = False
            else:
                response = None
                invalid_timer += 1
                prompt = "That was not a valid response, respond with only 'yes' or 'no'. "
        return guess_again

    def get_remaining_options(self):
        remaining_options = []
        for i in range(len(self.words)):
            if self.words[i][0] == '*':
                continue
            remaining_options.append(self.words[i])
        return remaining_options

    def get_answer(self):
        invalid_timer = 0
        guess = None
        prompt = ""
        while guess is None:
            prompt += "The remaining words are: " + str(self.get_remaining_options()) + ". "
            prompt += "The following is the Codemaster's clue: (" + str(self.clue) + ", " + str(self.num) + "). "
            prompt += "Select one of the remaining words that is most associated with this clue. "
            prompt += "You must select one of the remaining words and provide no additional text.  "
            print("\n\n" + prompt + "\n\n")
            response = self.manager.talk_to_ai(prompt)
            print(response)
            response = response.upper().strip()
            if response in self.words:
                guess = response
            elif response.split(" ")[0].strip() in self.words:
                guess = response.split(" ")[0].strip()
            elif response.split('"')[1:2] in self.words:
                guess = response.split('"')[1:2]
            elif response.split("'")[1:2] in self.words:
                guess = response.split("'")[1:2]
            elif invalid_timer > 10:
                print("You have made too many invalid guesses, selecting random remaining word")
                guess = random.choice(self.get_remaining_options())
            else:
                print("Warning! Invalid guess: " + response)
                prompt = "That was not a valid word. "
                invalid_timer += 1
        self.guesses += 1
        return guess
