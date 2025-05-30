from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, ID
import csv
import os

schema = Schema(
    id=ID(stored=True, unique=True),
    title=TEXT(stored=True),
    artist=TEXT(stored=True),
    year=TEXT(stored=True),
    rank=TEXT(stored=True),
    lyrics=TEXT(stored=True)
)

if not os.path.exists("search_index"):
    os.mkdir("search_index")

ix = create_in("search_index", schema)
writer = ix.writer()

with open("lyrics.csv", encoding="latin1") as f:
    reader = csv.DictReader(f)
    for i, row in enumerate(reader):
        writer.add_document(
            id=str(i),
            title=row['Song'],
            artist=row['Artist'],
            year=str(row['Year']),
            rank=str(row['Rank']),
            lyrics=row['Lyrics']
        )

writer.commit()
print("Indexing complete.")

