## Name and Uni
Yuhan Xia: yx2729

Jing Liu: jl6093

## Files Submitting:
```
bert.py
README.pdf
reqirements.txt
search-engine.py
searchsecrets.py
transcript.txt
```

## How to Run Program:
```shell
# this assumes you are using python3, otherwise use pip and python respectively
pip3 install -r requirements.txt
python3 search-engine.py [Google Custom Search Engine JSON API Key] [Engine ID] 0.9 "Columbia"
```

## Description of Internal Design:
- `requirements.txt` is used for downloading all required packages

- The main file is `search-engine.py`, and all other files used are imported there. It builds the custom search service. It then fetches the inputs from `searchsecrets.py`.

- The `searchsecrets.py` takes in the system inputs like the API key, google engine ID, precision and key word. It also imports the sys library. 

- `search-engine.py` then has a while loop that will keep searching as long as `keepSearching` is true. It also keeps track of the current query with `query`, the list of the individual words in a list `queryList`, and how many iterations `i` have occured. At the beginning, the `query` is given by `searchsecrets.query` and the number of iterations is 0.

- Inside the while loop, an iteration is documented, and the google search is executed with the given query. Then, the parameters are all printed, like the client key, engine key, query, precision, and google search results.

- `res` contains all of the search reults, and there is a for loop `for r in res['items']`, where it iterates through each individual result. It uses `i` to keep track of the result number, `numberRelevant` to count the number of answers relevant, `relevantSnippets` for a list of all relevant snippets, and `relevantWordsSet` for a set of all words that have occured in all of the relevant snippet. 

- For every single `r`, the result number, url, title, and summary are all printed. Then, it waits for a response from the user, and if the user responds with Y, then it increments the `numberRelevant`, appends the summary to the list of `relevantSnippets`, and updates the set `relevantWordsSet`. It uses the `clean_sentence` function to remove weird characters, spaces, and punctuation from a string, and then seperate the phrase into words that are all lowercase.

- Then, it turns `relevantWordsSet` into a list `relevantWords` and calculates the current precision `currentPrecision`. It prints out the general feedback summary like the query and precision, but then uses `currentPrecision` to determine what the next step is. If current precision is equal to or greater than the precision desired by the user, then the program stops and lets the user know. If the precision is 0, it lets the user know that it was 0 and can't proceed. To stop it, `keepSearching` is set to false. 

- However, if it is less than the desired precision, then a the new query list `newQueryList` is calculated using `info_retrieval` from `bert.py`. The inputs are the `relevantSnippets`, `relevantWords`, and `queryList`. The query in our code is represented by both a string and list because `info_retrieval` needs a list of words as an input, and outputs a list of words. Meanwhile, the code has many places where it needs to print the query, so a string type is needed. So, the `newQueryList` is joined together with spaces to become the new `query`. All of the words in `newQueryList` and not in `queryList` (the old query list) are extracted to show the user which words the query is augmented by. `queryList` then becomes `newQueryList`.

- `bert.py` handles the query modification calculations, and is explained below in "Description of Query Modification:"

- `transcript.txt` shows the transcript of the results

## Description of Query Modification:
- Function `info_retrieval` from the `bert.py` file is used to modify search queries. This function takes in a list of related `snippets` that have been marked by people, the `words` associated with those snippets, and the current query list called `old_query`. The output of this function is an updated query list called `new_query`, which has been augmented with additional search terms.

- To compute the augmented query list, we use a state-of-the-art text embedding framework called [SentenceTransformer](https://www.sbert.net/). Specifically, we use pre-trained model `all-MiniLM-L6-v2` to compute embeddings for both the related snippets and the associated words.

- Once we have the embeddings, we compute the cosine similarity between each word and snippet using the framework's `util.cos_sim` function. We then calculate a score for each term, which is the mean similarity with all snippets, and sort the terms in descending order based on their scores.

- Reorder the query in several steps. 
This process results in a new query list that is organized in descending order of word similarity and contains all words from the previous queries.
    - Truncate the `2+len(old_query)` most valuable related words to create a list called `sorted_query`, since the new query list length cannot exceed `2+len(old_query)`. 
    - Select query words that are in the `old_query` but not in the `sorted_query` as a list called `outdated_query`. These words should not be deleted from the new query, but should be given lower priority.
    - Traverse the words in `sorted_query`. If a word is in the `old_query`, we append it to the `new_query`. If not, we append it only when the length of `new_query` has not yet reached `2+len(old_query)-len(outdated_query)` to reserve space for the outdated_query.
    - Finally, add the `outdated_query` to the end of the `new_query`. 
