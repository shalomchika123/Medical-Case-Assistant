def clean_text(documents):
    for doc in documents:
        # Simple cleanup to remove excess newlines from PDF extraction
        doc.page_content = doc.page_content.replace("\n", " ").strip()
    return documents