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
    country_sentiment = defaultdict(list)
    
    with open("process/processedData/country_glossary.json", 'r') as jsonReader:
        data = jsonReader.readline()
        dict_country = json.loads(data)
        list_name = dict_country.keys()

    domain = "https://twitter.com"

    dict_date = defaultdict(int)

    for filename in os.listdir(path):
        temp = {}
        filepath = os.path.join(path, filename)
        with open(filepath, 'r') as reader:
            # Used to count posts with respect to date
            post = json.load(reader)
            date = post['datetime'].split(' ')[0]
            dict_date[date] += 1

            temp["doc_id"] = hashlib.sha256(post["text"].encode("utf-8")).hexdigest().upper()
            temp["raw_content"] = "."
            temp["url"] = domain + post["url"]
            temp["title"] = "."
            temp["content"] = post["text"]
            temp["author"] = post["usernameTweet"]

            timestamp = post["datetime"]
            timestamp = timestamp.replace(" ", "T")
            temp["datetime"] = timestamp

            temp["source"] = "twitter"

            # Country name extraction
            country_related = checkCountry(list_name, post["text"])
            if country_related:
                res = []
                for c in country_related:
                    name = dict_country[c]
                    res.append(name)
                temp["country"] = res
            else:
                temp["country"] = []
            
            # Sentiment analysis
            sentiment = analyzeSentiment(post["text"])
            temp["sentiment"] = sentiment

            for c in temp["country"]:
                country_sentiment[c].append(temp["sentiment"])

            with open(output, 'a') as writer:
                record = json.dumps(temp) + '\n'
                writer.write(record)
    
    # Output dict_date result 
    print("Number of posts for each date:")
    print(dict_date)
    with open("date_count.json", "w") as countWriter:
        countWriter.write(json.dumps(dict_date))

    # Output country_sentiment result
    for c in country_sentiment:
        country_sentiment[c] = sum(country_sentiment[c]) / len(country_sentiment[c])
        
    with open("country_sentiment.json", 'a') as writer1:
        writer1.write(json.dumps(country_sentiment) + '\n')

    print("Average sentiment score of country appearing in articles:")
    print(country_sentiment)

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
    output_path = "process/processedData/top_tweets.jl"
    generateJSONLD(path, output_path)