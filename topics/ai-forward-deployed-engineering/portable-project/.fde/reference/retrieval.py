"""Retrieval scored on its own, and answers from the context layer that name their source. Standard library only.

Two rankers: keyword overlap (how many distinct query words a document contains) and BM25. The BM25 parameters
k1 = 1.5 and b = 0.75 sit inside the ranges Robertson and Zaragoza report as reasonable; the IDF adds one inside the
logarithm so a very common word scores zero or more, never less. Ties are broken by document id.
"""
from __future__ import annotations

import datetime
import json
import math
import re
from fractions import Fraction
from pathlib import Path

CASES = Path(__file__).resolve().parent.parent / 'cases'


def load_context(path: Path = CASES / 'warranty-context.json') -> dict:
    data = json.loads(path.read_text(encoding='utf-8'))
    if data.get('synthetic') is not True:
        raise ValueError('refusing a fixture that is not marked synthetic')
    return data


def words(text: str) -> list[str]:
    return re.findall(r'[a-z0-9]+', text.lower())


class Index:
    def __init__(self, documents: list[dict]):
        self.documents = {d['id']: d for d in documents}
        self.terms = {d['id']: words(d['title'] + ' ' + d['text']) for d in documents}
        self.average = sum(len(t) for t in self.terms.values()) / len(self.terms)
        self.frequency: dict[str, int] = {}
        for terms in self.terms.values():
            for term in set(terms):
                self.frequency[term] = self.frequency.get(term, 0) + 1

    def overlap(self, query: str) -> dict[str, float]:
        q = set(words(query))
        return {doc: len(q & set(terms)) for doc, terms in self.terms.items()}

    def bm25(self, query: str, k1: float = 1.5, b: float = 0.75) -> dict[str, float]:
        n = len(self.terms)
        scores = {}
        for doc, terms in self.terms.items():
            score = 0.0
            for term in set(words(query)):
                tf = terms.count(term)
                if tf:
                    idf = math.log((n - self.frequency[term] + 0.5) / (self.frequency[term] + 0.5) + 1)
                    score += idf * tf * (k1 + 1) / (tf + k1 * (1 - b + b * len(terms) / self.average))
            scores[doc] = score
        return scores

    def search(self, query: str, method: str = 'bm25') -> list[str]:
        scores = getattr(self, method)(query)
        return sorted(scores, key=lambda doc: (-scores[doc], doc))


def score(ranked: dict[str, list[str]], queries: list[dict], k: int) -> dict[str, Fraction]:
    """Mean recall at k, precision at k and reciprocal rank of the first relevant document, as exact fractions."""
    recall = precision = reciprocal = Fraction(0)
    for q in queries:
        relevant, ranking = set(q['relevant']), ranked[q['id']]
        hits = len(relevant & set(ranking[:k]))
        recall += Fraction(hits, len(relevant))
        precision += Fraction(hits, k)
        reciprocal += next((Fraction(1, i) for i, doc in enumerate(ranking, 1) if doc in relevant), Fraction(0))
    n = len(queries)
    return {'recall_at_k': recall / n, 'precision_at_k': precision / n, 'mrr': reciprocal / n}


def is_stale(reviewed_on: str, today: str, max_age_days: int) -> bool:
    age = datetime.date.fromisoformat(today) - datetime.date.fromisoformat(reviewed_on)
    return age.days > max_age_days


def answer(index: Index, query: str, today: str, max_age_days: int) -> dict:
    """The best document for the query, with the governance fields an answer must carry."""
    doc = index.documents[index.search(query)[0]]
    return {'source': doc['id'], 'title': doc['title'], 'owner': doc['owner'], 'reviewed_on': doc['reviewed_on'],
            'stale': is_stale(doc['reviewed_on'], today, max_age_days), 'text': doc['text']}
