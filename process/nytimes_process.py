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
        for line in data:
            if not line or line == "\n":
                continue

            js = json.loads(line)            
            
            if "response" in js and len(js["response"]["docs"]) > 0:
                targets = js["response"]["docs"]
                for item in targets:
                    if "headline" in item and "main" in item["headline"]:
                        item["headline"] = item["headline"]["main"]                  

                    if "pub_date" not in item:
                        if "nytimes.com/" not in item["web_url"]:
                            item['pub_date'] = ""
                            continue

                        pub_date = item["web_url"].split("nytimes.com/")[1][0:10]
                        if not pub_date[0].isdigit():
                            item["pub_date"] = ""
                            continue

                        pub_date = pub_date.split('/')
                        year = pub_date[0]
                        month = pub_date[1]
                        day = pub_date[2]
                        pub_date = "%s-%s-%sT00:00:00" % (year, month, day)
                        item['pub_date'] = pub_date
                    
                    item["doc_id"] = hashlib.sha256(item["headline"].encode("utf-8")).hexdigest().upper()
                    item["url"] = item.pop("web_url")
                    item["raw_content"] = "."

                    country_related = checkCountry(list_name, item["headline"])
                    if country_related:
                        res = []
                        for c in country_related:
                            name = dict_country[c]
                            res.append(name)
                        item["country"] = res
                    else:
                        item["country"] = []
                    
                    sentiment = analyzeSentiment(item["headline"])
                    item["sentiment"] = sentiment
                    
                    with open(outputPath, 'a') as writer:
                        writer.write(json.dumps(item) + '\n')

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