import pickle
from pathlib import Path
from collections import Counter

file = open('results/crawler_labels.pkl', 'rb')
data = pickle.load(file)
file.close()

compliant = []
non_compliant = []
in_review = []
for item in data:
    match data[item]:
        case 'False':
            non_compliant.append(item)
        case 'True':
            compliant.append(item)
        case 'review':
            in_review.append(item)

f = open("results/compliant.txt", "w")
f.write('\n'.join(compliant))
f.close()

f = open("results/non_compliant.txt", "w")
f.write('\n'.join(non_compliant))
f.close()

suffixes = []
for file_path in in_review:
    suffix = Path(file_path).suffix
    suffixes.append(suffix)

print(Counter(suffixes))
