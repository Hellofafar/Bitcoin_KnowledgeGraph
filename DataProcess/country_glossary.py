import json

country_dict = {}

with open('../country_example.csv', 'r') as reader:
    countries = reader.readlines()
    for c in countries:
        names = c.split(',')
        id = names[0]
        for n in names:
            country_dict[n] = id

    
with open("country_glossary.json", 'w') as writer:
    res = json.dumps(country_dict)
    writer.write(res)