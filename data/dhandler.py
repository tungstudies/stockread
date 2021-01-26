import csv
import re


def csv_to_dict(filepath: str, has_header: bool, col_index, **names_and_indexes):
    """Convert a CSV file to a Python dictionary

    :param filepath: the csv filepath
    :type filepath: str
    :param has_header: declare if the csv file has headers of not
    :type has_header: bool
    :param col_index: the position of the index column containing they keys of each row
    :type col_index: int
    :param names_and_indexes: the names of the other columns and their indexes acting as values of each row
    :type names_and_indexes: key&value pair (i.e.: customer_name=2, country=3, city=4)
    :return: a Python dictionary
    :rtype: dict
    """
    index_of_keys = int(col_index)
    output_dict = {}
    with open(filepath, 'r') as file:
        reader = csv.reader(file)
        if has_header:
            next(reader, None)  # skip the headers
        for row in reader:
            output_dict[row[index_of_keys]] = dict()
            for key, value in names_and_indexes.items():
                output_dict[row[index_of_keys]][key] = row[int(value)]

    return output_dict


def csv_to_set(filepath: str,  has_header: bool, col_index: int = 1) -> set:
    """
    :param filepath: the csv filepath
    :type filepath:str
    :param has_header: declare if the csv file has headers of not
    :type has_header: bool
    :param col_index: the position of the index column containing the set elements
    :type col_index: int
    :return: a Python set
    :rtype: set
    """

    output_set = set()
    with open(filepath, 'r') as file:
        reader = csv.reader(file)
        if has_header:
            next(reader, None)  # skip the headers
        for row in reader:
            output_set.add(row[col_index - 1])
    return output_set


def extract_tickers(message: str, tickers: dict, non_tickers: set, dollar_countries: set) -> set:
    """
    :param message: the context string that might contain stock tickers
    :type message: str
    :param tickers: the set (hashset) of stock tickers
    :type tickers: set
    :param non_tickers: the set (hashset) of abbreviations/words that takes forms and values of stock tickers
    :type non_tickers: set
    :param dollar_countries: countries that have dollar currency with the $ sign
    :type dollar_countries: set
    :return: list of tickers found in the given string
    :rtype: set
    """
    valid_tickers = set()

    # check for substring starting with $ sign and ending with a space if it is not dollar notation
    filter_1 = re.findall(r'[$][A-Za-z][\S]*', str(message))
    reform_1 = [str.upper(word[1:]) for word in filter_1 if word[1:] not in dollar_countries]
    # check if the list of valid upper cases if it is in stock tickers and add to the result set
    valid_tickers.update([ticker for ticker in reform_1 if ticker in tickers])

    # check for substring starting with hashtag sign & ending with a whitespace against non-tickers
    filter_2 = re.findall(r'[#][A-Za-z][\S]*', str(message))
    reform_2 = [str.upper(word[1:]) for word in filter_2 if word[1:] not in non_tickers]
    # check if the list of valid upper cases if it is in stock tickers and add to the result set
    valid_tickers.update([ticker for ticker in reform_2 if ticker in tickers])

    # check for substring starting with a whitespace following by more than 2 upper cases against non-tickers
    filter_3 = re.findall(r'[\s][A-Z]{2,}', str(message))
    reform_3 = [str.upper(word[1:]) for word in filter_3 if word[1:] not in non_tickers]
    # check if the list of valid upper cases if it is in stock tickers and add to the result set
    valid_tickers.update([ticker for ticker in reform_3 if ticker in tickers])

    # check for substring starting with a open parenthesis against non-tickers (i.e.: '(FEIM)')
    filter_4 = re.findall(r'[(][A-Za-z]*', str(message))
    reform_4 = [str.upper(word[1:]) for word in filter_4 if word[1:] not in non_tickers]
    # check if the list of valid upper cases if it is in stock tickers and add to the result set
    valid_tickers.update([ticker for ticker in reform_4 if ticker in tickers])

    return valid_tickers


'''
def download_file(download_filepath, download_url):
    download_folder = os.path.dirname(download_filepath)

    # create download folder if not alrady exist
    if not os.path.exists(download_folder):
        try:
            os.makedirs(download_folder)
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    print(f'Downloading a file from: {download_url}')
    targetfile = urllib.request.urlretrieve(
        download_url, download_filepath)

    pathfile = os.path.abspath(targetfile[0])
    print("Saved the downloaded file to {}".format(pathfile))
'''
if __name__ == '__main__':
    file_path = "/data/vocab/non_tickers.csv"
    print(csv_to_set(file_path))
