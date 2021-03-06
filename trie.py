from document import *
from dataclasses import dataclass, field

TERMINATOR: str = '^'


@dataclass
class TrieNode:
    """A node in a standard trie."""
    children: dict = field(default_factory=dict)


@dataclass
class Trie:
    """A standard trie."""
    _root: TrieNode = field(default_factory=TrieNode)

    def add_doc(self, doc: Document) -> None:
        """Adds words from doc to the trie.

        Args:
        - self: this trie, the one to add to. mandatory object reference.
        - doc: the document whose words are to be added.

        Returns:
        None.
        """
        for w, locs in doc.words():
            add_word(self._root, trie_preprocess(w), locs)

    def complete(self, words: str) -> [(str, [Location])]:
        """Returns prefix-matches in the trie to each of the words and their locations
        in their documents.

        Args:
        - self: this trie, the one to match in . mandatory object reference.
        - words: contains words to match

        Returns:
        A list of pairs where each pair contains a prefix-matched word from the
        trie and a list of the locations where the word occurs in documents.
        """
        words = prefix_tokenize(words)
        matches = []
        for w in words:
            matches.extend(match(self._root, w, w))
        return matches


# ------------------------- Helpers -------------------------

def trie_preprocess(word: str) -> str:
    """Returns a processed version of word appropriate for adding to the trie.

    Implement as you wish. The default version returns word as is .

    Args:
    - word: the word to process.

    Returns:
    An appropriately processed version of word.
    """
    return word


def prefix_tokenize(prefix_string: str):
    """Returns a list of prefixes tokenized from prefix_string and appropriate
    for prefix matching in the trie.

    Implement as you wish. The default splits at whitespace.

    Args:
    - prefix_string: the string to tokenize.

    Returns:
    A list of prefix tokens appropriate for querying the index.
    """
    return prefix_string.split()


def add_word(node: TrieNode, word: str, locs: [Location]) -> None:
    """Adds word as a path beginning at node and saves the document locations of
    words.

    Args:
    - node: the addition has to start at node
    - word: the word to add
    - locs: the locations where word appears in different documents

    Returns:
    None.
    """
    pass


def match(node: TrieNode, prefix: str, trace: str) -> [(str, [Location])]:
    """Returns prefix-matching words starting at node and the document locations
    where the words occur.

    Prefix-matching is performed by tracing down the tree rooted at node. trace
    keeps track of the string remaining to be traced. When this function is
    called the first time, i.e. not recurcsively, prefix and trace MUST be the
    same.

    Args:
    - node: start prefix-matching at node.
    - prefix: the prefix to be matched.
    - trace: string to trace at node, MUST be == prefix at first call

    Returns:
    List of pairs where each pair contains a prefix-matched word and the
    locations where the word appears.
    """
    pass
