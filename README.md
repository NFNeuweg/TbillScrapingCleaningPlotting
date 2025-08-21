Features

Scrapers

treasuryScraper.py → pulls recent Treasury auction results.

treasuryScraperForFullDocument.py → scrapes a larger historical range of results.

Data

treasuryScraperAnalysis.csv → cleaned dataset used for visualization.

treasury_auction_results.csv → main dataset of auction results, updated by scrapers.

Plotting & Calculator

treasuryScraperPlotter.py:

Plots interactive line charts of investment rates across time and security terms.

Cleans date columns (Issue Date) and investment rates (parses % into decimals).

Provides a simple calculator:

“If I invest $X into a Y-week bill, how much do I pay today, what face value do I get, and what’s the profit?”
