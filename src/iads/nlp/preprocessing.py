import unidecode
import nltk
from spacy.lang.fr.stop_words import STOP_WORDS
import re
import spacy

# spacy.cli.download("fr_core_news_lg")
nlp = spacy.load("fr_core_news_lg")


def clean_text(text, cat=True):
    text = text.lower()

    if cat:
        # Pour le tokenizer des categories
        text = re.sub("['-/\n]", " ", text)

        # Pour garder le mot dé lors la suppression des stop words
        text = re.sub(r"\bdé\b", "dE", text)
        text = re.sub(r"\bdés\b", "dEs", text)

    text = unidecode.unidecode(text)

    text = re.sub(r"\bdE\b", "dé", text)
    text = re.sub(r"\bdEs\b", "dés", text)

    text = ''.join(c for c in text if c.isalpha() or c.isspace())

    return text


def tokenize_text(text):
    tokens = nltk.word_tokenize(text, language='french')
    return tokens


CAT_STOP_WORDS = set(map(clean_text,
                         (set(map(lambda sw: sw.replace("'", ""), STOP_WORDS)) - {"autres", "autre"}).union({"jeu", "jeux", "jouer", "etes", "secret", "collectionner"}))
                     )

DESC_STOP_WORDS = set(map(clean_text, (set(map(lambda sw: sw.replace("'", ""), STOP_WORDS))).union(
    {"jeu", "jeux", "jouer", "etes"})))


def remove_stopwords(tokens, stop_words=CAT_STOP_WORDS):
    tokens_sw = [token for token in tokens if token not in stop_words]
    return tokens_sw


def lemmatize_tokens(tokens):
    tokens_lem = []

    for token in tokens:
        doc = nlp(token)
        tokens_lem.append(doc[0].lemma_)

    return tokens_lem


def pos_tagging(tokens):
    doc = nlp(tokens)
    return [(d.text, d.pos_) for d in doc]
