# # Read the file and store the links in a list
# with open('links_duplicates.txt', 'r') as file:
#     links = file.readlines()

# # Remove duplicate links
# links = list(set(links))

# # Write the unique links back to the file
# with open('links_duplicates.txt', 'w') as file:
#     file.writelines(links)


# get every link attribute of each row from the sentiment.db sqlite database and save it to a text file 

# import sqlite3

# conn = sqlite3.connect('sentiment.db')
# c = conn.cursor()

# c.execute("SELECT link FROM sentiment")
# links = c.fetchall()

# with open('unique_links.txt', 'w') as file:
#     for link in links:
#         file.write(link[0] + '\n')

# conn.close()


# EXTRAHIERE JEDEN SATZ AUS DEM TEXT
# import nltk
# from nltk.tokenize import sent_tokenize

# text = """(Adds details on background in paragraphs 2-5)
# Dec 6 (Reuters) - Medical tools supplier Danaher said on Wednesday it has completed the $5.7 billion acquisition of Abcam, overcoming the initial opposition from the founder of the protein consumables maker.
# Danaher agreed to buy Abcam in September for $24 per share to expand its portfolio of products and services, but founder Jonathan Milner opposed it saying the offer undervalued the company.
# Milner, who owns a 6.14% stake, had said he would vote against the acquisition. But he later suspended his campaign after talks with shareholders, who said the company was fairly valued.
# Abcam's shareholder voted in favour of the deal in November. Milner served as Abcam's CEO from 1999 to 2014 and later as deputy chairman from 2015 to 2020.
# Cambridge, England-based Abcam manufactures and supplies so-called protein consumables such as antibodies and reagents used for medical research. (Reporting by Khushi Mandowara in Bengaluru; Editing by Saumyadeb Chakrabarty and Arun Koyyur)
# """

# # Lade den Punkt-Trenner
# nltk.download('punkt')

# def split_into_sentences(text):
#     return sent_tokenize(text)


# print(split_into_sentences(text))


# import nltk.data

# tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

# # Füge Abkürzungen hinzu, die nicht als Satzenden behandelt werden sollen
# abbreviations = ['no', 'dr', 'vs', 'mr', 'mrs', 'prof', 'inc']
# for abbr in abbreviations:
#     tokenizer._params.abbrev_types.add(abbr)

# def custom_sentence_tokenize(text):
#     return tokenizer.tokenize(text)

# text = "This is a sentence. No. 1 is an example. This is another sentence."
# sentences = custom_sentence_tokenize(text)
# print(sentences)

import sqlite3

# Connect to your SQLite database
conn = sqlite3.connect('sentiment.db')

# SQL query to select only desired columns
query = 'SELECT sentence_text, final_sentiment FROM sentences WHERE final_sentiment != "manual"'

# Execute the query and fetch all data
cursor = conn.cursor()
cursor.execute(query)
rows = cursor.fetchall()

import json

# Convert to a list of dictionaries (assuming column names: text, label) and convert label bullish to 0 neutral to 1 and bearish to 2
data = [{'text': row[0], 'label': 0 if row[1] == 'bullish' else 1 if row[1] == 'neutral' else 2} for row in rows]

# Convert the list of dictionaries to a JSON string
json_data = json.dumps(data, indent=4)  # 'indent' for pretty-printing

# Write the JSON data to a file
with open('output.json', 'w') as json_file:
    json_file.write(json_data)

# Close the connection to the database
conn.close()
