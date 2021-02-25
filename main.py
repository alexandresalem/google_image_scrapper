from utils import ImageSearch

if __name__ == '__main__':
    SEARCH_TERM = "US Flag"
    QUANTITY = 1
    FOLDER = '/home/username/Downloads'
    ImageSearch(SEARCH_TERM, QUANTITY, FOLDER).download()
