import json
from collections import defaultdict
from datetime import datetime
import os
import sys
import hashlib
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize


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
    with open("process/processedData/country_glossary.json", 'r') as jsonReader:
        data = jsonReader.readline()
        dict_country = json.loads(data)
        list_name = dict_country.keys()

    domain = "https://twitter.com"

    dict_date = defaultdict(int)

    for filename in os.listdir(path):
        filepath = os.path.join(path, filename)
        with open(filepath, 'r') as reader:
            # Used to count posts with respect to date
            post = json.load(reader)
            date = post['datetime'].split(' ')[0]
            dict_date[date] += 1
 
            timestamp = post["datetime"]
            timestamp = timestamp.replace(" ", "T")
            post["datetime"] = timestamp

            post["doc_id"] = hashlib.sha256(post["text"].encode("utf-8")).hexdigest().upper()
            post["url"] = domain + post["url"]
            post["raw_content"] = "."

            country_related = checkCountry(list_name, post["text"])
            if country_related:
                res = []
                for c in country_related:
                    name = dict_country[c]
                    res.append(name)
                post["country"] = res
            else:
                post["country"] = []
            
            sentiment = analyzeSentiment(post["text"])
            post["sentiment"] = sentiment

            with open(output, 'a') as writer:
                record = json.dumps(post) + '\n'
                writer.write(record)
    
    print(dict_date)

def checkCountry(countryList, content):
    token_content = tokenize.word_tokenize(content)
    common = set(countryList).intersection(set(token_content))
    return list(common)

def analyzeSentiment(content):
    sen_list = tokenize.sent_tokenize(content)
    sid = SentimentIntensityAnalyzer()
    
    compound = []
    for sentence in sen_list:
        # print(sentence)
        ss = sid.polarity_scores(sentence)
        compound.append(ss["compound"])
        # for k in sorted(ss):
        #     print('{0}: {1}, '.format(k, ss[k]), end='')
        # print()
    
    return sum(compound) / len(compound)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        path = "../data_crawl/TweetScraper/Data/tweet"
    else:
        path = sys.argv[1]

    # result = countDateNum(path)
    # print(result)
    output_path = "process/processedData/top_tweets_new.jl"
    generateJSONLD(path, output_path)