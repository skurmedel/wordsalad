import wordsalad
import wordsalad.input
import wordsalad.utils
import json
import logging
from flask import Flask

salads = {}
app = Flask(__name__)

@app.route("/salad/<int:n>/<string:corpus>")
def get(n, corpus):
    """Generate n word salads from the given (optional) corpus."""
    app.logger.debug("Call to get with n=%d corpus='%s'.", n, corpus)
    
    if corpus not in salads:
        return "404"
    mat, starts = salads[corpus]
    res = [list(k) for k in wordsalad.generate_sentences(mat, n, starts, stops=list(".?!"))]
    return " ".join([wordsalad.utils.join_germanic(k) for k in res])

@app.route("/salad/corpora")
def get_corpora():
    """Fetch a list of "corpora" we can use as a source text."""
    app.logger.debug("Call to get_corpora.")
    return json.dumps(app.config["corpora"])

DEFAULT_CONFIG_PATH="config.json"

def buildSalads(config):
    for corpus in config["corpora"]:
        txt = ""
        with open(corpus["filename"], encoding="utf-8") as f:
            txt = f.read()
        
        starts = []
        words = wordsalad.input.split_germanic(txt, start_words=starts)
        
        builder = wordsalad.WordSaladMatrixBuilder()
        builder.count_followers_in_sequence(words)

        salads[corpus["name"]] = (builder.build_matrix(), starts)

def loadConfig(path):
    app.logger.info("Loading config from '%s'.", path)
    with open(path, "r", encoding="utf-8") as f:
        config = json.load(f)
        return config

def main():
    config = loadConfig(DEFAULT_CONFIG_PATH)
    buildSalads(config)
    app.config.update(config)
    app.run()

if __name__ == '__main__':
    main()