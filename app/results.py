import pickle
from pathlib import Path
from collections import Counter

file = open('results/crawler_labels.pkl', 'rb')
data = pickle.load(file)
file.close()

compliant = []
non_compliant = []
in_review = []
not_converted = []
for item in data:
    match data[item]:
        case 'False':
            non_compliant.append(item)
        case 'True':
            compliant.append(item)
        case 'review':
            in_review.append(item)
        case 'not-converted':
            not_converted.append(item)

f = open("results/compliant.txt", "w")
f.write('\n'.join(compliant))
f.close()

f = open("results/non_compliant.txt", "w")
f.write('\n'.join(non_compliant))
f.close()

f = open("results/in_review.txt", "w")
f.write('\n'.join(in_review))
f.close()

f = open("results/not_converted.txt", "w")
f.write('\n'.join(not_converted))
f.close()

suffixes = []
for file_path in not_converted:
    suffix = Path(file_path).suffix
    suffixes.append(suffix)

print(Counter(suffixes))
