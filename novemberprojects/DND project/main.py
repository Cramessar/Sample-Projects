from flask import Flask, render_template, request, redirect, url_for, jsonify
import requests
import re
from crew_ai_agents import generate_companion_backstory

app = Flask(__name__)

DND_API_URL = "https://www.dnd5eapi.co/api"

# Store companions and the user's main character in memory
saved_companions = []
user_character = None

def fetch_dnd_data(endpoint):
    """Fetches data from a given endpoint in the D&D API."""
    response = requests.get(f"{DND_API_URL}/{endpoint}")
    if response.status_code == 200:
        return response.json().get('results', [])
    return []

def get_race_description(race_index):
    """Fetches the description for a specific race from the D&D API."""
    response = requests.get(f"{DND_API_URL}/races/{race_index}")
    if response.status_code == 200:
        data = response.json()
        return data.get("alignment", "") + " " + data.get("age", "") + " " + data.get("size_description", "")
    return "No description available."

def get_class_description(class_index):
    """Fetches detailed information for a specific class from the D&D API, including skills, weapons, spells, and proficiencies."""
    response = requests.get(f"{DND_API_URL}/classes/{class_index}")
    if response.status_code == 200:
        data = response.json()
        
        # Description
        description = data.get("desc", ["No description available."])[0]
        
        # Skills
        skills = [proficiency['name'] for proficiency in data.get("proficiencies", []) if 'Skill:' in proficiency['name']]
        
        # Weapons
        weapons = [proficiency['name'] for proficiency in data.get("proficiencies", []) if 'Weapon:' in proficiency['name']]
        
        # Proficiencies (other)
        proficiencies = [proficiency['name'] for proficiency in data.get("proficiencies", []) if 'Skill:' not in proficiency['name'] and 'Weapon:' not in proficiency['name']]
        
        # Spells (if available)
        spells = []
        if data.get("spellcasting"):
            spellcasting_url = data["spellcasting"]["url"]
            spell_response = requests.get(f"{DND_API_URL}{spellcasting_url}")
            if spell_response.status_code == 200:
                spell_data = spell_response.json()
                spells = [spell['name'] for spell in spell_data.get("spells", [])]
        
        return {
            "description": description,
            "skills": skills,
            "weapons": weapons,
            "proficiencies": proficiencies,
            "spells": spells
        }
    return {
        "description": "No description available.",
        "skills": [],
        "weapons": [],
        "proficiencies": [],
        "spells": []
    }

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/name-character', methods=['GET', 'POST'])
def name_character():
    """Route where the user names their character before proceeding with race selection."""
    if request.method == 'POST':
        name = request.form.get('name')
        if name:
            global user_character
            user_character = {"name": name}  # Initialize character with a name
            return redirect(url_for('select_race', character_type='user_character'))
    return render_template('name_character.html')

@app.route('/select-race/<character_type>', methods=['GET', 'POST'])
def select_race(character_type):
    races = fetch_dnd_data("races")
    if request.method == 'POST':
        selected_race = request.form.get('race')
        if selected_race:
            return redirect(url_for('select_class', race=selected_race, character_type=character_type))
    return render_template('select_race.html', races=races)

@app.route('/select-class/<race>/<character_type>', methods=['GET', 'POST'])
def select_class(race, character_type):
    classes = fetch_dnd_data("classes")
    if request.method == 'POST':
        selected_class = request.form.get('class')
        if selected_class:
            if character_type == "user_character":
                return redirect(url_for('user_character', race=race, character_class=selected_class))
            else:
                return redirect(url_for('companion', race=race, character_class=selected_class))
    return render_template('select_class.html', race=race, classes=classes)

@app.route('/user-character', methods=['GET', 'POST'])
def user_character():
    """Display and save the user's custom character."""
    race = request.args.get("race", "").lower()
    character_class = request.args.get("character_class", "").lower()

    race_description = get_race_description(race) if race else "No race selected."
    class_description = get_class_description(character_class) if character_class else "No class selected."

    # Generate backstory from Crew.ai for the custom character
    backstory = generate_companion_backstory(race, character_class)
    
    global user_character
    user_character.update({
        "race": race.title(),
        "class": character_class.title(),
        "race_description": race_description,
        "class_description": class_description,
        "backstory": backstory
    })

    return render_template('user_character.html', character=user_character)

@app.route('/view-my-character')
def view_my_character():
    """View the user's custom character."""
    return render_template('view_my_character.html', character=user_character)

@app.route('/companion', methods=['GET', 'POST'])
def companion():
    race = request.args.get("race", "").lower()
    character_class = request.args.get("character_class", "").lower()

    race_description = get_race_description(race) if race else "No race selected."
    class_description = get_class_description(character_class) if character_class else {
        "description": "No class selected.",
        "skills": [],
        "weapons": [],
        "proficiencies": [],
        "spells": []
    }

    # Generate complete backstory from Crew.ai
    backstory = generate_companion_backstory(race, character_class)

    # Extract the name if present
    name = "Unknown Companion"
    name_match = re.search(r"Name:\s*(.*)", backstory)
    if name_match:
        name = name_match.group(1).strip()

    # Package data for the companion
    companion_data = {
        "name": name,
        "race": race.title(),
        "class": character_class.title(),
        "race_description": race_description,
        "class_description": class_description,
        "backstory": backstory
    }

    # Save companion if submitted via POST request
    if request.method == 'POST':
        saved_companions.append(companion_data)
        return redirect(url_for('options'))

    return render_template('companion.html', companion=companion_data)

@app.route('/options')
def options():
    return render_template('options.html')

@app.route('/view-companions')
def view_companions():
    return render_template('view_companions.html', companions=saved_companions)

@app.route('/start-adventure')
def start_adventure():
    return "<h1>Adventure Started! (Placeholder)</h1>"

if __name__ == '__main__':
    app.run(debug=True)
