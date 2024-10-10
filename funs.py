# Functions for shiny app

# Packages
import pandas as pd


# Function to remove artists that only appear once
def remove_singles(data):
    # Count the occurrences of each artist
    artist_counts = data['artist'].value_counts()
    # Filter artists that appear more than once
    artists_to_keep = artist_counts[artist_counts > 1].index
    # Keep only rows where the artist is in the list of artists to keep
    filtered_data = data[data['artist'].isin(artists_to_keep)]
    # Return data
    return filtered_data


# Function to check answer
def questioner(data, guess, rand_number, rounds, tolerance):
    price = data.price.iloc[rand_number]

    # Logic for game
    if rounds <= 6:
        # Get user guess
        answer = guess
        try:
            answer = float(answer)
        except ValueError:
            answer = 0
        print('Your answer: $' + str(answer))
        # Logic for checking guess
        if answer == price:
            return (
                f'You are right! This is {data.name.iloc[rand_number]}, '
                f'by {data.artist.iloc[rand_number]}, and it was auctioned '
                f'for ${data.price.iloc[rand_number]}.'
            )
        elif price * (1 - tolerance) <= answer <= price * (1 + tolerance):
            return (
                f'You are within {100 * tolerance}%. The exact price was '
                f'${data.price.iloc[rand_number]}. This is '
                f'{data.name.iloc[rand_number]}, by '
                f'{data.artist.iloc[rand_number]}, and it was auctioned '
                f'for ${data.price.iloc[rand_number]}.'
            )
        elif answer > price:
            return 'Too High'
        elif answer < price:
            return 'Too low'
        else:
            pass
    else:
        return (
            f'This is {data.name.iloc[rand_number]}, by '
            f'{data.artist.iloc[rand_number]}, and it was auctioned '
            f'for ${data.price.iloc[rand_number]}'
        )


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