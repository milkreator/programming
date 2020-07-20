# -----------------------------------------------------------------------------
# Exercise 3 - Pandas
#
# "Wait, can't we just use Pandas for this?"
#
# Pandas (https://pandas.pydata.org) is a very popular library for manipulating
# data and reading CSV files.  In fact, it has a function `read_csv()` for
# doing just that.
#
#    >>> import pandas
#    >>> df = pandas.read_csv('portfolio.csv')
#    >>> df
#    ... look at the result
#    >>> df['shares']
#    ... look at the result
#    >>> df.iloc[1]
#    ... look at the result
#    >>> df.shape
#    ... look at the result
#    >>>
#
# Your task: Create a "PandasPortfolio" object that uses Pandas to
# read/internally store data, but which presents data to the outside
# work using the same abstractions as before.
# -----------------------------------------------------------------------------

import pandas
import ex1
import report

class PandasPortfolio:
    def __init__(self):
        self.data = None

        
    @classmethod
    def from_csv(cls, filename):
        self = cls()
        self.data = pandas.read_csv(filename)
        return self
    # You need to define additional methods
    def __getitem__(self, index):
        row = self.data.iloc[index]
        return report.Holding(self.data['name'][row],
                              self.data['shares'][row],
                              self.data['price'][row])
    def __getitem__(self, index):
        if index >= len(self.data):
            raise IndexError()
        return report.Holding(self.data['name'][index],
                              self.data['shares'][index],
                              self.data['price'][index])

    
    
def main():
    import report
    import ex1
    portfolio = PandasPortfolio.from_csv('/Users/zhaowenlong/workspace/proj/programming/advprog_2020_07/2_owning/portfolio.csv')
    prices = ex1.PriceMap.from_csv('/Users/zhaowenlong/workspace/proj/programming/advprog_2020_07/2_owning/prices.csv')
    # This should work without modification
    report.print_report(portfolio, prices)

if __name__ == '__main__':
    main()
    

