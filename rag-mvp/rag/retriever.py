"""Domain-filtered retrieval - the only public entry point is `retrieve()`.

    retrieve(domain, query, top_k=5) -> list[RetrievedChunk]

The MVP backend is a dependency-free TF-IDF / cosine retriever over the chunks
produced by `rag.chunker`. It exists so the whole RAG flow can run and be
integrated today, without Azure. To switch to Azure AI Search later, add a
backend class with the same `.domains` property and `.search(domain, query,
top_k)` method (returning `RetrievedChunk`s) and select it in `_build_backend()`.
Callers never see which backend is in use.
"""
from __future__ import annotations

import math
import re
from collections import Counter
from typing import Iterable, Optional

from .config import DOMAIN_ALIASES, get_settings
from .models import Chunk, RetrievedChunk

# --------------------------------------------------------------------------- #
# Text normalisation (stop words, light stemming, small synonym table)
# --------------------------------------------------------------------------- #
_WORD = re.compile(r"[a-z0-9]+")

_STOPWORDS = frozenset(
    """a about after all am an and any are as at be been being but by can could did do
    does for from get got had has have here how i if in into is it its just like me
    more much my need no not of off on or our out please so some than that the their
    them then there these they this those to too up us very want was we were what
    when where which who why will with would you your tell know also
    should thing things still someone somebody anyone""".split()
)

# Words people use for things the KB words differently. Both queries and chunks
# are normalised through this table (after stemming, so inflections are covered). Deliberately small: it patches the gap that
# a keyword retriever has and will be unnecessary once vector search is in place.
_SYNONYMS = {
    "two": "2", "three": "3", "four": "4", "five": "5", "six": "6",
    "seven": "7", "eight": "8", "nine": "9", "ten": "10",
    "cracked": "damaged", "broken": "damaged", "broke": "damaged",
    "smashed": "damaged", "faulty": "damaged", "defective": "damaged",
    "misplaced": "lost", "missing": "lost", "left": "lost",
    "theft": "stolen", "stole": "stolen", "robbed": "stolen",
    "mobile": "phone", "smartphone": "phone",
    "mail": "email",
    "salary": "payroll", "wages": "payroll", "paycheck": "payroll",
    "vacation": "annual", "pto": "annual",
    "keycard": "badge", "forgot": "forgotten",
    "ac": "hvac", "aircon": "hvac", "freezing": "cold", "chilly": "cold",
    "dripping": "leak", "leaking": "leak",
    "cab": "taxi", "uber": "taxi",
    "client": "visitor", "guest": "visitor", "customer": "visitor",
    "car": "vehicle",
}


def _stem(w: str) -> str:
    if w.isdigit() or len(w) <= 3:
        return w
    if w.endswith("ies") and len(w) > 4:
        w = w[:-3] + "y"
    elif w.endswith("s") and not w.endswith(("ss", "us", "is")):
        w = w[:-1]
    if w.endswith("ing") and len(w) > 5:
        w = w[:-3]
    elif w.endswith("ed") and len(w) > 4:
        w = w[:-2]
    if w.endswith("e") and len(w) > 4:
        w = w[:-1]
    if len(w) > 3 and w[-1] == w[-2] and w[-1] not in "aeiouls":
        w = w[:-1]
    return w


_SYN_STEMS = {_stem(k): _stem(v) for k, v in _SYNONYMS.items()}


def tokenize(text: str) -> list[str]:
    out = []
    for w in _WORD.findall(text.lower()):
        if w in _STOPWORDS or (len(w) < 2 and not w.isdigit()):
            continue
        w = _stem(w)
        out.append(_SYN_STEMS.get(w, w))  # synonyms are matched on stems: "cracked"/"cracks" -> "damag"
    return out


def _index_tokens(chunk: Chunk) -> list[str]:
    # Section title is repeated once so title words weigh more than body words.
    return tokenize(chunk.search_text) + tokenize(chunk.section_title)


# --------------------------------------------------------------------------- #
# Local TF-IDF backend
# --------------------------------------------------------------------------- #
class LocalRetriever:
    """TF-IDF + cosine similarity. Domain filtering happens *before* ranking.

    Query terms that appear nowhere in the KB still count toward the query's
    length, so off-topic queries ("weather in Delhi") score low and fall under
    `min_score` instead of matching on one stray word.
    """

    def __init__(self, chunks: Iterable[Chunk], min_score: float):
        self._chunks = list(chunks)
        self._min_score = min_score
        counts = [Counter(_index_tokens(c)) for c in self._chunks]
        self._n = len(self._chunks)
        self._df: Counter = Counter()
        for c in counts:
            self._df.update(c.keys())
        self._vectors = [self._weigh(c) for c in counts]
        self._by_domain: dict[str, list[int]] = {}
        for i, c in enumerate(self._chunks):
            self._by_domain.setdefault(c.domain, []).append(i)

    @property
    def domains(self) -> list[str]:
        return sorted(self._by_domain)

    def _idf(self, term: str) -> float:
        return math.log((self._n + 1) / (self._df.get(term, 0) + 1)) + 1.0

    def _weigh(self, counts: Counter) -> tuple[dict, float]:
        w = {t: (1.0 + math.log(c)) * self._idf(t) for t, c in counts.items()}
        return w, math.sqrt(sum(v * v for v in w.values()))

    def search(self, domain: str, query: str, top_k: int) -> list[RetrievedChunk]:
        q_counts = Counter(tokenize(query))
        if not q_counts:
            return []
        q_w, q_norm = self._weigh(q_counts)
        scored = []
        for i in self._by_domain.get(domain, []):
            c_w, c_norm = self._vectors[i]
            if not c_norm:
                continue
            dot = sum(wt * c_w[t] for t, wt in q_w.items() if t in c_w)
            score = dot / (q_norm * c_norm)
            if score >= self._min_score:
                scored.append((score, self._chunks[i]))
        scored.sort(key=lambda s: (-s[0], s[1].chunk_id))
        return [
            RetrievedChunk(
                content=c.content,
                score=round(score, 4),
                domain=c.domain,
                document_id=c.document_id,
                section_number=c.section_number,
                section_title=c.section_title,
                source_file=c.source_file,
                chunk_id=c.chunk_id,
                page=c.page,
            )
            for score, c in scored[:top_k]
        ]


# --------------------------------------------------------------------------- #
# Public interface
# --------------------------------------------------------------------------- #
_backend = None


def _build_backend():
    from .chunker import chunk_documents  # local imports keep module import cheap
    from .loader import load_documents

    settings = get_settings()
    if settings.backend == "local":
        chunks = chunk_documents(load_documents(settings.kb_dir))
        return LocalRetriever(chunks, settings.min_score)
    if settings.backend == "azure":
        raise NotImplementedError(
            "RAG_BACKEND=azure is reserved for the Azure AI Search backend, "
            "which is not implemented yet. Use RAG_BACKEND=local."
        )
    raise ValueError(f"Unknown RAG_BACKEND {settings.backend!r} (expected 'local' or 'azure')")


def reset_backend() -> None:
    """Drop the cached index (e.g. after the KB files or settings change)."""
    global _backend
    _backend = None


def normalize_domain(domain: str, known_domains: Iterable[str]) -> str:
    """Map 'it', 'Fees', 'finance / fees', ... to a canonical KB domain name."""
    known = {d.lower(): d for d in known_domains}
    key = (domain or "").strip().lower()
    if key in known:
        return known[key]
    alias = DOMAIN_ALIASES.get(key)
    if alias and alias.lower() in known:
        return known[alias.lower()]
    raise ValueError(f"Unknown domain {domain!r}. Supported domains: {sorted(known.values())}")


def retrieve(domain: str, query: str, top_k: int = 5) -> list[RetrievedChunk]:
    """Return up to `top_k` chunks from `domain` that are relevant to `query`.

    - Only chunks whose domain matches are ever returned (filter, not re-rank).
    - Results are ordered by descending score.
    - Returns [] when nothing is sufficiently relevant, or the query is blank;
      never invents or pads results.
    - Raises ValueError for an unknown domain or top_k < 1.
    """
    global _backend
    if top_k < 1:
        raise ValueError("top_k must be >= 1")
    if _backend is None:
        _backend = _build_backend()
    canonical = normalize_domain(domain, _backend.domains)
    if not query or not query.strip():
        return []
    return _backend.search(canonical, query.strip(), top_k)
