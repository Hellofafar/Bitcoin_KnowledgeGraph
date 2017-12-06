import sys
import json
from collections import defaultdict
import nltk
import hashlib
from datetime import datetime
nltk.download('words')
from nltk.corpus import stopwords
import nltk.data
from nltk.sentiment.vader import SentimentIntensityAnalyzer


def generateJSONLD(inputPath, outputPath):

    with open("process/processedData/country_glossary.json", 'r') as jsonReader:
        data = jsonReader.readline()
        dict_country = json.loads(data)
        set_name = set(dict_country.keys())

    with open(inputPath) as f:
        data_json = json.load(f)

        country_sentiment = defaultdict(list)

        for i in range(len(data_json)):
            data = data_json[i]
            temp = {}

            content = data["content"]
            temp["doc_id"] = hashlib.sha256(content.encode("utf-8")).hexdigest().upper()
            temp["raw_content"] = "."
            temp["url"] = "https://www.coindesk.com/"
            temp["title"] = data["title"]
            temp["content"] = content
            temp["author"] = data["author"]
            
            # Process datetime
            date = data["date"]
            time = data["time"]
            timestamp = date + ' ' + time
            timestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
            temp["datetime"] = datetime.strftime(timestamp, "%Y-%m-%dT%H:%M:%S")
            temp["source"] = "coindesk"

            # Process country
            named_entity = getNameEntity(content)
            country_related = set_name.intersection(named_entity)
            if country_related:
                res = []
                for c in country_related:
                    name = dict_country[c]
                    res.append(name)
                temp["country"] = res
            else:
                temp["country"] = []

            # Sentiment analysis
            sentiment = analyzeSentiment(temp["content"])
            temp["sentiment"] = sentiment

            for c in temp["country"]:
                country_sentiment[c].append(temp["sentiment"])
        
            with open(outputPath, 'a') as writer:
                writer.write(json.dumps(temp) + '\n')

        for c in country_sentiment:
            country_sentiment[c] = sum(country_sentiment[c]) / len(country_sentiment[c])
        
        with open("country_sentiment.json", 'a') as writer1:
            writer1.write(json.dumps(country_sentiment) + '\n')

        print("Average sentiment score of country appearing in articles:")
        print(country_sentiment)
        

def getNameEntity(content):
    ''' 
    Return named entity in content

    By Calvin
    '''
    sentences = nltk.sent_tokenize(content)
    tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]
    tagged_sentences = [nltk.pos_tag(sentence) for sentence in tokenized_sentences]
    chunked_sentences = nltk.ne_chunk_sents(tagged_sentences, binary=True)

    entity_names = []
    for tree in chunked_sentences:
        # Print results per sentence
        # print extract_entity_names(tree)
        entity_names.extend(extract_entity_names(tree))
    
    return set(entity_names)

def extract_entity_names(t):
    ''' 
    Extract entity from chunked sentences

    By Calvin
    '''
    entity_names = []

    if hasattr(t, 'label') and t.label:
        if t.label() == 'NE':
            entity_names.append(' '.join([child[0] for child in t]))
        else:
            for child in t:
                entity_names.extend(extract_entity_names(child))

    return entity_names

def analyzeSentiment(content):
    ''' 
    Analyze sentiment of content
    
    by Calvin
    '''
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    sentences = tokenizer.tokenize(content)[:-1]

    sid = SentimentIntensityAnalyzer()
    sum_score = 0
    num_total = 0
    for sentence in sentences:
        # print(sentence)
        ss = sid.polarity_scores(sentence)
        for k in ss:
            # print('{0}: {1}, '.format(k, ss[k]), end='')
            sum_score += float(ss['compound'])
        # if ss['compound'] != 0.0:
            num_total += 1

    score = sum_score/num_total
    return score


if __name__ == "__main__":
    if len(sys.argv) != 3:
        input_path = "crawl/data/coindesk.json"
        output_path = "process/processedData/coindesk.jl"
    else:
        input_path = sys.argv[1]
        output_path = sys.argv[2]

    generateJSONLD(input_path, output_path)