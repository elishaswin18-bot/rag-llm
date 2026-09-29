
```
Explain the complete RAG pipeline end-to-end. What happens at each stage?

Videos Links (Shown in reel)
LLM evals- https://youtu.be/6W92_t9FveA?si=1lL4q8IPL_yD6WGA
LLM gateway- https://youtu.be/RN3baOpNA6w?si=pSkQmADXZiCtvNWj
Guardrails with LangChain- https://youtu.be/ruiLq0OzjkI?si=j9yhlxbwoSehLvJ0
LLM Evals & LLM as a judge- https://youtu.be/9Ay0WcjrdGE?si=vs3xm1qT1VMyOz61
Model Armor - https://youtu.be/fH62NUGwsyo?si=R0kR61FdrzAN7ft1


The 3-Phase RAG Pipeline:
RAG (Retrieval Augmented Generation) has two main phases: 
Offline Indexing & Online Querying.

Phase 1 — Offline Indexing (runs once or periodically): 
How you are actually loading the document, like a PDF, into SharePoint or blob storage, and then you are doing the parsing, chunking, embedding, and storing into an active database in the form of an index
1.	Load: Ingest documents from sources (S3, SharePoint, databases) using document loaders. Parse: Extract text from PDFs, DOCX, HTML using Document AI or Unstructured.io. Preserve structure (headers, tables, code blocks).
2.	Chunk: Split documents into 256–512 token pieces with 50-token overlap. Respect natural boundaries.
3.	Embed: Convert each chunk to a dense vector using an embedding model (text-embedding-004, OpenAI text-embedding-3-large).
4.	Index: Store (vector, metadata, raw text) in a vector database (Pinecone, Vertex AI Vector Search, ChromaDB).
Phase 2 — Online Query (runs per request):
1.	Embed query: Convert user question to a vector using the SAME embedding model used during indexing.
2.	Retrieve: Find top-K most similar chunks via cosine similarity (ANN search). Apply metadata filters for access control.
3.	Rerank: Re-score top-20 retrieved chunks with a cross-encoder reranker. Keep top-5.
4.	Augment: - adding question+ receive chunk, Inject retrieved chunks into prompt: "Answer ONLY using the context below. If not found, say I don't know."
5.	Generate: LLM generates grounded answer with citations pointing to source chunks.
6.	Stream: Return tokens to user as generated via SSE for low perceived latency.

■ Interviewer often asks: Where does most latency come from in the RAG pipeline, and how do you reduce it?

■ Pro Tip: Interviewers expect you to know BOTH phases. Most candidates only describe the query phase. Mentioning
streaming, access control filters, and reranking shows production depth.




RAG Interview Questions and Answers
1. What kind of embedding have you used? How do you apply it? What if OCR does not work?
An interviewer may ask:
“What kind of embedding have you used, and how did you apply it?”
They may also ask:
“If OCR is not working, what will you do?”
This is important because documents may contain:
•	Images
•	Tables
•	Scanned pages
•	Structured content
In such cases, OCR or document parsing tools are required before chunking and embedding.
 
2. How do you decide the chunk size and overlap?
Chunk size is data-dependent and should be decided through experimentation and retrieval evaluation.
If chunks are too small:
•	Lose surrounding context
•	Evidence becomes fragmented
•	May improve recall, but reduce answer quality
If chunks are too large:
•	Contain irrelevant information
•	Embeddings become less specific
•	Consume more LLM context window
Production approach:
•	Structure-aware chunking
•	Suitable overlap
•	Retrieval evaluation
For complex documents, you can also use:
•	Parent-child chunking
•	Semantic chunking
 
3. Why do you use hybrid retrieval?
Typical flow:
BM25 + Vector Search → Fusion → Top 20 → Reranking → Top 5 → LLM
BM25
BM25 is useful for exact-match searches such as:
•	Error codes
•	Product names
•	IDs
•	Keywords
Vector Search
Vector search is useful for:
•	Semantic meaning
•	Similar concepts
•	Natural-language queries
Reranking
The reranker performs a more detailed query-document relevance check on a smaller candidate set.
 
4. How do you evaluate RAG?
RAG evaluation should be divided into two parts:
Retrieval Evaluation
Common metrics include:
•	Recall@K
•	Hit Rate@K
•	Precision@K
•	MRR
•	NDCG
•	Context relevance
Generation Evaluation
Common metrics include:
•	Faithfulness / Groundedness
•	Answer relevance
•	Correctness
•	Completeness
•	Citation accuracy
You can use tools such as:
•	RAGAS
•	LLM-as-a-Judge
•	Curated golden test datasets
The interviewer may ask:
“How can an LLM judge know whether an answer is correct?”
The key distinction is:
•	Correctness → compare against known ground truth
•	Groundedness → check whether the answer is supported by retrieved evidence
 
5. What happens when documents change?
In production, we normally use incremental document processing.
Typical flow:
1.	Check SharePoint for updated documents
2.	Detect the changed version or content hash
3.	Identify the document ID
4.	Find existing chunks belonging to that document
5.	Delete or update the affected chunks
6.	Parse the latest version
7.	Rechunk the document
8.	Generate new embeddings
9.	Insert the new chunks into the index
Store metadata such as:
•	document_id
•	chunk_id
•	version
•	source
•	updated_at
•	ACL information
•	content hash
This allows you to efficiently update or delete vectors when a document changes.
 
6. Where does RAG latency come from?
The main latency usually comes from:
•	LLM generation
•	Reranking
•	External tool or API calls
However, latency should always be measured rather than assumed.
Production optimisations:
•	Cache embeddings where appropriate
•	Cache retrieval results where appropriate
•	Reduce the number of retrieved candidates
•	Use a faster reranker
•	Use a smaller or faster LLM where suitable
•	Parallelise independent retrieval calls
•	Keep services in the same or nearby region
•	Reduce unnecessary context
•	Stream responses using SSE
Streaming does not reduce actual processing time, but it improves perceived latency for the user.





RAG


 

Retrieval and Generation.
RAG has two main parts: retrieval and generation. 

The retrieval part is like a search engine-: it finds the most relevant pieces of information from external sources such as databases, documents, or knowledge bases. 

Generation part, which is the large language model itself. The LLM takes both the user's question and the retrieved information and uses them together to create a clear and grounded answer.


Grounding: means making sure the model's answers are based on real, verifiable information instead of just what it "remembers." In RAG, grounding happens because the system retrieves facts from trusted sources-like company documents, databases, or knowledge bases-and feeds them into the model along with the question.

Chunking strategy

Types of Chunking in RAG
Chunking Type	How it works	Best for
Fixed-size chunking	Split every N characters/tokens, e.g. 500 tokens
 	Simple documents, quick prototypes

# Simple Python slice 
chunks = [text[i:i+500] for i in range(0, len(text), 500)]
Fixed-size + overlap	500-token chunks with, say, 50-token overlap
 	Common baseline for RAG

from langchain.text_splitter import CharacterTextSplitter 
splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50, separator="") 
chunks = splitter.split_text(text)
Sentence-based chunking	Split by complete sentences
 	Articles, natural-language text

import nltk 
nltk.download('punkt') 

# Tokenize into complete sentences 
chunks = nltk.sent_tokenize(text)
Paragraph-based chunking	Each paragraph or group of paragraphs becomes a chunk
 	Reports, Word documents

# Split on double line breaks 
chunks = [chunk.strip() for chunk in text.split("\n\n") if chunk.strip()]
Recursive chunking	Tries paragraph → sentence → word/token until the chunk fits
 	Most common practical approach

from langchain.text_splitter import RecursiveCharacterTextSplitter 

# Tries paragraph (\n\n), then sentence (\n), then words ( ), then chars 
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50) 
chunks = splitter.split_text(text)
Semantic chunking	Groups sentences based on meaning/embedding similarity
 	Complex knowledge documents

from langchain_experimental.text_splitter import SemanticChunker 
from langchain_openai import OpenAIEmbeddings 
# Groups sentences based on embedding similarity breakpoints splitter = SemanticChunker(OpenAIEmbeddings()) 
chunks = splitter.create_documents([text])
Structure-aware chunking	Uses headings, sections, tables, lists, chapters
 	PDFs, policies, technical docs

from langchain.text_splitter import MarkdownHeaderTextSplitter 
# Splits based on document structure (e.g., Markdown headers) headers_to_split_on = [("#", "H1"), ("##", "H2")] 
splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on) chunks = splitter.split_text(markdown_text)
Parent-child chunking
 (MOST POWERFULL)	Search small child chunks but return a larger parent section

 	Long documents where more context is needed

from langchain.retrievers import ParentDocumentRetriever 
from langchain.storage import InMemoryStore 

# Embeds small child chunks but returns the larger parent document on retrieval 
retriever = ParentDocumentRetriever( 
     vectorstore=vectorstore, 
     docstore=InMemoryStore(),     
     child_splitter=RecursiveCharacterTextSplitter(chunk_size=200) 
)
Sliding-window chunking	Moves through text with overlapping windows
 	Documents where context crosses boundaries

# Moves through a tokenized list with overlapping windows 
tokens = text.split() 
window, step = 100, 50 
chunks = [" ".join(tokens[i : i + window]) for i in range(0, len(tokens), step)]
Agentic/LLM-based chunking	An LLM decides meaningful boundaries

 	Highly complex/unstructured documents

from langchain_core.prompts import PromptTemplate 
# Prompts an LLM to insert special delimiters at logical topical boundaries 
prompt = PromptTemplate.from_template( "Insert '<chunk_break>' into the text where the core topic changes:\n{text}" ) 

response = llm.invoke(prompt.format(text=text)) 
chunks = response.content.split("<chunk_break>")
 

Recommended for Enterprise PDFs:
For a production RAG system, a strong starting point is:
Structure-aware → Recursive chunking → 500–1,000 tokens → 10–20% overlap.
Use Document AI (GCP) or Unstructured.io to parse PDF structure. Tables and code blocks stay intact. Small children for accurate retrieval, large parents for rich LLM context.

Chunk Size Rule of Thumb:
•	Too small (64 tokens): high precision, but not enough context for LLM to generate a good answer.
•	Too large (2048 tokens): retrieves relevant content, but diluted with irrelevant text → worse answers.
•	Sweet spot: 256–512 tokens with 50-token overlap.

■ Interviewer often asks: How does chunk overlap help, and what's the downside of too much overlap?
■ Pro Tip: Parent-child retrieval is the advanced answer that separates senior candidates. Small chunks for precise retrieval, large parents for rich generation context — solve the chunk size dilemma.



This video provides a comprehensive guide for answering common interview questions regarding chunking strategies in RAG (Retrieval-Augmented Generation) systems. It progresses from basic methods to advanced, production-grade techniques:
1.	Fixed-size chunking : The simplest approach using a set token length with overlaps. While easy to implement, it often leads to context dilution and poor retrieval quality because chunks are cut arbitrarily. here we are using recursive text splitter.
●	if you are going with too low chunk then the context will be diluted but embedding will be of high quality
●	if we are going with high chunks then the context will be high but embedding quality will be degraded
●	the sweet spot is roughly 200 to 800. yeah where we are using 800 tokens for the legal document where high context is required and the title and description might be different in the same page in different parts. small tokens are for q&a purposes where the questions and answers are in the same place but a middle ground like a research paper is used where token size is around 400.

Fixed-size chunking

from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=512,
    chunk_overlap=0,
)
chunks = splitter.split_text(text)

Fixed-size chunking with overlap

from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
     chunk_size=500,
     chunk_overlap=100
)

chunks = splitter.split_text(text)



2.	Structure-aware chunking : Uses document formatting (headings, paragraphs, sections) to create semantically meaningful splits, improving coherence and embedding quality.
structure chunking: we are actually having a long document like an html page. we have a markdown file in the html page. we will be having heading h1s, h2s, and subsections and further down. similarly we will be having double hash in markdown. 
1.	we are having a large section which we are going to split into subsections.
2.	if the subsection is large like more than 2000 characters then we are going to split into sentences.
3.	if the sentence is large then we are going to split into paragraphs.
4.	if the paragraph is large we are going to split into sentences and then chunks.
this is how the structure is made and we are doing this splitting of this . we are doing in this then our quality of chunk is context is very high.
         DOCUMENT STRUCTURE
  
  


# 2. CHUNK DOCUMENT
print("\n========== 2. CHUNK DOCUMENT ==========")
splitter = RecursiveCharacterTextSplitter(
   chunk_size=200, #prd=500 & 75
   chunk_overlap=20,
   separators=["\n\n", "\n", ". ", " ", ""]
)
chunks = splitter.split_documents([document])


Metadata enrichment : Emphasizes adding information like document names, dates, or chapters to chunks, which enables efficient filtering and better traceability in large-scale systems.

Metadata provides the document-related information, it tells how the document is stored in the chunk, so here with the help of this if we are talking about an example, what is the revenue? if there is metadata information somewhere, the filtering becomes easy. suppose there is some date of the report 2024 so it will skip the other dates and it will just take the information from 2024. that way the filtering enhances

3.	Parent-child/Sliding window: A sophisticated method that retrieves small 'child' chunks for precise semantic matching, while passing the larger 'parent' context to the LLM to ensure accuracy.
suppose there is a very big document and in that document we are searching for a particular sentence. with the help of a parent-child sentence it is not only searching the sentence but it will also take all the context of the parent to understand better. in this case when we are sending we are sending the whole parent and child which makes it more informative. it is specially used for legal documents where the context is much larger and it is there in multiple pages Suppose this is your document:
Parent Chunk: Authentication Architecture
Our application uses OAuth2 and Azure AD.
Access tokens expire after 60 minutes.
Refresh tokens are used to obtain new access tokens.
API permissions are controlled using RBAC.

We could create smaller child chunks:
Child 1: Our application uses OAuth2 and Azure AD.
Child 2:Access tokens expire after 60 minutes.
But instead of sending only that tiny child to the LLM, we retrieve its parent:

Sliding window preserves context between adjacent chunks through overlap. Parent-child retrieval separates retrieval granularity from generation context: small chunks improve search accuracy, while larger parent chunks provide the LLM enough context to answer correctly.

For a production RAG system, Parent-Child is often more sophisticated because you can use something like 200–400 token child chunks for retrieval while returning a 1,000–2,000 token parent section to the LLM.

•	Semantic chunking (Propositions/cosign similarity): Advanced, computationally intensive approaches that use LLMs or embedding similarity to detect topic shifts or extract self-contained facts (propositions), ideal for high-stakes domains like law or finance.

The complete document is divided into sentences, each sentence has an embedding, and now we are comparing sentence one and sentence two and I am finding the cosine similarities. if the cosine similarities are high then that means that they are close to each other. So we are appending sentence one and sentence two in chunk one. so this helps to find the similar kind of chunk at one place which is easy to search but the cost of working on this is very high.

Propositions are actual facts and they contain the full information. In this case, whenever we are trying to do the chunking with the help of a proposition, it is highly accurate, especially in the case of financial medical records.

In this what we are doing is we are actually sending the whole document to an llm and the llm is resizing the proposition. based on that proposition it is actually creating an embedding or chunking. you can say it is creating a chunking and then if we are doing the searching, it is very highly accurate. problem with this is that it is costly and used only in high-stakes work


Proposition:
Proposition chunking
    → split into individual FACTS

 

RAG gives fluent but wrong answers. How do you debug it? 
First of all, in an interview, you cannot call everything hallucination. You need to have a structured approach. We are going to start with isolating the failing stage: whether the problem is retrieval or generation.
1.	Check if the correct source passage is even present in the top K retrieved results. If not, it is a retrieval problem.
2.	We are going to inspect query rewriting, chunking strategy, embedding quality, metadata filters, and hybrid source configuration. The focus will be on why the right document is not being fetched or retrieved.
3.	If the correct context is retrieved and the answer is still wrong, then it is a generation problem.
4.	We are going to check prompt grounding, context ordering, too many distracted chunks, and whether the model is answering without enough evidence. We are not going to debug randomly. We are going to build evals with real user questions and test retrieval and answer quality systematically. In short, instead of blaming LLM generation directly, you should have a structured approach to debug your agent tech system
5.	Finally, the video covers how to evaluate these strategies using metrics like retrieval recall, MRR (Mean Reciprocal Rank), faithfulness, and context precision to determine the most effective setup for specific use cases 

Production RAG Evaluation
In production, we typically prepare a golden evaluation dataset of around 200–500 questions. For every question, we already know the expected answer, the source/context document, and ideally the relevant chunk(s) that should be retrieved.
We then run the RAG system against this dataset and measure:
•	Retrieval Recall – whether the required chunks were successfully retrieved. suppose we are only getting two correct answers out of five and suppose we are getting four correct answers out of five. that means the precision and recall values are much higher in the second ex; ⅖, ⅘, here ⅘ is better
•	MRR (Mean Reciprocal Rank) – how high the first correct/relevant chunk appears in the retrieval ranking.- we are retrieving the chunk. there might be one, two, three, or four chunks but in our case how high the chunk is in the group. suppose our exact answer is at the third position then it is a bad quality. the reciprocal rank mean will be low, if it is at the top, the mean reciprocal rank value will be, TOP BEST CHUNK
•	Context Precision – how many retrieved chunks are actually relevant versus noisy or irrelevant. we have retrieved multiple chunks but what is more, what particular area chunk is very relevant? suppose we have 5 and only one is irrelevant. then the context precision is low but if we have all 5 relevant things then the context precision is high
•	Answer Faithfulness – whether the generated answer is supported by the retrieved context and avoids hallucination. it says whether the llm is answering from the chunk only or it is doing hallucination. It helps to calculate hallucinations.
•	Answer Relevance – whether the generated answer directly addresses the user's question.
Overall Retrieval/Answer Quality – compares different chunking, embedding, retrieval, reranking, and prompt strategies.
We compare these metrics across different configurations—for example, chunk size, overlap, embedding model, hybrid search, top-K, reranker, and prompting strategy. The configuration that gives the best overall balance across the evaluation metrics is selected for production.


   

































Retrieval Strategy
 

RRF – Reciprocal Rank Fusion 
 
I retrieve candidates independently using BM25 and vector search, then use Reciprocal Rank Fusion to combine the ranked lists. Each document receives 1/(k + rank) from each retriever, and documents ranked highly by multiple retrievers naturally rise to the top. I can then send the fused top-N candidates to a reranker.”
One small clarification: k=60 in RRF is a rank-smoothing constant;
 
 






Retrieval Strategy 
For retrieval, we used hybrid search combining BM25 keyword search with vector semantic search. We applied metadata and access-control filters, retrieved the top candidate chunks, and used semantic reranking before passing the most relevant context to the LLM.
 
RRF = Reciprocal Rank Fusion. It combines results from multiple retrieval methods—here BM25 (keyword search) and vector search (semantic search)—using their rank positions, rather than trying to compare their incompatible raw scores.
Fusion RAG works by combining results from multiple retrievers instead of relying on just one. For example, it might use a sparse retriever like BM25 for keyword matches, and a dense retriever using embeddings for semantic matches. Then it merges or reranks the combined results before passing them to the LLM.

The benefit is better balance-sparse methods catch precise keywords, while dense methods capture meaning. Together, they cover more ground and reduce the chance of missing important context. Fusion RAG is especially useful in domains where both exact terms and broader concepts matter, like legal or technical documents.


There is Formula which actually calculates the top one from both the combined BM25 and vector rankings.
 

 




Hello did you use?"
        ↓
Hybrid = BM25 + Vector
"Why both?"
        ↓
Exact matching + semantic matching
"How did you combine them?"
        ↓
Search engine's hybrid ranking / RRF
"Did you rerank?"
        ↓
Yes → semantic reranker
"What was Top-K?"
        ↓
Explain your actual candidate/final K,
not an invented number
"How did you know it worked?"
        ↓
Offline evaluation + production monitoring
Recall@K / NDCG / answer groundedness



What is the 'Lost in the Middle' problem and how do you solve it?
Answer:
Sometimes it happens that the LLM gets lost from the retrieved chunk because the context is more in the top and bottom, but it forgets the actual result which is there in the middle.

Lost in the Middle means an LLM may pay less attention to important information placed in the middle of a long context, while information near the beginning or end can be easier for it to use.
Retrieved context sent to LLM

Chunk 1  ← relevant
Chunk 2
Chunk 3
Chunk 4
Chunk 5  ← ★ ANSWER IS HERE
Chunk 6
Chunk 7
Chunk 8
Chunk 9  ← relevant



Question:
"What caused INC-101?"

1.	Re-ranking: Making the relevant chunk at the top
2.	Summarising - Mixing the two chunks together to have more context
3.	Query Decomposition: splitting a complex query into a subquery






Problem (lost in middle): Research shows that LLMs pay more attention to information at the beginning and end of the context, and often ignore or underweight information in the middle. If you retrieve 10 chunks and the correct answer is in chunk #5 (middle), the LLM might miss it. 
Solutions: 
a)	Reduce the number of retrieved chunks - use fewer, more relevant chunks so nothing gets buried. 
b)	Re-rank before injection - put the most relevant chunks FIRST in the prompt. 
c)	Chunk summarization - summarize retrieved chunks into a condensed context. 
d)	Query decomposition - split complex queries into sub-queries, retrieve separately, then combine. 
e)	Smart positioning - put critical context at the START of the prompt, instructions at the END.

Example:

10 retrieved chunks ordered by similarity:
Chunk 1: 0.95 relevance (start - LLM pays attention)
Chunk 2: 0.93
Chunk 3: 0.91
Chunk 4: 0.89
Chunk 5: 0.87 -> THE ACTUAL ANSWER IS HERE
Chunk 6: 0.85
Chunk 10: 0.75 (end - LLM pays attention)
Problem: LIM focuses on chunks 1-3 and 9-10, skips chunk 5.


Solution 1: Only retrieve top 3-5 chunks instead of 10.
Solution 2: Re-rank so the answer chunk moves to position 1.


—---
The Problem: this is at LLM level retrieval
Research (Stanford, 2023) shows LLMs are significantly better at using information at the BEGINNING and
END of their context window than information in the MIDDLE. If you retrieve 10 chunks and the most relevant
one is chunk #5 or #6, the LLM may miss it or underweight it.

Why It Happens:
•	LLMs use attention mechanisms trained on natural text where relevant context appears early (beginning) or as a summary (end).
•	Middle positions receive less attention weight during generation — especially in long contexts.

5 Mitigation Strategies:
1.	Position optimization: Place most relevant chunks first AND last in context. Less relevant chunks go in the middle.
2.	Reranking: Better reranking = more relevant chunks = less irrelevant middle content.
3.	Reduce context size: Send fewer, more precise chunks. Better to send 3 highly relevant chunks than 10 mixed ones
4.	Context compression: Use a small LLM (Gemini Flash) to extract only the relevant sentences from each retrieved chunk before sending to main LLM.
5.	Long-context models: Gemini 2.0 Pro (1M token context) is trained to handle long contexts better. Still not perfect, but significantly better than shorter context models.










■ Interviewer often asks: How would you test whether 'lost in the middle' is hurting your RAG system's accuracy?



—---

How we fix it
Your retrieval pipeline already gives us the main solution:
 

In a RAG pipeline, Context Compression and Deduplication happen after retrieval to reduce unnecessary context before sending it to the LLM. They are related, but not the same.
 
 

Small example
 
 

 
Query rewriting actually does simplify the query. Hide actually generates the answer based on the answer. It sends the request to get the closest match, which does the faster retrieval, and Sub Query Decomposition splits the query into multiple small pieces.



















Different type of RAG in the system.

Hallucination is not always a prompting problem.
Sometimes it is a retrieval and architecture problem.
Most tutorials stop at Naive RAG.




𝗤𝘂𝗶𝗰𝗸 𝗚𝘂𝗶𝗱𝗲: 𝗪𝗵𝗲𝗻 𝘁𝗼 𝘂𝘀𝗲 𝗲𝗮𝗰𝗵
✓ 𝗡𝗮𝗶𝘃𝗲 𝗥𝗔𝗚 — Retrieves relevant documents and sends them to the LLM. Simple, but limited.
✓ Hybrid RAG → When you need the best recall + precision.  this is about vector semantic search, and Hybrid search both combined together to get the result - Keyword(BM25) + vector search(cosign similarity)
✓ Advanced RAG → Query Rewriting + Hybrid Search(semantic_keyword(BM25)) + re-renking
✓ Multi-Modal RAG → When info lives in more than just text.  it is also searching text, image, video, ppt, or audio 
✓ Corrective RAG/Self RAG → When accuracy is non-negotiable. highly accurate system like a financial document where the llm only just judges to correct itself and get the query again. LLM AS JUDEGE?
✓ Agentic RAG → Research, multi-step reasoning, dynamic retrieval. here the agent is decided and search happens in multiple series and the agent is llm + harness 
✓ Modular RAG→ if we are doing the search in a vector database, we are optimising our query and getting a result from the vector database. Suppose the query output is not sufficient enough, so we need an external tool to search the query differently. What we are doing is that, in parallel, we are doing the search, and both the parallel module outputs are combined and re-ranked. Based on that re-ranking, we are finding the relevant change, then we are building the prompt, and based on that prompt, we are submitting to the LLM
✓ CRAG → Corrective RAG, or CRAG, is an advanced version of RAG that adds an extra validation step. In standard RAG, the model uses whatever documents are retrieved, even if some are irrelevant. CRAG fixes this by checking the quality of the retrieved results-using filters, rerankers, or even the LLM itself to decide which chunks are useful and which should be discarded.
✓ SELF RAG→It checks the answer, double-checks the answer that is written, and if it doesn't think they have performed well, it asks the LLM to ask the question again to rewrite it. The self-reg lets the model act like a student, double-checking their source before writing the final response. - Self-RAG makes the LLM more adaptive and self-checking. It can decide whether retrieval is needed, evaluate whether retrieved information is useful, and assess whether its answer is sufficiently supported.
 

✓ Graph RAG → Data is highly connected (entities, relationships, networks).  here the documents are scattered in different places so each has a relationship so the search is happening there with the help of the graph.
✓Adaptive RAG? -> Based on the easy, simple, and complex query, it smartly identifies what to choose and how to retrieve the context. Here we are having a query classifier. We check whether the query is simple, medium, or compact.
 
✓ Multi-hop RAG

Production systems often combine multiple approaches based on data, query complexity, latency, accuracy, and cost.

 
 
RAG vs. CAG, clearly explained!
Corrective RAG, or CRAG, is an advanced version of RAG that adds an extra validation step.It does not trust easily. It checks whether the relevant documents are coming correctly. In standard RAG, the model uses whatever documents are retrieved, even if some are irrelevant.

CRAG fixes this by checking the quality of the retrieved results-using filters, rerankers, or even the LLM itself to decide which chunks are useful and which should be discarded.

KY-Caching

RAG is the default, but there's a problem most teams don't address.
Every single query retrieves from the vector DB. Even when the data hasn't changed in months.
That's wasted compute, added latency, and cost you don't need to pay.

🔺What RAG does:

Query comes in → embedding model converts it → vectors hit the DB → context retrieved → LLM generates response.

Clean pipeline. But expensive at scale when half your queries are pulling the same static data every time.

🔺What CAG adds:
Cache-Augmented Generation lets the model store static information directly in KV memory.
Instead of retrieving the same policies or documentation on every query, it's already there.

🔺RAG + CAG combined: 
→ Static data (policies, docs, reference material) gets cached once in KV memory. 
→ Dynamic data (live documents, recent updates) gets fetched via retrieval as usual.




 
It have retrieval evaluator, that check if the context Is good or not. If it is good, then it would learn the answer. If it is not good, then the agent will decide to rewrite the query again and retry again. If it is still strong, then it will ask for another tool, like web search or API, to get the answer.









Top RAG interview questions you should prepare
For a Senior AI Engineer / AI Architect interview, prioritize these:
1.	What is RAG and why use it instead of fine-tuning?
2.	Explain a production RAG architecture end-to-end.
3.	Naive RAG vs Advanced RAG?
4.	Vector search vs BM25 vs Hybrid Search?
5.	Why do we need reranking after retrieval?
6.	How do you choose chunk size and chunk overlap?
7.	Parent-child vs semantic chunking?
8.	How do you handle poor retrieval and hallucinations?
9.	What are query rewriting, multi-query and HyDE?
10.	What is Hybrid RAG and when would you use it?
11.	What is Self-RAG vs Corrective RAG?
12.	What is Adaptive RAG?
13.	What is Graph RAG and when is it better than vector RAG?
14.	What is Agentic RAG and how is it different from traditional RAG?
15.	How do you evaluate RAG: Recall@K, Precision@K, MRR/NDCG, context relevance, faithfulness, answer correctness and latency/cost?
The highest-value sequence for interviews is:
Naive RAG → Advanced RAG → Hybrid Search → Reranking → Parent-Child → Query Transformation → Corrective/Adaptive RAG → Graph RAG → Agentic RAG → RAG Evaluation.

10 retrieved chunks ordered by similarity:
Chunk 1: 0.95 relevance (start - LLM pays attention)
Chunk 2: 0.93
Chunk 3: 0.91
Chunk 4: 0.89
Chunk 5: 0.87 -> THE ACTUAL ANSWER IS HERE
Chunk 6: 0.85
Chunk 10: 0.75 (end - LLM pays attention)
Problem: LIM focuses on chunks 1-3 and 9-10, skips chunk 5.










1. Simple RAG
Question
   ↓
Embedding
   ↓
Vector DB → Top-K chunks
   ↓
LLM
   ↓
Answer


Example: "What is our maternity leave policy?" → similarity search finds relevant HR-policy chunks → LLM answers using them.
2.Advanced Hybrid RAG (used in production)
It's a combination of Keyword Search and Semantic Search. Keywords Search is BM-25, and Semantic Search is Vectors Cosine.
                                  ┌→   BM25  ────┐
Question → Query ┤                                ├→ Fusion → Reranker → Top 5 → LLM
                                  └→ Vector ──—─┘

How are result combined - RRF - Reciprocal Rank Fussion

This is one of the most important architectures for interviews. BM25 catches exact terms such as INC-12345, product names and error codes, while vector search catches semantic meaning. Reranking then improves precision.
3. Adaptive / Corrective RAG
Question
   ↓
Query Router
   ↓
Need retrieval?
  /         \
No          Yes
↓               ↓
LLM      Retrieve
               ↓
         Relevant?
          /        \
     Yes      No
      ↓         ↓
    LLM    Rewrite Query
                  ↓
            Retrieve again

The important production idea is that retrieval itself becomes conditional rather than blindly running vector search for every request.
Self-Corrective RAG == corrective RAG
Self-Corrective RAG = RAG that detects when retrieval or the generated answer is poor and tries to correct it automatically.
Think of it as:
Retrieve → Check → If bad, fix → Generate → Check again

4. Graph RAG
Suppose the question is:
“Which applications could be affected if Service A fails?”
Vector similarity alone may struggle because the answer depends on relationships.
Service A
   ↓ depends-on
Database B
   ↓ used-by
Application C
   ↓ supports
Business Process D

Graph RAG is valuable when relationships, entities and multi-hop reasoning matter.
What is Graph RAG and when would you use it over standard RAG?
Answer:
Graph RAG combines vector retrieval with a knowledge graph. Instead of just finding similar chunks, it traverses relationships between entities. 

Standard RAG retrieves isolated text chunks. Graph RAG understands connections: 'Person A works at Company B, which is a subsidiary of Company C, which operates in Industry D.' 

When to use Graph RAG: 
(1) Questions involving relationships ('Who reports to the VP of Engineering?'). 
(2) Multi-hop reasoning (What products does the parent company of our supplier make?'). 
(3) Entity-centric queries (Tell me everything about Client X across all documents').
(4) Global questions ('What are the main themes across all 1000 documents?).

Microsoft's GraphRAG implementation uses LLMs to extract entities and relationships from documents, builds a community hierarchy, and generates summaries at different levels.

EX: Alice ->Project AP -> works -AWS
Use when the relationship is there. Legal document, company document, such kind of scenario


Standard RAG VS Graph RAG:
Question: 'Which customers are affected by the Acme Corp supply chain disruption?'
Standard RAG:

Searches for 'Acme Corp supply chain disruption'
Finds: 'Acme Corp reported delays in chip manufacturing' Answor: 'Acme Corp has supply chain issues' (incomplete)

Graph RAG:
Step 1: FindAcme Corp  in knowledge graph
Step 2: Traverse: Acme Corp [supplies_tof-> WidgetCo, TechInc, DataCorp Step 3: Traverse: Widgetto -|sell$_to]-> Customer A, Customer B Step 4: Traverse: IechInc - [sells_to]-> Customer C
Answer: 'Customers A, B (through WidgetCo) and Customer C (through TechInc) are affected by Acme Corp supply chain disruption. '

Graph RAG connects dots that standard RAG can't.
• Interview Tip: Say ' use Graph RAG when questions involve relationships or require connecting information across multiple documents. For simple Q&A;;, standard RAG is sufficient.' Knowing when NOT to use it is as important as knowing when to use it.

 

 
 

5. Agentic RAG — most sophisticated common pattern

        User Question
               ↓
       Planner / Agent
                ↓
 ┌────┼────────┐
 ↓             ↓                       ↓
Vector     SQL                API
Search     DB                Search
 ↓                ↓                    ↓
 └─────┼───────┘
                  ↓
      Evidence Evaluation
                  ↓
Enough evidence? ──No──→ Rewrite / Retrieve again
                 │
                Yes
                 ↓
              LLM
                 ↓
       Grounded Answer + Citations


This is where frameworks such as LangGraph become useful: retrieval is no longer a single function call; the system can route, retrieve, validate, retry, call multiple tools and maintain state.

What is Agentic RAG, and how does it integrate planning and retrieval? - MODULER RAG
Agentic RAG is when RAG is combined with agent-like behaviour.
Instead of just retrieving once and generating an answer, the model can plan multiple steps, refine its query(query rewriting), retrieve again, and even decide which tools or data sources to use. This planning-and-retrieval loop makes it more interactive and Flexible.

For example, if the first retrieval is weak, an Agentic RAG system can rewrite the question and try again, just like a researcher would. This approach is powerful for complex or multi-step tasks, because it doesn't settle for the first result-it actively reasons about how to get the best context.

Here it is trying to search from the company-owned data. If it is not able to do that, the agent (agentic RAG) decides it will search from the external tool, like web search. (tmy)

Here, from DK, it actually checks the answer. If the answer is not relevant or the answer is not full, then it is asked to rewrite the query from the LLM, and it generates again and checks again.

What is Agentic RAG and how is it different from standard RAG?
“Here, the agent actually thinks, plans, and decides. Based on the retrieved context”
In standard RAG, the retrieval pipeline is fixed - same query, same retriever, same top-K, one shot. In Agentic RAG, an Al agent controls the entire retrieval process dynamically. 
The agent: 
1)	Decides WHEN to retrieve — maybe the question doesn't need retrieval at all. 
2)	Decides WHAT to search — reformulates queries, tries different search strategies. (3) Evaluates results - checks if retrieved chunks actually answer the question. 
3)	Iterates — if results are poor, the agent tries different queries, different indexes, or different strategies. 
4)	(Routes - sends different queries to different knowledge bases. 
5)	Combines tools — can use RAG + SQL queries + API calls + web search together. 

The key difference: standard RAG is a pipeline, Agentic RAG is a decision-making system.

 



Modular RAG means designing RAG as a set of independent, replaceable components/modules rather than one fixed retrieve → LLM pipeline.
A simple RAG is:
A Modular RAG can look like:Start: Modular rag is an advanced rag where we are optimising our retrieval strategy. Every retrieval strategy works as a module. It's kind of like a Lego block where every module works independently.
For example, if we are doing the search in a vector database, we are optimising our query and getting a result from the vector database. Suppose the query output is not sufficient enough, so we need an external tool to search the query differently. What we are doing is that, in parallel, we are doing the search, and both the parallel module outputs are combined and re-ranked. Based on that re-ranking, we are finding the relevant change, then we are building the prompt, and based on that prompt, we are submitting to the LLM. 


               User Query
                        ↓
                 Query Rewriter
                        ↓
              Metadata / ACL Filter
                        ↓
           ┌─       ┴────┐
           ↓                         ↓
         BM25                 Vector
           ↓                         ↓
             ─        ┬─       ┘
                        ↓
                       RRF
                        ↓
                    Reranker
                        ↓
               Context Compressor
                        ↓
                     Top-K
                        ↓
                       LLM
                        ↓
              Answer + Citations



              


def rewrite_query(question):
    return question

def retrieve(query):
    return hybrid_search(query)

def rerank(query, documents):
    return documents[:5]

def build_context(documents):
    return "\n".join(
        doc.page_content for doc in documents
    )

def generate(question, context):
    return llm.invoke(
        f"Context:\n{context}\n\nQuestion:{question}"
    )

question = "What caused INC-101?"
query = rewrite_query(question)
documents = retrieve(query)
documents = rerank(query, documents)
context = build_context(documents)
answer = generate(question, context)
print(answer.content)




 

What is Multi-Index RAG and when do you use it?
Answer:
Multi-Index RAG maintains multiple separate vector indexes optimized for different types of content, then routes queries to the right index. Instead of dumping everything into one big index, you create specialized indexes that handle their content type better. 

Types of indexes: 
(1) Summary index - stores document-level summaries for broad questions.
(2) Chunk index - stores granular chunks for specific detail questions. 
(3) Table index - stores structured/tabular data separately with specialized retrieval. 
(4) KG index - stores knowledge graph triples for relationship queries. 

A router (LLM or classifier) decides which index to search based on the query type.
Example:
Enterprise knowledge base with mixed content:

Index 1 - Text chunks:
Company policies, procedures, guides -> standard RAG retrieval

Index 2 - Summaries:
Document-level summaries - for broad questions like 'What topics does the handbook cover?'

Index 3 - Tables:
Financial data, pricing tables, comparison matrices -> structured retrieval

Index 4 - Q&A; pairs:
Pre-existing FAQ pairs -> exact match retrieval

Query routing:

'What is our vacation policy?' - Routes to Index 1 (text chunks)
'Give me an overview of the employee handbook' -> Routes to Index 2 (summaries)
'What was 03 EBITDA?' -> Routes to Index 3 (tables)


 

Actually, we are trying to understand what the difference is between a bi-encoder and a cross-encoder. A bi-encoder is a technology where it is happening when we are getting the first 20 records as a chunk when we are doing the cosine similarity. After that, when we are doing the re-ranking and we are getting the three records out of 20, that is done by the encoder. These two are the different areas that are tackled here.


 









How do you evaluate a RAG system? What metrics do you use?
 Answer:
 RAG evaluation has two parts - retrieval quality and generation quality. 
1.	Retrieval metrics: 
a.	Hit Rate / Recall@K — does the correct chunk appear in the top K results? 
b.	MRR (Mean Reciprocal Rank) — how high is the correct chunk ranked? 
c.	NDCG - measures ranking quality considering relevance grades. 
2.	Generation metrics: 
a.	Faithfulness - does the answer stick to the retrieved context? No hallucination? 
b.	Answer Relevancy — does the answer actually address the question?
(6) Context Relevancy - are the retrieved chunks relevant to the question? 
c.	Context Utilization - does the answer use all relevant retrieved information? 

RAGAS (Retrieval Augmented Generation Assessment) is an open source framework that automatically evaluates RAG systems using LLM based, reference free metrics such as faithfulness, answer relevance, and context quality .

What RAGAS Is?
RAGAS is a Python framework designed to grade Retrieval Augmented Generation pipelines without requiring human written ground truth answers. It evaluates how well a RAG system retrieves information and how faithfully the LLM uses that information when generating answers. It was introduced in a 2023 research paper and is widely used in industry for automated RAG evaluation.

The RAGAS framework automates all of these using LLM-as-judge.
 Example:
 Evaluating a customer support RAG:
 Test set: 200 questions with ground truth answers
 
Retrieval evaluation: -Getting the chunks.
 Hit Rate@5: 0.87 (878 of time, correct chunk in top 5)
 MRR: 0.72 (correct chunk is usually ranked Ist or 2nd)

Generation evaluation (using RAGAS) : - When the LLM calls, it is giving the answer which is checked by these three parameters.
 Faithfulness: 0.91 (918 of claims are grounded in context)
 Answer Relevancy: 0.88 (888 of answers address the question)
 Context Relevancy: 0.79 (21% of retrieved context is irrelevant)
 
Diagnosis:
 Retrieval is good (878 hit rate)
 But context has noise (798 relevancy) -> need better rerankina -- make this note fo me
RAGAS -It's a framework that evaluates the LLM without human intervention. It also checks end to end from question to the answer generated of the RAG system.
 

 

 


 

 
 

How does Graph RAG differ from traditional RAG? NEED PRACTICAL???
Graph RAG is different from traditional RAG because instead of retrieving plain text chunks, it retrieves information from a knowledge graph. A knowledge graph stores data as entities and relationships, like "Alice works at Microsoft" or "Diabetes is linked to high blood sugar."

This structure makes it easier to answer complex, multi-hop questions that need reasoning across connections. For example, in healthcare, Graph RAG can link symptoms → diseases → treatments in a way plain text retrieval cannot. In short, traditional RAG finds text, while Graph RAG finds facts and relationships, making the answers more structured and explainable.

What role does HyDE (Hypothetical Document Embedding) play in RAG?
Here, the LLM actually checks the answer and generates a dummy version of the hypothetical answer from the question, and that answer then goes back to the vector and serves the semantic meaning, which gives a proper. 
“HyDE, or Hypothetical Document Embedding, is a clever trick used in RAG to improve retrieval. Instead of sending the raw use query to the retriever, the LLM first generates a short
"hypothetical answer" or draft document to that query. That draft is then converted into embeddings and used to search the database.”

The idea is that the generated text captures the intent of the question more fully than just the query alone, so retrieval finds more relevant documents. This approach is especially useful for vague or complex queries, where a simple keyword or embedding search might miss the right context.

The Raw Query: "Why is my Node.js API intermittently returning 502 errors on Azure?"
•	Traditional RAG (Without HyDE): The system converts this exact sentence into an embedding. Because the query is short, the vector search relies heavily on the surface-level terms "Node.js," "502," and "Azure." It likely retrieves generic Azure documentation defining what a 502 error is, rather than actionable troubleshooting steps.
•	The HyDE Approach:
1.	Drafting the Hypothetical Answer: Before querying the vector database, the LLM intercepts the prompt and writes a confident (even if unverified) response: "A 502 Bad Gateway on an Azure Web App running Node.js typically happens when the application container crashes or the Node server exhausts its database connection pool. Common causes include unhandled promise rejections, blocking the event loop with heavy synchronous operations, or the Azure load balancer timing out."
2.	Embedding the Draft: This entire generated paragraph is converted into a vector embedding.
3.	Retrieving with Context: The system searches the database using this rich, detailed paragraph instead of the short raw query.
The Result: Because the hypothetical answer introduces specific technical vocabulary ("connection pool", "event loop", "container crash", "unhandled promise rejections"), the search space shifts dramatically. It bypasses the generic glossaries and successfully pulls deep technical documentation, internal runbooks, or specific architectural guides that perfectly match the semantic density of the actual solution.





 

A citation in generative AI is a reference or footnote that connects a specific claim in a model's generated response directly back to the external source document or paragraph where that information was retrieved.

While traditional search engines return links and standalone LLMs return synthesized text, citations are the bridge that connects the two—transforming a generic AI response into a verifiable, trustworthy document.
 

Why Citations are Crucial
1.	Defeating Hallucinations: Large language models optimize for fluency and word probability rather than factual truth. Without constraints, a model can easily hallucinate fake facts or generate entirely fabricated sources (such as fake research papers, fake authors, or fake journal names that look real but do not exist). Citations prove that the output is grounded in actual retrieved evidence.
2.	Fact-Checking & Auditing: In high-stakes fields like medicine, legal review, and corporate search, accuracy is non-negotiable. Inline citations (like clickable footnotes) allow users to quickly audit a system's output by jumping directly to the exact paragraph or page in the source material. This eliminates the need for humans to manually read through massive files to verify if the AI made a mistake

How do you build RAG over tables, charts, and images (Multimodal RAG)?
Answer:
Standard RAG only handles text. Multimodal RAG extends it to tables, images, charts, and other non-text content. Approaches: 
➢	Tables: Extract tables from documents -> convert to markdown/CSV chunk and embed as text. Or use specialized table embeddings. For complex tables, convert to natural language descriptions. 
➢	Images/Charts: Use a vision model (GPT-4V, Claude Vision) to generate text descriptions of images/charts > embed the descriptions. Store original image for display.
➢	Mixed documents: Use Unstructured.io to parse PDFs into text + table + image elements. Process each element type differently. 
➢	ColPali approach: Embed entire document pages as images using vision-language models, bypassing text extraction entirely. Emerging approach gaining traction in 2026.


PDF
   ↓
TEXT - text-embedding
Table - Table parser
Image - There are vision model  like OCR and CLIP.
   ↓
Vector DB
   ↓
Retrviver(top K)
   ↓
LLM



Your RAG system is hallucinating despite having the right documents. How do you fix it?
Answer:
Systematic debugging approach: 
1.	Check retrieval first - are the right chunks being retrieved? If not, it's a retrieval problem (better embeddings, chunking, hybrid search). 
2.	Check if the answer is in  the chunks — manually verify. If the answer IS in the retrieved text but the LLM ignores it, it's a generation problem.
3.	 Prompt engineering fixes: Add 'Answer ONLY based on the provided context. If the context doesn't contain the answer, say I don't know.'
4.	Reduce distracting context — fewer chunks, reranking, compression. 
5.	Use structured output - force the LLM to cite sources for each claim. 
6.	Add a faithfulness check — post-generation, use a separate LLM call to verify each claim against the context. 
7.	Try a stronger model — more capable models follow grounding instructions better.

Simple:
1.	Verify retrieval.
2.	Verify prompt: poor point leads to poor retrieval.
3.	Reduce Context Noise
4.	Ad re-rankers.
5.	Improves chunking
6.	Do evaluation with langsmith and so on.

 


How do you optimize RAG latency for real-time applications?
RAG latency ≈ Query processing + Retrieval + Reranking + LLM generation + Network/orchestration overhead
Answer:
RAG latency has three components: embedding latency (query embedding), retrieval latency (vector search), and generation latency (LLM response). 

Optimizations: 
(1) Embedding: Use smaller embedding models (384 dims vs 3072). Cache frequent query embeddings. 
(2) Retrieval: Use HNSW index (fastest). Pre-filter with metadata before vector search. Use approximate search (lower ef values).
(3) Reranking: Use fast rerankers (Cohere) or skip for simple queries. 
(4) Generation: Use streaming (show tokens as they generate). Use faster models (GPT-40-mini, Haiku) for simple queries. Reduce context size (fewer chunks, compression). 
(5) Caching: Semantic cache — if a similar question was asked before, return the cached answer. Can eliminate 30-50% of LLM calls. 
(6) Async parallel: Run retrieval and reranking in parallel across multiple indexes.

1.	Fast Embeding  model
2.	Efficient vector
3.	Hybrid
4.	Cashew.
5.	praller processing.
6.	Stream respawn


How do you handle multi-turn conversations in RAG?
Answer:
In multi-turn chat, the user's latest message often references previous context: 'What about the premium plan?' only makes sense if the previous message was about pricing. 

Strategies: 
(1)	Conversation-aware query rewriting - use the LLM to rewrite the latest message incorporating conversation history. 'What about the premium plan?' -> What are the features and pricing of the premium plan?' 
(2)	Chat history in context - include the last 3-5 turns in the prompt alongside retrieved chunks. But be careful of context window limits.
(3)	Conversation summarization - summarize older turns to save tokens. Keep last 2-3 turns verbatim, summarize the rest.
(4)	Session-based retrieval - maintain a per-session context buffer of previously retrieved chunks. If the new query is related, include previous chunks without re-retrieving. 
(5)	Coreference resolution - resolve pronouns and references (it', that', the previous one') before retrieval.





1.	Store the conversation memory - Using append + summary
2.	Query Rewriting
3.	Memory Type: 
a.	Shorter Memory - To capture the short-term memory
b.	In long memory - This is to capture the long-term information, like caching.

 














How do you design caching strategies for RAG to reduce cost/latency?
Caching in RAG helps cut down both cost and latency by reusing results instead of repeating the same work. One strategy is query-level caching-if the same or very similar query comes again, return the stored retrieval results instead of searching the database again.

Another is embedding caching-store the vector representations so you don't recompute them each time. You can also cache common responses from the LLM for FAQs or repeated tasks. The challenge is balancing freshness with speed, since cached results may get outdated if the underlying data changes. Done right, caching makes RAG systems faster and cheaper.

What are the most common failure points in a RAG system?
1.	First is at the chunking level where we are doing the wrong chunking.
2.	Second is at the retrieval layer, where the actually retrieved chunk is wrong, Case: even if the LLM produces a, it is working fine. It will not work.
3.	This is at the Generative level, where the chunking is right. Retrieval is right, but the LLM itself is hallucinating.

https://medium.com/@devesh-kr-sri/ai-project-question-7ce331c79f5e


Give an example of how RAG is used in enterprise search.
In enterprise search, RAG is used to make company knowledge easily accessible. For example, instead of employees digging through SharePoint, emails, or PDFs, they can just ask a natural question like "What's our policy on remote work?" The system retrieves the most relevant documents from internal sources and then the LLM generates a clear, summarized answer.

This saves time, reduces confusion, and ensures people get accurate information quickly. Microsoft 365 Copilot is a real-world example-it uses RAG to ground answers in Microsoft Graph data like Teams chats, Word files, and Outlook emails.

That information is then fed into the LLM to generate answers that are both accurate and specific to your work. For example, in Outlook, it can draft a reply using details from a related document, or in Excel, it can summarize trends using your company data. RAG makes Copilot grounded, trustworthy, and enterprise-ready.





































































AI Mode conversation: what is adaptive rag
what is adaptive rag
Adaptive Retrieval-Augmented Generation (Adaptive RAG) is an advanced AI framework that dynamically adjusts its data retrieval strategy based on the complexity of a user's query. Introduced in a 2024 research paper by Soyeong Jeong et al., it moves away from standard RAG systems that execute the exact same retrieval pipeline for every question, regardless of whether it is simple or complex. [1, 2, 3, 4]
Instead, Adaptive RAG uses a smaller classifier (a fast language model) to evaluate the query upfront. It then routes the request through one of three pathways to maximize accuracy while minimizing computational cost and time. [1, 2, 3, 4]
 
How Adaptive RAG Routes Queries
Depending on the question's difficulty, the system intelligently selects the most efficient route:
Complexity Level	Strategy Used	Example Query	How It Works
Low	No Retrieval	"What is machine learning?"	The system relies purely on the LLM's pre-trained internal knowledge, skipping the database search entirely to save time.
Medium	Single-Step Retrieval	"How does OAuth2 work?"	The system queries a single database or vector store once, retrieves the relevant documentation, and answers the prompt.
High	Multi-Step / Iterative Retrieval	"Compare caching strategies in microservices architectures."	The system breaks the question down into multiple steps, pulls from various external sources, and cross-references data dynamically.
 
Key Technical Characteristics
●	Upfront Query Analysis: It assesses user intent, urgency, and necessary data depth before taking action. [1, 2]
●	Multi-Source Flexibility: It can query internal vector databases, fetch real-time data from web search engines, or consult live external APIs depending on what the question demands. [1, 2]
●	Self-Correction & Flow Engineering: Advanced implementations (often built using orchestration frameworks like LangGraph) include automated evaluation steps. These steps grade document relevance and check the output for hallucinations before serving it to the user. [1, 2]
Standard RAG systems suffer from two main flaws: they waste expensive computing resources performing deep lookups for easy questions, and they fail on complex queries because a single search cannot capture all necessary context. Adaptive RAG solves both issues, ensuring applications like enterprise chatbots and research tools run significantly faster, cost less to operate, and deliver highly accurate, contextual answers. [1, 2, 3, 4]

What is a reranker? When and why do you add it to a RAG pipeline?

For an interview, I’d prioritize Cross-Encoder → LLM reranking → RRF/fusion, while being explicit that RRF belongs to the fusion stage.

How a Reranker Works:
• Stage 1 — Fast retrieval: Vector search returns top-20 candidates in ~20ms.
• Stage 2 — Precise reranking: Cross-encoder reads BOTH query AND each chunk together and scores
their relevance (not just similarity). Returns top-5.

Cross-encoder advantage: sees the relationship between query and document, not just individual
Embeddings.

Popular Rerankers:
1. Cross-Encoder reranker• cross-encoder/ms-marco-MiniLM (HuggingFace) — open source, good quality• BGE-Reranker-v2 (BAAI) — state-of-the-art open source 2025
2. LLM-based reranking- LLM judges relevance/order, Complex/high-value queries, latency high
3. Score/Rank fusion - Combines multiple retrieval rankings, Hybrid retrieval, Low latency 







How would you design a production RAG architecture for thousands of enterprise users?Also, I want to see a very low latency. How to fix that? Thousands or millions of users using the system at once. Give me a bullet point reference in ten bullet points. 

1.	Stateless API Layer — Put FastAPI/Node services behind API Gateway + Load Balancer; scale horizontally with Kubernetes/ECS/AKS. Never keep user session state inside application pods.
2.	Separate Offline and Online RAG — Offline pipeline handles ingestion → parsing → chunking → embeddings → indexing. Online pipeline only handles query → retrieve → rerank → generate, keeping request latency low.
3.	Use Hybrid Retrieval — Combine BM25 keyword search + vector search. This gives exact-match precision plus semantic matching. For enterprise workloads, use scalable engines such as Azure AI Search, OpenSearch, Elasticsearch, Pinecone, or equivalent.
4.	Optimize Vector Search — Use ANN indexes such as HNSW, metadata pre-filtering, partitioning/sharding, and sensible top_k such as 10–30. Avoid searching millions of vectors exhaustively.
5.	Rerank Only a Small Candidate Set — Retrieve maybe 20–50 chunks, rerank them, and send only the best 3–8 chunks to the LLM. Do not rerank hundreds or thousands of documents per request.
6.	Multi-Level Caching — Use Redis for exact-query cache, semantic-answer cache, query-embedding cache, retrieval-result cache, and frequently accessed metadata. Cache hits can bypass embedding, retrieval, reranking, and sometimes even the LLM.
7.	Model Routing — Do not send every query to the biggest model. Route simple questions to a small/fast model, complex reasoning to a stronger model, and reject or answer deterministic requests without an LLM when possible. This reduces both latency and cost.
8.	Parallelize the Pipeline — Run independent operations concurrently: authentication/context lookup, query classification, metadata retrieval, BM25 search, and vector search. Then fuse results using RRF → reranker → LLM instead of executing everything sequentially.
9.	Scale for Millions of Requests — Use autoscaling, queues, rate limits, backpressure, circuit breakers, retries with jitter, connection pooling, regional deployment, read replicas, index sharding, and tenant isolation. Design for graceful degradation when the LLM or search service is overloaded.
10.	Measure Latency Stage-by-Stage — Track p50/p95/p99 for API → embedding → BM25/vector search → reranking → LLM TTFT → total response. A practical low-latency target is roughly: retrieval <100–200 ms, reranking <100–300 ms, TTFT <500–1000 ms, with streaming immediately after first token.
Reference architecture:
 Users → CDN/WAF → API Gateway → Load Balancer → RAG API → Redis Cache → Query Router → [BM25 || Vector Search] → RRF → Reranker → LLM Router → Streaming Response
For an interview, the strongest one-line answer is: “I achieve enterprise RAG scale by making the API stateless, horizontally scaling compute and search, using hybrid ANN retrieval, aggressively caching, parallelizing independent stages, routing across models, minimizing retrieved context, and monitoring p95/p99 latency at every RAG stage


<img width="451" height="675" alt="image" src="https://github.com/user-attachments/assets/76eb802d-189a-422f-9ef2-ad131fcac6c7" />


```
