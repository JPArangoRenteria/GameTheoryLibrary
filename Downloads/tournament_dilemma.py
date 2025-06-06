import random
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict
import math

class Player:
    def __init__(self):
        self.last_action = None
        self.score = 0  # Initialize score
        self.elo_rating = 1200  # Starting ELO rating
        
    def update_score(self, reward):
        self.score += reward
    
    def reset_score(self):
        self.score = 0

class HumanPlayer(Player):
    def __init__(self):
        super().__init__()
        
    def choose_action(self, opponents):
        print(f"\n--- Your turn ---")
        print(f"Your current score: {self.score}")
        print("Opponents' last actions:")
        for i, opponent in enumerate(opponents):
            last_action = opponent.last_action if opponent.last_action else "None (first round)"
            print(f"  Opponent {i+1} ({type(opponent).__name__}): {last_action}")
        
        while True:
            choice = input("Choose your action (c for cooperate, d for defect): ").lower().strip()
            if choice in ['c', 'cooperate']:
                return 'cooperate'
            elif choice in ['d', 'defect']:
                return 'defect'
            else:
                print("Invalid input. Please enter 'c' for cooperate or 'd' for defect.")

class TitForTatPlayer(Player):
    def __init__(self):
        super().__init__()
        
    def choose_action(self, opponents):
        for opponent in opponents:
            if opponent.last_action == 'defect':
                return "defect" 
        return 'cooperate'

class TitForTatMixedPlayer(Player):  # Fixed typo in class name
    def __init__(self):
        super().__init__()
        
    def choose_action(self, opponents):
        n_defect = 0
        n_cooperate = 0
        for opponent in opponents:
            if opponent.last_action == 'defect':
                n_defect += 1
            elif opponent.last_action == 'cooperate':  # Fixed logic
                n_cooperate += 1
        if n_cooperate >= n_defect:
            return "cooperate"
        else:
            return "defect"

class RandomPlayer(Player):
    def __init__(self):
        super().__init__()
        
    def choose_action(self, opponents):  # Fixed parameter
        return random.choice(["cooperate", "defect"])
    
class GrimTriggerPlayer(Player):
    def __init__(self):
        super().__init__()
        self.triggered = False
        
    def choose_action(self, opponents):
        for opponent in opponents:
            if opponent.last_action == 'defect':  # Fixed logic and typo
                self.triggered = True
                return 'defect'
        if self.triggered:
            return 'defect'
        return 'cooperate'

class GrimTriggerMixPlayer(Player):
    def __init__(self):
        super().__init__()
        self.triggered = False
        self.defect_count = 0
        
    def choose_action(self, opponents):
        limit = 3
        for opponent in opponents:
            if opponent.last_action == 'defect':
                self.defect_count += 1
                if self.defect_count >= limit:
                    self.triggered = True
                    
        if self.triggered:
            return 'defect'
        return 'cooperate'

class ForgivingTitForTatPlayer(Player):
    def __init__(self):
        super().__init__()
        
    def choose_action(self, opponents):
        n = len(opponents)  # Fixed variable name
        cooperate_count = 0
        for opponent in opponents:
            if opponent.last_action == 'cooperate':
                cooperate_count += 1  # Fixed operator
                
        if cooperate_count > n / 5:
            return "cooperate"
        elif any(opponent.last_action == 'defect' for opponent in opponents):
            return "defect"
        return "cooperate"

class RuthlessTitForTatPlayer(Player):
    def __init__(self):
        super().__init__()
        
    def choose_action(self, opponents):
        n = len(opponents)  # Fixed variable name
        cooperate_count = 0
        for opponent in opponents:
            if opponent.last_action == 'cooperate':
                cooperate_count += 1  # Fixed operator
                
        if cooperate_count > n / 5:
            return "defect"
        elif any(opponent.last_action == 'defect' for opponent in opponents):
            return "defect"
        return random.choice(["cooperate", "defect"])

class SuperForgivingPlayer(Player):  # Fixed inheritance
    def __init__(self):
        super().__init__()
        
    def choose_action(self, opponents):
        return "cooperate"

class SuperUnforgivingPlayer(Player):  # Fixed inheritance and name
    def __init__(self):
        super().__init__()
        
    def choose_action(self, opponents):
        return "defect"

class ELOSystem:
    def __init__(self, k_factor=32):
        self.k_factor = k_factor
        
    def expected_score(self, rating_a, rating_b):
        return 1 / (1 + 10**((rating_b - rating_a) / 400))
    
    def update_ratings(self, player_a, player_b, score_a):
        """Update ELO ratings based on match result
        score_a: 1 if player_a wins, 0.5 for tie, 0 if player_b wins"""
        expected_a = self.expected_score(player_a.elo_rating, player_b.elo_rating)
        expected_b = self.expected_score(player_b.elo_rating, player_a.elo_rating)
        
        player_a.elo_rating += self.k_factor * (score_a - expected_a)
        player_b.elo_rating += self.k_factor * ((1 - score_a) - expected_b)

def play_match(player1, player2, rounds=100):
    """Play a match between two players and return the winner"""
    # Reset scores for this match
    player1.reset_score()
    player2.reset_score()
    
    # Reset any internal state
    if hasattr(player1, 'triggered'):
        player1.triggered = False
    if hasattr(player2, 'triggered'):
        player2.triggered = False
    if hasattr(player1, 'defect_count'):
        player1.defect_count = 0
    if hasattr(player2, 'defect_count'):
        player2.defect_count = 0
    
    for round_num in range(rounds):
        # Get actions
        action1 = player1.choose_action([player2])
        action2 = player2.choose_action([player1])
        
        # Calculate rewards
        if action1 == 'cooperate' and action2 == 'cooperate':
            reward1, reward2 = 3, 3
        elif action1 == 'cooperate' and action2 == 'defect':
            reward1, reward2 = 0, 5
        elif action1 == 'defect' and action2 == 'cooperate':
            reward1, reward2 = 5, 0
        else:  # Both defect
            reward1, reward2 = 1, 1
            
        player1.update_score(reward1)
        player2.update_score(reward2)
        
        # Update last actions
        player1.last_action = action1
        player2.last_action = action2
        
        # Show round results for human player
        if isinstance(player1, HumanPlayer) or isinstance(player2, HumanPlayer):
            print(f"Round {round_num + 1}: "
                  f"{type(player1).__name__} ({action1}) vs "
                  f"{type(player2).__name__} ({action2}) | "
                  f"Scores: {player1.score} vs {player2.score}")
    
    # Determine winner (1 for player1, 0.5 for tie, 0 for player2)
    if player1.score > player2.score:
        return 1.0
    elif player1.score < player2.score:
        return 0.0
    else:
        return 0.5

def run_tournament(player_classes, include_human=False, matches_per_pair=5):
    """Run a round-robin tournament with ELO rankings"""
    elo_system = ELOSystem()
    
    # Create players
    players = []
    if include_human:
        players.append(HumanPlayer())
    
    for player_class in player_classes:
        players.append(player_class())
    
    # Tournament results
    results = defaultdict(lambda: {'wins': 0, 'losses': 0, 'ties': 0, 'total_score': 0})
    
    print(f"\n=== Starting Tournament ===")
    print(f"Players: {[type(p).__name__ for p in players]}")
    print(f"Matches per pair: {matches_per_pair}")
    
    # Play all pairs
    total_matches = len(players) * (len(players) - 1) // 2 * matches_per_pair
    match_count = 0
    
    for i, player1 in enumerate(players):
        for j, player2 in enumerate(players):
            if i < j:  # Avoid duplicate matches
                for match_num in range(matches_per_pair):
                    match_count += 1
                    print(f"\nMatch {match_count}/{total_matches}: "
                          f"{type(player1).__name__} vs {type(player2).__name__} "
                          f"(Game {match_num + 1})")
                    
                    score = play_match(player1, player2)
                    
                    # Update ELO ratings
                    elo_system.update_ratings(player1, player2, score)
                    
                    # Update results
                    p1_name = type(player1).__name__
                    p2_name = type(player2).__name__
                    
                    results[p1_name]['total_score'] += player1.score
                    results[p2_name]['total_score'] += player2.score
                    
                    if score == 1.0:
                        results[p1_name]['wins'] += 1
                        results[p2_name]['losses'] += 1
                    elif score == 0.0:
                        results[p2_name]['wins'] += 1
                        results[p1_name]['losses'] += 1
                    else:
                        results[p1_name]['ties'] += 1
                        results[p2_name]['ties'] += 1
                    
                    print(f"Result: {type(player1).__name__} {player1.score} - "
                          f"{player2.score} {type(player2).__name__}")
                    print(f"ELO Ratings: {type(player1).__name__}: {player1.elo_rating:.1f}, "
                          f"{type(player2).__name__}: {player2.elo_rating:.1f}")
    
    return players, results

def display_rankings(players, results):
    """Display final rankings and statistics"""
    print(f"\n{'='*60}")
    print("FINAL TOURNAMENT RESULTS")
    print(f"{'='*60}")
    
    # Sort by ELO rating
    players_sorted = sorted(players, key=lambda p: p.elo_rating, reverse=True)
    
    print(f"\n{'Rank':<4} {'Player':<25} {'ELO':<8} {'W-L-T':<10} {'Total Score':<12}")
    print("-" * 65)
    
    for rank, player in enumerate(players_sorted, 1):
        name = type(player).__name__
        w = results[name]['wins']
        l = results[name]['losses']
        t = results[name]['ties']
        total_score = results[name]['total_score']
        
        print(f"{rank:<4} {name:<25} {player.elo_rating:<8.1f} "
              f"{w}-{l}-{t:<7} {total_score:<12}")

def plot_elo_ratings(players):
    """Create a bar chart of final ELO ratings"""
    names = [type(player).__name__ for player in players]
    ratings = [player.elo_rating for player in players]
    
    plt.figure(figsize=(12, 8))
    bars = plt.bar(names, ratings, color=['red' if 'Human' in name else 'blue' for name in names])
    
    # Add rating values on top of bars
    for bar, rating in zip(bars, ratings):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
                f'{rating:.0f}', ha='center', va='bottom')
    
    plt.axhline(y=1200, color='gray', linestyle='--', alpha=0.7, label='Starting ELO (1200)')
    plt.xlabel('Players')
    plt.ylabel('ELO Rating')
    plt.title('Final ELO Ratings - Prisoner\'s Dilemma Tournament')
    plt.xticks(rotation=45, ha='right')
    plt.legend()
    plt.tight_layout()
    plt.grid(axis='y', alpha=0.3)
    plt.show()

def main():
    print("Welcome to the Enhanced Prisoner's Dilemma Tournament!")
    print("This tournament will pit different strategies against each other using ELO rankings.")
    
    # Available player types
    player_classes = [
        TitForTatPlayer,
        TitForTatMixedPlayer,
        RandomPlayer,
        GrimTriggerPlayer,
        GrimTriggerMixPlayer,
        ForgivingTitForTatPlayer,
        RuthlessTitForTatPlayer,
        SuperForgivingPlayer,
        SuperUnforgivingPlayer
    ]
    
    # Ask if user wants to participate
    while True:
        human_input = input("\nDo you want to participate as a human player? (y/n): ").lower().strip()
        if human_input in ['y', 'yes']:
            include_human = True
            break
        elif human_input in ['n', 'no']:
            include_human = False
            break
        else:
            print("Please enter 'y' for yes or 'n' for no.")
    
    # Get number of matches per pair
    while True:
        try:
            matches = int(input("How many matches should each pair play? (recommended: 3-5): "))
            if matches > 0:
                break
            else:
                print("Please enter a positive number.")
        except ValueError:
            print("Please enter a valid number.")
    
    # Run tournament
    players, results = run_tournament(player_classes, include_human, matches)
    
    # Display results
    display_rankings(players, results)
    
    # Plot results
    plot_elo_ratings(players)
    
    print(f"\nTournament completed! Check the graph for visual ELO rankings.")

if __name__ == "__main__":
    main()
