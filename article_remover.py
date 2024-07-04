import re
import csv

with open('./regex_experiment/regex_experiment2.txt', mode='r') as file:
        
        #csv_reader = csv.DictReader(file)
        #exodus_count_chapters_total = []

        
        for row in file:
            pattern = r'\+(\d+)'
            matches = re.search(pattern, row)
            #row2 = str(row)+",1"
            def article_remover(row):
                row = row.strip()
                #print(row)
                if matches:
                    article_number = matches.group(1)
                    replacement = ""
                    new_text = re.sub(pattern, replacement, row)
                    #print(new_text)
                    if '"' not in new_text:
                        print('"'+str(new_text)+'"'+","+str(article_number))
                    else:
                        print(new_text+","+str(article_number))

                    #print(article_number)
                #print(str(row)+",1")
                #print(new_text)
                #if "+" in row:
                    #print(row)

            article_remover(row)