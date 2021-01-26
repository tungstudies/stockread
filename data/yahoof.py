from datetime import datetime

import yfinance as yf


def get_data_element(instance_var, stock_dict, stock_info, dict_key):
    try:
        # print('{dict_key}: {dict_value}'.format(dict_key=dict_key, dict_value=stock_info[dict_key]))
        stock_dict[dict_key] = stock_info[dict_key]
        return stock_info[dict_key]
    except KeyError as err:
        print('Stock Info Element Error - {}'.format(err))
        stock_dict[dict_key] = 'n/a'
        return instance_var


def timestamp_to_datetime_string(timestamp):
    ex_date = 'n/a'
    try:
        ex_date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
    except TypeError as err:
        print('Stock Info TypeError - {}'.format(err))

        return ex_date


class Stock:
    def __init__(self, ticker):
        self.symbol = ticker
        print(ticker)
        self.stock_yf = yf.Ticker(ticker)
        self.stock_dict = dict()
        self.longName: str = ''
        self.sector: str = ''
        self.industry: str = ''

        # self.longBusinessSummary: str = ''

        self.website: str = ''
        self.exchange: str = ''
        self.twoHundredDayAverage = 0
        self.fiftyDayAverage = 0
        self.trailingAnnualDividendYield = 0
        self.fiveYearAvgDividendYield = 0
        self.dividendYield = 0
        self.payoutRatio = 0
        self.trailingAnnualDividendRate = 0
        self.dividendRate = 0
        self.exDividendDate = 0
        self.lastDividendDate = 0
        self.beta = 0
        self.trailingPE = 0
        self.forwardPE = 0
        self.marketCap = 0
        self.regularMarketVolume = 0
        self.averageVolume = 0
        self.averageVolume10days = 0
        self.enterpriseToRevenue = 0
        self.profitMargins = 0
        self.enterpriseToEbitda = 0
        self.trailingEps = 0
        self.forwardEps = 0
        self.bookValue = 0
        self.priceToBook = 0
        self.heldPercentInstitutions = 0

    def get_stock_data(self):
        stock_info = self.stock_yf.info

        # print(stock_info)

        self.longName = get_data_element(self.longName, self.stock_dict, stock_info, 'longName')
        self.sector = get_data_element(self.sector, self.stock_dict, stock_info, 'sector')
        self.industry = get_data_element(self.industry, self.stock_dict, stock_info, 'industry')

        # self.longBusinessSummary = get_data_element(self.longBusinessSummary, self.stock_dict, stock_info,
        #                                             'longBusinessSummary')

        self.website = get_data_element(self.website, self.stock_dict, stock_info, 'website')
        self.exchange = get_data_element(self.exchange, self.stock_dict, stock_info, 'exchange')
        self.twoHundredDayAverage = get_data_element(self.twoHundredDayAverage, self.stock_dict, stock_info,
                                                     'twoHundredDayAverage')
        self.fiftyDayAverage = get_data_element(self.fiftyDayAverage, self.stock_dict, stock_info, 'fiftyDayAverage')
        self.trailingAnnualDividendYield = get_data_element(self.trailingAnnualDividendYield, self.stock_dict,
                                                            stock_info, 'trailingAnnualDividendYield')
        self.fiveYearAvgDividendYield = get_data_element(self.fiveYearAvgDividendYield, self.stock_dict, stock_info,
                                                         'fiveYearAvgDividendYield')
        self.dividendYield = get_data_element(self.dividendYield, self.stock_dict, stock_info, 'dividendYield')
        self.payoutRatio = get_data_element(self.payoutRatio, self.stock_dict, stock_info, 'payoutRatio')
        self.trailingAnnualDividendRate = get_data_element(self.trailingAnnualDividendRate, self.stock_dict, stock_info,
                                                           'trailingAnnualDividendRate')
        self.dividendRate = get_data_element(self.dividendRate, self.stock_dict, stock_info, 'dividendRate')

        self.exDividendDate = get_data_element(self.exDividendDate, self.stock_dict, stock_info, 'exDividendDate')
        self.exDividendDate = timestamp_to_datetime_string(self.exDividendDate)
        self.stock_dict['exDividendDate'] = timestamp_to_datetime_string(self.stock_dict['exDividendDate'])

        self.lastDividendDate = get_data_element(self.lastDividendDate, self.stock_dict, stock_info, 'lastDividendDate')
        self.lastDividendDate = timestamp_to_datetime_string(self.lastDividendDate)
        self.stock_dict['lastDividendDate'] = timestamp_to_datetime_string(self.stock_dict['lastDividendDate'])

        self.beta = get_data_element(self.beta, self.stock_dict, stock_info, 'beta')
        self.trailingPE = get_data_element(self.trailingPE, self.stock_dict, stock_info, 'trailingPE')
        self.forwardPE = get_data_element(self.forwardPE, self.stock_dict, stock_info, 'forwardPE')
        self.marketCap = get_data_element(self.marketCap, self.stock_dict, stock_info, 'marketCap')
        self.regularMarketVolume = get_data_element(self.regularMarketVolume, self.stock_dict, stock_info,
                                                    'regularMarketVolume')
        self.averageVolume = get_data_element(self.averageVolume, self.stock_dict, stock_info, 'averageVolume')
        self.averageVolume10days = get_data_element(self.averageVolume10days, self.stock_dict, stock_info,
                                                    'averageVolume10days')
        self.enterpriseToRevenue = get_data_element(self.enterpriseToRevenue, self.stock_dict, stock_info,
                                                    'enterpriseToRevenue')
        self.profitMargins = get_data_element(self.profitMargins, self.stock_dict, stock_info, 'profitMargins')
        self.enterpriseToEbitda = get_data_element(self.enterpriseToEbitda, self.stock_dict, stock_info,
                                                   'enterpriseToEbitda')
        self.trailingEps = get_data_element(self.trailingEps, self.stock_dict, stock_info, 'trailingEps')
        self.forwardEps = get_data_element(self.forwardEps, self.stock_dict, stock_info, 'forwardEps')
        self.bookValue = get_data_element(self.bookValue, self.stock_dict, stock_info, 'bookValue')
        self.priceToBook = get_data_element(self.priceToBook, self.stock_dict, stock_info, 'priceToBook')
        self.heldPercentInstitutions = get_data_element(self.heldPercentInstitutions, self.stock_dict, stock_info,
                                                        'heldPercentInstitutions')


if __name__ == '__main__':
    stock = Stock('INE.TO')
    stock.get_stock_data()
    print(stock.dividendRate)
    print(stock.symbol)
    print(stock.longName)
    print(stock.stock_dict['dividendRate'])
    print(stock.stock_dict['trailingPE'])
