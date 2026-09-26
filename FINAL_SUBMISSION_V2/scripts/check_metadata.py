from datasets import load_dataset_builder

try:
    b = load_dataset_builder('ai4bharat/IndicVoices', 'santali')
    print('Dataset name:', b.info.builder_name)
    print('Features:', list(b.info.features.keys()) if b.info.features else 'None')
    print('Splits:', list(b.info.splits.keys()) if b.info.splits else 'None')
except Exception as e:
    print('Error:', e)
