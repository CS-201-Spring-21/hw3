from dataclasses import dataclass
import pathlib


@dataclass
class Location:
    """The location of a word in a document."""
    doc_id: str
    start: int
    stop: int


class Document:
    """A document in a corpus. It allows to access the contained words with stop
    words and punctuation filterd out."""

    def __init__(self, path: str):
        """Creates the document.

        Args:
        - self: this document, the one to create.
        - path: path in the file system to the file which contains the document.

        Returns:
        None.
        """
        # Extract ID from path.
        path = pathlib.Path(path)
        self.doc_id = path.stem
        # Tokenize the content, replacing Unicode characters with '?'
        content = path.read_text(encoding='UTF-8', errors='replace')
        self._words = document_tokenize(content)

    def words(self) -> [(str, [Location])]:
        """Returns words along with their locations in the document.

        Args:
        - self: words of this document are sought, mandatory object reference.

        Returns:
        list of pairs where each pair contains a unique word in the document
        and the locations where it appears.
        """
        words = []
        for word, locs in self._words.items():
            locs = [Location(self.doc_id, start, stop) for start, stop in locs]
            words.append((word, locs))
        return words

# ------------------------- Helpers -------------------------


def document_tokenize(content: str) -> {str: [(int, int)]}:
    """Returns tokens from content in the form of words and the (start, stop)
    indexes in content.

    content is usually the entire content of a document but can also be any
    arbitrary string. (start, stop) indexes follow python slicing convention.

    Args:
    - content: the string to tokenize

    Returns:
    A dictionary in which each key is a unique token from content and the value
    is a list of (start, stop) indexes in content where the word appears.
    """
    # Extract ID from path and read the content.
    i = 0
    words = dict()
    while content[i:]:
        # Ignore non-letters
        if not content[i].isalpha():
            i += 1
            continue
        # A word stops at a space.
        start = i
        stop = content.find(' ', i)
        if stop == -1:
            stop = len(content)
        word = content[start:stop]
        # Save index bounds of word, proceed with the remaining content.
        words[word] = words.get(word, []) + [(start, stop)]
        i = stop + 1
    return words
