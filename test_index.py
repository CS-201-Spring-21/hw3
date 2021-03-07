from urllib.request import urlopen

import pathlib
import zipfile

from corpus import *


def fetch_testcases(path) -> [(str, [(str, [Location])])]:
    '''Returns completion test cases read from path.

    path may be local or online.

    A list of test cases is returned.
    - Each test case is of the form: (query, result)
    - Each result is a list of candidates.
    - Each candidate is of the form: (completion, [Location]).
    '''
    # Read content from path.
    if path.startswith("http"):
        lines = [line.decode('utf-8').strip()
                 for line in urlopen(path).readlines()]
    else:
        lines = [line.strip() for line in open(path).readlines()]
    # Parse for test cases and store.
    itr = iter(lines)
    completions = []
    try:
        while query := next(itr):
            num_results = int(next(itr))
            locs = dict()
            for _ in range(num_results):
                word, doc_id, start, stop = next(itr).split()
                start, stop = int(start), int(stop)
                locs[word] = locs.get(word, []) + \
                    [Location(doc_id, start, stop)]
            completions.append((query, list(locs.items())))
    except StopIteration:
        pass
    return completions


path = 'https://waqarsaleem.github.io/cs201/hw4/'
cases = fetch_testcases(path + 'cases.txt')
# Read and initialize corpus.
zipfilename = 'articles.zip'
open(zipfilename, 'wb').write(urlopen(path + zipfilename).read())
zipfile.ZipFile(zipfilename, 'r').extractall()
corpus = Corpus('articles/', trie=False)


def test_index():
    '''Tests search results through some sanity tests.
    COVID-19: does not check the accuracy of scoring.

    Performs various checks:
    - The result must be sorted by score.
    - The result must contain unique documents.
    - Results must not exceed corpus size.
    - The query term appears in the retrieved document.
    '''
    # Inverted Index.
    corpus_size = len(list(pathlib.Path('./articles/').glob('*.txt')))
    for query in ['Pakistan', 'corona', 'virus', 'distance']:
        result = corpus.search(query)
        if not result:
            continue
        docs, scores = zip(*result)
        # Result is sorted by score.
        assert list(scores) == sorted(scores, reverse=True), \
            f'Obtained search results below are not ranked:\n{result}'
        # Result contains unique documents.
        assert len(docs) == len(set(docs)), \
            f'Obtained search results below are not unique:\n{result}'
        # Sanity check - results do no exceed corpus size.
        assert len(docs) <= corpus_size, \
            f'Obtained search results exceed corpus size:\n{len(result)}'
        # query appears in each result document
        for doc in docs:
            assert query in open(f'articles/{doc}.txt', errors='replace').read(), \
                f'query {query} does not appear in result document {doc}'
