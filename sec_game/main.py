import tkinter as tk

class SECGame:
    def __init__(self, master):
        self.master = master
        self.master.title("SEC College Football Card Collector")

        # Game state variables
        self.player_cards = 0
        self.computer_cards = 0
        self.player_rate = 1        # Cards per second for the player
        self.computer_rate = 1      # Cards per second for the computer
        self.manual_click_value = 1 # Cards per manual click
        self.upgrade_cost = 10      # Starting upgrade cost
        self.upgrade_increase = 1   # Increase in player's generation rate per upgrade

        # UI Elements
        self.info_label = tk.Label(master, text="Bienvenue au jeu de collection de cartes SEC!")
        self.info_label.pack(pady=5)

        self.player_label = tk.Label(master, text=f"Your Cards: {self.player_cards} (Cartes)")
        self.player_label.pack(pady=5)

        self.computer_label = tk.Label(master, text=f"Computer Cards: {self.computer_cards}")
        self.computer_label.pack(pady=5)

        self.rate_label = tk.Label(master, text=f"Your Generation Rate: {self.player_rate} cards/sec")
        self.rate_label.pack(pady=5)

        self.status_label = tk.Label(master, text="Status: Game On!")
        self.status_label.pack(pady=5)

        self.collect_button = tk.Button(master, text="Collect Card", command=self.manual_collect)
        self.collect_button.pack(pady=5)

        self.upgrade_button = tk.Button(master, text=f"Upgrade (Cost: {self.upgrade_cost})", command=self.upgrade)
        self.upgrade_button.pack(pady=5)

        # Start the game loop
        self.update_game()

    def update_game(self):
        # Idle accrual: add generation rates to the card counts every second
        self.player_cards += self.player_rate
        self.computer_cards += self.computer_rate

        # Update the UI
        self.update_labels()

        # Check win status
        if self.player_cards > self.computer_cards:
            self.status_label.config(text="Status: You are winning! (Vous gagnez!)")
        elif self.player_cards < self.computer_cards:
            self.status_label.config(text="Status: Computer is winning!")
        else:
            self.status_label.config(text="Status: It's a tie!")

        # Schedule the next update after 1000ms (1 second)
        self.master.after(1000, self.update_game)

    def update_labels(self):
        self.player_label.config(text=f"Your Cards: {self.player_cards} (Cartes)")
        self.computer_label.config(text=f"Computer Cards: {self.computer_cards}")
        self.rate_label.config(text=f"Your Generation Rate: {self.player_rate} cards/sec")
        self.upgrade_button.config(text=f"Upgrade (Cost: {self.upgrade_cost})")

    def manual_collect(self):
        # Manual click increases player's card count
        self.player_cards += self.manual_click_value
        self.update_labels()

    def upgrade(self):
        # Upgrade player's generation rate if enough cards are available
        if self.player_cards >= self.upgrade_cost:
            self.player_cards -= self.upgrade_cost
            self.player_rate += self.upgrade_increase
            # Increase cost for the next upgrade (rounded to an integer)
            self.upgrade_cost = int(self.upgrade_cost * 1.5)
            self.update_labels()
        else:
            self.status_label.config(text="Not enough cards to upgrade! (Pas assez de cartes pour améliorer!)")

if __name__ == "__main__":
    root = tk.Tk()
    game = SECGame(root)
    root.mainloop()
