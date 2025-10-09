#!/usr/bin/env python3
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

from poma import Poma
from poma.integrations.langchain_poma import (
    PomaFileLoader,
    PomaChunksetSplitter,
    PomaCheatsheetRetrieverLC,
)
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser


load_dotenv()
for key in ("OPENAI_API_KEY", "POMA_API_KEY"):
    if not os.getenv(key):
        raise SystemExit(f"Set {key} as env-var or in a .env file")


client = Poma(os.environ.get("POMA_API_KEY"))


LOCAL_DIR = Path(__file__).parent
INDEX_DIR = LOCAL_DIR / "faiss_index_lang"
LLM_MODEL = "gpt-4o"  # <= or any model your OpenAI key allows


#############
# Ingestion #
#############


INPUT_PATH = LOCAL_DIR / "Coffee.txt"
try:
    print("Starting ingestion...")
    doc = PomaFileLoader(INPUT_PATH).load()
    chunkset_docs = PomaChunksetSplitter(client=client, verbose=True).split_documents(
        doc
    )
    print("\nCreating vector store...")
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    vector_store = FAISS.from_documents(documents=chunkset_docs, embedding=embeddings)
    print("Vector store created successfully!")
    vector_store.save_local(str(INDEX_DIR))
    print("Persist chunkset_docs in vector store!")
    try:
        embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
        vector_store = FAISS.load_local(
            folder_path=str(INDEX_DIR),
            embeddings=embeddings,
            allow_dangerous_deserialization=True,
        )
        print(f"Loaded existing vector store from: {INDEX_DIR}")
    except Exception as e:
        print(f"Found {INDEX_DIR} but failed to load it; will rebuild. Reason: {e}")
except Exception as exception:
    print(f"\nError during ingestion: {exception}")
    sys.exit(1)


#############
# Retrieval #
#############

try:
    print("\nStarting retrieval...")
    retriever = PomaCheatsheetRetrieverLC(vector_store, top_k=3)
    llm = ChatOpenAI(model=LLM_MODEL)
    prompt = PromptTemplate.from_template(
        "Use the following context to answer the question.\n\n{context}\n\nQuestion: {question}"
    )
    qa_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    query = "Which are the three countries with the highest coffee consumption?"
    print(f"Query: {query}")
    print(f"\nResponse:\n{qa_chain.invoke(query)}")
except Exception as exception:
    print(f"\nError during retrieval: {exception}")
    sys.exit(1)
