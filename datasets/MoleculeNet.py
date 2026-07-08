import deepchem as dc

tasks, datasets, transformers = dc.molnet.load_delaney()

train_dataset, valid_dataset, test_dataset = datasets

print("예측 task:", tasks)
print("Train 크기:", len(train_dataset))
print("Valid 크기:", len(valid_dataset))
print("Test 크기:", len(test_dataset))