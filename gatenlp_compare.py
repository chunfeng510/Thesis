from IPython.display import display
from gatenlp import Document
# To load a document from a file with the name "file.bdocjs" into gatenlp simply use:
# doc = Document.load("test2a.bdocjs")

# But it is also possible to load from a file that is somewhere on the internet. For this notebook, we use
# an example document that gets loaded from a URL:
doc = Document.load(
    "https://gatenlp.github.io/python-gatenlp/testdocument1.txt")

# We can visualize the document by printing it:
print(doc)

display(doc)
