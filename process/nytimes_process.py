import json
from collections import defaultdict
from datetime import datetime
import os
import sys
import hashlib
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize

def generateJSONLD(inputPath, outputPath):
    with open("process/processedData/country_glossary.json", 'r') as jsonReader:
        data = jsonReader.readline()
        dict_country = json.loads(data)
        list_name = dict_country.keys()

    with open(inputPath, 'r') as reader:
        data = reader.readlines()
        country_sentiment = defaultdict(list)

        for line in data:
            if not line or line == "\n":
                continue

            js = json.loads(line)          
            
            if "response" in js and len(js["response"]["docs"]) > 0:
                targets = js["response"]["docs"]
                for item in targets:
                    temp = {}
                    if "headline" in item and "main" in item["headline"]:
                        # item["headline"] = item["headline"]["main"]
                        title = item["headline"]["main"]
                        temp["doc_id"] = hashlib.sha256(title.encode("utf-8")).hexdigest().upper()
                        temp["raw_content"] = "."
                        temp["url"] = item["web_url"]
                        temp["title"] = item["headline"]["main"]
                        temp["content"] = "."
                        temp["author"] = "."

                        if "pub_date" not in item:
                            if "nytimes.com/" not in item["web_url"]:
                                # item['pub_date'] = ""
                                temp["datetime"] = "."
                                continue

                            pub_date = item["web_url"].split("nytimes.com/")[1][0:10]
                            if not pub_date[0].isdigit():
                                temp["datetime"] = "."
                                continue

                            pub_date = pub_date.split('/')
                            year = pub_date[0]
                            month = pub_date[1]
                            day = pub_date[2]
                            pub_date = "%s-%s-%sT00:00:00" % (year, month, day)
                            temp["datetime"] = pub_date
                        
                        else:
                            temp["datetime"] = item["pub_date"]

                        temp["source"] = "nytimes"

                        # Country name extraction
                        country_related = checkCountry(list_name, temp["title"])
                        if country_related:
                            res = []
                            for c in country_related:
                                name = dict_country[c]
                                res.append(name)
                            temp["country"] = res
                        else:
                            temp["country"] = []
                        
                        # Sentiment analysis
                        sentiment = analyzeSentiment(temp["title"])
                        temp["sentiment"] = sentiment

                        for c in temp["country"]:
                            country_sentiment[c].append(temp["sentiment"])
                    
                        with open(outputPath, 'a') as writer:
                            writer.write(json.dumps(temp) + '\n')
                    
                    else:
                        continue

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
    if len(sys.argv) != 3:
        input_path = "crawl/data/nytimes_btc.txt"
        output_path = "process/processedData/nytimes_btc_new.jl"
    else:
        input_path = sys.argv[1]
        output_path = sys.argv[2]

    generateJSONLD(input_path, output_path)