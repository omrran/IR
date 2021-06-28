import math
import re, vectorMath
from tkinter import *
import ast

from nltk import WordNetLemmatizer
from nltk.stem import PorterStemmer

import processing

# print(vectorMath.inner_product([2, -3], [1, 4]))
# print(vectorMath.length_vector([1, 4]))

# print(vectorMath.angle_between_two_vector([2, 3, 5], [0, 0, 2]))
# print(vectorMath.angle_between_two_vector([3, 7, 1], [0, 0, 2]))
# print(math.sin(90))

## building vector model and save it in file result.txt
processing.build_vec_mod()

## read terms that extract from curpus
f3 = open("terms.txt", "r")
saved_terms = f3.read()
f3.close()
saved_terms = list(ast.literal_eval(saved_terms))


def search():
    q = input1.get()
    ## processing the query
    # read stop words
    f = open("stop words.txt", "r")
    content = f.read()
    f.close()
    stop_words = re.findall("\S+", content)

    termsInQuery = []  # this contain all terms in query without stop words
    terms = []  #
    ########################################################################
    # extract dates from query
    dates = re.findall("(0[1-9]|[12]\d|3[01])[/.-]"
                       "(0[1-9]|1[012])"
                       "[/.-](\d{4})", q)
    dates.extend(re.findall("(0[1-9]|[12]\d|3[01])[/.-]"
                            "(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)"
                            "[/.-](\d{4})", q))
    dates.extend(re.findall("(0[1-9]|[12]\d|3[01])[/.-]"
                            "(January|February|March|April|May|June|July|August|September|October|November|December)"
                            "[/.-](\d{4})", q))
    years = re.findall("\d{4}", q)

    # remove dates from string
    q = re.sub("(0[1-9]|[12]\d|3[01])[/.-]"
               "(0[1-9]|1[012])"
               "[/.-](\d{4})", "", q)
    q = re.sub("(0[1-9]|[12]\d|3[01])[/.-]"
               "(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)"
               "[/.-](\d{4})", "", q)
    q = re.sub("(0[1-9]|[12]\d|3[01])[/.-]"
               "(January|February|March|April|May|June|July|August|September|October|November|December)"
               "[/.-](\d{4})", "", q)
    q = re.sub("\d{4}", "", q)
    # convert dates to regular form 01-Mar-2020
    dates = processing.convert_to_regular_date(dates)

    ## processing emails
    # extract emails from string in contentAFile
    emails = re.findall("\w+@\w+[.]\w+", q)
    # remove emails from string
    q = re.sub("\w+@\w+[.]\w+", "", q)

    ## processing phones
    # extract phones from string in contentAFile
    phones = re.findall("(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4} | "
                        "\(\d{3}\)\s *\d{3}[-\.\s]??\d{4} |"
                        "\d{3}[-\.\s]??\d{4})", q)
    # remove phones from string
    q = re.sub("(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4} | "
               "\(\d{3}\)\s *\d{3}[-\.\s]??\d{4} |"
               "\d{3}[-\.\s]??\d{4})", "", q)

    verbs_nounes = processing.filter_verbs_nouns(q)
    verbs = processing.remove_stop_words(verbs_nounes[0], stop_words)
    nounes = processing.remove_stop_words(verbs_nounes[1], stop_words)

    #######################################################################

    lmtzr = WordNetLemmatizer()
    lemmatizedVerbs = []
    for v in verbs:
        lemmatizedVerbs.append(WordNetLemmatizer().lemmatize(v, 'v'))

    verbs = lemmatizedVerbs

    porter = PorterStemmer()
    porteredNouns = []
    for n in nounes:
        porteredNouns.append(porter.stem(n))

    nounes = porteredNouns

    ################################################################
    termsInQuery.extend(verbs)
    termsInQuery.extend(nounes)
    termsInQuery.extend(years)
    termsInQuery.extend(phones)
    termsInQuery.extend(dates)
    termsInQuery.extend(emails)

    diction_query = {}  # dictionary for  terms and its frequencies
    for y in termsInQuery:
        diction_query.update({y: (1 + math.log(termsInQuery.count(y), 10)).__round__(5)})

    # remove duplication from termsInQuery
    tempTerms = []
    for w in termsInQuery:
        if w not in tempTerms:
            tempTerms.append(w)

    termsInQuery = tempTerms
    print(termsInQuery)
    print(diction_query)


    # # Extension of the previous diction in order to contain all terms
    # # and show their repetition within the query
    temp_dic2 = diction_query.copy()
    diction_query.clear()

    for term in saved_terms:
        if term not in temp_dic2.keys():
            diction_query.update({term: 0.0})
        else:
            diction_query.update({term: temp_dic2[term]})
            # diction_query.update({y: 505})

    print("\nssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss")
    # print(diction_query)
    for x, y in diction_query.items():
        print(x," ====> ", y)
    print("after extensionnnnnnnnn ",diction_query["effort"])

    #######################################################################

    output1.delete(0, END)  # reset the output field
    output1.insert(0, q)  # write in output field
    print(q)


root = Tk()
root.title("IR")
root.minsize(600, 150)
lable1 = Label(root, text="inter your query", font=("Arial Bold", 20))
lable1.pack()

input1 = Entry(root, width=75)
input1.pack()

B = Button(root, text="search", font=("Arial Bold", 10), command=search)
B.pack()

output1 = Entry(root, width=50)
output1.pack()

root.mainloop()
