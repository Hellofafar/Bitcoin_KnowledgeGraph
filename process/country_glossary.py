import json

dict_country = {}
list_country = []

with open("allCountryNames.txt", 'r') as reader:
    countries = reader.readlines()
    for c in countries:
        names = c.split('\t')
        id = names[0]
        list_country.append(id)
        for n in names:
            n = n.strip()
            dict_country[n] = id

    
with open("process/processedData/country_glossary.json", 'w') as writer:
    res = json.dumps(dict_country)
    writer.write(res)