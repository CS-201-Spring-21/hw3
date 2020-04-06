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
zipfilename = 'articles.zip'
open(zipfilename, 'wb').write(urlopen(path + zipfilename).read())
zipfile.ZipFile(zipfilename, 'r').extractall()
corpus = Corpus('articles/')
cases = fetch_testcases(path + 'cases.txt')


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


def test_trie():
    '''Tests completion results by comparing them with reference results.

    Performs various checks:
    - The number of completions must match
    - The completions must match
    - For each completion:
    -- The document ID's and their multiplicity must match.
    -- The start & stop indexes within the document must match, with tolerance.
    '''
    # Trie.
    for query, reference in cases:
        result = corpus.complete(query)
        # Same number of completions.
        res, ref = len(result), len(reference)
        assert res == ref, f'For query: {query}, result of length: {res} '\
            f'does not match reference length: {ref}'
        # Same completions.
        result = dict(result)
        reference = dict(reference)
        res, ref = set(result.keys()), set(reference.keys())
        assert res == ref, f'For query: {query}, result completions:\n{res}\n'\
            f'do not match reference completions:\n{ref}'
        # Check result for each completion.
        for word, res_locs in result.items():
            # Sort locations, secondary key: start, promary key: document ID.
            res_locs = sorted(res_locs, key=lambda loc: loc.start)
            res_locs = sorted(res_locs, key=lambda loc: loc.doc_id)
            ref_locs = sorted(reference[word], key=lambda loc: loc.start)
            ref_locs = sorted(ref_locs, key=lambda loc: loc.doc_id)
            for i, locs in enumerate(zip(res_locs, ref_locs)):
                # Same document ID's in the same frequency.
                res_loc, ref_loc = locs
                res, ref = res_loc.doc_id, ref_loc.doc_id
                assert res == ref, f'For {word}, mismatch at postiion {i+1} '\
                    f'between result documents:\n{[l.doc_id for l in res_locs]}\n '\
                    f'and reference documents:\n{[l.doc_id for l in ref_locs]}'
                # Same start and stop, with some tolerance, in each document.
                rs1, rs2 = res_loc.start, res_loc.stop
                rf1, rf2 = ref_loc.start, ref_loc.stop
                assert abs(rf1-rs1) <= 5 and abs(rf2-rs2) <= 5, \
                    f'For {word}, mismatch in boundaries at postiion {i+1} '\
                    f'between result documents:\n{res_locs}\n '\
                    f'and reference documents:\n{ref_locs}'
