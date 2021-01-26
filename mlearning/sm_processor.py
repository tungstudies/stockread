from config import FinanceConfig

import re
import nltk
import string

# punkt - module which provides word_tokenize() method
nltk.download('punkt')

# stopwords - words which does not add much meaning to a sentence, can be safely filtered out
nltk.download('stopwords')

# wordnet - module which provides lemmatize() method
nltk.download('wordnet')

# lexicon - words and their meanings.
# corpus (singular) - body of text --> corpora (plural) - collection of bodies of text

# get ticker dictionary to check if a target text contains tickers in it
fc = FinanceConfig()
tickers = fc.tickers


class StockMessageProcessor(object):
    stop_words = set(nltk.corpus.stopwords.words("english"))
    stemmer = nltk.stem.PorterStemmer()
    lemmatizer = nltk.stem.WordNetLemmatizer()

    def __init__(self, message: str):
        self.message = message
        self.tickers = set()
        self.tokens = list()

    def get_tickers_and_tokens(self):
        # Replace URLs with a space in the message
        # @see https://www.runoob.com/python/python-reg-expressions.html
        url_pattern = r"http\S+"
        text = re.sub(url_pattern, "", self.message, flags=re.MULTILINE)

        # Replace @tag username with a space in the message
        attag_pattern = r"@\S+"
        text = re.sub(attag_pattern, "", text, flags=re.MULTILINE)

        # Split remaining text by punctuation
        punctuation = string.punctuation

        punctuation = punctuation.replace('$', '')  # exclude '$' character
        punctuation = punctuation.replace('.', '')  # exclude '.' character

        re_punc = re.compile(r'[\s{}]+'.format(re.escape(punctuation)))  # prepare regex for char filtering

        # Split message text to tokenize
        words = re_punc.split(text)

        while words:
            last_word = words.pop()

            if len(last_word) > 2 and last_word[0] == "$" and last_word[1:] in tickers:
                self.tickers.add(last_word[1:])

            elif last_word in tickers:
                self.tickers.add(last_word)

            else:
                token = last_word.lower()
                if token.isalpha() and token not in self.stop_words:
                    self.tokens.append(self.lemmatizer.lemmatize(token))

        return {'tickers': self.tickers, 'tokens': self.tokens}


if __name__ == '__main__':
    sample_message = "I'm a long term investor, and business owner from Calgary Alberta, Canada"

    nlp = StockMessageProcessor(message=sample_message)
    tickers = nlp.get_tickers_and_tokens()['tickers']
    print(tickers)
