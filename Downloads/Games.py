import random
import matplotlib.pyplot as plt
class Player:
    def __init__(self,opponent):
        self.opponent = opponent
        self.last_action = None
    def update_score(self, reward):
        self.score += reward

class TitForTatPlayer(Player):
    def __init__(self):
        super().__init__()
    def choose_action(self, opponent):
        if opponent.last_action == 'cooperate':
            return "cooperate"
        else:
            return 'defect'

class RandomPlayer(Player):
    def __init__(self):
        super().__init__()
    def choose_action(self, opponent):
        return random.choice(["cooperate", "defect"])
    
class GrimTriggerPlayer(Player):
    def __init__(self):
        super().__init__()
        self.triggered = False
    def choose_action(self,opponent):
        if opponent.last_action == 'cooperate' and self.triggeres is False:
            self.triggered = False
            return 'cooperate'
            
        else:
            self.triggered = True
            return 'defect'
class ForgivingTitForTatPlayer(Player):
    def __init__(self):
        super().__init__()
    def choose_action(self, opponent):
        if opponent.last_action == 'cooperate':
            return "cooperate"
        else:
            return random.choice(["cooperate", "defect"])
class RuthlessTitForTatPlayer(Player):
    def __init__(self):
        super().__init__()
    def choose_action(self, opponent):
        if opponent.last_action == 'cooperate':
            return "cooperate"
        else:
            return random.choice(["cooperate", "defect"])
class SuperForgivingPlayer:
    def __init__(self):
        super().__init__()
    def choose_action(self, opponent):
        return "cooperate"
class SuperUnForgivingPlayer:
    def __init__(self):
        super().__init__()
    def choose_action(self, opponent):
        return "defect"

def play_round(prisoner1, prisoner2):
    action1 = prisoner1.choose_action(prisoner2.last_action)
    action2 = prisoner2.choose_action(prisoner1.last_action)

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

    prisoner1.update_score(reward1)
    prisoner2.update_score(reward2)
def run_simulation(player1_class, player2_class, rounds=1000, simulations=100):
    player1_wins = 0
    player2_wins = 0
    draws = 0

    for _ in range(simulations):
        player1 = player1_class()
        player2 = player2_class()

        for _ in range(rounds):
            play_round(player1, player2)

        if player1.score > player2.score:
            player1_wins += 1
        elif player2.score > player1.score:
            player2_wins += 1
        else:
            draws += 1

    return {
        'player1_wins': player1_wins,
        'player2_wins': player2_wins,
        'draws': draws,
        'player1_average_score': player1.score / simulations,
        'player2_average_score': player2.score / simulations
    }

def plot_results(results):
    labels = ['Player 1 Wins', 'Player 2 Wins', 'Draws']
    values = [results['player1_wins'], results['player2_wins'], results['draws']]

    plt.figure(figsize=(10, 5))
    plt.bar(labels, values, color=['green', 'blue', 'orange'])
    plt.title('Simulation Results')
    plt.xlabel('Outcome')
    plt.ylabel('Frequency')
    plt.show()

def main():
    player_classes = [TitForTatPlayer, RandomPlayer, GrimTriggerPlayer, ForgivingTitForTatPlayer, RuthlessTitForTatPlayer, SuperForgivingPlayer, SuperUnForgivingPlayer]

    for player1_class in player_classes:
        for player2_class in player_classes:
            results = run_simulation(player1_class, player2_class)
            print(f"{player1_class.__name__} vs {player2_class.__name__}:")
            print(f"Player 1 wins: {results['player1_wins']}, Player 2 wins: {results['player2_wins']}, Draws: {results['draws']}")
            print(f"Player 1 average score: {results['player1_average_score']}, Player 2 average score: {results['player2_average_score']}\n")

            # Plot the results for each combination
            plot_results(results)

if __name__ == "__main__":
    main()
        
