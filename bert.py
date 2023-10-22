from sentence_transformers import SentenceTransformer, util
import torch

# https://www.sbert.net/docs/usage/semantic_textual_similarity.html

model = SentenceTransformer('all-MiniLM-L6-v2')
model.max_seq_length = 200


def info_retrieval(snippets, words, old_query):
    embeddings_s = model.encode(snippets, convert_to_tensor=True)
    embeddings_w = model.encode(words, convert_to_tensor=True)
    cosine_scores = util.cos_sim(embeddings_s, embeddings_w)

    # compute the scores for each term
    term_scores = torch.mean(cosine_scores, axis=0)
    sorted_index = sorted(range(len(term_scores)), key=lambda k: term_scores[k], reverse=True)
    sorted_words = [words[i] for i in sorted_index[:2+len(old_query)]]

    # words in old query but not in the new query
    outdated_query = [q for q in old_query if q not in sorted_words]

    new_query = []
    for q in sorted_words:
        if q in old_query:
            new_query.append(q)
        elif len(new_query) < 2 + len(old_query)-len(outdated_query):
            new_query.append(q)
    new_query += outdated_query

    return new_query




