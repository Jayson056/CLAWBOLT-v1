import os

def is_text_file(filename):
    excluded_extensions = {
        '.mp3', '.mp4', '.pdf', '.png', '.jpg', '.jpeg', '.gif', 
        '.zip', '.pyc', '.exe', '.bin', '.so', '.dll', '.pyo',
        '.sqlite', '.db', '.ttf', '.woff', '.woff2', '.eot'
    }
    _, ext = os.path.splitext(filename)
    if ext.lower() in excluded_extensions:
        return False
    return True

def combine_files(root_dir, output_file):
    with open(output_file, 'w', encoding='utf-8') as outfile:
        # First, add a structure overview
        outfile.write("================================================================\n")
        outfile.write("PROJECT STRUCTURE OVERVIEW\n")
        outfile.write("================================================================\n\n")
        
        for root, dirs, files in os.walk(root_dir):
            # Skip hidden directories and __pycache__
            dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
            
            level = root.replace(root_dir, '').count(os.sep)
            indent = '  ' * level
            outfile.write(f"{indent}{os.path.basename(root)}/\n")
            sub_indent = '  ' * (level + 1)
            for f in sorted(files):
                if not f.startswith('.') and is_text_file(f):
                    outfile.write(f"{sub_indent}{f}\n")
        
        outfile.write("\n\n")
        outfile.write("================================================================\n")
        outfile.write("FILE CONTENTS\n")
        outfile.write("================================================================\n\n")

        for root, dirs, files in os.walk(root_dir):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
            
            for file in sorted(files):
                if file.startswith('.') or not is_text_file(file):
                    continue
                
                # Also skip the output file itself if it's in the same directory
                if file == os.path.basename(output_file):
                    continue
                
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, root_dir)
                
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='replace') as infile:
                        content = infile.read()
                        
                        outfile.write(f"\n{'#'*80}\n")
                        outfile.write(f"FILE: {rel_path}\n")
                        outfile.write(f"{'#'*80}\n\n")
                        outfile.write(content)
                        outfile.write("\n\n")
                except Exception as e:
                    outfile.write(f"\n[Error reading {rel_path}: {e}]\n\n")

if __name__ == "__main__":
    project_root = "/home/son/CLAWBOLT"
    output_path = os.path.join(project_root, "CombineAllCode.txt")
    combine_files(project_root, output_path)
    print(f"Combined code written to {output_path}")
