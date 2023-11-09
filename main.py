import colorama, ctypes, json, os, random, time
from colorama import Fore, Style

difficulties = {"1": #Hard
                  {"attempts": 3,
                   "coin_modifier": 1.25,
                   "score_modifier": 1.5},
                "2":  #Medium
                  {"attempts": 5,
                   "coin_modifier": 1.5,
                   "score_modifier": 1},
                "3": #Easy
                  {"attempts": 10,
                   "coin_modifier": 1.75,
                   "score_modifier": 0.75}}

def choose_cheater() -> int:
  return random.choice([x+1 for x in range(20)])

def get_throws(difficulty:str, cheater:int) -> dict:
  agents = []
  faces = "HT"
  for agent in range(20):
    if agent + 1 == cheater:
      throws = random.choices(faces, weights=(difficulties[difficulty]["coin_modifier"], 0.75), k=100)
    else:
      throws = random.choices(faces, weights=(1,1), k=100)
    heads = 0
    for x in throws:
      if x == "H":
        heads += 1
    agents.append(heads)
  return agents

def print_table(agents:list, lives_remaining:int, tries:list = None):
  line1 = ["agent " + str(x+1).rjust(2) + ": " + str(agents[x]) for x in range(5)]
  line2 = ["agent " + str(x+6).rjust(2) + ": " + str(agents[x+5]) for x in range(5)]
  line3 = ["agent " + str(x+11) + ": " + str(agents[x+10]) for x in range(5)]
  line4 = ["agent " + str(x+16) + ": " + str(agents[x+15]) for x in range(5)]

  print("One of the following agents is a cheater, find him")
  print(f"Lives remaining: {Fore.RED + str(lives_remaining) + Fore.RESET}")
  print(str(line1).replace("['", "").replace("']", "").replace("', '", "  "))
  print(str(line2).replace("['", "").replace("']", "").replace("', '", "  "))
  print(str(line3).replace("['", "").replace("']", "").replace("', '", "  "))
  print(str(line4).replace("['", "").replace("']", "").replace("', '", "  "))
  if len(tries) != 0:
    print("Innocent Agents: " + str(tries).replace("[", "").replace("]", ""). replace("'", ""))

def leave(score:float):
  save = input(f"Do you want to save your score of {Fore.GREEN + str(score) + Fore.RESET}? [Y/N] >> ").upper()
  while save not in ["Y", "N"]:
    print(f"[{Fore.RED}+{Fore.RESET}] Invalid choice, valid options are: {Style.BRIGHT}Y{Style.RESET_ALL} or {Style.BRIGHT}N{Style.RESET_ALL}")
    save = input("Do you want to save? [Y/N] >> ").upper()

  if save == "Y":
    with open("scores.json", "r") as f:
      scores = json.load(f)
    username = input("Choose a username >> ")
    scores[username] = score
    with open("scores.json", "w") as f:
      json.dump(scores, f, indent=4)

  quit(0)

def print_leaderboard():

  def sort_board(board:list):
    board.sort(key=lambda x: x[1], reverse=True)
    return board

  with open("scores.json", "r") as f:
    scores:dict = json.load(f)
  board = []
  for key, value in scores.items():
    board.append((key, value))

  sorted_board = sort_board(board)

  os.system("cls")
  print(f"{Fore.YELLOW}Leaderboard{Fore.RESET}\n")
  if sorted_board == []:
    print(f"[{Fore.RED}+{Fore.RESET}] No scores yet.")
  for x, item in enumerate(sorted_board):
    print(f"{Fore.BLUE}{x+1}{Fore.RESET}) {item[0]} - Score: {item[1]}") 

  print("\nPress <ENTER> to go back...", end="")
  input()

def main():
  colorama.init()
  ctypes.windll.kernel32.SetConsoleTitleW(f'Cheater Catcher | made by piombacciaio')

  #Init
  tries = []
  score:float = 0
  if not os.path.exists("scores.json"):
    with open("scores.json", "w") as f:
      f.write("{}")

  while True:

    #Choose difficulty
    os.system("cls")
    print(f"[{Fore.GREEN}++++{Fore.RESET}] Cheater Catcher | made by piombacciaio [{Fore.GREEN}++++{Fore.RESET}]\n")
    print(f"Session score: {Fore.GREEN + str(score) + Fore.RESET}")
    print(f"""Select game difficulty
[{Fore.BLUE}1{Fore.RESET}] - Hard
[{Fore.BLUE}2{Fore.RESET}] - Medium
[{Fore.BLUE}3{Fore.RESET}] - Easy
[{Fore.BLUE}L{Fore.RESET}] - Leaderboard
[{Fore.BLUE}Q{Fore.RESET}] - Quit""")
    difficulty = input(">> ").upper()

    while difficulty not in ["1", "2", "3", "Q", "L"]:
      print(f"[{Fore.RED}+{Fore.RESET}] Invalid choice, valid options are: {Style.BRIGHT}1{Style.RESET_ALL}, {Style.BRIGHT}2{Style.RESET_ALL}, {Style.BRIGHT}3{Style.RESET_ALL}, {Style.BRIGHT}L{Style.RESET_ALL} or {Style.BRIGHT}Q{Style.RESET_ALL}")
      difficulty = input("Input desired difficulty >> ").upper()

    else:
      if difficulty == "L":
        print_leaderboard()
        continue

      if difficulty == "Q":
        leave(score)

      #Init game
      cheater = choose_cheater()
      agents = get_throws(difficulty, cheater)
      lives = difficulties[difficulty]["attempts"]
      score_modifier = difficulties[difficulty]["score_modifier"]

      #Game
      playing = True
      start_time = time.time()

      while playing:
        os.system("cls")
        print_table(agents, lives, tries)

        if lives != 0:

          choice = input("The cheater is Agent ")

          if choice not in tries:

            if choice == str(cheater): #Win game and calc score + 100

              playing = False
              end_time = time.time()
              score = round((score + 100 + (100 / (end_time - start_time) * score_modifier) - (len(tries) * (1/score_modifier))), 2)

            else:

              lives -= 1
              tries.append(choice)
              print(f"[{Fore.RED}+{Fore.RESET}] Agent {choice} was innocent. Press <ENTER> to continue...", end="")
              input()

          else:

            print(f"[{Fore.RED}+{Fore.RESET}] Invalid choice, agent was already guessed. Press <ENTER> to continue...", end="")
            input()

        else: #Lose game and calc score + 0
          playing = False
          end_time = time.time()
          score = round((score + (100 / (end_time - start_time) * score_modifier) - (len(tries) * (1/score_modifier))), 2)
          print(f"[{Fore.RED}+++{Fore.RESET}] GAME OVER [{Fore.RED}+++{Fore.RESET}]\nThe cheater was {Fore.RED}Agent {cheater}{Fore.RESET}.\nPress <ENTER> to continue...", end="")
          input()

      tries = []

if __name__ == '__main__': main()