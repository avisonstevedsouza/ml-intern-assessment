import random
import re
from collections import defaultdict


class TrigramModel:
    def __init__(self):
        # store trigram counts as:
        # (w1, w2) → {w3: count}
        self.trigrams = defaultdict(lambda: defaultdict(int))
        self.vocabulary = set()
        self.fitted = False

    def _clean_text(self, text):
        # Lowercase + keep only words
        text = text.lower()
        words = re.findall(r"\b\w+\b", text)
        return words

    def fit(self, text: str):
        if not text:
            self.fitted = False
            return

        words = self._clean_text(text)

        if len(words) < 3:
            # Not enough to build trigrams
            self.vocabulary = set(words)
            self.fitted = True
            return

        self.vocabulary = set(words)

        # Build trigram counts
        for i in range(len(words) - 2):
            w1, w2, w3 = words[i], words[i + 1], words[i + 2]
            self.trigrams[(w1, w2)][w3] += 1

        self.fitted = True

    def _sample_next_word(self, bigram):
        """Sample next word using trigram probabilities."""
        next_words = self.trigrams.get(bigram, None)

        if not next_words:
            return None

        # Weighted probabilistic sampling
        words = list(next_words.keys())
        counts = list(next_words.values())
        total = sum(counts)
        probs = [c / total for c in counts]

        return random.choices(words, probs)[0]

    def generate(self, max_words=30):
        if not self.fitted:
            return ""

        if len(self.vocabulary) < 3 or not self.trigrams:
            # Not enough data; return whatever text is possible
            return " ".join(list(self.vocabulary))

        # Start from a random bigram
        bigram = random.choice(list(self.trigrams.keys()))
        w1, w2 = bigram
        generated = [w1, w2]

        # Generate iteratively
        for _ in range(max_words - 2):
            w3 = self._sample_next_word((w1, w2))
            if not w3:
                break
            generated.append(w3)
            w1, w2 = w2, w3

        return " ".join(generated)
