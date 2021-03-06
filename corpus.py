from document import *
from trie import *
from index import *


class Corpus:
    """A corpus of documents that supports:

    - search: given a query, return a list of contained documents ranked by
      relevance
    - compelte: given a query, return prefix-matched words from the corpus
    """

    def __init__(self, path):
        """ Creates the corpus from *.txt files under path.

        Args:
        - self: the corpus to create, mandatory object reference
        - path: the documents to add are under path as *.txt files

        Returns:
        nothing.
        """
        # The structures that will support the main functionalities.
        self._index = Index()
        self._trie = Trie()
        # Initialize the structures with all *.txt files under path.
        path = pathlib.Path(path)
        for i, doc in enumerate(sorted(path.rglob("*.txt"))):
            if i % 500 == 0:
                print(f'Building Corpus: Read {i:5} documents.')
            doc = Document(doc)
            self._index.add_doc(doc)
            self._trie.add_doc(doc)
        print(f'Built corpus from {i} documents.')

    def search(self, query: str) -> [(str, float)]:
        """Returns a list of the top 100 contained documents ranked by relevance to
        query.

        Each pair in the returned list contains a document ID and the matching
        score of the corresponding document to the query.

        Args:
        - self: mandatory object reference.
        - query: documents are to be sorted according to relevance to query.

        Returns:
        a list of the top 100 (document id, matching score) pairs sorted by
        matching score.
        """
        # Delegete the search to the inverted index.
        return self._index.query(query)

    def complete(self, query: str) -> [(str, Location)]:
        """Returns a list of words from the corpus that prefix-match the words
        in query.

        Each pair in the retruned list contains a word and a Location where the
        word can be found.

        Args:
        - self: mandatory object reference.
        - query: documents are to be sorted according to relevance to query.

        Returns:
        a list of (word, Location) pairs in arbitrary order.
        """
        # Delegete the search to the trie.
        return self._trie.complete(query)
