from flask import Flask, redirect, render_template, request
from random2 import randint

import pandas as pd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Load data
art_df = pd.read_csv('art_data.csv')


# Initalise global variables
tolerance = 0.05
counter = 1
clues = []
outcomes = {}


# Set random number
rand_number = randint(0, len(art_df) + 1)
# Get information on random art
artist = art_df.Artist.iloc[rand_number]
art_name = art_df.Title.iloc[rand_number]
art_url = art_df.Image.iloc[rand_number]
art_price = art_df['Selling Price'].iloc[rand_number]
art_date = art_df.Date.iloc[rand_number]




# Function to provide clues
def get_clue(data, rand_number, rounds):
    artist = data.Artist.iloc[rand_number]
    price = data['Selling Price'].iloc[rand_number]
    # Control flow with match-case 
    match rounds:
        case 1:
            return f'The art is titled as: {data.Title.iloc[rand_number]}'
        case 2:
            return f'The auction category is: {data.Category.iloc[rand_number]}'
        case 3:
             return f'The artist is listed as: {artist}'
        case 4:
            art_other = data.loc[(data['Artist'] == artist) & (data['Selling Price'] != price), 'Selling Price'].sample(n=1).values[0]
            return f'Other art by this artist has auctioned for: ${art_other:,.2f}'
        case 5:
            art_low = art_df.low_estimate.iloc[rand_number]
            art_high = art_df.high_estimate.iloc[rand_number]
            return f'The auction price was estimated to be between ${art_low:,.2f} and ${art_high:,.2f}'




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
        return render_template('over.html', result='Game Over!', art_name=art_name, art_url=art_url, clues=clues, art_price=art_price, art_date=art_date, guess=outcomes[max(outcomes.keys())]["guess"])




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
        
        # Check if guess is within +/- tolerance of the actual price
        if art_price * (1 - tolerance) <= guess <= art_price * (1 + tolerance):
            clues.clear()
            for i in range(5):
                clues.append(get_clue(art_df, rand_number, (i + 1)))
            return render_template('over.html', result='Correct!', art_name=art_name, art_url=art_url, clues=clues, art_price=art_price, art_date=art_date, guess=guess)
            
        elif guess > art_price:
            result = 'Too High'
        elif guess < art_price:
            result = 'Too Low'
        
        # Store guess and result
        outcomes[counter] = {"guess": guess, "result": result}

        # Increment the counter
        counter += 1

    return redirect('/')
