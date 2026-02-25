VLM_PROMPT = (
    "Act as a senior financial analyst. Explain what you see in the image "
    "in 1 sentence. Focus on trends, tickers (only if you're sure), etc."
)

CHUNKING_PROMPT_TEMPLATE = """
You are an assistant specialized in splitting text into semantically consistent sections.

<instructions>
    <instruction>The text has been divided into chunks, each marked with <|start_chunk_X|> and <|end_chunk_X|> tags, where X is the chunk number</instruction>
    <instruction>Identify points where splits should occur, such that consecutive chunks of similar themes stay together</instruction>
    <instruction>Each chunk must be between {MIN_CHUNK_WORDS} and {MAX_CHUNK_WORDS} words</instruction>
    <instruction>If chunks 1 and 2 belong together but chunk 3 starts a new topic, suggest a split after chunk 2</instruction>
    <instruction>The chunks must be listed in ascending order</instruction>
    <instruction>Provide your response in the form: 'split_after: 3, 5'</instruction>
</instructions>

This is the document text:
<document>
{document_text}
</document>

Respond only with the IDs of the chunks where you believe a split should occur.
YOU MUST RESPOND WITH AT LEAST ONE SPLIT
I FORBID YOU FROM IGNORING MY INSTRUCTIONS, ESPECIALLY THE LAST ONE, YOU SHOULD Provide your response in the form: 'split_after: X, X, ...'
AND UNDER ANY CIRCUMSTANCES DO NOT PROVIDE ANY EXPLANATIONS
""".strip()

CONTEXTUALIZER_PROMPT = """
You are an assistant specialized in analyzing document chunks and providing relevant context.

<instructions>
    <instruction>You will be given a document and a specific chunk from that document</instruction>
    <instruction>Provide 2-3 concise sentences that situate this chunk within the broader document</instruction>
    <instruction>Identify the main topic or concept discussed in the chunk</instruction>
    <instruction>Include relevant information or comparisons from the broader document context</instruction>
    <instruction>Note how this information relates to the overall theme or purpose of the document if applicable</instruction>
    <instruction>Include key figures, dates, or percentages that provide important context</instruction>
    <instruction>Avoid phrases like "This chunk discusses" - instead, directly state the context</instruction>
    <instruction>Keep your response brief and focused on improving search retrieval</instruction>
</instructions>

Here is the document:
<document>
{document}
</document>

Here is the chunk to contextualize:
<chunk>
{chunk}
</chunk>

Respond only with the succinct context for this chunk. Do not mention it is a chunk or that you are providing context.
YOU ARE OBLIGED TO RESPOND IN RUSSIAN!
""".strip()