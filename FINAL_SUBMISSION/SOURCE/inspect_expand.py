import inspect
from transformers.generation.utils import GenerationMixin
print(inspect.signature(GenerationMixin._expand_inputs_for_generation))
