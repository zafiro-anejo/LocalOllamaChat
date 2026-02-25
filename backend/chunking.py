import re
from ollama import chat
from tqdm import tqdm
from config import (
    CHUNKING_LLM_MODEL, CHUNKING_SPLIT_PATTERN,
    MIN_CHUNK_WORDS, MAX_CHUNK_WORDS
)
from prompts import CHUNKING_PROMPT_TEMPLATE, CONTEXTUALIZER_PROMPT

def call_llm(prompt: str) -> str:
    try:
        response = chat(
            model=CHUNKING_LLM_MODEL,
            messages=[{"role": "user", "content": prompt}],
            keep_alive="-1h",
            options={
                "num_ctx": 16384,
                "temperature": 0.0,
                "min_p": 0.01,
                "repeat_penalty": 1.0,
                "top_k": 64,
                "top_p": 0.95
            }
        )
        return response.message.content
    except Exception:
        return ""

def build_dynamic_chunks(document_text: str):
    raw_chunks = document_text.split(CHUNKING_SPLIT_PATTERN)
    for i in range(1, len(raw_chunks)):
        raw_chunks[i] = "#" + raw_chunks[i]

    chunked_text = ""
    for n, chunk in enumerate(raw_chunks):
        chunked_text += f"<|start_chunk_{n}|>\n{chunk}<|end_chunk_{n}|>\n"

    prompt = (CHUNKING_PROMPT_TEMPLATE
              .replace("{MIN_CHUNK_WORDS}", str(MIN_CHUNK_WORDS))
              .replace("{MAX_CHUNK_WORDS}", str(MAX_CHUNK_WORDS))
              .format(document_text=chunked_text))

    response = call_llm(prompt)

    split_after = []
    if "split_after:" in response:
        split_points = response.split("split_after:")[1].strip()
        split_after = [int(x.strip()) for x in split_points.split(",") if x.strip().isdigit()]

    if not split_after:
        sections = [chunked_text]
    else:
        chunk_pattern = r"<\|start_chunk_(\d+)\|>(.*?)<\|end_chunk_\1\|>"
        chunks = re.findall(chunk_pattern, chunked_text, re.DOTALL)
        sections = []
        current_section = []
        for chunk_id, chunk_text in chunks:
            current_section.append(chunk_text)
            if int(chunk_id) in split_after:
                sections.append("".join(current_section).strip())
                current_section = []
        if current_section:
            sections.append("".join(current_section).strip())

    contexts = []
    for sec in tqdm(sections, desc="Contextualizing chunks"):
        prompt = CONTEXTUALIZER_PROMPT.format(document=document_text, chunk=sec)
        ctx = call_llm(prompt)
        contexts.append(ctx)

    final_chunks = []
    for chunk, context in zip(sections, contexts):
        final_chunks.append(f"<chunk_context>{context}</chunk_context>\n<chunk>{chunk}</chunk>")

    return final_chunks