try:
    import sys
    print('System Version: {}'.format(sys.version))

    from data.dhandler import extract_tickers
    from config import StockConfig, VocabularyConfig

except ModuleNotFoundError as err:
    print('Some modules are missing: {}'.format(err))
    sys.exit()

tsx_tickers = StockConfig('TSX').tickers
nasdaq_tickers = StockConfig('NASDAQ').tickers
non_tickers = VocabularyConfig().non_tickers
dollar_countries = VocabularyConfig().dollar_countries


def find_tickers(str_context: str, country: str = 'United States') -> set:
    if country == 'United States':
        return extract_tickers(message=str_context, tickers=nasdaq_tickers, non_tickers=non_tickers,
                               dollar_countries=dollar_countries)
    if country == 'Canada':
        return extract_tickers(message=str_context, tickers=nasdaq_tickers, non_tickers=non_tickers,
                               dollar_countries=dollar_countries)
    else:
        return set()


if __name__ == '__main__':
    message = 'Ark Invest Bought THIS Space Stock [HUGE Potential] Ark Invest Bought This Space related stock. ' \
              'EXPC is doing a SPAC merger with Blade, an Urban Air Mobility platform. Could it be included in ARKX?'

    tickers_found = find_tickers(message)
    print(tickers_found)
