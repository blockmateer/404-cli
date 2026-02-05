import os

# Read prompts.txt and extract base filenames
with open('prompts.txt', 'r') as f:
    lines = f.readlines()

# Extract filenames from URLs (remove extension and domain)
prompt_files = set()
for line in lines:
    line = line.strip()
    if line:
        # Extract filename from URL
        filename = line.split('/')[-1]
        # Remove extension (.png)
        base_name = filename.rsplit('.', 1)[0]
        prompt_files.add(base_name)

print(f"Found {len(prompt_files)} unique files in prompts.txt\n")

# List all .ply files in results folder
results_folder = '/root/results'
result_files = [f for f in os.listdir(results_folder) if f.endswith('.ply')]

print(f"Found {len(result_files)} .ply files in results folder\n")

# Find files to delete (in results but not in prompts)
files_to_delete = []
for ply_file in result_files:
    base_name = ply_file.rsplit('.', 1)[0]  # Remove .ply extension
    if base_name not in prompt_files:
        files_to_delete.append(ply_file)

if files_to_delete:
    print(f"Files to DELETE ({len(files_to_delete)}):")
    for f in sorted(files_to_delete):
        file_path = os.path.join(results_folder, f)
        file_size = os.path.getsize(file_path) / (1024 * 1024)  # Size in MB
        print(f"  - {f} ({file_size:.1f} MB)")
    
    print(f"\nTotal size to free: {sum(os.path.getsize(os.path.join(results_folder, f)) for f in files_to_delete) / (1024 * 1024):.1f} MB")
    
    # Delete the files
    print("\nDeleting files...")
    for f in files_to_delete:
        file_path = os.path.join(results_folder, f)
        os.remove(file_path)
        print(f"  ✓ Deleted {f}")
    
    print(f"\n✓ Successfully deleted {len(files_to_delete)} files")
else:
    print("No files to delete - all files in results folder exist in prompts.txt")

# Show remaining files
remaining = [f for f in os.listdir(results_folder) if f.endswith('.ply')]
print(f"\nRemaining files in results folder: {len(remaining)}")