import zipfile
import os

def zip_project():
    # Name of the output file
    zip_filename = "med_app.zip"
    
    # Folders we MUST include (The Modular Structure)
    folders_to_include = [
        "app", 
        "data", 
        "embeddings", 
        "generation", 
        "ingest", 
        "retrieval"
    ]
    
    # Files we MUST include
    files_to_include = ["config.py", "requirements.txt"]

    print(f"📦 Packaging project into {zip_filename}...")
    
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # 1. Add the standalone files
        for file in files_to_include:
            if os.path.exists(file):
                print(f"  + Adding file: {file}")
                zipf.write(file)
        
        # 2. Add the folders recursively
        for folder in folders_to_include:
            if os.path.exists(folder):
                print(f"  + Adding folder: {folder}/")
                for root, dirs, files in os.walk(folder):
                    # Remove __pycache__ from the list so we don't zip junk
                    if '__pycache__' in dirs:
                        dirs.remove('__pycache__')
                        
                    for file in files:
                        if file.endswith(".pyc"): continue # Skip compiled python
                        
                        file_path = os.path.join(root, file)
                        print(f"    - {file_path}")
                        zipf.write(file_path)
            else:
                print(f"  ⚠️ Warning: Folder '{folder}' not found. Skipping.")

    print(f"\n✅ Done! Upload '{zip_filename}' to Google Colab.")

if __name__ == "__main__":
    zip_project()