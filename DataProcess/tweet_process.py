import json
from collections import defaultdict
from datetime import datetime
import os
import sys

# def cleanData(path):

def countDateNum(path):
    dict_date = defaultdict(int)
    
    for filename in os.listdir(path):
        filepath = os.path.join(path, filename)
        with open(filepath, 'r') as reader:
            post = json.load(reader)
            date = post['datetime'].split(' ')[0]
            dict_date[date] += 1
        
    return dict_data

def generateJSONLD(path, output):
    domain = "https://twitter.com"

    dict_date = defaultdict(int)

    for filename in os.listdir(path):
        filepath = os.path.join(path, filename)
        with open(filepath, 'r') as reader:
            # Used to count posts with respect to date
            post = json.load(reader)
            date = post['datetime'].split(' ')[0]
            dict_date[date] += 1

            post = json.load(reader)
            post["url"] = domain + post["url"]
            timestamp = post["datetime"]
            timestamp = timestamp.replace(" ", "T")
            # print(timestamp)
            # isotime = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
            # print(isotime.isoformat())
            post["datetime"] = timestamp
            with open(output, 'a') as writer:
                res = json.dumps(post) + '\n'
                writer.write(res)
    
    print(dict_date)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        path = "../data_crawl/TweetScraper/Data/tweet"
    else:
        path = sys.argv[1]

    # result = countDateNum(path)
    # print(result)
    output_path = "top_tweets.json"
    generateJSONLD(path, output_path)