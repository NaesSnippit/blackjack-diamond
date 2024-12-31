import random

class Card:
    def __init__(self, suit, value, display_value):
        self.suit = suit
        self.value = value
        self.display_value = display_value

    def __repr__(self):
        return f"{self.display_value} of {self.suit}"

class Deck:
    suits = ["5-Pointed Star", "4-Pointed Star", "Upside-Down Spade", "X"]
    values = {"N": 1, "A": 1, "E": 1, "O": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "J": 10, "Q": 10, "K": 10}

    def __init__(self):
        self.cards = [Card(suit, value, display_value) for suit in self.suits for display_value, value in self.values.items()]
        self.cards.append(Card("Joker", 0, "Tarot Card"))

    def shuffle(self):
        random.shuffle(self.cards)

    def draw_card(self):
        return self.cards.pop() if self.cards else None

class Player:
    def __init__(self, name, money):
        self.name = name
        self.money = money
        self.hand = []

    def calculate_hand_value(self):
        total = 0
        aces = 0
        for card in self.hand:
            total += card.value
            if card.display_value in ["N", "A", "E", "O"]:
                aces += 1
        while total > 21 and aces:
            total -= 10
            aces -= 1
        return total

    def add_card(self, card):
        self.hand.append(card)

    def reset_hand(self):
        self.hand = []

class StarfallBlackjack:
    def __init__(self):
        self.deck = Deck()
        self.deck.shuffle()
        self.player = Player("You", 100)
        self.diamond = Player("Diamond", float("inf"))  # Diamond has infinite money

    def deal_initial_cards(self):
        for _ in range(2):
            self.player.add_card(self.deck.draw_card())
            self.diamond.add_card(self.deck.draw_card())

    def display_hands(self, reveal_diamond=False):
        print("\nYour hand:")
        for card in self.player.hand:
            print(card)
        print(f"Total value: {self.player.calculate_hand_value()}")

        print("\nDiamond's hand:")
        if reveal_diamond:
            for card in self.diamond.hand:
                print(card)
            print(f"Total value: {self.diamond.calculate_hand_value()}")
        else:
            print(self.diamond.hand[0])
            print("[Hidden]")

    def diamond_cheats(self):
        cheat_chance = random.random()
        if cheat_chance < 0.3:  # 30% chance Diamond cheats
            print("\nDiamond smirks... She's up to something!")
            if random.random() < 0.5 and self.diamond.calculate_hand_value() < 17:
                card = self.deck.draw_card()
                self.diamond.add_card(card)
                print(f"Diamond sneakily draws an extra card: {card}")
            else:
                if self.diamond.hand:
                    removed_card = self.diamond.hand.pop()
                    print(f"Diamond discards a card to manipulate her hand!")

    def player_turn(self):
        while True:
            self.display_hands()
            move = input("Do you want to [H]it or [S]tand? ").strip().lower()
            if move == 'h':
                card = self.deck.draw_card()
                self.player.add_card(card)
                print(f"You draw: {card}")
                if self.player.calculate_hand_value() > 21:
                    print("Bust! You exceeded 21.")
                    return False
            elif move == 's':
                return True
            else:
                print("Invalid input. Please enter H or S.")

    def diamond_turn(self):
        while self.diamond.calculate_hand_value() < 17:
            self.diamond_cheats()
            card = self.deck.draw_card()
            self.diamond.add_card(card)
            print(f"Diamond draws: {card}")

    def determine_winner(self):
        player_value = self.player.calculate_hand_value()
        diamond_value = self.diamond.calculate_hand_value()

        print("\nFinal hands:")
        self.display_hands(reveal_diamond=True)

        if player_value > 21:
            return "Diamond wins! You busted."
        elif diamond_value > 21 or player_value > diamond_value:
            return "You win! Diamond loses."
        elif player_value < diamond_value:
            return "Diamond wins! Better luck next time."
        else:
            return "It's a tie!"

    def play_round(self):
        print("\n--- New Round ---")
        self.player.reset_hand()
        self.diamond.reset_hand()
        self.deck = Deck()
        self.deck.shuffle()
        self.deal_initial_cards()

        bet = 0
        while True:
            try:
                bet = int(input(f"You have ${self.player.money}. Enter your bet: "))
                if 1 <= bet <= self.player.money:
                    break
                else:
                    print("Invalid bet amount. Please enter a value within your balance.")
            except ValueError:
                print("Please enter a valid number.")

        if not self.player_turn():
            self.player.money -= bet
            print(f"You lost ${bet}. Remaining balance: ${self.player.money}")
            return

        self.diamond_turn()
        result = self.determine_winner()
        print(result)

        if "You win" in result:
            self.player.money += bet
        elif "Diamond wins" in result:
            self.player.money -= bet

        print(f"Your balance: ${self.player.money}")

    def play_game(self):
        print("Welcome to Starfall Blackjack!")
        while self.player.money > 0:
            self.play_round()
            if input("Play another round? (y/n): ").strip().lower() != 'y':
                break
        print("Game over! Thanks for playing.")

if __name__ == "__main__":
    game = StarfallBlackjack()
    game.play_game()
