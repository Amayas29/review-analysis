import unidecode
import nltk
from spacy.lang.fr.stop_words import STOP_WORDS
import re
import spacy
from translate import Translator
from langdetect import detect 
import string

# spacy.cli.download("fr_core_news_lg")
nlp = spacy.load("fr_core_news_lg")


def clean_text(text, cat=True):
    text = text.lower()

 
    if cat:
        text = text.replace("\n", " ")
        text = text.replace("\r", " ")
        text = text.replace("\t", " ")
        text = text.replace("\u2028", " ")
        text = text.replace("\x1e", " ")
        text = text.replace("\x1f", " ")
    
        for c in string.punctuation:
            text = text.replace(c, " ")

        text = text.replace("’", " ")

        # Pour garder le mot dé lors la suppression des stop words
        text = re.sub(r"\bdé\b", "dE", text)
        text = re.sub(r"\bdés\b", "dEs", text)

    text = unidecode.unidecode(text)

    text = re.sub(r"\bdE\b", "dé", text)
    text = re.sub(r"\bdEs\b", "dés", text)

    text = ''.join(c for c in text if c.isalpha() or c.isspace())

    return text


def tokenize_text(text):

    tokens = []
    for w in text.split(" "):
        if len(w.strip()) == 0:
            continue
        tokens.append(w)
        
    return tokens


CAT_STOP_WORDS = set(map(clean_text,
                         (set(map(lambda sw: sw.replace("'", ""), STOP_WORDS)) - {"autres", "autre"}).union({"jeu", "jeux", "jouer", "etes", "secret", "collectionner"}))
                     )

DESC_STOP_WORDS = set(map(clean_text, (set(map(lambda sw: sw.replace("'", ""), STOP_WORDS))).union(
    {"jeu", "jeux", "jouer", "etes", "joueur"})))


def remove_stopwords(tokens, stop_words=CAT_STOP_WORDS):
    tokens_sw = [token for token in tokens if token not in stop_words]
    return tokens_sw


# def lemmatize_tokens(tokens):
#     tokens_lem = []

#     for token in tokens:
#         doc = nlp(token)
#         tokens_lem.append(doc[0].lemma_)

#     return tokens_lem

def lemmatize_tokens(tokens):
    docs = list(nlp.pipe(tokens, disable=["parser", "ner"]))
    tokens_lem = [doc[0].lemma_ for doc in docs]
    return tokens_lem


def pos_tagging(tokens):
    doc = nlp(tokens)
    return [(d.text, d.pos_) for d in doc]


translator = Translator(to_lang='fr')

def traduire_phrase(phrase):

    try:
        phrase_lang = detect(phrase)

        if phrase_lang != 'fr' :
            return translator.translate(phrase)

        return phrase
    
    except Exception:
        return phrase