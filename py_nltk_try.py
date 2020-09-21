from nltk import ngrams

str = "This is @a wonderful@ day"
bigram = ngrams(str.split('@'), 2)

for grams in bigram:
    print(grams)
# print(bigram)
