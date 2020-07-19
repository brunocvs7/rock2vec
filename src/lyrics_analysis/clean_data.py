#Import libs
#Import libs
import spacy
import nltk
from nltk.corpus import words
import gensim 
nlp = spacy.load('pt')
from tqdm import tqdm
from googletrans import Translator
from collections import Counter



def detect_lang_lyrics(df, column):
    lang = []
    trl = Translator()
    for lyrics in tqdm(df[column]):
        try:
            lang.append(trl.detect(lyrics).lang)
        except:
            lang.append('Error')
    df['lang'] = lang
    return df

# Lowercasing
def normalize(df, column, new_name=None):
    if new_name != None:
        df[new_name] = df[column].str.lower()
    else:
        df[column] = df[column].str.lower()
    return df

# Remover StopWords
def tokenize_lemmatize(df, column, new_name=None, remove_stopwords=False, stopwords=None):
    if new_name != None:
        if remove_stopwords==False:
            df[new_name] = df[column].apply(lambda x:' '.join([token.lemma_ for token in nlp(x) if not token.is_punct]))
        else:
            df[new_name] = df[column].apply(lambda x:' '.join([token.lemma_ for token in nlp(x) if not token.is_punct and token.orth_ not in stopwords]))
    else:
        if remove_stopwords==True:
            df[column] = df[column].apply(lambda x:' '.join([token.lemma_ for token in nlp(x) if not token.is_punct and token.orth_ not in stopwords]))
        else:
            df[column] = df[column].apply(lambda x:' '.join([token.lemma_ for token in nlp(x) if not token.is_punct and token.orth_ not in stopwords]))
    return df 



def word_count(tokens):
    word_counts = Counter()
    word_counts.update(tokens)
    return word_counts

