import random
import matplotlib.pyplot as plt
import numpy as np
class Player:
    def __init__(self,opponent):
        self.opponent = opponent
        self.last_action = None
    def update_score(self, reward):
        self.score += reward

class TitForTatPlayer(Player):
    def __init__(self):
        super().__init__()
    def choose_action(self, opponents):
        for opponent in opponents:
            if opponent.last_action == 'defect':
                return "defect" 
        return 'cooperate'

class TitForTatPlayeMixed(Player):
    def __init__(self):
        super().__init__()
    def choose_action(self, opponents):
        n_defect = 0
        n_cooperate = 0
        for opponent in opponents:
            if opponent.last_action == 'defect':
                n_defect+=1
            else:
                n_cooperate+=1
        if n_cooperate >= n_defect:
            return "cooperate"
        else:
            return "defect"

class RandomPlayer(Player):
    def __init__(self):
        super().__init__()
    def choose_action(self, opponent):
        return random.choice(["cooperate", "defect"])
    
class GrimTriggerPlayer(Player):
    def __init__(self):
        super().__init__()
        self.triggered = False
    def choose_action(self,opponents):
        for opponent in opponents:
            if opponent.last_action == 'cooperate' and self.triggeres is False:
                self.triggered = False       
            else:
                self.triggered = True
                return 'defect'
        return 'cooperate'
class GrimTriggerMixPlayer(Player):
    def __init__(self):
        super().__init__()
        self.triggered = False
    def choose_action(self,opponents):
        counter = 0
        limit = 3
        for opponent in opponents:
            if counter < limit:
                if opponent.last_action == 'cooperate' and self.triggeres is False:
                    self.triggered = False       
                elif not(opponent.last_action == 'cooperate' and self.triggeres is False):
                    self.triggered = True
                    counter =+ 1
            else:
                return 'defect'
        return 'cooperate'

class ForgivingTitForTatPlayer(Player):
    def __init__(self):
        super().__init__()
    def choose_action(self, opponents):
        n = len(opponent)
        m = 0
        for opponent in opponents:
            if m > n/5:
                return "cooperate"
            elif opponent.last_action == 'cooperate':
                m =+1
        return random.choice(["cooperate", "defect"])
class RuthlessTitForTatPlayer(Player):
    def __init__(self):
        super().__init__()
    def choose_action(self, opponents):
        n = len(opponent)
        m = 0
        for opponent in opponents:
            if m > n/5:
                return "defect"
            elif opponent.last_action == 'cooperate':
                m =+ 1    
        return random.choice(["cooperate", "defect"])
class SuperForgivingPlayer:
    def __init__(self):
        super().__init__()
    def choose_action(self, opponents):
        return "cooperate"
class SuperUnForgivingPlayer:
    def __init__(self):
        super().__init__()
    def choose_action(self, opponents):
        return "defect"

def play_round(players):
    for i, player1 in enumerate(players):
        for j, player2 in enumerate(players):
            if i != j:  # Avoid playing against oneself
                action1 = player1.choose_action(player2)
                action2 = player2.choose_action(player1)

                if action1 == 'cooperate' and action2 == 'cooperate':
                    reward1 = 2
                    reward2 = 2
                elif action1 == 'cooperate' and action2 == 'defect':
                    reward1 = -1
                    reward2 = 3
                elif action1 == 'defect' and action2 == 'cooperate':
                    reward1 = 3
                    reward2 = -1
                else:  # Both defect
                    reward1 = 0
                    reward2 = 0

                player1.update_score(reward1)
                player2.update_score(reward2)

def run_simulation(players, rounds):
    for _ in range(rounds):
        play_round(players)

def plot_scores(players):
    names = [type(player).__name__ for player in players]
    scores = [player.score for player in players]

    plt.bar(names, scores)
    plt.xlabel('Players')
    plt.ylabel('Scores')
    plt.title('Prisoner\'s Dilemma Simulation')
    plt.show()

def plot_average_scores(player_classes, num_simulations):
    average_scores = {player_class.__name__: [] for player_class in player_classes}

    for _ in range(num_simulations):
        for player_class in player_classes:
            players = [player_class() for _ in range(2)]  # Create two players of the same class
            run_simulation(players, rounds=100)  # Adjust the number of rounds as needed
            scores = [player.score for player in players]
            average_score = np.mean(scores)
            average_scores[player_class.__name__].append(average_score)

    plt.figure(figsize=(10, 6))
    for player_class, scores in average_scores.items():
        plt.plot(scores, label=player_class)

    plt.xlabel('Simulation')
    plt.ylabel('Average Score')
    plt.title('Average Scores of Player Types over Simulations')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    player_classes = [TitForTatPlayer, RandomPlayer, GrimTriggerPlayer, ForgivingTitForTatPlayer, RuthlessTitForTatPlayer, SuperForgivingPlayer, SuperUnForgivingPlayer]
    plot_average_scores(player_classes, num_simulations=10)
