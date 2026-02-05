#!/usr/bin/env python3
import json, sys, re, os
from pathlib import Path
from dotenv import load_dotenv
from poma import Poma


load_dotenv()
POMA_API_KEY = os.getenv("POMA_API_KEY")
if not POMA_API_KEY:
    sys.exit("❌  Set POMA_API_KEY in your shell or .env file!")


client = Poma(POMA_API_KEY)


STORE = Path("store")


#############
# Ingestion #
#############


def ingest(src: str) -> None:
    """Submit a document to be chunked asynchronously and save results."""

    STORE.mkdir(exist_ok=True)

    src_path = Path(src)
    if not src_path.exists():
        sys.exit(f"File not found: {src}")

    try:
        print(f"🪄 Submitting document {src_path.name} for background chunking...")
        start_result = client.start_chunk_file(src_path)
        job_id = start_result.get("job_id")
        if not job_id:
            sys.exit("❌ Failed to receive job ID from server.")

        print(f"⏳ Job {job_id} started. Polling for results...")
        result = client.get_chunk_result(job_id, show_progress=True) # download_dir=STORE
        chunks, chunksets = result.get("chunks", []), result.get("chunksets", [])
        print(f"✅ Processed {len(chunks)} chunks and {len(chunksets)} chunksets.")

        filename = STORE / f"{src_path.name}.json"
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "w", encoding="utf-8") as f:
            json.dump({"chunks": chunks, "chunksets": chunksets}, f)
        print(f"✅ Saved to {filename}")

        print("\n📊 Document Structure Overview:")
        print(f"  • Document: {src_path.name}")
        print(f"  • Chunks: {len(chunks)}")
        print(f"  • Chunksets: {len(chunksets)}")
        print("  • Ready for retrieval with 'python example.py retrieve <query>'")

    except Exception as exception:
        sys.exit(f"Error processing document: {exception}")


#############
# Retrieval #
#############


def _tokenize(text: str) -> list[str]:
    """Simple tokenization for keyword matching."""
    return re.findall(r"[\w']+", text.lower())


def retrieve(query: str, top_k: int = 2) -> None:
    """Find relevant chunksets and generate a query-specific cheatsheet."""
    if not STORE.exists():
        sys.exit(
            "No store/ directory found. Run 'python example.py ingest <file>' first."
        )

    print(f"🔍 Searching for: '{query}'")

    # Load all document data
    all_data = []
    for doc in STORE.glob("*.json"):
        with open(doc) as file:
            all_data.append((doc.stem, json.load(file)))

    if not all_data:
        sys.exit(
            "No documents found in store. Run 'python example.py ingest <file>' first."
        )

    # Simple keyword matching (replace with vector search in production)
    query_tokens = set(_tokenize(query))
    scored_chunksets = []

    # Score each chunkset based on keyword overlap
    for doc_id, data in all_data:
        chunks, chunksets = data["chunks"], data["chunksets"]
        chunk_by_id = {c["chunk_index"]: c for c in chunks}

        for cs in chunksets:
            # Get text from all chunks in this chunkset
            text = " ".join(
                chunk_by_id[cid]["content"]
                for cid in cs["chunks"]
                if cid in chunk_by_id
            )
            # Score based on keyword overlap
            score = len(query_tokens & set(_tokenize(text)))
            if score > 0:
                scored_chunksets.append((score, doc_id, cs, chunks))

    if not scored_chunksets:
        print("No relevant information found.")
        return

    # Sort results by score
    scored_chunksets.sort(key=lambda x: x[0], reverse=True)

    unique_docs = set(doc_id for _, doc_id, _, _ in scored_chunksets)
    print(
        f"✅ Found {len(scored_chunksets)} relevant chunksets across {len(unique_docs)} documents"
    )

    # Group results by document
    results_by_doc = {}
    doc_chunks_by_id = {doc_id: data["chunks"] for doc_id, data in all_data}

    # Process all documents with relevant results
    for score, doc_id, cs, _ in scored_chunksets:
        if doc_id not in results_by_doc:
            results_by_doc[doc_id] = []
        results_by_doc[doc_id].append((score, cs))

    cheatsheets = []
    # Generate a cheatsheet for each document with hits
    for doc_id, doc_results in results_by_doc.items():
        relevant_chunksets = [cs for _, cs in doc_results]
        # Prepare chunks with document ID as tag
        doc_chunks = doc_chunks_by_id[doc_id]
        for chunk in doc_chunks:
            chunk["tag"] = doc_id
        cheatsheet = client.create_cheatsheet(relevant_chunksets, doc_chunks)
        cheatsheets.append(cheatsheet)

        print(f"\n📚 Cheatsheet for '{query}' from document '{doc_id}'\n{'-'*80}")
        print(cheatsheets)
        print("-" * 80)

    print("These cheatsheets preserve each document's hierarchical structure,")
    print("making them ideal context for LLM prompts.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Usage: python example.py [ingest|retrieve] [file|query]")
    if sys.argv[1] == "ingest":
        if len(sys.argv) < 3:
            sys.exit("Usage: python example.py ingest <file_path>")
        src = sys.argv[2]
        ingest(src)
    elif sys.argv[1] == "retrieve":
        if len(sys.argv) < 3:
            sys.exit("Usage: python example.py retrieve <query-keyword>")
        retrieve(" ".join(sys.argv[2:]))
    else:
        sys.exit("Unknown command. Use 'ingest' or 'retrieve'.")
