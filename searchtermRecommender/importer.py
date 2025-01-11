from Orange.widgets import widget, gui
from Orange.widgets.utils.signals import Output
from Orange.widgets.utils.widgetpreview import WidgetPreview
from orangewidget.utils.signals import summarize, PartialSummary

from AnyQt.QtCore import Qt
from AnyQt.QtWidgets import QSizePolicy, QFileDialog
from AnyQt.QtGui import QIcon

from classes.document_list import DocumentList


class Importer(widget.OWWidget):
    name = "Import documents"
    description = "Imports one or multiple text files as input for the search term recommender"
    icon = "icons/file.svg"
    priority = 10

    class Outputs:
        documents = Output("Documents", DocumentList, auto_summary=True)

    resizing_enabled = False
    want_main_area = False
    documents = None

    def __init__(self):
        super().__init__()

        layout = self.controlArea.layout()
        box = gui.widgetBox(
            widget=self.controlArea,
            box="Imported documents:"
        )
        self.text = gui.widgetLabel(
            widget=box,
            label=""
        )
        file_button = gui.button(
            widget=self.controlArea, 
            master=self, 
            label="Browse files...", 
            callback=self.browse_file, 
            )
        # file_button.setIcon(QIcon("icons/directory.svg"))
        file_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        layout.addWidget(box)
        layout.addWidget(file_button, alignment=Qt.AlignHCenter)
        
        self.controlArea.setLayout(layout)

    @summarize.register(DocumentList)
    def summarize_documents(documents: DocumentList):
        details = []
        for doc in documents.docs:
            details.append(f"{doc.fname} ({len(doc.raw_text.split())}) words")
            
        return PartialSummary(
            len(documents.docs),
            ", ".join(details)
        )

    def browse_file(self):
        fpaths, _ = QFileDialog.getOpenFileNames(
            None, 
            "Select one or more files to open", 
            "/Users/liane/", # start dir
            "Text files (*.txt)"
            )
        self.import_files(fpaths)

    def import_files(self, fpaths):
        self.documents = DocumentList(fpaths)
        self.set_info()
        self.Outputs.documents.send(self.documents)

    def set_info(self):
        fnames = [getattr(doc, "fname") for doc in self.documents.docs]
        info = "\n".join(fnames)
        self.text.setText(info)

                 
if __name__ == "__main__":
    WidgetPreview(Importer).run()