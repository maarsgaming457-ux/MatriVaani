from datasets import load_dataset_builder
builder = load_dataset_builder("google/fleurs", "sat_in")
print(builder.info.splits)
