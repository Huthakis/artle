# artle
#### Video Demo: [Link to video demo] (URL HERE)
#### Description:
A wordle type clone for art and art prices. On each launch, the user is presented with a piece of artwork and given up to 6 rounds to correctly guess its price (to within 10%). After each guess, the user will be told if their guess was correct, too high, or too low. If the guess if not correct they will also be given a clue about the auction, painting, or artist.

This web application uses 7 files:
1. app.py
	- Backend application code, there is setup code and two app routes in this file:
		- The setup code loads the art data file and randomly selects a row to be used for the game
		- app.route('/') contains logic for rendering the index.html page until the user is out of rounds, then the over.html page is rendered
		- app.route('/guess') contains logic for checking the guess against the art price, renders the winner.html page if the guess is correct (to within 10%), otherwise returns the too high/low result, increments the round counter, and redirects to app.route('/')
2. art_data.csv
	- Data about the artwork, contains multiple columns of information, including a link to an online image of the artwork. Modified from the original source by removing duplicates, artists with only one piece of artwork, art without data for estimates, Chinese characters, and reformatted text to title case
4. static/styles.css
	- CSS style page to maintain consistent styling between pages.
5. index.html
	- Landing page for the app and where the user will make their guesses, above the guess box is a table that will populate with the guesses from the previous rounds and the outcome (too high or too low). Below the guess box is a table that will populate with the clues after each incorrect guess
6. winner.html
	- Display page for when the user guesses the price correctly (to within 10%), provides all information from the clues
7. over.html
	- Display page for when the user is out of rounds and the price has not been guessed correctly, provides all information from the clues

This project was inspired a YouTube video from Wendover Productions called "The Art Market is a Scam (And Rich People Run It). The video covers how some art is auctioned for very large sums, then discusses how these prices are manipulated by purchasers and dealers. The idea behind creating this web application was to reinforce how difficult it is to put a price on art when minimal information is provided.

Currently using data from the "SothebysData_clean.csv" file from "What-Makes-Art-Valuable" repository on [GitHub](https://github.com/georgiecoetzer/What-Makes-Art-Valuable), owned by [Georgina Coetzer](https://github.com/georgiecoetzer). The creation of the data is discussed in an article posted to Medium: [What makes Art Valuable: Data Scraping and Exploratory Data Visualizations](https://medium.com/@gcoetzer/what-makes-art-valuable-data-scraping-and-exploratory-data-visualizations-82966b218a07).