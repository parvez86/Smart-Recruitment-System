import re, unicodedata
import inflect
import nltk
nltk.download('punkt')
nltk.download('wordnet')
from nltk.stem import LancasterStemmer, WordNetLemmatizer
from stop_words import get_stop_words


def remove_non_ascii(words):
    """Remove non-ASCII characters from list of tokenized words"""
    new_words = []
    for word in words:
        new_word = unicodedata.normalize('NFKD', word).encode('ascii', 'ignore').decode('utf-8', 'ignore')
        new_words.append(new_word)
    return new_words


def to_lowercase(words):
    """Convert all characters to lowercase from list of tokenized words"""
    new_words = []
    for word in words:
        new_word = word.lower()
        new_words.append(new_word)
    return new_words


def remove_punctuation(words):
    """Remove punctuation from list of tokenized words"""
    new_words = []
    for word in words:
        new_word = re.sub(r'[^\w\s]', '', word)
        if new_word != '':
            new_words.append(new_word)
    return new_words


def replace_numbers(words):
    """Replace all interger occurrences in list of tokenized words with textual representation"""
    p = inflect.engine()
    new_words = []
    for word in words:
        if word.isdigit():
            new_word = p.number_to_words(word)
            new_words.append(new_word)
        else:
            new_words.append(word)
    return new_words


def remove_stopwords(words):
    """Remove stop words from list of tokenized words"""
    new_words = []
    stp_words = list(get_stop_words('en'))
    for word in words:
        # print(word)
        if word not in stp_words:
            new_words.append(word)
    return new_words


def get_keywords(words):
    # keywords = open('jobDetails/keywords.txt', 'r').read().replace('\n', '').replace(' ', '').split(',')
    # keywords = open('../jobDetails/normalized_keywords.txt', 'r').read().replace('\n', '').split(' ')

    keywords = open('jobDetails/normalized_keywords.txt', 'r').read().replace('\n', '').split(' ')

    new_words = list()
    for word in words:
        if word in keywords:
            new_words.append(word)

    return new_words


def stem_words(words):
    """Stem words in list of tokenized words"""
    stemmer = LancasterStemmer()
    stems = []
    for word in words:
        stem = stemmer.stem(word)
        stems.append(stem)
    return stems


def lemmatize_verbs(words):
    """Lemmatize verbs in list of tokenized words"""
    lemmatizer = WordNetLemmatizer()
    lemmas = []
    for word in words:
        lemma = lemmatizer.lemmatize(word, pos='v')
        lemmas.append(lemma)
    return lemmas


def normalize(words):
    words = remove_non_ascii(words)
    words = to_lowercase(words)
    words = remove_punctuation(words)
    words = replace_numbers(words)
    words = remove_stopwords(words)
    words = stem_words(words)
    words = lemmatize_verbs(words)
    words = get_keywords(words)
    return words


# for understanding
# print(os.getcwd())
# job_desc = re.sub(' +', ' ', open('../jobDetails/keywords.txt').read())
# print("Job_description: \n", job_desc)
#
# words = nltk.word_tokenize(job_desc)
# print("After tokenization:\n", words)
#
# words = normalize(words)
# words = ' '.join(map(str, words))
# print("\nAfter Normalization: \n", words)
