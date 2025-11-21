    def generate(self, max_words=30):
        # If not fitted or no data, return empty string (tests expect this)
        if not self.fitted:
            return ""

        # If vocabulary is too small (less than 3 words), return what we can
        if len(self.vocab) < 3 or not self.trigrams:
            # join vocab items into a simple string
            return " ".join(list(self.vocab))

        # Pick a random bigram
        bigrams = list(self.trigrams.keys())
        if not bigrams:
            return ""

        w1, w2 = random.choice(bigrams)
        generated = [w1, w2]

        # Generate more words
        for _ in range(max_words - 2):
            next_word = self._sample_next((w1, w2))
            if not next_word:
                break
            generated.append(next_word)
            w1, w2 = w2, next_word

        # Return as string
        return " ".join(generated)
