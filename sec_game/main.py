import tkinter as tk
from tkinter import PhotoImage
import logging
from random import choice
import os
import time

# Configure logging
logging.basicConfig(filename="game_log.txt", level=logging.INFO, format='%(asctime)s - %(message)s')

SEC_TEAMS = {
    "Alabama": "logos/tide.png",
    "Georgia": "logos/bulldog.png",
    "LSU": "logos/tiger.png",
    "Florida": "logos/gator.png",
    "Tennessee": "logos/volunteer.png",
    "Texas A&M": "logos/aggies.png"
}

class SECGame:
    def __init__(self, master):
        self.master = master
        self.master.configure(bg='green')  # Set background color to resemble a football field
        self.master.title("SEC College Football Card Collector")
        self.master.geometry("800x700")  # Increased window size for better layout  # Increased window size
        self.available_teams = list(SEC_TEAMS.keys())
        self.player_team = None
        self.computer_team = None
        self.winner_team = choice(self.available_teams)
        self.team_images = {}

        # Load and scale images
        for team, path in SEC_TEAMS.items():
            if os.path.exists(path):
                img = PhotoImage(file=path)
                self.team_images[team] = img.subsample(4, 4)  # Slightly larger images
            else:
                logging.warning(f"Missing image: {path}")
                self.team_images[team] = None

        # UI Elements
        self.info_label = tk.Label(master, text="Choose a team!")
        self.info_label.grid(row=0, column=0, columnspan=3, pady=5)

        self.team_buttons = []
        row, col = 1, 0
        for team in self.available_teams:
            img = self.team_images.get(team)
            if img:
                img_label = tk.Label(master, image=img)
                img_label.image = img  # Keep reference to avoid garbage collection
                img_label.grid(row=row, column=col)
            btn = tk.Button(master, text=team, command=lambda t=team: self.choose_team(t))
            btn.grid(row=row+1, column=col, pady=5)
            self.team_buttons.append(btn)
            col += 1
            if col > 2:  # Move to next row after 3 columns
                col = 0
                row += 2

        self.status_label = tk.Label(master, text="Waiting for selection...")
        self.status_label.grid(row=row+1, column=0, columnspan=3, pady=5)

    def choose_team(self, team):
        if team not in self.available_teams:
            logging.error(f"Attempted to remove non-existent team: {team}")
            return  # Avoid ValueError if team was already removed
        
        logging.info(f"Player chose: {team}")
        self.player_team = team
        self.available_teams.remove(team)
        self.status_label.config(text=f"You chose {team}. AI is selecting...")
        self.master.update()
        time.sleep(1.5)  # Pause before AI selects
        self.computer_select()

    def computer_select(self):
        if self.available_teams:
            self.computer_team = choice(self.available_teams)
            logging.info(f"AI chose: {self.computer_team}")
            self.status_label.config(text=f"AI chose {self.computer_team}.")
            self.master.update()
            time.sleep(1.5)  # Pause before displaying winner
            self.check_winner()

    def check_winner(self):
        if self.player_team == self.winner_team:
            self.status_label.config(text=f"Winner! {self.player_team} won the championship!")
            logging.info(f"Player's team {self.player_team} won!")
        else:
            self.status_label.config(text=f"AI wins! {self.computer_team} won the championship!")
            logging.info(f"AI's team {self.computer_team} won!")

if __name__ == "__main__":
    root = tk.Tk()
    game = SECGame(root)
    root.mainloop()