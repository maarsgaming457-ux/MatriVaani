import inspect
from transformers.generation.utils import GenerationMixin
print(type(GenerationMixin.__dict__['_expand_inputs_for_generation']))
