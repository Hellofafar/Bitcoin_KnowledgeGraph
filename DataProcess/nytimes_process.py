import json
from collections import defaultdict
from datetime import datetime
import os
import sys

def generateJSONLD(inputPath, outputPath):
    with open(inputPath, 'r') as reader:
        data = reader.readlines()
        for line in data:
            if not line or line == "\n":
                continue

            js = json.loads(line)            
            
            if "response" in js and len(js["response"]["docs"]) > 0:
                targets = js["response"]["docs"]
                for i, item in enumerate(targets):
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
                    
                    item["url"] = item.pop("web_url")
                    item["raw_content"] = "."
                    item["doc_id"] = i
                    
                    with open(outputPath, 'a') as writer:
                        writer.write(json.dumps(item) + '\n')

if __name__ == "__main__":
    if len(sys.argv) < 2:
        input_path = "../DataCrawl/data/nytimes_bitcoin.txt"
        output_path = "nytimes_bitcoin.jl"
    else:
        input_path = sys.argv[1]
        output_path = sys.argv[2]

    generateJSONLD(input_path, output_path)