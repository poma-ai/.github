![POMA AI Logo](https://raw.githubusercontent.com/poma-ai/.github/main/assets/POMA_AI_Logo_Pink.svg)

[![](https://img.shields.io/badge/patented%20at%20USPTO-8A2BE2)]() 
[![](https://img.shields.io/badge/patented%20at%20DPA-8A2BE2)]() 
[![](https://img.shields.io/badge/pypi-repo-blue?logo=pypi)](https://pypi.org/project/poma/) 
[![License: MPL 2.0](https://img.shields.io/badge/License-MPL_2.0-brightgreen.svg)](https://opensource.org/licenses/MPL-2.0)   
 
## Problem

Retrieval-augmented generation (RAG) enables LLMs to better answer questions by utilizing external documents. Most RAG tools however split documents linearly by tokens or lines, thus ignoring real-world structure. This causes **hallucinations**, **context loss**, and **token waste** at retrieval.

## Solution

POMA AI solves this by preserving the **structural tree** of your documents when chunking them, enabling **context-preserving retrieval**, so every answer comes with context, not confusion.

Use POMA AI's **structural chunking** inside your RAG pipeline; integrate it with *LlamaIndex*, *LangChain*, *Haystack*, *Weaviate*, *Pinecone*, etc. POMA AI works both **vector search** and **keyword/fulltext search** backends.

### Features

- Structure-preserving chunking (headings, lists, articles, etc.)
- LLM-friendly data extraction for precise retrieval
- up to 90% token savings in prompt context for structured docs
- Plug-in to any RAG pipeline
- Supported input types:
  <details>
  <summary> .pdf, .md, .html, .txt, and many more</summary>
   ['ai', 'bmp', 'csv', 'djvu', 'doc', 'docx', 'dotx', 'dwf', 'dwfx', 'dwg', 'dxf', 'eps', 'epub', 'gif', 'heic', 'heif', 'htm', 'html', 'ico', 'jpeg', 'jpg', 'key', 'md', 'mdi', 'mobi', 'numbers', 'odc', 'odf', 'odp', 'ods', 'odt', 'oxps', 'pages', 'pdf', 'png', 'pot', 'potx', 'pps', 'ppsx', 'ppt', 'pptx', 'prn', 'ps', 'psd', 'pub', 'rtf', 'svg', 'tif', 'tiff', 'txt', 'vsd', 'vsdx', 'webp', 'xls', 'xlsb', 'xlsx', 'xltx', 'xml', 'xps']
  </details>

---

- [Installation](#SDK-Installation)
- [Example Integrations](#Integrations)
- [Why POMA AI?](#why-poma-ai)
- [How POMA AI Works](#How-POMA-AI-Works---The-Structural-Chunking-Workflow)
- [Real-World Performance Example](#real-world-performance-example)
- [FAQ](#faq)
- [Licensing](#Licensing)

---

## SDK Installation

```bash
pip install poma
```

> [!IMPORTANT]  
> Requires Python 3.10+  
> Requires `POMA_API_KEY` as env variable (get it [here](https://app.poma-ai.com) by selecting your plan or contact us at **[support@poma-ai.com](mailto:support@poma-ai.com)**)

The poma client then offers three endpoints:
- Use `start_chunk_file()` to start the chunking process.
- With `get_chunk_result()` you can download the result after it finished processing.
- And `create_cheatsheets()` is used at retrieval time.  

See [How POMA AI Works](#How-POMA-AI-Works---The-Structural-Chunking-Workflow) for more details in the workflow.

> [!WARNING]  
> *Please do NOT send any sensitive and/or personal information to POMA AI endpoints without having a signed contract & DPA !*

---

## Integrations

We provide four example implementations to help you get started with POMA AI:
1. Standalone implementation (basic POMA AI workflow with simple keyword-based retrieval)
2. Integration with LangChain
3. Integration with LlamaIndex

| Module             | What it does                               | PyPI / wheel       | License | Link |
|--------------------|--------------------------------------------|--------------------|---------|------|
| poma(sdk)          | Build depth-aware chunks & chunksets       | poma               | MPL-2.0 |[pypi](https://pypi.org/project/poma/)|
| poma(integrations) | Drop-in classes for LangChain / LlamaIndex | poma[integrations] | MPL-2.0 |[github](https://github.com/poma-ai/.github/tree/main/examples)|

Get integrations classes (including examples):
```bash
pip install 'poma[integrations]'
```
```bash
pip install 'poma[integration-examples]'
```

> [!NOTE]  
> *The integration examples use OpenAI embeddings. Make sure to set your `OPENAI_API_KEY` as environment variable.*

### Standalone Implementation - [example.py](https://github.com/poma-ai/.github/tree/main/examples/example.py)

A complete, self-contained implementation that demonstrates the POMA AI workflow. It uses a keyword-based approach for simplicity, avoiding the need to set up a vector database.

Use your CLI with these ingest and retrieve commands (from inside the examples directory):
```bash
cd examples
```
**Ingest** a document to create structured *chunks* and *[chunksets](#what-exactly-is-a-chunkset)*, which are stored locally.
```bash
python example.py ingest Coffee.txt
```
**Retrieve** with a query to find relevant information; returns one *[cheatsheet](#what-exactly-is-a-cheatsheet)* per "affected" document.
```bash
python example.py retrieve "finland"
```
*Swap the simple keyword search with your vector/full-text DB, and you have a minimal RAG loop. See example_langchain.py and example_llamaindex.py for full integrations.*

> [!NOTE]  
> In POMA AI, the units you embed are *[chunksets](#what-exactly-is-a-chunkset)* — structure-preserving contexts, **NOT** isolated *chunks*.

### LangChain Integration - [example_langchain.py](https://github.com/poma-ai/.github/tree/main/examples/example_langchain.py)

Integrate POMA AI with LangChain’s retrieval and QA components.

- Uses PomaFileLoader, PomaChunksetSplitter, PomaCheatsheetRetrieverLC from `poma.integrations.langchain_poma
  and POMA AI's API to chunk text.
- Stores *chunks* and *[chunksets](#what-exactly-is-a-chunkset)* in LangChains Document Metadata for later retrieval.
- FAISS vector search with OpenAI embeddings — Make sure to set your `OPENAI_API_KEY` as environment variable.
- QA chain using LangChain’s LCEL
- Custom *[cheatsheet](#what-exactly-is-a-cheatsheet)* retriever for context-aware retrieval

### LlamaIndex Integration - [example_llamaindex.py](https://github.com/poma-ai/.github/tree/main/examples/example_llamaindex.py)

Use POMA AI with LlamaIndex’s document processing and query engine.

- Uses PomaFileReader, PomaChunksetNodeParser, PomaCheatsheetRetrieverLI from `poma.integrations.llamaindex_poma`
  and POMA AI's API to chunk text.
- Stores *chunks* and *[chunksets](#what-exactly-is-a-chunkset)* in LlamaIndex Nodes Metadata for later retrieval.
- VectorStoreIndex (implemented with FAISS) and OpenAI embeddings — Make sure to set your `OPENAI_API_KEY` as environment variable.
- Using LlamaIndex as_query_engine upon the retriever
- Custom *[cheatsheet](#what-exactly-is-a-cheatsheet)* retriever for context-aware retrieval

---

## Why POMA AI?

Retrieval-augmented generation (RAG) enables LLMs to better answer questions by utilizing external documents. But if you feed LLMs linear, structureless chunks you get:
- Orphaned headings (a title with no details)
- Fragmented lists (missing key info)
- Chapter–Article Disconnection (context lost)
- Bloated prompts (wasted tokens)
- Hallucinated or incomplete answers

Linear chunking splits docs by tokens or lines — ignoring real-world structure. Tools like LlamaIndex default to this, but linear chunking fails for anything hierarchical: laws, manuals, policies, contracts, technical docs.

### Failure Cases of Linear Chunking (with Real-World Impact)

1) **Isolated Headings** → incomplete information  
   Chunk A (retrieved): “Article 26. Personalized License Plate Fees”  
   Chunk B (missing): “The fees vary by character count and composition.”  
   Impact: Incomplete answers, confusion about fees, potential legal/financial misunderstandings.  

2) **Fragmented Lists** → partial information  
   Chunk A (retrieved):  
   “a) 2 letters and 3 digits: 300 euros; b) 3 letters and 2 digits: 500 euros; c) 4 letters and 1 digit: 1,000 euros; d) 5 letters: 3,000 euros;”  
   Chunk B (missing): “e) Less than 5 characters: 6,000 euros”  
   Impact: Missing premium fees; compliance failures or financial errors.  

3) **Chapter–Article Disconnection** → ambiguity and misattribution  
   Chunk A (retrieved): “Chapter 5. Reservation Fee for Personalized License Plates”  
   Chunk B (missing): “Article 21. Tax Quota … fixed amount of 40.74 euros.”  
   Impact: Misattribution across chapters; incorrect legal interpretations.  

### Current Workarounds Are Insufficient

Avoiding chunking in the middle of sentences is a no-brainer, but how do you deal with really long (for example legal) paragraphs that are longer than your chunk limit?

Including neighboring chunks seems to be the method of choice for most chunkers, but limit/target based chunking with overlap  
→ doubles the information that needs embedding  
→ bloats prompts with irrelevant information  
→ consumes valuable token context  
and still misses structural boundaries.

Other proposed solutions use auto-summarization or guessed relations, relying on heuristics rather than true document structure, to create additional "context" information for chunks thus  
→ losing accuracy (through abstractions)  
→ and risking hallucinations.

---

## How POMA AI Works - The Structural Chunking Workflow

Rather than slicing blindly or extracting structure from messy documents using brittle heuristics, POMA AI re-generates documents by using powerful generative intelligence and creating structural coherence inside these documents.

## The Processing Pipeline

```
+----------------+     \    +----------------+
| (unstructured) |  ----\   |    POMA SDK    |
|   documents    |  ----/   |     client     |
+--------+-------+     /    +--------+-------+
                            start_chunk_file()
                                    +
                            get_chunk_result()
                                    |
                                    v
                         (chunks[], chunksets[])
                              |            |
                              v            v

Vector/Keyword  <---- Index chunksets in your DB, also store chunks
                                    …
search/retrieve ----> Retrieve relevant chunksets (context trees)
                                    |
                                    v
                        Get all chunk_IDs referenced
                        in the retrieved chunksets
                                    +
                       Get content for these chunk_IDs
                                    |
                                    v
                           +----------------+
                           |    POMA SDK    |
                           |     client     |
                           +--------+-------+
                          create_cheatsheets()
                                    |
                                    v
                      Use cheatsheet(s) in LLM prompt
```

## Key Concepts

POMA AI converts documents into structurally aware *chunks* and lossless *chunksets*. *Chunksets* can then be embedded and later used to create *cheatsheets*, a compact representation of the retrieved information, optimized for LLM consumption. This approach ensures full structure preservation, enabling accurate retrieval and context assembly.

### Step 1 - Structural Chunking (Ingestion)

SDK:
```
json = client.start_chunk_file(src_path)
result = client.get_chunk_result(job_id_from_json)
chunks, chunksets = result["chunks"], result["chunksets"]
```

### Step 1.1 - Creating Chunks with Depth

**Input**: your documents ([supported types](#Features))

**Process**:
- Text is analyzed and structural relationships between sentences / text units are identified
- Each sentence / text unit is assigned a depth in the hierarchy

**Output**: Short, granular, context aware chunks with assigned depth
```
chunks[{'chunk_index': 0, 'content': 'some text', 'depth': 0}, ...]
```
*We recommend storing the chunks separately in a relational database for faster and safer retrieval.*

### Step 1.2 - Building Chunksets

**Input**: *chunks* with depth information

**Process**:
- Chunks are grouped into semantic units
- Complete root-to-leaf paths are created
- Parent–child relationships are preserve, full hierarchical context is maintained

**Output**: chunksets containing complete contextual paths
```
[{'chunkset_index': 0, 'chunks': [0, 1, 2, 3, 4], 'contents': 'combined chunk texts (to embed)'}, ...]
```
*Embed these and store them for later retrieval.*

> ### What exactly is a Chunkset?
> First of all a chunkset is a "set of chunks", a sequence of single sentences or chunks (usually one sentence is one chunk).  
> Secondly a chunkset is a complete root-to-leaf path for every "leaf chunk" in a document, for example: `title → chapter → section → clause`, with the clause being the "leaf" and the title being the "root".  
> Thus chunksets preserve the complete hierarchical context for every chunk in a document - from document root to specific details.
> This ensures:
> - Headings are never separated from their content
> - Lists remain intact with all items
> - Hierarchical relationships between sections are preserved
> - Context is never lost during retrieval
> So chunksets are also meaningful parts of text, enabling accurate retrieval and context assembly.

> [!NOTE]  
> When comparing traditional chunks with POMA AI's chunking result, *chunksets* are the correct counter part.  
> POMA AI's *chunks* are very short and used solely to make up the root-to-leaf paths we call *chunksets*.  
> **Chunksets are the fundamental unit of storage and retrieval in POMA AI.**

### Step 2 - Cheatsheet Assembly (Retrieval)

Use your vector or full-text search to retrieve query relevant chunksets (could be from different documents). Also collect all chunks indicated by the relevant chunksets (indicated in the `chunks` field of the relevant [chunksets](#what-exactly-is-a-chunkset)).

**Input**: relevant *chunksets* (complete root-to-leaf paths) and all necessary *chunks* (single sentences with depth information)

```
[{'chunkset_index': 0, 'chunks': [0, 1, 2, 3, 4], ...}, ...]
```

**Process**:
- Overlapping content is deduplicated while preserving structural relationships (per document)
- Parents, children, and adjacent chunks are added as needed to ensure structural continuity
- All information is formatted hierarchically

**Output**: The final LLM context information ready for efficient use in any RAG pipeline. We call them [cheatsheets](#what-exactly-is-a-cheatsheet). Use them as the input for LlamaIndex, LangChain, or custom retrieval engines — in place of their default flat chunkers and retrievers.  
If all chunksets necessary to answer a query originate from the same document only one single cheatsheet is produced, otherwise you get as many cheatsheets as documents involved.

SDK:
```python
cheatsheets = client.generate_cheatsheets(relevant_chunksets, all_necessary_chunks)
```
 
> ### What exactly is a Cheatsheet?
> 
> *Cheatsheets provide the LLM with precisely the **context** it needs to answer queries accurately, without wasting tokens on redundant information.*  
> It is a compact representation of the retrieved information. It comprises several relevant chunksets, deduplicated and optimized for LLM consumption.  
> We call them *cheatsheets* because they are compact summaries of the most important points on a topic, like the ones none of us use during a test or exam.
> 
> Cheatsheet characteristics:
> - Single coherent context block
> - Hierarchical relationships preserved
> - Logical, structured organization
> - LLM-friendly ellipses ([…]) indicate omitted content
> - Deduplicated content to minimize token usage
> - One cheatsheet per as document involved
> 
> Example input:
> ```python
> retrieved_chunksets = [
>   {"chunkset_index": 0, "chunks": [0, 10, 16, 17], "file_id": "doc_1"},
>   {"chunkset_index": 1, "chunks": [0, 4, 5, 6], "file_id": "doc_2"}
> ]
> ```
> 
> Example output (conceptual, IDs only for brevity):
> ```
> [0, 4, 5, 6, 10, 16, 17]
> ```

---

## Real-World Performance Example

POMA AI significantly outperforms traditional chunking in token efficiency and retrieval accuracy. While a dedicated benchmark repo is pending, real-world comparisons show substantial improvements.

To illustrate with a (very) niche example: a legal-document query about Andorra’s personalized license-plate law (a notoriously tough document for RAGs) needed **1,542 tokens** of retrieved context with traditional RAG, versus **337 tokens** with POMA (a roughly 80% reduction), with zero information loss.

This efficiency enables energy and cost savings and/or more context within token limits.

---

## FAQ

We’ll start building out this FAQ as soon as we receive the first real questions from users.  
If you have a question, suggestion, or found something unclear in our readme, please reach out to us:  
**sdk@poma-ai.com**

Your feedback will help us expand this section into a valuable reference for everyone.

---

## Licensing

Usage of the POMA AI API & ecosystem under [MPL-2.0](../LICENSE).

