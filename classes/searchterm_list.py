from collections import namedtuple

class SearchTermList:
    def __init__(self, fnames: list, chosen_kws: list):
        assert(len(fnames) == len(chosen_kws))
        self.terms = []
        SearchTerms = namedtuple("SearchTerms", ["source_doc", "terms"])
        for fname, chosen in zip(fnames, chosen_kws):
            self.terms.append(SearchTerms(fname, chosen))


if __name__=='__main__':
    source_docs = ["paper1.txt", "paper2.txt"]
    chosen = [{"hello", "world"}, {"good", "morning"}]
    
    my_terms = SearchTermList(source_docs, chosen)

    for terms in my_terms.terms:
        print(terms.source_doc, terms.terms)