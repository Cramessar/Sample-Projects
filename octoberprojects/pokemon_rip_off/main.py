import sys
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QTextEdit, QProgressBar, QLabel
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QMovie


class Move:
    def __init__(self, name, move_type, base_damage, accuracy, guaranteed_hit=False):
        self.name = name
        self.move_type = move_type 
        self.base_damage = base_damage
        self.accuracy = accuracy
        self.guaranteed_hit = guaranteed_hit


type_chart = {
    ('fire', 'water'): 0.5,
    ('fire', 'earth'): 0.5,
    ('fire', 'fire'): 0.5,
    ('fire', 'grass'): 2.0,
    ('water', 'fire'): 2.0,
    ('water', 'earth'): 2.0,
    ('water', 'water'): 0.5,
    ('earth', 'water'): 0.5,
    ('earth', 'fire'): 2.0,
    ('earth', 'earth'): 0.5,
}


class Creature:
    """A class to represent a creature."""
    def __init__(self, name, creature_type, hp, attack, defense, moves, level=1, xp=0):
        self.name = name
        self.creature_type = creature_type
        self.hp = hp
        self.max_hp = hp
        self.attack = attack
        self.defense = defense
        self.level = level
        self.xp = xp
        self.xp_to_next_level = 10 * level
        self.moves = moves

    def take_damage(self, damage):
        """Reduce HP by the damage taken, ensuring it doesn't drop below 0."""
        self.hp -= max(0, damage - self.defense)
        if self.hp < 0:
            self.hp = 0
        return self.hp

    def is_defeated(self):
        """Check if the creature is defeated."""
        return self.hp <= 0

    def gain_xp(self, amount):
        """Increase XP and check for level-up."""
        self.xp += amount
        if self.xp >= self.xp_to_next_level:
            return self.level_up()
        return None

    def level_up(self):
        """Increase creature's level and improve stats."""
        self.level += 1
        self.xp = 0 
        self.xp_to_next_level = 10 * self.level
        self.max_hp += 5
        self.hp = self.max_hp
        self.attack += 2
        self.defense += 1
        return f"{self.name} leveled up to level {self.level}!"

    def use_move(self, move, target_creature):
        """Use a move against another creature, applying level-based scaling, elemental bonuses, and lucky hits."""
        hit = True
        if not move.guaranteed_hit:  # accuracy check
            hit = random.randint(1, 100) <= move.accuracy
        
        if hit:
            level_difference = self.level - target_creature.level
            base_damage = move.base_damage
            if level_difference > 0:
                base_damage += (level_difference * 0.03) * base_damage
            elif level_difference < 0:
                base_damage -= (abs(level_difference) * 0.03) * base_damage
            lucky_hit = False
            if random.random() < 0.1:  # 10% chance for lucky hit
                lucky_multiplier = random.uniform(1.5, 1.9)
                base_damage *= lucky_multiplier
                lucky_hit = True
            type_multiplier = type_chart.get((move.move_type, target_creature.creature_type), 1.0)
            final_damage = int(base_damage * type_multiplier)
            target_creature.take_damage(final_damage)
            effectiveness_text = ""
            if type_multiplier > 1:
                effectiveness_text = "It's super effective!"
            elif type_multiplier < 1:
                effectiveness_text = "It's not very effective..."
            return f"{self.name} used {move.name}! {effectiveness_text} {target_creature.name} took {final_damage} damage.", lucky_hit
        else:
            return f"{self.name} tried to use {move.name} but it missed!", False


class Game(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Creature Capture Game")
        self.setGeometry(100, 100, 1200, 800)
        self.load_styles()
        self.money = 0
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.player_health_bar = QProgressBar(self)
        self.enemy_health_bar = QProgressBar(self)
        self.player_name_label = QLabel(self)
        self.enemy_name_label = QLabel(self)
        self.layout.addWidget(self.player_name_label)
        self.layout.addWidget(self.player_health_bar)
        self.layout.addWidget(self.enemy_name_label)
        self.layout.addWidget(self.enemy_health_bar)
        self.story_display = QTextEdit(self)
        self.story_display.setReadOnly(True)
        self.layout.addWidget(self.story_display)

        # Add QLabel for the star GIF animation using QMovie
        self.star_label = QLabel(self)
        self.movie = QMovie('star.gif')  
        self.star_label.setMovie(self.movie)
        self.star_label.setFixedSize(400, 400)  
        self.star_label.setScaledContents(True) 
        self.star_label.setVisible(False)  

        # Add QLabel for the lucky hit banner
        self.lucky_hit_banner = QLabel("Lucky Hit!", self)
        self.lucky_hit_banner.setObjectName("lucky_hit_banner")  
        self.lucky_hit_banner.setVisible(False)

        # Add QLabel for the 1up.gif animation for level-up
        self.level_up_label = QLabel(self)
        self.level_up_movie = QMovie('1up.gif')  # 1up.gif
        self.level_up_label.setMovie(self.level_up_movie)
        self.level_up_label.setFixedSize(400, 400)  
        self.level_up_label.setScaledContents(True) 
        self.level_up_label.setVisible(False)  

        # Add QLabel for the level-up banner
        self.level_up_banner = QLabel("Level Up!", self)
        self.level_up_banner.setObjectName("level_up_banner") 
        self.level_up_banner.setVisible(False)

        # Timer for animations
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate_star_and_banner)
        self.star_x = 0
        self.star_y = 0

        # Battle Buttons
        self.button_battle = QPushButton("Search for Creatures", self)
        self.button_battle.clicked.connect(self.encounter_creature)
        self.layout.addWidget(self.button_battle)

        # moves
        self.move_buttons = []
        for i in range(4):  
            move_button = QPushButton(f"Move {i+1}", self)
            move_button.clicked.connect(self.use_move(i))
            self.move_buttons.append(move_button)
            self.layout.addWidget(move_button)
        self.gil_label = QLabel(f"Current Gil: {self.money}", self)
        self.layout.addWidget(self.gil_label)
        self.central_widget.setLayout(self.layout)

        # our buddy flarewing
        self.player_creature = Creature("Flarewing", "fire", 30, 10, 5, [
            Move("Ember", "fire", 40, 90),
            Move("Flame Charge", "fire", 50, 85),
            Move("Swift", "normal", 35, 100, guaranteed_hit=True),
            Move("Hyper Beam", "normal", 100, 75)
        ])
        self.enemy_creature = None
        self.in_battle = False
        self.start_game()

    def load_styles(self):
        """Load styles from styles.css and apply them to the application."""
        try:
            with open("styles.css", "r") as file:
                self.setStyleSheet(file.read())
        except FileNotFoundError:
            print("styles.css file not found. Default styles will be used.")

    def start_game(self):
        """Display initial game state."""
        self.update_health_bars()
        self.update_gil_display()
        self.story_display.setText(f"Welcome to the creature capture game!\nExplore the world and find new creatures.\n"
                                   f"Your creature: {self.player_creature.name} (Level {self.player_creature.level}, XP: "
                                   f"{self.player_creature.xp}/{self.player_creature.xp_to_next_level})")

    def encounter_creature(self):
        """Simulate a random encounter with a creature."""
        if not self.in_battle:
            opponent_level = self.generate_opponent_level(self.player_creature.level)
            creatures = [Creature("Aquaclaw", "water", 20, 8, 4, [
                Move("Water Gun", "water", 40, 100),
                Move("Aqua Tail", "water", 50, 90)
            ], level=opponent_level), 
            Creature("Earthguard", "earth", 25, 6, 8, [
                Move("Rock Throw", "earth", 40, 95),
                Move("Earthquake", "earth", 60, 85)
            ], level=opponent_level)]
            self.enemy_creature = random.choice(creatures)
            self.in_battle = True
            self.story_display.setText(f"A wild {self.enemy_creature.name} has appeared (Level {self.enemy_creature.level})!\n"
                                       f"HP: {self.enemy_creature.hp}, Attack: {self.enemy_creature.attack}, Defense: {self.enemy_creature.defense}")
            self.update_health_bars()
            self.update_move_buttons()
        else:
            self.story_display.setText(f"You're already in a battle with {self.enemy_creature.name}!")

    def generate_opponent_level(self, player_level):
        """Generate an opponent level within ±3 levels of the player's level using a standard deviation."""
        mean = player_level
        std_dev = 1.5  
        level = int(random.gauss(mean, std_dev))
       
        return max(player_level - 3, min(player_level + 3, level))

    def enemy_attack(self):
        """Enemy creature attacks the player."""
        if self.enemy_creature:
            base_damage = random.uniform(0.1, 0.3) * self.player_creature.max_hp
            final_damage = int(base_damage) 
            self.player_creature.take_damage(final_damage)
            self.update_health_bars()
            return f"The enemy {self.enemy_creature.name} attacked and did {final_damage} damage!"

    def update_move_buttons(self):
        """Update move buttons with the player's creature's moves."""
        for i, move in enumerate(self.player_creature.moves):
            self.move_buttons[i].setText(move.name)
            self.move_buttons[i].setEnabled(True)
        for i in range(len(self.player_creature.moves), 4):
            self.move_buttons[i].setEnabled(False)

    def use_move(self, move_index):
        """Handle using a move during battle."""
        def move_func():
            if self.in_battle and self.enemy_creature:
                if move_index < len(self.player_creature.moves):
                    move = self.player_creature.moves[move_index]
                    result, lucky_hit = self.player_creature.use_move(move, self.enemy_creature)
                    self.story_display.setText(result)
                    self.update_health_bars()

                    if lucky_hit:
                        self.trigger_lucky_hit_animation()

                    if self.enemy_creature.is_defeated():
                        xp_gained = random.randint(4, 10)  #  exp gain between 4 and 10
                        gil_reward = random.randint(3, 11)  # gil reward between 3 and 11
                        level_up_message = f"{self.player_creature.name} gained {xp_gained} XP and earned {gil_reward} gil!"

                        level_up_result = self.player_creature.gain_xp(xp_gained)
                        self.money += gil_reward
                        self.update_gil_display()

                        if level_up_result:  
                            self.trigger_level_up_animation()
                            level_up_message += f" {level_up_result}"

                        self.story_display.append(f"The wild {self.enemy_creature.name} has been defeated!\n"
                                                  f"{level_up_message}\nYou now have {self.money} gil.")
                        self.in_battle = False
                    else:
                        self.story_display.append(self.enemy_attack())
            else:
                self.story_display.setText("You're not in a battle!")
        return move_func

    def trigger_lucky_hit_animation(self):
        """Trigger the star and banner animation for a lucky hit."""
        self.star_label.setVisible(True)
        self.movie.start()
        self.star_x = self.width() // 2 - 200  
        self.star_y = 100 + self.lucky_hit_banner.height() 
        self.star_label.move(self.star_x, self.star_y)
        self.lucky_hit_banner.setVisible(True)
        self.lucky_hit_banner.setGeometry(self.width() // 2 - 100, 50, 200, 50) 
        self.timer.start(50)  

    def trigger_level_up_animation(self):
        """Trigger the level-up GIF and banner animation."""
        self.level_up_label.setVisible(True)
        self.level_up_movie.start()
        self.star_x = self.width() // 2 - 200  
        self.star_y = 100 + self.level_up_banner.height()
        self.level_up_label.move(self.star_x, self.star_y)
        self.level_up_banner.setVisible(True)
        self.level_up_banner.setGeometry(self.width() // 2 - 100, 50, 200, 50)
        self.timer.start(50)

    def animate_star_and_banner(self):
        """Animate the star or level-up animation dropping down and hide the banner after animation."""
        self.star_y += 20
        if self.star_y > self.height():  
            self.timer.stop()
            self.star_label.setVisible(False)
            self.lucky_hit_banner.setVisible(False)
            self.level_up_label.setVisible(False)
            self.level_up_banner.setVisible(False) 
        else:
            self.star_label.move(self.star_x, self.star_y)
            self.level_up_label.move(self.star_x, self.star_y)

    def update_health_bars(self):
        """Update the health bars for both player and enemy creatures, ensuring health doesn't drop below 0, and apply color coding."""
        if self.enemy_creature:
            self.enemy_health_bar.setMaximum(self.enemy_creature.max_hp)
            self.enemy_health_bar.setValue(self.enemy_creature.hp)
            self.enemy_name_label.setText(f"{self.enemy_creature.name} (Level {self.enemy_creature.level}) (HP: {self.enemy_creature.hp}/{self.enemy_creature.max_hp})")
            self.set_health_bar_color(self.enemy_health_bar, self.enemy_creature.hp, self.enemy_creature.max_hp)
        else:
            self.enemy_health_bar.setValue(0)
            self.enemy_name_label.setText("")
        self.player_health_bar.setMaximum(self.player_creature.max_hp)
        self.player_health_bar.setValue(self.player_creature.hp)
        self.player_name_label.setText(f"{self.player_creature.name} (Level {self.player_creature.level}, XP: {self.player_creature.xp}/{self.player_creature.xp_to_next_level}) "
                                       f"(HP: {self.player_creature.hp}/{self.player_creature.max_hp})")
        self.set_health_bar_color(self.player_health_bar, self.player_creature.hp, self.player_creature.max_hp)

    def set_health_bar_color(self, health_bar, current_hp, max_hp):
        """Set the health bar color based on the percentage of health remaining."""
        health_percentage = (current_hp / max_hp) * 100

        if health_percentage > 50:
            health_bar.setStyleSheet("QProgressBar::chunk { background-color: green; }")
        elif health_percentage > 25:
            health_bar.setStyleSheet("QProgressBar::chunk { background-color: yellow; }")
        else:
            health_bar.setStyleSheet("QProgressBar::chunk { background-color: red; }")

    def update_gil_display(self):
        """Update the gil display with the current amount of gil."""
        self.gil_label.setText(f"Current Gil: {self.money}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = Game()
    game.show()
    sys.exit(app.exec_())
