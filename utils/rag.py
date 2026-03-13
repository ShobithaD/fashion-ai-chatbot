import os
import faiss
import numpy as np

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import CharacterTextSplitter

from models.embeddings import load_embedding_model

embedding_model = load_embedding_model()


def load_documents():   

    folder = "docs"
    all_docs = []

    for file in os.listdir(folder):

        if file.endswith(".pdf"):

            loader = PyPDFLoader(os.path.join(folder,file))
            docs = loader.load()

            all_docs.extend(docs)

    splitter = CharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = splitter.split_documents(all_docs)

    texts = [doc.page_content for doc in chunks]

    embeddings = embedding_model.encode(texts)

    index = faiss.IndexFlatL2(len(embeddings[0]))
    index.add(np.array(embeddings))

    return texts,index


def retrieve_context(query,texts,index):

    query_embedding = embedding_model.encode([query])

    D,I = index.search(query_embedding,3)

    context=""

    for i in I[0]:
        context+=texts[i]+"\n"

    return context