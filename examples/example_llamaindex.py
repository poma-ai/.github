#!/usr/bin/env python3
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

from poma import Poma
from poma.integrations.llamaindex_poma import (
    PomaFileReader,
    PomaChunksetNodeParser,
    PomaCheatsheetRetrieverLI,
)
import faiss
from llama_index.vector_stores.faiss import FaissVectorStore
from llama_index.core import Settings, StorageContext, VectorStoreIndex
from langchain_openai import OpenAIEmbeddings as LcOpenAIEmbeddings
from llama_index.embeddings.langchain import LangchainEmbedding


load_dotenv()
for key in ("OPENAI_API_KEY", "POMA_API_KEY"):
    if not os.getenv(key):
        raise SystemExit(f"Set {key} as env-var or in a .env file")


client = Poma(os.environ.get("POMA_API_KEY"))


LOCAL_DIR = Path(__file__).parent
LLM_MODEL = "gpt-4o"  # <= or any model your OpenAI key allows


#############
# Ingestion #
#############


INPUT_PATH = LOCAL_DIR / "Coffee.txt"
try:
    print("Starting ingestion…")
    docs = PomaFileReader().load_data(str(INPUT_PATH))
    parser = PomaChunksetNodeParser(client=client)
    chunkset_nodes = parser._get_nodes_from_documents(docs, True)
    print("\nCreating vector store...")
    embed_model = LangchainEmbedding(LcOpenAIEmbeddings(model="text-embedding-3-large"))
    embed_dimension = len(
        embed_model._langchain_embedding.embed_query("detect vector dimension")
    )
    faiss_index = faiss.IndexFlatL2(embed_dimension)
    vector_store = FaissVectorStore(faiss_index=faiss_index)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    Settings.embed_model = embed_model
    index = VectorStoreIndex(chunkset_nodes, storage_context=storage_context)
    print("Vector index created successfully!")
    storage_context.persist(LOCAL_DIR / "faiss_index_llama")
    print("Persist chunkset_docs in Vector store!")
except Exception as exc:
    print(f"\nError during ingestion: {exc}")
    sys.exit(1)


#############
# Retrieval #
#############

try:
    print("\nStarting retrieval...")
    base_retriever = index.as_retriever(similarity_top_k=3)
    cheat_retriever = PomaCheatsheetRetrieverLI(base_retriever)
    qe = cheat_retriever.as_query_engine()
    query = "Which are the three countries with the highest coffee consumption?"
    print(f"Query: {query}")
    print(f"\nResponse:\n{qe.query(query)}")
except Exception as exception:
    print(f"\nError during retrieval: {exception}")
    sys.exit(1)
