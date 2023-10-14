import itertools
import random


class CardSimulator:
    n = 5

    def __init__(self):
        self.deck = self.shuffle_deck()

    def shuffle_deck(self):
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        deck = list(itertools.product(ranks, suits))
        random.shuffle(deck)
        return deck

    def simulate_event(self, event, num_simulations):
        count = 0
        for _ in range(num_simulations):
            self.deck = self.shuffle_deck()  # Shuffle the deck before each simulation
            hand = self.deck[:self.n]  # Draw the first two cards from the shuffled deck
            if event(hand):
                count += 1
        probability = count / num_simulations
        return probability

    # (a) The first two cards include at least one ace.
    def event_a(self, hand):
        self.n = 2
        return any(card[0] == 'A' for card in hand[:2])

    # (b) The first five cards include at least one ace.
    def event_b(self, hand):
        self.n = 5
        return any(card[0] == 'A' for card in hand)

    # (c) The first two cards are a pair of the same rank.
    def event_c(self, hand):
        self.n = 2
        return hand[0][0] == hand[1][0]

    # (d) The first five cards are all diamonds.
    def event_d(self, hand):
        self.n = 5
        return all(card[1] == 'Diamonds' for card in hand)

    # (e) The first five cards form a full house.
    def event_e(self, hand):
        self.n = 5
        ranks = [card[0] for card in hand]
        rank_counts = [ranks.count(rank) for rank in set(ranks)]
        return sorted(rank_counts) == [2, 3]


def main():
    simulator = CardSimulator()

    num_simulations = int(input("Enter the number of iterations: "))
    event_choice = input("Choose an event to simulate (a, b, c, d, e): ")

    if event_choice == 'a':
        probability = simulator.simulate_event(simulator.event_a, num_simulations)
    elif event_choice == 'b':
        probability = simulator.simulate_event(simulator.event_b, num_simulations)
    elif event_choice == 'c':
        probability = simulator.simulate_event(simulator.event_c, num_simulations)
    elif event_choice == 'd':
        probability = simulator.simulate_event(simulator.event_d, num_simulations)
    elif event_choice == 'e':
        probability = simulator.simulate_event(simulator.event_e, num_simulations)
    else:
        print("Invalid event choice. Please choose a, b, c, d, or e.")
        return

    print(f"Probability for event {event_choice}: {probability:.4f}")


if __name__ == "__main__":
    main()
