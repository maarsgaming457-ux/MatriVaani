# Testing Strategy

## Philosophy
After every major architectural/model change, regression tests must be run. Never make a major change and assume the system still works.

## Levels of Testing
1. **Unit Tests**: Test individual functions, dataset loaders, and data transformations.
2. **Integration Tests**: Test the connection between components (e.g., ASR output to NMT input).
3. **Regression Tests**: Automated tests on a golden dataset to ensure WER, BLEU, and MOS do not regress.
4. **Benchmarking**: Continuously measure:
   - Inference latency (Target: < 3s end-to-end)
   - Memory footprint (RAM < 2GB constraint)
   - Model size

## Golden Datasets
Each language and component will have a protected Golden Test Set. The test set will *never* be used for training.

## Automation
Tests will be implemented using `pytest` for Python components and standard Android testing frameworks for the mobile application.
