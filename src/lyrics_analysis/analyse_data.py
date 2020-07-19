from collections import Counter
import itertools
import pandas as pd

def n_most_common(df, column, n=10):
    
    all_tokens = df[column].tolist()
    all_tokens = list(itertools.chain(*all_tokens))

    word_counts_lyrics = Counter(all_tokens)

    topnterms = pd.DataFrame(word_counts_lyrics.most_common(n),
                             columns=['tokens', 'count'])
    return topnterms