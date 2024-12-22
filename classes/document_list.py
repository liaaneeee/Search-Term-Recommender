import os
from collections import namedtuple

class DocumentList:
    def __init__(self, fpaths: list):
        self.docs = []
        Document = namedtuple("Document", ["fname", "raw_text"])
        for path in fpaths:
            fname = os.path.basename(path)
            with open(path, "r") as f:
                raw_text = f.read()
            self.docs.append(Document(fname, raw_text))


if __name__=='__main__':
    paths = [
        "/Users/liane/Desktop/example_papers/paper1.txt",
        "/Users/liane/Desktop/example_papers/paper2.txt"
        ]
    my_documents = DocumentList(paths)

    for d in my_documents.docs:
        print(d.fname, d.raw_text)