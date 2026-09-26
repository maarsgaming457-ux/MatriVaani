from transformers import DynamicCache
print("Checking properties:")
c = DynamicCache()
print("Has keys?", hasattr(c, "key_cache"))
