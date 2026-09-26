import os
import shutil

src_dir = "."
dest_dir = "FINAL_SUBMISSION_V2"

if os.path.exists(dest_dir):
    shutil.rmtree(dest_dir)

os.makedirs(dest_dir)

exclude_dirs = {
    "venv", ".git", ".vscode", "__pycache__", 
    "FINAL_SUBMISSION", "FINAL_SUBMISSION_V2",
    "bhashaverse_ho_env", "indictrans2_env",
    "models", "ho_test_env", "test_venv", "android/build"
}
exclude_files = {
    ".env", ".env.local"
}
exclude_ext = {
    ".safetensors", ".bin", ".pt", ".pth", ".arrow", ".wav", ".mp3", ".m4a", ".ogg", ".flac", ".mp4", ".pkl"
}

for root, dirs, files in os.walk(src_dir):
    dirs[:] = [d for d in dirs if d not in exclude_dirs and not d.startswith('.')]
    
    relative_path = os.path.relpath(root, src_dir)
    dest_path = os.path.join(dest_dir, relative_path)
    
    if not os.path.exists(dest_path):
        os.makedirs(dest_path)
        
    for file in files:
        if file in exclude_files:
            continue
        ext = os.path.splitext(file)[1]
        if ext in exclude_ext:
            continue
            
        src_file = os.path.join(root, file)
        dest_file = os.path.join(dest_path, file)
        
        # skip large files > 50MB
        if os.path.getsize(src_file) > 50 * 1024 * 1024:
            continue
            
        shutil.copy2(src_file, dest_file)

print("Created FINAL_SUBMISSION_V2 successfully.")
