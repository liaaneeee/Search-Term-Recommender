from Orange.widgets import widget, gui
from Orange.widgets.utils.signals import Input, Output
from Orange.widgets.utils.widgetpreview import WidgetPreview

from AnyQt.QtCore import Qt
from AnyQt.QtWidgets import QSizePolicy

from classes.searchterm_list import SearchTermList

class Displayer(widget.OWWidget):
    name = "Display search terms"
    description = "Display the recommended search terms that were chosen"
    icon = "icons/list.svg"
    priority=10

    class Inputs:
        searchterms = Input("Search terms", SearchTermList, auto_summary=True)

    resizing_enabled = False
    want_control_area = False

    chosen_searchterms = None
    selected = []

    def __init__(self):
        super().__init__()

        layout = self.mainArea.layout()

        self.box = gui.widgetBox(
            widget=self.mainArea,
            box="Search terms"
        )
        refresh_button = gui.button(
            widget=self.mainArea,
            master=self,
            label="Refresh",
            callback=self.display_searchterms
        )
        refresh_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        layout.addWidget(self.box)
        layout.addWidget(refresh_button, alignment=Qt.AlignHCenter)

    @Inputs.searchterms
    def set_searchterms(self, searchterms):
        if not searchterms:
            self.chosen_searchterms = None
        else:
            self.chosen_searchterms = searchterms
            self.add_boxes()

    def add_boxes(self):
        fnames = [getattr(terms, "source_doc") for terms in self.chosen_searchterms.terms]
        for fname in fnames:
            stem = fname.split(".")[0]
            if not stem + "_box" in self.__dict__.keys():
                box = gui.widgetBox(
                    widget=self.box,
                    box=fname
                )
                label = gui.widgetLabel(
                    widget=box,
                    label=""
                )
                setattr(self, stem + "_box", box)
                setattr(self, stem + "_label", label)


    def display_searchterms(self):
        for terms in self.chosen_searchterms.terms:
            stem = terms.source_doc.split(".")[0]
            label = getattr(self, stem + "_label")
            label.setText("\n\n".join(terms.terms))


if __name__=="__main__":
    with open("/Users/liane/Desktop/example_papers/paper1.txt", "r") as f:
        WidgetPreview(Displayer).run({"paper1.txt": {"hello", "there"}, "paper2.txt": {"beautiful", "human"}})