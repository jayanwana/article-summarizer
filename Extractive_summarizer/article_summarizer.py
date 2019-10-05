from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import SnowballStemmer
import re
sb = SnowballStemmer('english')

def extractive_article_summarizer(text_param):

    stop_words = set(stopwords.words('english'))
    text_strip = remove_special_char(text_param)
    words = word_tokenize(text_strip)

    freq_table = {}

    for word in words:
        word = word.lower()
        if word in stop_words:
            continue
        word = sb.stem(word)

        if word in freq_table:
            freq_table[word] += 1
        else:
            freq_table[word] = 1


    sentences = sent_tokenize(text_param)

    sentence_value = {}

    for sentence in sentences:
        sentence = sentence.replace('\n', '')

        for word, freq in freq_table.items():

            if word in sentence.lower():
                if sentence in sentence_value:
                    sentence_value[sentence] += freq

                else:
                    sentence_value[sentence] = freq

    sum_values = 0

    for sentence in sentence_value:
        # print(sentence, sentence_value[sentence])
        sum_values += sentence_value[sentence]

    avg = int(sum_values/len(sentence_value))

    summary = ''
    sentence_length = 100
    for sentence in sentences:
        sentence = sentence.replace('\n', '')
        if (sentence in sentence_value) and (sentence_value[sentence] > (1.2 * avg)):
            if len(sentence) > sentence_length:
                for letter in sentence[sentence_length:]:
                    if letter == ' ':
                        idx = sentence[sentence_length:].index(letter)
                idx += sentence_length
                sentence = sentence[:idx] + '\n' + sentence[idx:]
            summary += sentence + '\n'

    return summary


def remove_special_char(tp):
    stripped = re.sub('[^\w\s\n]', '', tp)
    stripped = re.sub('_', '', stripped)
    stripped = re.sub('\s+', ' ', stripped)
    stripped = stripped.strip()
    return stripped




t = open('test.txt', 'r')

text = t.read()
t.close()

summary = extractive_article_summarizer(text)

file = open('summary.txt', 'w')
file.write(summary)
file.close()

