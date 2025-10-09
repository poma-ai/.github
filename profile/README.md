![POMA AI Logo](https://raw.githubusercontent.com/poma-ai/.github/main/assets/POMA_AI_Logo_Pink.svg)


# 📚 POMA: Preserving Optimal Markdown Architecture

Most RAG tools split documents linearly and destroy structure, causing hallucinations, context loss, and token waste. POMA AI solves this by preserving the document's implicit textual structure tree, enabling context-preserving retrieval.

POMA AI is a toolkit for turning unstructured and structured documents — like markdown, HTML, or simple text files (and everything convertable into that, e.g. PDFs) — into structure-preserving “chunksets” for retrieval, resulting in "cheatsheets" as augmentation in Retrieval-Augmented Generation (RAG) with Large Language Models.

**This README covers:**
- Quick-Start Guide 
- Why POMA AI? See Problem Overview
- How POMA AI Works
- Example Implementations
- Detailed POMA AI Pipeline & Workflow Example
- Real-World Performance Example
- FAQ

---

## 💡Key Concepts

### Chunksets: Structure-Preserving Document Paths

A chunkset is a sequence of sentences that preserves the complete hierarchical context from document root to specific details. Unlike traditional linear chunks, chunksets maintain the document's tree structure, ensuring that:
- Headings are never separated from their content
- Lists remain intact with all items
- Hierarchical relationships between sections are preserved
- Context is never lost during retrieval

*Chunksets are the fundamental unit of storage and retrieval in POMA AI, allowing for more accurate and contextually rich information retrieval. See detailed examples below.*

### Cheatsheets: Optimized LLM Context

A cheatsheet is a compact, deduplicated representation of the retrieved information, optimized for LLM consumption. When you retrieve relevant chunksets, POMA AI:
- Collects all chunks from the relevant chunksets
- Deduplicates overlapping content
- Preserves structural relationships
- Formats the information hierarchically

*The resulting cheatsheet provides the LLM with precisely the **context** it needs to answer queries accurately, without wasting tokens on redundant information. See a cheatsheet example below.*

Learn more in How POMA AI Works and Example Implementations.

---

## 🚀Quick-Start Guide

### Installation

Requires Python 3.10+. Install the core packages:
```bash
pip install poma
```

For integrations into LangChain and LlamaIndex:
```bash
pip install poma[integrations]
# Or LangChain/LlamaIndex including example extras:
pip install poma[integration-examples]
```


- You may also want: `pip install python-dotenv` to load API keys from a .env file.
- API keys required (POMA_API_KEY) for the POMA AI client via environment variables.
- **To request a POMA_API_KEY, please contact us at [support@poma-ai.com](mailto:support@poma-ai.com)**


### Example Implementations - all examples -> [examples/](https://github.com/poma-ai/poma/tree/main/examples)

We provide four example implementations to help you get started with POMA AI:
- example.py — A standalone implementation for documents, showing the basic POMA AI workflow with simple keyword-based retrieval
- example_langchain.py — Integration with LangChain, demonstrating how easy it is to use POMA AI with LangChain
- example_llamaindex.py — Integration with LlamaIndex, showing how simple it is to use POMA AI with LlamaIndex

*Note: The integration examples use OpenAI embeddings. Make sure to set your OPENAI_API_KEY environment variable, or replace the embeddings with your preferred ones.*


All examples follow the same two-phase process (ingest → retrieve) but demonstrate different integration options for your RAG pipeline.

---

## 🔗 Quick Links

- [Why POMA AI? (Problem Overview)](#why-poma-ai-problem-overview)
- [How POMA AI Works](#how-poma-ai-works-re-generating-document-structure)
- [Example Implementations](#example-implementations)
- [Detailed POMA AI Pipeline & Workflow Example](#the-poma-processing-pipeline-detailed)
- [Real-World Performance Example](#real-world-performance-example)
- [FAQ](#faq)

---

## 🤔Why POMA AI? (Problem Overview)

Retrieval-augmented generation (RAG) enables LLMs to answer questions by utilizing external documents. But if you feed LLMs linear, structureless chunks, you get:
- Orphaned headings (a title with no details)
- Fragmented lists (missing key info)
- Ambiguous articles (context lost)
- Bloated prompts (wasted tokens)
- Hallucinated or incomplete answers

Linear chunking splits docs by tokens or lines — ignoring real-world structure. Tools like LlamaIndex default to this, but it fails for anything hierarchical: laws, manuals, policies, contracts, technical docs.

POMA AI preserves the true structural tree of your documents - so every answer comes with context, not confusion.

### Failure Cases of Linear Chunking (with Real-World Impact)

1) Isolated Headings (leads to incomplete information)
- Chunk A (retrieved): “Article 26. Personalized License Plate Fees”
- Chunk B (missing): “The fees vary by character count and composition.”
- Impact: Incomplete answers, confusion about fees, potential legal/financial misunderstandings.

2) Fragmented Lists (causes partial information retrieval)
- Chunk A (retrieved): “a) 2 letters and 3 digits: 300 euros; b) 3 letters and 2 digits: 500 euros”
- Chunk B (missing): “c) 4 letters and 1 digit: 1,000 euros; d) 5 letters: 3,000 euros; e) Less than 5 characters: 6,000 euros”
- Impact: Missing premium fees; compliance failures or financial errors.

3) Chapter–Article Disconnection (creates ambiguity and misattribution)
- Chunk A (retrieved): “Chapter 5. Reservation Fee for Personalized License Plates”
- Chunk B (missing): “Article 21. Tax Quota … fixed amount of 40.74 euros.”
- Impact: Misattribution across chapters; incorrect legal interpretations.

### Current Workarounds Are Insufficient

Including neighboring chunks:
- Bloats prompts with irrelevant information
- Consumes valuable token context
- Still misses structural boundaries
- Relies on heuristics rather than true document structure
- Risks hallucinations from auto-summarization or guessed relations

---

## 🧠How POMA AI Works: Re-Generating Document Structure

Rather than extracting structure from messy documents using brittle heuristics, POMA AI re-generates documents by using powerful generative intelligence and creating structural coherence inside these documents.

POMA AI runs as an intelligent pipeline:
1) Structural Chunking: Analyzes the texts, assigns each sentence a depth in the hierarchy, and groups them into chunksets: paths from document root to leaf content.

Result:
- You get *chunks* (sentences + structure) and *chunksets* (full context paths), finally deduplicated *cheatsheets* ready for efficient use in any RAG pipeline.
- Use POMA AI output as the input for LlamaIndex, LangChain, or custom retrieval engines — in place of their default flat chunkers and retrievers.

### What is a Chunkset?

A chunkset is a sequence of sentences that preserves the complete hierarchical context from document root to specific details, enabling accurate context retrieval. Instead of slicing documents blindly, POMA AI:
- Parses the full heading hierarchy (title → chapter → section → clause)
- Assigns each sentence a depth within this hierarchy
- Creates chunksets: complete root-to-leaf paths that maintain structural integrity

---

## Features

- 🔛 Structure-preserving chunking (headings, lists, articles, etc.)
- ✂️ One-sentence-per-line segmentation for precise retrieval
- ⚡ up to 90% token savings in prompt context for structured docs
- 🔗 Plug-in to any RAG pipeline

---

## 📜Example Implementations

### 🌱Basic Workflow - for Standalone Example

POMA AI offers a simple two-step process for document processing and retrieval.

*In this basic example, we use a keyword-based approach for simplicity, avoiding the need to set up a vector database.*

### 0) Change to the examples directory (or use your system-specific paths)

```bash
cd examples
```

### 1) Ingest a document to create structured chunks/chunksets

```bash
python example.py ingest Coffee.txt
```

### 2) Retrieve with a query to find relevant information

```bash
python example.py retrieve "finland"
```

*Swap the simple keyword search with your vector/full-text DB, and you have a minimal RAG loop. See example_langchain.py and example_llamaindex.py for full integrations.*

---

### 1) Standalone Example ([example.py](https://github.com/poma-ai/poma/tree/main/examples/example.py)) 
A complete, self-contained implementation that demonstrates the core POMA AI workflow.

- Ingest: Converts documents to POMA AI format, processes into chunks/chunksets, stores locally
- Retrieve: Simple keyword matching to find relevant chunksets and generate a cheatsheet

Key features:
- CLI with ingest and retrieve commands
- Local JSON storage
- Detailed structure-aware output
- Minimal dependencies (POMA AI core)

### 2) LangChain Integration ([example_langchain.py](https://github.com/poma-ai/poma/tree/main/examples/example_langchain.py))
Integrate POMA AI with LangChain’s retrieval and QA components.

- Uses: PomaFileLoader, PomaChunksetSplitter, PomaCheatsheetRetrieverLC - from poma.integrations.langchain_poma
- Stores chunks and chunksets in LangChains Document Metadata
- FAISS vector search with OpenAI embeddings — *Note: Make sure to set your OPENAI_API_KEY environment variable.*
- QA chain using LangChain’s LCEL
- Custom cheatsheet retriever for context-aware retrieval


### 3) LlamaIndex Integration ([example_llamaindex.py](https://github.com/poma-ai/poma/tree/main/examples/example_llamaindex.py))
Use POMA AI with LlamaIndex’s document processing and query engine.

- Uses: PomaFileReader, PomaChunksetNodeParser, PomaCheatsheetRetrieverLI - from poma.integrations.llamaindex_poma
- Stores chunks and chunksets in LlamaIndex Nodes Metadata
- VectorStoreIndex (implemented with FAISS) and OpenAI embeddings — *Note: Make sure to set your OPENAI_API_KEY environment variable.*
- Using LlamaIndex as_query_engine upon the retriever
- Custom cheatsheet retriever for context-aware retrieval

### Common Patterns Across Examples

- Chunking: Poma AI's API to chunk text into → chunks + chunksets
- Storage: persist chunks/chunksets for later retrieval
- Retrieval: find relevant chunksets per query
- Cheatsheet Generation: create a hierarchical deduplicated context for the LLM

*Note: In POMA AI, the units you embed are **chunksets** — structure-preserving contexts, **NOT** isolated chunks.*

---

## ➕Module Overview & Optional Imports

| Module             | What it does                               | PyPI / wheel       | License |
|--------------------|--------------------------------------------|--------------------|---------|
| poma(core-api)     | Build depth-aware chunks & chunksets       | poma               | MPL-2.0 |
| poma(integrations) | Drop-in classes for LangChain / LlamaIndex | poma[integrations] | MPL-2.0 |
| meta-README        | How all pieces fit                         | –                  | –       |

---

## ⚙️Installation

Requires Python 3.10+.

```bash
pip install poma
```

For the integration examples:

```bash
pip install poma[integrations]
# LangChain|LlamaIndex examples
pip install poma[integration-examples]
```

Packages:
- poma: text cleaner & segmenter (one sentence per line) and high-performance, chunking & context-extraction engine per API
- poma[integrations]: integration classes for LangChain and LlamaIndex

Licensing:
- Usage of the POMA AI API & ecosystem under [MPL-2.0](LICENSE).

Models and credentials:
- For POMA AI's API for chunking your documents, you’ll need credentials in the form of a POMA_API_KEY. Please contact us at [support@poma-ai.com](mailto:support@poma-ai.com) to request one.
- Model/provider for the usage of integrations; ensure your API keys for embeddings are set as environment variables (e.g., OPENAI_API_KEY).
- Recommended: OpenAI's "text-embedding-3-large" as embeddings for retrieval.

---

## 🧭The POMA Processing Pipeline (Detailed)

Processing Flow:

```
+----------------+     \    +----------------+
|  unstructured  |  ----\   | POMA AI (core) |
|   documents    |  ----/   |  client - API  |
+--------+-------+     /    +--------+-------+
                                    |
                                    v
                         (chunks[], chunksets[])
                                |            |
                                v            v

Vector/Keyword  <---- Index chunksets in your DB, also store chunks
search/retrieve ----> Retrieve relevant chunksets (context trees)
                                    |
                                    v
                        Get all chunk IDs referenced
                        in the retrieved chunksets
                                    |
                                    v
                        Get chunks with content for IDs
                                    |
                                    v
            client.generate_cheatsheet/s(relevant_chunksets, all_chunks)
                                    |
                                    v
                     Use cheatsheet(s) in LLM prompt
```

---

## Input Formats

Currently supports the following document types, ensuring LLM-friendly data extraction:
- HTML (raw structural DOM)
- Markdown (.md, markdown)
- Plain text (.txt)


### File Processing

HTML documents are parsed directly as structured data, without rendering:
- Parses the DOM, stripping layout noise and irrelevant elements
- Converts content to structured markdown with proper heading hierarchy
- Extracts images and replaces with descriptive placeholders ([🖼️IMAGE X PLACEHOLDER around here])
- Extracts tables and replaces with placeholders ([📋TABLE X PLACEHOLDER around here])
- Extracts code and replaces with placeholders ([💻CODE X PLACEHOLDER around here])
- Marks page breaks ([📄PAGE X begins here])

The other file types are processed similarly if an asset is detected.

---

## 📑🖍️Structural Chunking with Poma AI (patented at USPTO and DPA)

Inside POMA's core, documents are converted into structurally aware chunks and lossless chunksets.

### Phase 1: Creating Chunks with Depth

Input: Cleaned and normalized text

Process:
- Determine hierarchical depth per sentence
- Identify structural relationships between sentences
- Process table HTML from /assets to maintain tabular context

Output: `chunks[]` array with each sentence assigned a depth value
```python
chunks[{'content': 'Chunk text', 'depth': 0, 'chunk_index': 0},...]
```

### Phase 2: Building Chunksets

Input: `chunks[]` with depth information

Process:
- Group sentences into semantic units
- Create complete root-to-leaf paths
- Preserve parent–child relationships
- Maintain full hierarchical context

Output: `chunksets[]` array containing complete contextual paths
```python
[{'chunkset_index': 0, 'chunks': [0, 1, 2, 3, 4], 'contents': 'Chunkset text (to embed)'},...]
```

This two-phase approach ensures full structure preservation, enabling accurate retrieval and context assembly.

---

## 🛠️Complete End-to-End Workflow

- Content Chunking: `client.start_chunk_file(src_path)` → chunks + chunksets (then save/embed/index)
- Chunkset Retrieval: Use your vector or full-text search to retrieve relevant chunksets
  1. Retrieval of `relevant_chunksets` (e.g., via a vector database)
  2. Retrieval/Fetch of `chunks` belonging to the documents inside the retrieved relevant_chunksets
  *- We recommend storing the chunks separately in a relational database for faster and safer vector database retrieval*
- Cheatsheet Generation: `client.generate_cheatsheet(relevant_chunksets, chunks)` to create a concise, structured context for the LLM prompt

### Example: Chunk ID Enrichment and Cheatsheet Assembly

At retrieval time, work with the embedded chunksets, not isolated chunks.

- Use your embedding/RAG stack to retrieve relevant chunksets
- Pass them together with their chunk IDs to:

```python
cheatsheet = client.generate_cheatsheet(relevant_chunksets, document_chunks)
```

`generate_cheatsheet()`:
- Deduplicates overlapping chunk IDs
- Adds parents, children, and adjacent chunks as needed to ensure structural continuity
- Returns a complete set of Chunk objects (content + metadata) for final context assembly

Input (example):

```python
# Vector search returns these chunksets (complete root-to-leaf paths)
retrieved_chunksets = [
    [0, 1, 132, 133, 194, 195, 196, 197, 198, 199, 200, 201],   # Article 26 path
    [0, 1, 207, 208, 217, 218, 219],                            # Article 30 path
    [0, 1, 162, 163, 172, 173, 174]                             # Article 21 path
]
# Flatten to one list of IDs
chunk_ids = [
    0, 1, 132, 133, 194, 195, 196, 197, 198, 199, 200, 201,
    0, 1, 207, 208, 217, 218, 219,
    0, 1, 162, 163, 172, 173, 174
]
```

Output (conceptual, IDs only for brevity):
```
[
  0, 1,
  132, 133, 162, 163, 172, 173, 174,
  194, 195, 196, 197, 198, 199, 200, 201,
  207, 208, 217, 218, 219
]
```

### Cheatsheet Assembly (Final LLM Input)

```python
cheatsheet = client.generate_cheatsheet(all_relevant_chunks, all_chunks_of_the_docs)
```

Cheatsheet characteristics:
- Single coherent context block
- Hierarchical relationships preserved
- Logical, structured organization
- LLM-friendly ellipses ([…]) indicate omitted content
- Deduplicated content to minimize token usage

---

## 🧩Integration with RAG Tools

POMA AI is designed to be the chunker inside your RAG pipeline.

- Use POMA output with LlamaIndex, LangChain, Haystack, Weaviate, Pinecone, etc.
- Replace default linear chunkers with structure-preserving chunksets
- Works with both vector search and keyword/fulltext search backends

---

## 🌍📊Real-World Performance Example

POMA AI significantly outperforms traditional chunking in token efficiency and retrieval accuracy. While a dedicated benchmark repo is pending, real-world comparisons show substantial improvements.

This efficiency enables energy and cost savings and/or more context within token limits.

---

## ❓💬FAQ

We’ll start building out this FAQ as soon as we receive the first real questions from users.  
If you have a question, suggestion, or found something unclear in our readme, please reach out to us:  
📧 **sdk@poma-ai.com**

Your feedback will help us expand this section into a valuable reference for everyone.

---

## Release History (SDK)

- v0.1.x (Oct 2025): Initial public release
