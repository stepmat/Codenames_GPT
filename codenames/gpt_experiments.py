import subprocess

for i in range(0,50):
    subprocess.run(["python", "run_game.py", "players.codemaster_gpt.AICodemaster", "players.guesser_gpt.AIGuesser", "--seed", str(i)])
