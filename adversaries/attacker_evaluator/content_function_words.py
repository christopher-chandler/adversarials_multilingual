# Standard
import collections
from collections import Counter
import matplotlib.pyplot as plt

# Pip
# None

# Custom
# None

import spacy


nlp = spacy.load("de_core_news_sm")
text1 = open("Prompt1_de.txt").read()
text2 = open("Prompt2_de.txt").read()
text3 = open("Prompt10_de.txt").read()

doc = nlp(text1 + text2 + text3)
pos = list()

for tok in doc:
    pos.append(tok.pos_)
data = Counter(pos)


sorted_data = dict(sorted(data.items(), key=lambda x: x[1], reverse=True))

# Extract labels and frequencies
labels = list(sorted_data.keys())
values = list(sorted_data.values())

# Plotting
plt.figure(figsize=(10, 6))
plt.bar(labels, values)
plt.xlabel("Part of Speech")
plt.ylabel("Frequency")
plt.title("Frequency of Parts of Speech")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()
if __name__ == "__main__":
    pass
