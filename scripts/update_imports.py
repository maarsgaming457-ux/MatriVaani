import os
import glob

def replace_in_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                
                new_content = content.replace("from data_modules.nmt", "from data_modules.nmt")
                new_content = new_content.replace("from data_modules.santali", "from data_modules.santali")
                new_content = new_content.replace("import data_modules.nmt", "import data_modules.nmt")
                new_content = new_content.replace("import data_modules.santali", "import data_modules.santali")
                
                if new_content != content:
                    with open(path, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    print(f"Updated {path}")

def main():
    directories = ["tests", "data_modules", "scripts", "models", "training", "evaluation"]
    for d in directories:
        if os.path.exists(d):
            replace_in_files(d)
            
if __name__ == "__main__":
    main()
