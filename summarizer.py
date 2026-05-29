import re
from typing import Optional
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
_tokenizer: Optional[AutoTokenizer] = None
_model: Optional[AutoModelForSeq2SeqLM] = None
def _get_t5():
    global _tokenizer, _model
    if _model is None:
        _tokenizer = AutoTokenizer.from_pretrained("t5-small")
        _model = AutoModelForSeq2SeqLM.from_pretrained("t5-small")
    return _tokenizer, _model
def _split_sentences(text: str) -> list[str]:
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sentences if s.strip()]
def _extractive_summarize(text: str, num_sentences: int = 3) -> str:
    sentences = _split_sentences(text)
    if len(sentences) <= num_sentences:
        return text
    vectorizer = TfidfVectorizer(stop_words=None)
    tfidf_matrix = vectorizer.fit_transform(sentences)
    sim_matrix = cosine_similarity(tfidf_matrix)
    scores = sim_matrix.sum(axis=1).flatten()
    ranked = scores.argsort()[-num_sentences:][::-1]
    ranked.sort()
    return " ".join(sentences[i] for i in ranked)
def _extractive_bullets(text: str, num_points: int = 5) -> list[str]:
    sentences = _split_sentences(text)
    if len(sentences) <= num_points:
        return sentences
    vectorizer = TfidfVectorizer(stop_words=None)
    tfidf_matrix = vectorizer.fit_transform(sentences)
    sim_matrix = cosine_similarity(tfidf_matrix)
    scores = sim_matrix.sum(axis=1).flatten()
    ranked = scores.argsort()[-num_points:][::-1]
    return [sentences[i] for i in ranked]
def summarize(transcript: dict) -> dict:
    text = transcript["text"]
    lang = transcript.get("language", "unknown")
    if lang.startswith("en"):
        tokenizer, model = _get_t5()
        inputs = tokenizer(
            "summarize: " + text,
            max_length=1024,
            return_tensors="pt",
            truncation=True,
        )
        summary_ids = model.generate(
            inputs["input_ids"],
            max_length=150,
            min_length=30,
            num_beams=4,
            early_stopping=True,
        )
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        bullet_points = _extractive_bullets(text)
    else:
        summary = _extractive_summarize(text)
        bullet_points = _extractive_bullets(text)
    return {
        "summary": summary,
        "bullet_points": bullet_points,
        "language": lang,
    }