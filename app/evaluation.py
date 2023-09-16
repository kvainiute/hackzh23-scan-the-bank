import csv

def evaluate(labels):
    print(">>")
    print(">> EVALUATION")
    print(">>")
    
    correct = {}

    with open('/app/labels.csv', mode='r') as file:
        csv_reader = csv.DictReader(file)
    
        for row in csv_reader:
            key = row['filename']
            value = row['sensitive'] == "TRUE"
            correct[key] = value
    
    true_true = 0
    true_false = 0
    true_review = 0
    false_false = 0
    false_true = 0
    false_review = 0

    for key in labels:
        if (correct[key] == True):
            if (labels[key] == True):
                true_true += 1
            elif (labels[key] == False):
                print(f"should be true, but is false: {key}")
                true_false += 1
            else:
                true_review += 1
        else:
            if (labels[key] == True):
                false_true += 1
                print(f"should be false, but is true: {key}")
            elif (labels[key] == False):
                false_false += 1
            else:
                false_review += 1
    
    print(f"true_true:   +20 x {true_true}    = {true_true*20}")
    print(f"true_false:  -20 x {true_false}   = {true_false*-20}")
    print(f"true_review: +10 x {true_review}  = {true_review*10}")
    print(f"false_false:  +2 x {false_false}  = {false_false*+2}")
    print(f"false_true:   -2 x {false_true}   = {false_true*-2}")
    print(f"false_review: -1 x {false_review} = {false_review*-1}")
    total = true_true*20 + true_false*-20 + true_review*10 + false_false*2 + false_true*-2 + false_review*-1
    maxPoints = 5300
    print("total: ", total)
    print("percentage: ", (total / maxPoints)*100, "%")
