import json
from collections import defaultdict
import os

# def cleanData(path):

def countDateNum(path):
    dict_date = defaultdict(int)
    
    for filename in os.listdir(path):
        filepath = os.path.join(path, filename)
        with open(filepath, 'r') as reader:
            post = json.load(reader)
            date = post['datetime'].split(' ')[0]
            dict_date[date] += 1
        
    print(dict_date)


if __name__ == "__main__":
    path = "../data_crawl/TweetScraper/Data/tweet"

    countDateNum(path)