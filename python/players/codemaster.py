from abc import ABC, abstractmethod
import random


class codemaster(ABC):
    words = 0
    map = 0
    bot_array = 0


    def __init__(self):
        pass


    def get_map(self, map_list):
        self.maps = map_list


    def give_clue(self):
        pass


class human_codemaster(codemaster):


    def __init__(self):
        pass


    def get_board(self, words):
        self.words = words


    def get_map(self, map_list):
        self.maps = map_list


    def give_clue(self):
        clue_input = input("Input CM Clue:\nPlease enter a Word followed by a space and a Number >> ")
        type(clue_input)
        clue = clue_input.split(" ")

        if len(clue) == 1:
            clue.append('1')
        return clue

