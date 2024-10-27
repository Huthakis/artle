# artle
#### Video Demo: [artle - Final Project for CS50](https://youtu.be/zqYcBOo1Nd8)
#### Description:
Artle is a new twist on the Wordle model, focusing on art and its auction prices. On each launch the user is presented with a piece of artwork and challenged to correctly guess its auction price (to within 5%), they are given up to six attempts. After each guess, the user receives feedback indicating if their guess was too high or too low. If incorrect, a clue related to the auction, artist, or painting itself will appear to help guide subsequent guesses. The game ends when the user guesses correctly or is out of rounds, at this time an ending screen page will load.

This project was inspired by a YouTube video from Wendover Productions called "The Art Market is a Scam (And Rich People Run It)". The video covers how some art is auctioned for very large sums, then discusses how these prices are manipulated by purchasers and dealers. The idea behind creating this web application was to reinforce how difficult it is to put a price on art when minimal context is provided. The app's was built to be simple and responsive using Flask and several supporting files to manage data processing, logic, and front-end presentation.

#### Files and Structure
The application comprises six files:
1. app.py
	- Backend application code, containing setup, functions, and routing logic. It manages data setup, user input processing, and game progression through two main routes and a helper function, get_clue.
		- Setup Code: The setup code loads the cleaned art data from art_data.csv and randomly selects a row representing an artwork to display for the current game. This selection includes details like the artwork's title, artist, auction estimates, and selling price, setting up all necessary data for gameplay.
		- app.route('/'): This route handles the main game page. When the page is loaded, it renders index.html, displaying the selected artwork and an input field for the user's guesses. This route also generates a clue for the player using the get_clue function. If the player has run out of attempts it redirects them to a "Game Over!" version of over.html, providing the final price and a summary of clues.
		- app.route('/guess'): This route processes the user's guess, checking it against the actual auction price. If the guess is within 5% of the price, it renders a “Correct!” version of over.html, ending the game. If the guess is incorrect, it gives feedback on whether the guess was too high or too low, and increments the round counter. The user is then redirected back to app.route('/') to make another guess.
		- get_clue Function: The get_clue function is a helper function designed to enhance gameplay by generating informative hints after each incorrect guess. Depending on the current round, get_clue provides specific hints about the artwork or artist. This progressive clue system helps users refine their guesses and makes the game more engaging and educational.
2. data_cleaner.py
	- This script is responsible for fetching and cleaning the art data, sourced from a GitHub repository. The data undergoes several cleaning steps to ensure quality and consistency for gameplay, including: remove singular artists, remove art without auction estimates, remove non-standard characters, and reformatted text to title case.
3. art_data.csv
	- This file stores the cleaned art data, derived from the original GitHub source. It contains columns such as artist name, title, auction house, and price estimates, with each record representing a unique artwork. This dataset allows the app to randomly select an artwork for each game, providing a new experience every time.
4. styles.css
	- The CSS file maintains a consistent style across the game. The design choices prioritize simplicity and readability, using straightforward layouts and color schemes.
5. index.html
	- This is the main page of the application, where users make their guesses. It dynamically displays the current artwork and offers input boxes for guesses. Above the input box is a table where past guesses and outcomes (e.g., “too high” or “too low”) are displayed, giving users a helpful history to guide their next guess. Below the input box, a section shows clues revealed after each incorrect guess, offering insights to improve their chances of success.
6. over.html
	- This page appears when the game ends, the heading will change depending on if the user has successfully guessed the price or has run out of attempts. The page displays all clues, providing complete information for the user to reference.

#### Design Choices
- Clues: It was decided to provide clues to make the game more interactive and interesting. This has the added benefit of making the game easier.
- Random Selection: Having a large dataset ensures that the user is unlikely to see the same artwork twice. A different, much larger, dataset was originally selected, but shortly before the submission of this project the image links stopped working.
- Data Cleaning: The suitable datasets that were discovered all had varying amounts of incomplete and/or messy data. Writing a script dedicated to cleaning makes the preparation from the source reproducible.
- Tolerance Threshold: Allowing the guess to be correct within a certain percentage, currently set to 5%, provided a good balance of enabling users to actually win without the game getting too easy. The threshold was also tested at 0% and 10%, but these made the game too hard and too easy respectively.

#### Acknowledgments
This project is currently using data from the "SothebysData_clean.csv" file available in the "What-Makes-Art-Valuable" repository on [GitHub](https://github.com/georgiecoetzer/What-Makes-Art-Valuable), owned by [Georgina Coetzer](https://github.com/georgiecoetzer). The creation of the data is discussed in their article posted to Medium: [What makes Art Valuable: Data Scraping and Exploratory Data Visualizations](https://medium.com/@gcoetzer/what-makes-art-valuable-data-scraping-and-exploratory-data-visualizations-82966b218a07).