import os
import zipfile

def build_store_zip():
    source_dir = 'bookmart'
    zip_filename = 'bookmart.zip'
    
    # Exclude patterns for clean Odoo Store package
    exclude_dirs = {'__pycache__', '.git', '.github', '.vscode'}
    exclude_files = {'index - Copy.html', 'install_or_upgrade.bat', '.DS_Store', 'Thumbs.db'}
    exclude_exts = {'.pyc', '.pyo', '.bat', '.tmp'}

    if os.path.exists(zip_filename):
        os.remove(zip_filename)
        print(f"Removed existing {zip_filename}")

    file_count = 0
    total_size = 0

    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_dir):
            # Modify dirs in-place to avoid descending into excluded directories
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            
            for file in files:
                if file in exclude_files:
                    continue
                ext = os.path.splitext(file)[1].lower()
                if ext in exclude_exts:
                    continue
                
                full_path = os.path.join(root, file)
                # Ensure archive path starts with 'bookmart/...'
                arcname = os.path.relpath(full_path, start=os.path.dirname(os.path.abspath(source_dir)))
                arcname = arcname.replace('\\', '/')
                
                zipf.write(full_path, arcname)
                file_count += 1
                total_size += os.path.getsize(full_path)
                print(f"  + {arcname}")

    zip_size_mb = os.path.getsize(zip_filename) / (1024 * 1024)
    print("\n" + "="*50)
    print(f"SUCCESS: Created {zip_filename}")
    print(f"Total files packaged: {file_count}")
    print(f"Uncompressed size: {total_size / (1024 * 1024):.2f} MB")
    print(f"Compressed ZIP size: {zip_size_mb:.2f} MB")
    print("="*50)

if __name__ == '__main__':
    build_store_zip()

