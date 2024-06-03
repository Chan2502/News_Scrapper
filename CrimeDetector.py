import os
from dotenv import load_dotenv
import newspaper
from gensim.models import Word2Vec
from nltk.corpus import wordnet
import nltk
from nltk.corpus import brown


load_dotenv()

nltk.download('brown')
nltk.download('punkt')

sentences = brown.sents()
model = Word2Vec(sentences, vector_size=100, window=5, min_count=2, workers=4)
model.train(sentences, total_examples=len(sentences), epochs=10)

keywords = ["crime", "illegal activity", "unlawful behavior", "wrongdoing", "offense",
            "criminal", "lawbreaker", "offender", "perpetrator", "felon", "delinquent", "convict",
            "theft", "stealing", "robbery", "burglary", "larceny", "shoplifting",
            "murder", "killing", "homicide", "assassination", "manslaughter",
            "assault", "attack", "battery", "violence", "aggression", "abuse",
            "fraud", "deception", "scam", "swindle", "embezzlement", "forgery",
            "drug", "trafficking", "drug dealing", "narcotics trade", "smuggling",
            "arson", "fire-raising", "incendiarism", "arsonist",
            "kidnapping", "abduction", "hostage-taking",
            "cybercrime", "online crime", "computer crime", "hacking", "phishing",
            "bribery", "corruption", "graft", "kickback", "bribe",
            "forgery", "counterfeiting", "falsification", "imitation", "fabrication",
            "extortion", "blackmail", "coercion", "shakedown", "ransom",
            "vandalism", "destruction", "damage", "defacement", "sabotage",
            "money laundering", "illegal money conversion", "financial crime", "laundering",
            "terrorism", "extremist violence", "terrorist activity", "radicalism",
            "assault", "battery", "attack", "violence", "aggression",
            "robbery", "theft", "burglary", "hold-up", "mugging",
            "carjacking", "vehicle theft", "hijacking", "auto theft",
            "embezzlement", "theft", "misappropriation", "fraud", "stealing"]


def get_similar_words(keyword, model):
    similar_words = set()

    try:
        similar_words.update(
            [word for word, _ in model.wv.most_similar(keyword, topn=5)])
    except KeyError:
        pass

  
    for syn in wordnet.synsets(keyword):
        for lemma in syn.lemmas():
            similar_words.add(lemma.name())

    return similar_words



additional_keywords = set(keywords)
for keyword in keywords:
    additional_keywords.update(get_similar_words(keyword, model))

# Print all the keywords including the original and additional synonyms and similar words
print("All Keywords:")
print(", ".join(additional_keywords))


def scrape_news(place_name):
    # Scrape news articles from CNN based on the specified location
    cnn_paper = newspaper.build('http://cnn.com', memoize_articles=False)
    relevant_articles = []

    for article in cnn_paper.articles:
        try:
            article.download()
            article.parse()
            article.nlp()
            if place_name.lower() in article.text.lower() and any(keyword in article.text.lower() for keyword in additional_keywords):
                relevant_articles.append(article)
        except Exception as e:
            print(f"Error processing article: {e}")

    return relevant_articles


def estimate_crime_rate(place_name):
    relevant_articles = scrape_news(place_name)
    total_articles = len(relevant_articles)
    total_crime_keywords = sum(count_crime_keywords(
        article.text) for article in relevant_articles)

    if total_articles == 0:
        print("No relevant articles found.")
        return
    crime_rate = total_crime_keywords / total_articles
    print(f"Estimated crime rate in {place_name}: {crime_rate}")


def count_crime_keywords(text):
    count = 0
    for keyword in additional_keywords:
        if keyword in text.lower():
            count += 1
    return count



place_name = input("Enter the name of the place: ")
estimate_crime_rate(place_name)