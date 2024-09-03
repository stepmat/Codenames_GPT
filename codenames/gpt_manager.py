from openai import OpenAI

client = OpenAI(api_key="Enter Your API key here")

game_rules = """
Codenames is a game of language understanding and communication. 
The Codemaster and Guesser are both on the Red team, and their goal is to discover their words as quickly as possible, while minimizing the number of incorrect guesses.
At the start of the game, the board consists of 25 English words.
The Codemaster has access to a hidden map that tells them the identity of all of the words (Red, Blue, Civilian or Assassin).
The Codemaster then supplies a clue and a number (the number of guesses the Guesser is obligated to make)
The clue must:
- Be semantically related to what the Codemaster wants their guesser to guess.
- Be a single English word.
- NOT be derived from or derive one of the words on the board.
It is important for the guesser to correctly order their guesses, as ordering is important.
If a guesser guesses an invalid clue (a non-red word), their turn is forfeit.
Play proceeds, passing back and forth, until one of 3 outcomes is achieved:
All of the Red tiles have been found -- you win
All of the Blue tiles have been found -- you lose
The single Assassin tile is found -- you lose
You will be scored by the number of turns required to guess all 8 red words. 
Scores will be calculated in an inverse proportional fashion, so the lower the better.
Guessing an assassin-linked word or the 7 blue words before all 8 red words will result in an instant loss and a score of 25 turns or points.
"""


def talk_to_ai(conversation_history, prompt, model="gpt-4o"):
    # model options = [gpt-3.5-turbo-0125 , gpt-4-1106-preview , gpt-4-0125-preview]
    conversation_history.append({"role": "user", "content": prompt})
    response = client.chat.completions.create(
        messages=conversation_history,
        model=model
    ).choices[0].message.content
    conversation_history.append({"role": "assistant", "content": response})
    return response
