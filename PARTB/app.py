from flask import Flask, request, render_template
from whoosh.index import open_dir
from whoosh.qparser import MultifieldParser

app = Flask(__name__)
ix = open_dir("search_index")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search")
def search():
    query_str = request.args.get("q", "")
    results = []

    if query_str:
        with ix.searcher() as searcher:
            parser = MultifieldParser(["title", "artist", "lyrics"], ix.schema)
            query = parser.parse(query_str)
            hits = searcher.search(query, limit=20)
            hits.fragmenter.charlimit = None  # Disable snippet cutoff
            for hit in hits:
                snippet = hit.highlights("lyrics", top=2)
                results.append({
                    "id": hit["id"],
                    "title": hit["title"],
                    "artist": hit["artist"],
                    "year": hit["year"],
                    "rank": hit["rank"],
                    "snippet": snippet
                })

    return render_template("results.html", query=query_str, results=results)

@app.route("/lyrics/<doc_id>")
def lyrics(doc_id):
    with ix.searcher() as searcher:
        doc = searcher.document(id=doc_id)
        return render_template("lyrics.html", song=doc)

