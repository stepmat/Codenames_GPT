from abc import ABC, abstractmethod
from copy import deepcopy

from google.generativeai.types import HarmCategory, HarmBlockThreshold
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from openai import OpenAI
import torch
import google.generativeai as genai
from anthropic import Anthropic

openAI_api_key = "ENTER YOUR API KEY HERE"
google_api_key = "ENTER YOUR API KEY HERE"
anthropic_api_key = "ENTER YOUR API KEY HERE"
huggingface_token = "ENTER YOUR API KEY HERE"

# https://czechgames.com/files/rules/codenames-rules-en.pdf
# Codemaster = Spymaster, Guesser = Field Operative
game_rules = """
1) Overview:
Codenames is a word-based game of language understanding and communication. 
Players are split into two teams (red and blue), with each team consisting of a Codemaster and Guesser. 
The red team always goes first.
2) Setup:
At the start of the game, the board consists of 25 English words. 
The Codemaster on each team has access to a hidden map that tells them the identity of all of the words (Red, Blue, Civilian or Assassin). 
A standard map in Codenames has 9 red words, 8 blue words, 7 civilian words and 1 assassin word. 
The Guessers on each team do not have access to this map, and so do not know the identity of any words. 
Players need to work as a team to select all their words in as few turns as possible, while minimising the number of incorrect guesses.
3) Turns: 
At the start of each team’s turn, the Codemaster supplies a clue and a number (the number of words related to that clue). 
The clue must:
- Be semantically related to the words the Codemaster wants their Guesser to guess.
- Be a single English word.
- Not derive, or be derived from, one of the words on the board.
The clue number must be greater than or equal to zero. 
The Guesser then selects from the remaining words on the board, based on which word is most associated with the Codemaster’s clue. 
The identity of the selected word is then revealed to all players. 
If the Guesser selected a word that is their team’s colour, then they may get to select another word. 
The Guesser must always make at least one guess each turn, and can guess up to one word more than the number provided in the Codemaster’s clue. 
The only exception to this is if the Codemaster’s clue number is zero, then there is no limit on the maximum number of guesses. 
If a Guesser selects a word that is not their team’s colour, their turn ends. 
The Guesser can choose to stop selecting words (ending their turn) any time after the first guess.
4) Ending: 
Play proceeds, passing back and forth, until one of two outcomes is achieved:
- All of the words of a team’s colour have been selected (this team wins).
- A team’s guesser selects the assassin word (this team loses).
"""


class LLM(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def talk_to_ai(self, prompt, store_in_context):
        pass


class GPT(LLM):

    # gpt-4o-2024-05-13, gpt-4-turbo-2024-04-09, gpt-3.5-turbo-0125
    def __init__(self, system_prompt="", version="gpt-4o-2024-05-13"):
        super().__init__()
        self.model_name = version
        self.client = OpenAI(api_key=openAI_api_key)
        self.conversation_history = [{"role": "system", "content": system_prompt}]

    def talk_to_ai(self, prompt, store_in_context=True):
        conversation_history_copy = deepcopy(self.conversation_history)
        self.conversation_history.append({"role": "user", "content": prompt})
        response = self.client.chat.completions.create(
            messages=self.conversation_history,
            model=self.model_name,
        ).choices[0].message.content
        self.conversation_history.append({"role": "assistant", "content": response})
        if not store_in_context:
            self.conversation_history = conversation_history_copy
        return response


class Gemini(LLM):

    # gemini-1.5-flash, gemini-1.5-pro
    def __init__(self, system_prompt="", version="gemini-1.5-pro"):
        super().__init__()
        genai.configure(api_key=google_api_key)
        self.model = genai.GenerativeModel(model_name=version, system_instruction=system_prompt)
        self.chat = self.model.start_chat(history=[])

    def talk_to_ai(self, prompt, store_in_context=True):
        if store_in_context:
            response = self.chat.send_message(prompt, safety_settings={
                    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE})
        else:
            response = self.model.generate_content(prompt, safety_settings={
                    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE})
        return response.text


class Claude(LLM):

    # claude-3-5-sonnet-20240620, claude-3-opus-20240229, claude-3-sonnet-20240229, claude-3-haiku-20240307
    def __init__(self, system_prompt="", version="claude-3-5-sonnet-20240620"):
        super().__init__()
        self.model_name = version
        self.client = Anthropic(api_key=anthropic_api_key)
        self.system_prompt = system_prompt
        self.conversation_history = []

    def talk_to_ai(self, prompt, store_in_context=True):
        conversation_history_copy = deepcopy(self.conversation_history)
        self.conversation_history.append({"role": "user", "content": prompt})
        response = self.client.messages.create(
            messages=self.conversation_history,
            model=self.model_name,
            max_tokens=512,
            system=self.system_prompt
        ).content[0].text
        self.conversation_history.append({"role": "assistant", "content": response})
        if not store_in_context:
            self.conversation_history = conversation_history_copy
        return response


class LLama(LLM):

    # meta-llama/Meta-Llama-3-8B-Instruct, meta-llama/Meta-Llama-3-70B-Instruct
    def __init__(self, system_prompt="", version="meta-llama/Meta-Llama-3-8B-Instruct"):
        super().__init__()
        self.pipe = pipeline(
            "text-generation",
            model=version,
            model_kwargs={"torch_dtype": torch.bfloat16},
            device_map="auto",
            token=huggingface_token
        )
        self.conversation_history = [{"role": "system", "content": system_prompt}]

    def talk_to_ai(self, prompt, store_in_context=True):
        conversation_history_copy = deepcopy(self.conversation_history)
        self.conversation_history.append({"role": "user", "content": prompt})
        generation_args = {
            "max_new_tokens": 500,
            "return_full_text": False,
            "do_sample": True,
        }
        output = self.pipe(self.conversation_history, **generation_args)
        response = output[0]["generated_text"]
        self.conversation_history.append({"role": "assistant", "content": response})
        if not store_in_context:
            self.conversation_history = conversation_history_copy
        return response


class Phi(LLM):

    # microsoft/Phi-3-mini-128k-instruct, microsoft/Phi-3-small-128k-instruct, microsoft/Phi-3-medium-128k-instruct
    def __init__(self, system_prompt="", version="microsoft/Phi-3-mini-128k-instruct"):
        super().__init__()
        self.model = AutoModelForCausalLM.from_pretrained(
            version,
            device_map="cuda",
            torch_dtype="auto",
            trust_remote_code=True,
        )
        self.tokenizer = AutoTokenizer.from_pretrained(version, trust_remote_code=True)
        self.pipe = pipeline("text-generation", model=self.model, tokenizer=self.tokenizer)
        self.conversation_history = [{"role": "system", "content": system_prompt}]

    def talk_to_ai(self, prompt, store_in_context=True):
        conversation_history_copy = deepcopy(self.conversation_history)
        self.conversation_history.append({"role": "user", "content": prompt})
        generation_args = {
            "max_new_tokens": 500,
            "return_full_text": False,
            "do_sample": True,
        }
        output = self.pipe(self.conversation_history, **generation_args)
        response = output[0]["generated_text"]
        self.conversation_history.append({"role": "assistant", "content": response})
        if not store_in_context:
            self.conversation_history = conversation_history_copy
        return response


class Mistral(LLM):

    # mistralai/Mistral-7B-Instruct-v0.1, mistralai/Mistral-7B-Instruct-v0.2, mistralai/Mistral-7B-Instruct-v0.3,
    # mistralai/Mixtral-8x7B-Instruct-v0.1
    def __init__(self, system_prompt="", version="mistralai/Mistral-7B-Instruct-v0.1"):
        super().__init__()
        self.model = AutoModelForCausalLM.from_pretrained(version, token=huggingface_token)
        self.tokenizer = AutoTokenizer.from_pretrained(version, token=huggingface_token)
        self.pipe = pipeline("text-generation", model=self.model, tokenizer=self.tokenizer)

        self.conversation_history = [{"role": "user", "content": system_prompt}]
        self.conversation_history.append({"role": "assistant", "content": ""})

    def talk_to_ai(self, prompt, store_in_context=True):
        conversation_history_copy = deepcopy(self.conversation_history)
        self.conversation_history.append({"role": "user", "content": prompt})
        generation_args = {
            "max_new_tokens": 500,
            "return_full_text": False,
            "do_sample": True,
        }
        output = self.pipe(self.conversation_history, **generation_args)
        response = output[0]["generated_text"]
        self.conversation_history.append({"role": "assistant", "content": response})
        if not store_in_context:
            self.conversation_history = conversation_history_copy
        return response



