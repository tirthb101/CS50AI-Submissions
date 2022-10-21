from audioop import reverse
from math import log
import nltk
import sys
import os
import string
from nltk.corpus import stopwords

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    dictionary = {}

    for file in os.listdir(os.path.join(os.getcwd(), directory)):
        with open(os.path.join(os.getcwd(), directory, file), "r", encoding="utf-8") as f:
            dictionary[file] = f.read()

    return dictionary


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    stopW = stopwords.words("english")

    list = []

    for x in document.lower().split(" "):
        word = x.strip(string.punctuation)
        if word not in stopW and word != "":
            list.append(word)

    return list


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    NUMOFDOC = len(documents.keys())

    dictionary = {}

    for doc in documents:
        for word in documents[doc]:
            wordOtherDocuments = 0
            for doc in documents:
                if word in documents[doc]:
                    wordOtherDocuments += 1
            dictionary[word] = log(NUMOFDOC/wordOtherDocuments)

    return dictionary


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    scores = {}
    filestoreturn = []
    for file in files:
        score = 0
        for word in query:
            if word in files[file]:
                score += (files[file].count(word) * idfs[word])
        scores[file] = score
        filestoreturn.append(file)
    filestoreturn.sort(key=lambda x: scores[x], reverse=True)

    return filestoreturn[:n]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    scores = {}
    sentenceToReturn = []

    for sentence in sentences:
        score = 0
        queryterms = 0
        for word in query:
            if word in sentences[sentence]:
                queryterms += 1
                score += idfs[word]
        sentenceToReturn.append(sentence)

        scores[sentence] = (queryterms/len(query)) + score

    sentenceToReturn.sort(key=lambda x: scores[x], reverse=True)

    return sentenceToReturn[:n]


if __name__ == "__main__":
    main()
