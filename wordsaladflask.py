import wordsalad
from flask import Flask

App = Flask(__name__)

@App.route("salad/<int:n>/<string:corpus>")
def _get(self, n, corpus="default"):
    """Generate n word salads from the given (optional) corpus."""
    pass

@App.route("salad/corpuses")
def _get_corpuses(self):
    """Fetch a list of "corpus:es" we can use as a source text.
    
    Returns the list as a JSON-list of strings."""
    pass
