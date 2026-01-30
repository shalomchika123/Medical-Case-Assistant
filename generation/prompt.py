def build_prompt(question, context):
    return f"""
You are a clinical decision support assistant.
Answer using only the provided patient case context.
If the answer is not present, say you do not have enough information.

Patient Case Context:
{context}

Clinical Question:
{question}
"""