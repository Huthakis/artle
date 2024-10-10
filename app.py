from flask import Flask, redirect, render_template, request
from funs import get_clue, remove_singles
from random2 import randint

import pandas as pd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Load data
useful_cols = [
    'artist',
    'country',
    'yearOfBirth',
    'yearOfDeath',
    'name',
    'year',
    'price',
    'material',
    'height',
    'width',
    'link',
    'source',
]
art_df = pd.read_csv('sdata.txt', sep='\t', usecols=useful_cols)
art_df = remove_singles(art_df)

# Set random number
rand_number = randint(0, len(art_df) + 1)

# Get information random art
art_name = art_df.name.iloc[rand_number]
art_url = art_df.source.iloc[rand_number]
art_price = art_df.price.iloc[rand_number]
print(art_price)

# Initalise global variables
tolerance = 0.1
counter = 1
clues = []
outcomes = {}

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
        for i in range(counter):
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
