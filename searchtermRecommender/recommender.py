from pke.unsupervised.graph_based.multipartiterank import MultipartiteRank

from Orange.widgets import widget, gui
from Orange.widgets.utils.signals import Input, Output
from Orange.widgets.utils.widgetpreview import WidgetPreview
from orangewidget.utils.signals import summarize, PartialSummary

from AnyQt.QtCore import Qt
from AnyQt.QtWidgets import QSizePolicy, QGridLayout
from AnyQt.QtCore import QSize

from classes.document_list import DocumentList
from classes.searchterm_list import SearchTermList

class Recommender(widget.OWWidget):
    name = "Recommend search terms"
    description = "Recommends search terms based on input documents"
    icon = "icons/analysis-tool.svg"
    priority=10

    class Inputs:
        documents = Input("Documents", DocumentList, auto_summary=True)

    class Outputs:
        searchterms = Output("Search terms", SearchTermList, auto_summary=True)

    resizing_enabled = False

    alpha = 1.2
    N_idx = 1
    N_values = ["5", "10", "15"]
    N = 10

    documents = None
    chosen_searchterms = None

    def __init__(self):
        super().__init__()

        layout = QGridLayout()
        self.setLayout(layout)

        info_box = gui.widgetBox(
            widget=self.controlArea,
            box="Info"
        )

        self.info_msg = gui.widgetLabel(
            widget=info_box,
            label="0 documents imported"
        )

        options_box = gui.widgetBox(
            widget=self.controlArea,
            box="Options"
        )

        gui.hSlider(
            widget=options_box,
            master=self,
            value="alpha",
            box="Select a value for α",
            minValue=0.8,
            maxValue=1.6,
            step=0.1,
            labelFormat="α=%.1f",
            ticks=True,
            intOnly=False
        )
        gui.radioButtonsInBox(
            widget=options_box,
            master=self,
            value="N_idx",
            btnLabels=self.N_values,
            box="Select the number of search term recommendations",
            callback=self.set_N
        )

        recommend_button = gui.button(
            widget=self.controlArea,
            master=self,
            label="Recommend search terms",
            callback=self.get_recommendations
        )

        layout.addWidget(self.controlArea, 0, 0)
        layout.addWidget(self.mainArea, 1, 0)
        
        # Main area
        self.box = gui.widgetBox(
            widget=self.mainArea,
            box="Recommended search terms"
        )
        self.text = gui.widgetLabel(
            widget=self.mainArea,
            label="0 terms selected",
        )
        select_button = gui.button(
            widget=self.mainArea,
            master=self,
            label="Select",
            callback=self.commit_chosen
        )
        select_button.setAutoDefault(True)
    
    @summarize.register(SearchTermList)
    def summarize_searchterms(searchterms: SearchTermList):
        total = sum(map(len, [getattr(terms, "terms") for terms in searchterms.terms]))
        details = []
        for terms in searchterms.terms:
            details.append(f"{len(terms.terms)} terms from {terms.source_doc}")
        
        return PartialSummary(
            total,
            f", ".join(details)
        )

    @Inputs.documents
    def set_documents(self, documents):
        if not documents:
            self.documents = None
        else:
            self.documents = documents

            if len(self.documents.docs) == 1:
                info = "1 document imported"
            else:
                info = f"{len(self.documents.docs)} documents imported"
            self.info_msg.setText(info)
            self.addListBoxes()

    def addListBoxes(self):
        fnames = [getattr(doc, "fname") for doc in self.documents.docs]
        for fname in fnames:
            stem = fname.split(".")[0]
            if not stem + "_box" in self.__dict__.keys():
                setattr(self, stem + "_recommendations", [])
                setattr(self, stem + "_chosen", [])    
                box = gui.listBox(
                    widget=self.box,
                    master=self,
                    value=stem + "_chosen",
                    labels=stem + "_recommendations",
                    box=fname,
                    selectionMode=2, # 2=multiple selection
                    sizeHint=QSize(300, 150)
                )
                setattr(self, stem + "_box", box)                

    def set_N(self):
        self.N = int(self.N_values[self.N_idx])

    def get_recommendations(self):
        extractor = MultipartiteRank()
        for doc in self.documents.docs:
            extractor.load_document(doc.raw_text)
            extractor.candidate_selection()
            extractor.candidate_weighting(alpha=self.alpha)
            recommendations = [kp for kp, _ in extractor.get_n_best(n=self.N)]
            
            stem = doc.fname.split(".")[0]
            setattr(self, stem + "_recommendations", recommendations)
            setattr(self, stem + "_chosen", [])        


    def commit_chosen(self):
        fnames = [getattr(doc, "fname") for doc in self.documents.docs]
        chosen_terms = []
        for fname in fnames:
            stem = fname.split(".")[0]
            chosen = set()
            recommendations = getattr(self, stem + "_recommendations")
            chosen_idxs = getattr(self, stem + "_chosen")
            for idx in chosen_idxs:
                chosen.add(recommendations[idx])
            chosen_terms.append(chosen)

        self.text.setText(f"{sum(map(len, chosen_terms))} terms selected")
        self.chosen_seachterms = SearchTermList(fnames, chosen_terms)
        self.Outputs.searchterms.send(self.chosen_seachterms)

if __name__=="__main__":
    with open("/Users/liane/Desktop/example_papers/paper1.txt", "r") as f:
        documents = {"paper1.txt": f.read()}
        WidgetPreview(Recommender).run(documents)