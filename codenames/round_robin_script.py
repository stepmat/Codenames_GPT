import subprocess
import itertools

all_codemasters = [
    # ["players.codemaster_llm.AICodemaster", "GPT", "o1-preview-2024-09-12"],
    # ["players.codemaster_llm.AICodemaster", "GPT", "o1-mini-2024-09-12"],
    # ["players.codemaster_llm.AICodemaster", "GPT", "o3-mini-2025-01-31"],
    ["players.codemaster_llm.AICodemaster", "GPT", "gpt-4o-2024-08-06"],

    ["players.codemaster_llm.AICodemaster", "Gemini", "gemini-1.5-pro-002"],
    # ["players.codemaster_llm.AICodemaster", "Gemini", "gemini-1.5-pro"],

    ["players.codemaster_llm.AICodemaster", "Claude", "claude-3-5-sonnet-20241022"],
    # ["players.codemaster_llm.AICodemaster", "Claude", "claude-3-5-sonnet-20240620"],

    # ["players.codemaster_llm.AICodemaster", "Llama", "meta-llama/Llama-3.2-3B-Instruct"],
    ["players.codemaster_llm.AICodemaster", "Llama", "meta-llama/Meta-Llama-3.1-70B-Instruct"],

    # ["players.codemaster_llm.AICodemaster", "Phi", "microsoft/Phi-3-medium-128k-instruct"],

    # ["players.codemaster_llm.AICodemaster", "Mistral", "mistralai/Mistral-7B-Instruct-v0.3"],
    # ["players.codemaster_llm.AICodemaster", "Mistral", "mistralai/Mixtral-8x7B-Instruct-v0.1"],

    # ["players.codemaster_w2v.AICodemaster", "", ""],
    # ["players.codemaster_glove.AICodemaster", "", ""],
    # ["players.codemaster_w2vglove.AICodemaster", "", ""],
]

all_guessers = [
    # ["players.guesser_llm.AIGuesser", "GPT", "o1-preview-2024-09-12"],
    # ["players.guesser_llm.AIGuesser", "GPT", "o1-mini-2024-09-12"],
    # ["players.guesser_llm.AIGuesser", "GPT", "o3-mini-2025-01-31"],
    ["players.guesser_llm.AIGuesser", "GPT", "gpt-4o-2024-08-06"],

    ["players.guesser_llm.AIGuesser", "Gemini", "gemini-1.5-pro-002"],
    # ["players.guesser_llm.AIGuesser", "Gemini", "gemini-1.5-pro"],

    ["players.guesser_llm.AIGuesser", "Claude", "claude-3-5-sonnet-20241022"],
    # ["players.guesser_llm.AIGuesser", "Claude", "claude-3-5-sonnet-20240620"],

    # ["players.guesser_llm.AIGuesser", "Llama", "meta-llama/Llama-3.2-3B-Instruct"],
    ["players.guesser_llm.AIGuesser", "Llama", "meta-llama/Meta-Llama-3.1-70B-Instruct"],

    # ["players.guesser_llm.AIGuesser", "Phi", "microsoft/Phi-3-medium-128k-instruct"],

    # ["players.guesser_llm.AIGuesser", "Mistral", "mistralai/Mistral-7B-Instruct-v0.3"],
    # ["players.guesser_llm.AIGuesser", "Mistral", "mistralai/Mixtral-8x7B-Instruct-v0.1"],

    # ["players.guesser_w2v.AIGuesser", "", ""],
    # ["players.guesser_glove.AIGuesser", "", ""],
    # ["players.guesser_w2vglove.AIGuesser", "", ""],
]


def round_robin_tournament(codemasters, guessers, num_games=1, single_team=True, only_matching_teams=True):
    # single_team: True means that the single team version of Codenames is played, otherwise two teams version
    # only_matching_teams: True means that only teams with the same codemaster and guesser models are evaluated

    # Generate all valid agent combinations
    agent_combinations = []
    if single_team:
        for cmr, gr in itertools.product(codemasters, guessers):
            if not only_matching_teams or (codemasters.index(cmr) == guessers.index(gr)):
                agent_combinations.append([cmr, cmr, gr, gr])
    else:
        for cmr, cmb, gr, gb in itertools.product(codemasters, codemasters, guessers, guessers):
            if not only_matching_teams or (codemasters.index(cmr) == guessers.index(gr) and codemasters.index(cmb) == guessers.index(gb)):
                agent_combinations.append([cmr, cmb, gr, gb])

    # Run specified number of games for each valid agent combination
    for [cmr, cmb, gr, gb] in agent_combinations:
        for seed in range(num_games):
            subprocess.run(["python", "run_game.py", cmr[0],
                            gr[0], cmb[0],
                            gb[0], "--seed", str(seed),
                            "--cmr_model", cmr[1], "--cmr_version", cmr[2],
                            "--gr_model", gr[1], "--gr_version", gr[2],
                            "--cmb_model", cmb[1], "--cmb_version", cmb[2],
                            "--gb_model", gb[1], "--gb_version", gb[2],
                            # "--w2v", "players/GoogleNews-vectors-negative300.bin",
                            # "--glove", "players/glove.6B.300d.txt",
                            "--single_team", str(single_team)
                            ])


round_robin_tournament(all_codemasters, all_guessers, 100, True, True)
