import os

def update_team_number():
    # Folder yang tidak perlu dicek (biar cepat dan tidak error)
    ignore_dirs = {'venv', '.venv', '__pycache__', '.git', 'instance', 'node_modules'}
    
    # Hanya cek file dengan ekstensi ini
    allowed_exts = {'.html', '.py', '.txt', '.md', '.css', '.js'}
    
    updated_files = 0
    total_replacements = 0

    print("Memulai proses pencarian '308' menjadi '308'...\n")

    # Menyisir semua folder dan file
    for root, dirs, files in os.walk("."):
        # Buang folder yang ada di ignore_dirs
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        
        for file in files:
            ext = os.path.splitext(file)[1]
            if ext in allowed_exts:
                filepath = os.path.join(root, file)
                
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Jika ada angka "308" di dalam file
                    if "308" in content:
                        # Ganti dengan "308"
                        new_content = content.replace("308", "308")
                        
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        
                        updated_files += 1
                        print(f"✅ Diperbarui: {filepath}")
                        
                except Exception as e:
                    # Abaikan file jika tidak bisa dibaca (misal file binary)
                    pass
                    
    print(f"\nSelesai! Berhasil memperbarui {updated_files} file.")

if __name__ == "__main__":
    update_team_number()