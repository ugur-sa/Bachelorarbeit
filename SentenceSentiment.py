from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch

# ProsusAI/finbert
# mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis
# Sigma/financial-sentiment-analysis
model_name = "ProsusAI/finbert"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

# get each row from senteces table in sentiment.db sqlite

import sqlite3

conn = sqlite3.connect("sentiment.db")
c = conn.cursor()

c.execute("SELECT * FROM sentences WHERE finbert_result != 'bullish'")
rows = c.fetchall()

for row in rows:
    id = row[0]
    sentence_text = row[2]

    inputs = tokenizer(sentence_text, return_tensors="pt", padding=True, truncation=True, max_length=512)

    # Wende das Modell an
    with torch.no_grad():
        outputs = model(**inputs)

    # Hole die Modellvorhersagen
    predictions = outputs.logits

    # Konvertiere Vorhersagen in Wahrscheinlichkeiten und hole das maximale
    predictions = torch.nn.functional.softmax(predictions, dim=1)
    predicted_class = torch.argmax(predictions).item()

    # behalte die Wahrscheinlichkeit für die Vorhersage
    predicted_probability = predictions.flatten()[predicted_class].item()

    # CLASSES ARE DIFFERENT FOR FINBERT
    classesFINBERT = ["bullish", "bearish", "neutral"]
    classes = ["bearish", "neutral", "bullish"]
    # print(f"Class: {classesFINBERT[predicted_class]}, Probability: {predicted_probability:.3f}")

    # update _result and _score column for each model but only take 3 decimals for _score
    c.execute("UPDATE sentences SET finbert_result = ?, finbert_score = ? WHERE id = ?", (classesFINBERT[predicted_class], round(predicted_probability, 3), id))
    if(id % 100 == 0):
        print(id)

conn.commit()
conn.close()