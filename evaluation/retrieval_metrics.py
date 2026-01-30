def count_sources(documents):
    sources = set(doc.metadata["source"] for doc in documents)
    return len(sources)
