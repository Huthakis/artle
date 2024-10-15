from flask import Flask, redirect, render_template, request
from funs import get_clue, remove_singles
from random2 import randint

import pandas as pd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Load data
art_df = pd.read_csv('art_data.csv')

# Set random number
rand_number = randint(0, len(art_df) + 1)

# Get information random art
art_name = art_df.name.iloc[rand_number]
art_url = art_df.source.iloc[rand_number]
art_price = art_df.price.iloc[rand_number]

# Initalise global variables
tolerance = 0.1
counter = 1
clues = []
outcomes = {}

# Function to provide clues
def get_clue(data, rand_number, rounds):
    # Local variables
    artist = data.artist.iloc[rand_number]
    price = data.price.iloc[rand_number]

    # Control flow with match-case 
    match rounds:
        case 1:
            return f'The art is called: {data.name.iloc[rand_number]}'
        case 2:
            return f'The artist is: {data.country.iloc[rand_number]}'
        case 3:
            if pd.isna(data.yearOfDeath.iloc[rand_number]):
                return 'The artist is alive.'
            else:
                return f'The artist died in: {data.yearOfDeath.iloc[rand_number]}'
        case 4:
            return f'The artist is: {artist}'
        case 5:
            other_prices = data[data['artist'] == artist].price
            selection = other_prices[other_prices != price].sample(n=1).values[0]
            return f'Other art by this artist has sold for: ${selection}'

@app.route('/')
def index():
    # Clear clues to avoid duplicating them on refresh
    clues.clear()

    if counter == 1:
        return render_template('index.html', art_name=art_name, art_url=art_url, outcomes=outcomes, clues=clues)
    elif counter <=6:
        # Get clue information
        for i in range((counter - 1)):
            clues.append(get_clue(art_df, rand_number, (i + 1)))
        return render_template('index.html', art_name=art_name, art_url=art_url, outcomes=outcomes, clues=clues)
    else:
        # Get clue information
        for i in range(5):
            clues.append(get_clue(art_df, rand_number, (i + 1)))
        return render_template('over.html', art_name=art_name, art_url=art_url, clues=clues, art_price=art_price)


@app.route('/guess', methods=['POST'])
def guess():
    global counter

    guess = request.form.get("guess")

    if not guess:
        return redirect('/')
    else:
        try:
            guess = float(guess)
            if len(outcomes) != 0:
                for guessed in outcomes.values():
                    if guess == guessed['guess']:
                        return redirect('/')
        except ValueError:
            return redirect('/')
        
        if art_price * (1 - tolerance) <= guess <= art_price * (1 + tolerance):
            information = []
            for i in range(5):
                information.append(get_clue(art_df, rand_number, (i + 1)))
            return render_template('winner.html', art_name=art_name, art_url=art_url, information=information, art_price=art_price)
            
        elif guess > art_price:
            result = 'Too High'
        elif guess < art_price:
            result = 'Too Low'
            
        outcomes[counter] = {"guess": guess, "result": result}

        # Increment the counter
        counter += 1

    return redirect('/')
