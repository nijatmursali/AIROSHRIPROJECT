import nltk
#from nltk import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import state_union
from nltk.tokenize import PunktSentenceTokenizer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet

import spacy

def allaboutNLTK():
    #tokenizing - word tokenizers... sentence tokenizers
    # lexicon and corporas
    #corpora - body of text. ex: medical journals, english language
    # lexicon - words and their means

    our_list = "This is so damn big sentence and you have to say what you want to do with it."

    stop_words = set(stopwords.words("english"))
    words = word_tokenize(our_list)

    filtered_sentence = []

    for w in words:
        if w not in stop_words:
            filtered_sentence.append(w)
    #print(filtered_sentence)
    #print(sent_tokenize(our_list))
    #print(word_tokenize(our_list))

    #stemming - bringing the word in to initial root form
    #I was taking a ride in the car.
    #I was riding in the car.
    ps = PorterStemmer()

    example_words = ["pythoner","python","pythoning","pythoned","pythonly"]

    # for w in example_words:
    #     print(ps.stem(w))

    new_text = "It is very important to be pythonly while you are pythoning with python. All pythoners love pythoning."

    words = word_tokenize(new_text)

    # for w in words:
    #     print(ps.stem(w))

    #POST - PART OF SPEECH TAGGING
    trained_text = state_union.raw("2005-GWBush.txt")
    sample_text = "What do we need to do today?"
    custom_sent_tokenizer = PunktSentenceTokenizer(trained_text)

    tokenized = custom_sent_tokenizer.tokenize(sample_text)

    return tokenized

def process_content():
    tokenized = allaboutNLTK()
    try:
        for i in tokenized[5:]:
            words = nltk.word_tokenize(i)
            tagged = nltk.pos_tag(words)

            #chunkGram = r"""Chunk: {<RB.?>*<VB.?>*<NNP>+<NN>?}"""
            chunkGram = r"""Chunk: {<.*>+}"""
            chunkParser = nltk.RegexpParser(chunkGram)
            chunked = chunkParser.parse(tagged)

            #chunked.draw()

            #NAMED ENTITY
            #namedEnt = nltk.ne_chunk(tagged, binary = True)
            #namedEnt.draw()

            #LEMMATIZATION -
        lemmatizer = WordNetLemmatizer()

        print(lemmatizer.lemmatize("doing"))

    except Exception as e:
        print(str(e))



def nlpthing():
    nlp = spacy.load('en_core_web_sm')
    doc = nlp("This is just for testing purposes.")




#allaboutNLTK()
#process_content()