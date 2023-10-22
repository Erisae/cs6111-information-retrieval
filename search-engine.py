import pprint
import searchsecrets
import string
from bert import info_retrieval
from googleapiclient.discovery import build

def clean_sentence(input_string):
    remove_chars = string.punctuation.translate(str.maketrans('', '', '%$@#-'))
    trans_table = str.maketrans('', '', remove_chars)
    no_punct = input_string.translate(trans_table)
    return " ".join(no_punct.lower().split())

def main():
    service = build(
        "customsearch", "v1", developerKey=searchsecrets.google_api_key
    )

    keepSearching = True
    query = searchsecrets.query
    queryList = searchsecrets.query.split(" ")
    searchIterations = 0
    while (keepSearching):
        searchIterations += 1

        # execute Google search
        res = (
            service.cse()
            .list(
                q=query,
                cx=searchsecrets.google_engine_id,
            )
            .execute()
        )

        # print parameters of search
        print("Parameters:")
        print("Client key  = "+searchsecrets.google_api_key)
        print("Engine key  = "+searchsecrets.google_engine_id)
        print("Query       = "+query)
        print("Precision   = "+str(searchsecrets.precision))
        print("Google Search Results:")
        print("======================")

        # iterate through each result
        i = 1
        numberRelevant = 0
        relevantSnippets = []
        relevantWordsSet = set()
        for r in res['items']:

            # print result
            print("Result " + str(i) + "\n[")
            print(" URL: " + r['formattedUrl'])
            print(" Title: " + r['title'])
            print(" Summary: " + r['snippet'])
            print("]\n")

            # save information for processing later
            response = input("Relevant  (Y/N)?")
            if response == "Y":
                numberRelevant += 1
                relevantSnippets.append(r['snippet'])
                currentWords = clean_sentence(r['snippet']).split(' ')
                relevantWordsSet.update(set(currentWords))
            i += 1

        # create general feedback
        relevantWords = list(relevantWordsSet)
        currentPrecision = numberRelevant / len(res['items'])
        print("====================")
        print("FEEDBACK SUMMARY")
        print("Query "+ query)
        print("Precision " + str(currentPrecision))

        # decide if continue
        if currentPrecision >= searchsecrets.precision:
            keepSearching = False
            print("Desired precision reached, done")
        elif currentPrecision == 0:
            keepSearching = False
            print("Precision is 0, cannot proceed")
        else:
            newQueryList = info_retrieval(relevantSnippets, relevantWords, queryList)
            query = " ".join(newQueryList)
            augment = ' '.join([w for w in newQueryList if w not in queryList])
            queryList = newQueryList[:]
            print("Still below the desired precision of "+str(searchsecrets.precision))
            print("Indexing results ....")
            print("Indexing results ....")
            print("Augmented by "+ augment)



if __name__ == "__main__":
    main()
