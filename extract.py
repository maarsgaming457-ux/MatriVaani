import ast
import json

with open('test_phase34_structured_suite.py', 'r', encoding='utf-8') as f:
    tree = ast.parse(f.read())

cat_a = []
cat_b = []

for node in ast.walk(tree):
    if isinstance(node, ast.Assign):
        for target in node.targets:
            if isinstance(target, ast.Name):
                if target.id == 'cat_a':
                    cat_a = ast.literal_eval(node.value)
                elif target.id == 'cat_b':
                    cat_b = ast.literal_eval(node.value)

with open('phase34_cats.json', 'w', encoding='utf-8') as f:
    json.dump({'cat_a': cat_a, 'cat_b': cat_b}, f)
