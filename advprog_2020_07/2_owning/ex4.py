# -----------------------------------------------------------------------------
# Exercise 4 : Real-time prices challenge
#
# The report.py program is currently programmed to read stock prices
# from a file `prices.csv`.   However, could you create a custom
# PriceMap class that obtains the prices from some kind of
# online data source (i.e., website, API, etc.)?
#
# Note: This exercise is open-ended.  I don't actually know a good API
# from which to obtain stock prices.  You might need to use a libraries
# such as requests, beautifulsoup, and others to scrape it off
# a public website.

import report
import requests

class PriceMap:
    def __init__(self):
        self.prices = {}

    def __getitem__(self, name):
        # fetch a price from some web 
        if name not in self.prices:
            r = requests.get(f'https://finnhub.io/api/v1/quote?symbol={name}')
            self.prices[name] = r.json()['pc']

        return self.prices[name]

def main():
    import report
    import ex1
    # Verify the mutability tests with a standard list
    portfolio = ex1.Portfolio.from_csv('/Users/zhaowenlong/workspace/proj/programming/advprog_2020_07/2_owning/portfolio.csv')
    prices = PriceMap()     # must modify
    report.print_report(portfolio, prices)
    
if __name__ == '__main__':
    main()
    
        
        




