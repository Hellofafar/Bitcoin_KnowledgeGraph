writer = open("allCountryNames.txt", 'a')

# Extract nationality name of a country
with open("crawl/data/nationality.txt", 'r') as reader0:
    list_nationality = {}
    headline = reader0.readline()
    data = reader0.readlines()
    for line in data:
        try:
            country = line.split('\t')[0]
            nationality = line.split('\t')[1]
            if nationality != "-":
                list_nationality[country] = nationality
        except:
            print(line)
            exit(0)


# Extract usual name, long name, short name and abbreviation of a country name
newCountry = True
# dict_country = {}
with open("crawl/data/countries.txt", 'r') as reader1:
    data = reader1.readlines()
    country = ""
    # i = 0
    for line in data:
        if newCountry:
            country = line.split(':')[0]
            if ',' in country:
                # writer.write('"' + country + '"')
                print(country)
            # dict_country[country] = i
            # i += 1
            writer.write(country)
            newCountry = False

        elif "conventional long form" in line:
            name = line.split(':')[1].strip()
            if name != "none":
                writer.write('\t' + name)

        elif "conventional short form" in line:
            name = line.split(":")[1].strip()
            if name != "none":
                writer.write('\t' + name)
        
        elif "abbreviation" in line:
            name = line.split(":")[1].strip()
            if name != "none":
                writer.write('\t' + name)
        
        elif line == '\n':
            if country in list_nationality:
                writer.write('\t' + list_nationality[country])
            newCountry = True
            writer.write('\n')

        else:
            continue
    
writer.close()