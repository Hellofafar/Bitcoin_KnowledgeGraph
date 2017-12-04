from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize
import sys
import os
import json

def analyze(input_path, output_path):
    with open(input_path, 'r') as reader:
        data = reader.readlines()
        for record in data:
            js = json.loads(record)
            content = js["headline"]
            sen_list = tokenize.sent_tokenize(content)
            sid = SentimentIntensityAnalyzer()
            
            pos = []
            neu = []
            neg = []
            for sentence in sen_list:
                # print(sentence)
                ss = sid.polarity_scores(sentence)
                pos.append(ss["pos"])
                neu.append(ss["neu"])
                neg.append(ss["neg"])
                # for k in sorted(ss):
                #     print('{0}: {1}, '.format(k, ss[k]), end='')
                # print()
            
            len_sen_list = len(sen_list)
            if sum(pos) / len_sen_list >= 0.5:
                js["sentiment"] = 1
            elif sum(neg) / len_sen_list >= 0.5:
                js["sentiment"] = -1
            else:
                js["sentiment"] = 0
            
            with open(output_path, 'a') as writer:
                writer.write(json.dumps(js) + '\n')
            

if __name__ == "__main__":
    if len(sys.argv) != 3:
        input_path = "process/processedData/nytimes_bitcoin.jl"
        output_path = "process/processedData/nytimes_bitcoin_sa.jl"
    else:
        input = sys.argv[1]
        output = sys.argv[2]
    
    analyze(input_path, output_path)