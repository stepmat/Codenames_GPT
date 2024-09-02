from gpt_manager import talk_to_ai, game_rules
from players.codemaster import Codemaster


class AICodemaster(Codemaster):

    def __init__(self):
        super().__init__()
        self.cm_wordlist = []
        with open('players/cm_wordlist.txt') as infile:
            for line in infile:
                self.cm_wordlist.append(line.rstrip())
        self.conversation_history = [{"role": "system", "content": game_rules},
                                     {"role": "system", "content": "You are playing the association game 'Codenames' as the red codemaster. "}]

    def set_game_state(self, words, maps):
        self.words = words
        self.maps = maps

    def get_remaining_options(self):
        # Converts the words and map variables into a more gpt-friendly text format
        red, blue, civilian, assassin = [], [], [], []
        for i in range(len(self.words)):
            if self.words[i][0] == '*':
                continue
            if self.maps[i] == "Red":
                red.append(self.words[i])
            if self.maps[i] == "Blue":
                blue.append(self.words[i])
            if self.maps[i] == "Civilian":
                civilian.append(self.words[i])
            if self.maps[i] == "Assassin":
                assassin.append(self.words[i])
        return red, blue, civilian, assassin

    def get_clue(self):
        clue = None
        number = None
        red, blue, civilian, assassin = self.get_remaining_options()
        while clue is None or number is None:
            
            # Uncomment one of the following sections to perform the respective prompt engineering

            # DEFAULT
            prompt = "The remaining words are: "
            prompt += "Red: " + str(red) + ". "
            prompt += "Blue: " + str(blue) + ". "
            prompt += "Civilian: " + str(civilian) + ". "
            prompt += "Assassin: " + str(assassin) + ". "
            prompt += "Provide a single word clue and number for the guesser in the following format ('pebble',2). "
            prompt += "Stick to this format exactly and provide no additional text. "
            response = talk_to_ai(self.conversation_history, prompt)

            # CAUTIOUS
            # prompt = "The remaining words are: "
            # prompt += "Red: " + str(red) + ". "
            # prompt += "Blue: " + str(blue) + ". "
            # prompt += "Civilian: " + str(civilian) + ". "
            # prompt += "Assassin: " + str(assassin) + ". "
            # prompt += "Provide a single word clue and number for the guesser in the following format ('pebble',2). "
            # prompt += "Stick to this format exactly and provide no additional text. "
            # prompt += "Make sure that the number for your guess is always 1. "
            # response = talk_to_ai(self.conversation_history, prompt)

            # RISKY
            # prompt = "The remaining words are: "
            # prompt += "Red: " + str(red) + ". "
            # prompt += "Blue: " + str(blue) + ". "
            # prompt += "Civilian: " + str(civilian) + ". "
            # prompt += "Assassin: " + str(assassin) + ". "
            # prompt += "Provide a single word clue and number for the guesser in the following format ('pebble',2). "
            # prompt += "Stick to this format exactly and provide no additional text. "
            # prompt += "Make sure to pick a large number for your guess. "
            # response = talk_to_ai(self.conversation_history, prompt)

            # CHAIN-OF-THOUGHT
            # prompt = "The remaining words are: "
            # prompt += "Red: " + str(red) + ". "
            # prompt += "Blue: " + str(blue) + ". "
            # prompt += "Civilian: " + str(civilian) + ". "
            # prompt += "Assassin: " + str(assassin) + ". "
            # prompt += """
            #     Provide a single word clue and number for the guesser in the following format ('pebble' , 2)
            #     Solve the task step by step.
            #     Your output should be of the following format:
            #     ---
            #     Steps: Your steps here.
            #     Answer: (a single word here) / (A list of words here)
            # """
            # explanation_response = talk_to_ai(self.conversation_history, prompt)
            # print("\n\n" + explanation_response + "\n\n")
            # prompt = "Give me only the final answer in the previous prompt in the following format ('pebble',2). "
            # prompt += "Stick to this format exactly and provide no additional text. "
            # response = talk_to_ai(self.conversation_history, prompt)

            # SELF-REFINE
            # prompt = "The remaining words are: "
            # prompt += "Red: " + str(red) + ". "
            # prompt += "Blue: " + str(blue) + ". "
            # prompt += "Civilian: " + str(civilian) + ". "
            # prompt += "Assassin: " + str(assassin) + ". "
            # prompt += "Provide a single word clue and number for the guesser in the following format ('pebble',2). "
            # prompt += "The clue should avoid associations with Blue, Assassin and Civilian words. "
            # print("\n\n" + prompt + "\n\n")
            # initial_response = talk_to_ai(self.conversation_history, prompt)
            # print("\n\n" + initial_response + "\n\n")
            # other_words = "{" + str(blue).replace("[", "").replace("]", "").replace("'", "") + ", " + str(assassin).replace("[", "").replace("]", "").replace("'", "") + ", " + str(civilian).replace("[","").replace("]", "").replace("'", "") + "}";
            # prompt = "Evaluate the Codenames clue " + initial_response + " for the Red words {" + str(red).replace("[","").replace("]","").replace("'","") + "} and avoid words " + other_words + " on how related it is to the red words, and likelihood of accidental associate with blue, assassin, or civilian words."
            # prompt += """
            #     Give your answer in the form:
            #     Feedback:
            #     …
            # """
            # print("\n\n" + prompt + "\n\n")
            # feedback = talk_to_ai(self.conversation_history, prompt)
            # print("\n\n" + feedback + "\n\n")
            # prompt = "The remaining words are: "
            # prompt += "Red: " + str(red) + ". "
            # prompt += "Blue: " + str(blue) + ". "
            # prompt += "Civilian: " + str(civilian) + ". "
            # prompt += "Assassin: " + str(assassin) + ". "
            # prompt += "Refine the initial Codenames clue '" + initial_response + "' for the above words based on the following feedback: '" + feedback + "'. "
            # prompt += "You can stick with the initial clue if the feedback indicates that this is a good choice. "
            # prompt += "Provide a single word clue and number for the guesser in the following format ('pebble',2). "
            # prompt += "Stick to this format exactly and provide no additional text. "
            # print("\n\n" + prompt + "\n\n")
            # response = talk_to_ai(self.conversation_history, prompt)

            # SOLO-PERFORMANCE
            # prompt = """
            # When faced with a task, begin by identifying the participants who will contribute to solving the task. Then, initiate a multi-round collaboration process until a final solution is reached. The participants will give critical comments and detailed suggestions whenever necessary.
            # Here are some examples:
            # --
            # Example Task 1: Use numbers and basic arithmetic operations (+ - * /) to obtain 24. You need to use all numbers, and each number can only be used once.
            # Input: 6 12 1 1
            # Participants: AI Assistant (you); Math Expert
            # Start collaboration! Math Expert: Let's analyze the task in detail. You need to make sure that you meet the requirement, that you need to use exactly the four numbers (6 12 1 1) to construct 24. To reach 24, you can think of the common divisors of 24 such as 4, 6, 8, 3 and try to construct these first. Also you need to think of potential additions that can reach 24, such as 12 + 12.
            # AI Assistant (you): Thanks for the hints! Here's one initial solution: (12 / (1 + 1)) * 6 = 24
            # Math Expert: Let's check the answer step by step. (1+1) = 2, (12 / 2) = 6, 6 * 6 = 36 which is not 24! The answer is not correct. Can you fix this by considering other combinations? Please do not make similar mistakes.
            # AI Assistant (you): Thanks for pointing out the mistake. Here is a revised solution considering 24 can also be reached by 3 * 8: (6 + 1 + 1) * (12 / 4) = 24.
            # Math Expert: Let's first check if the calculation is correct. (6 + 1 + 1) = 8, 12 / 4 = 3, 8 * 3 = 24. The calculation is correct, but you used 6 1 1 12 4 which is not the same as the input 6 12 1 1. Can you avoid using a number that is not part of the input?
            # AI Assistant (you): You are right, here is a revised solution considering 24 can be reached by 12 + 12 and without using any additional numbers: 6 * (1 - 1) + 12 = 24.
            # Math Expert: Let's check the answer again. 1 - 1 = 0, 6 * 0 = 0, 0 + 12 = 12. I believe you are very close, here is a hint: try to change the "1 - 1" to "1 + 1".
            # AI Assistant (you): Sure, here is the corrected answer: 6 * (1+1) + 12 = 24
            # Math Expert: Let's verify the solution. 1 + 1 = 2, 6 * 2 = 12, 12 + 12 = 12. You used 1 1 6 12 which is identical to the input 6 12 1 1. Everything looks good!
            # Finish collaboration!
            # Final answer: 6 * (1 + 1) + 12 = 24
            # --
            # Example Task 2: Write a poem that meets the following requirements: (1) the poem has seven lines and the first letters of each line forms the word "CHATGPT"; (2) the poem is about explaining what is a quantum computer. (3) the poem needs to be easy to understand by a ten years old kid.
            # Participants: AI Assistant (you); Poet; Computer Scientist; Ten year old child
            # Poet: Make sure that you write the poem with seven lines, and the first letters of the lines should be C, H, A, T, G, P, T.
            # Computer Scientist: A quantum computer is an advanced computing device that uses the principles of quantum mechanics to process and store information. Unlike classical computers that use bits to represent information as 0s and 1s, quantum computers use quantum bits or qubits. Qubits can exist in multiple states simultaneously, due to a quantum phenomenon called superposition. You can consider using these information for the poem.
            # Ten year old child: I hope the poem to be fun and easy to understanding. I don't want to see a lot of jargons or complicated concepts.
            # AI Assistant (you): Thanks for the guidance! Here's my initial attempt at the poem: Computational wonder of our age, Harnessing the quantum world's strange ways, Atoms dance, entwined in dual state, Tapping secrets hidden in their haze. Grand power to solve, simulate, Profound problems that perplex the wise, Transforming our future, we await.
            # Poet: Let's verify if the poem meets the requirements. The first letters are CHATGPT which is correct! And the poem rhymes well. Good job!
            # Computer Scientist: Everything looks good to me! Ten year old child: I don't know what does perplex mean. Can you make the use of words easier to understand?
            # AI Assistant (you): Sure, let me revise the poem by using more common words. Check out the revised version: Curious machine of our time, Harnessing the quantum realm's odd ways, Atoms play, two states they embrace, Taking secrets from their puzzling maze. Great power to solve and imitate, Problems that confuse the brightest minds, Transforming our future, we await.
            # Poet: Let's check again if the poem meets the requirements. The first letters are C H A T G P T. And now the poem is more accessible to children. Everything looks good to me.
            # Computer Scientist: Looking good!
            # Ten year old child: I like this version a lot!
            # Finish collaboration!
            # Final answer:
            # Curious machine of our time, Harnessing the quantum realm's odd ways, Atoms play, two states they embrace, Taking secrets from their puzzling maze. Great power to solve and imitate, Problems that confuse the brightest minds, Transforming our future, we await.
            # --
            # Now, identify the participants and collaboratively solve the following task step by step. Give your answer in the form "WORD: (NUMBER)"
            # Task: You are playing a game of Codenames. You are playing as the Codemaster and must generate a one-word clue for the Guesser on your team that will semantically link to some of your target words.
            # The clue should help the Guesser figure out some of your target words. A clue comes in the form WORD: NUMBER (e.g. FLOWER: 2) with the word being the clue and the number is how many target words the clue relates to.
            # Clues should also aim to avoid associations with words that are not target words, i.e. the rest of the words on the board.
            # """
            # prompt += "Here is a list of your target words {" + str(red).replace("[", "").replace("]", "").replace("'", "") +"}. "
            # other_words = "{" + str(blue).replace("[", "").replace("]", "").replace("'", "") + ", " + str(assassin).replace("[", "").replace("]", "").replace("'", "") + ", " + str(civilian).replace("[", "").replace("]", "").replace("'", "") +"}";
            # prompt += "Here are the rest of the words on the board: " + other_words + ". "
            # print("\n\n" + prompt + "\n\n")
            # initial_response = talk_to_ai(self.conversation_history, prompt)
            # print("\n\n" + initial_response + "\n\n")
            # prompt = "Give me only the final answer in the previous response in the following format ('pebble',2). "
            # prompt += "Stick to this format exactly and provide no additional text. "
            # response = talk_to_ai(self.conversation_history, prompt)

            try:
                split_input = response.split(",");
                clue = split_input[0].replace("(","")
                number = int(split_input[1].replace(")",""))
            except:
                print("Warning! Invalid clue: " + response)
                clue = None
                number = None
        return [clue, number]
