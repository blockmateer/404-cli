#!/usr/bin/env python3
"""
Script to count files in results folder and identify prompts without corresponding files.
"""

import os

def main():
    prompts_file = '/root/failed_prompts.txt'
    results_folder = '/root/results_3'
    failed_prompts_file = '/root/failed_prompts.txt'
    
    # Read prompts.txt and extract base filenames
    print("=" * 60)
    print("ANALYZING PROMPTS AND RESULTS")
    print("=" * 60)
    
    with open(prompts_file, 'r') as f:
        lines = f.readlines()
    
    # Extract filenames from URLs (remove extension and domain)
    # Also keep a mapping of base_name -> full URL
    prompt_files = set()
    prompt_urls = {}
    for line in lines:
        line = line.strip()
        if line:
            # Extract filename from URL
            filename = line.split('/')[-1]
            # Remove extension (.png)
            base_name = filename.rsplit('.', 1)[0]
            prompt_files.add(base_name)
            prompt_urls[base_name] = line
    
    print(f"\n📄 Total prompts in prompts.txt: {len(prompt_files)}")
    
    # List all .ply files in results folder
    if os.path.exists(results_folder):
        result_files = [f for f in os.listdir(results_folder) if f.endswith('.ply')]
        result_base_names = {f.rsplit('.', 1)[0] for f in result_files}
        
        print(f"📁 Total files in results folder: {len(result_files)}")
        
        # Calculate total size
        total_size = sum(os.path.getsize(os.path.join(results_folder, f)) 
                        for f in result_files) / (1024 * 1024)
        print(f"💾 Total size of results folder: {total_size:.1f} MB")
    else:
        print(f"❌ Results folder not found: {results_folder}")
        result_base_names = set()
        result_files = []
    
    # Find prompts without corresponding files
    missing_files = prompt_files - result_base_names
    
    print(f"\n⚠️  Prompts WITHOUT corresponding files: {len(missing_files)}")
    
    # Write missing prompts to failed_prompts.txt
    if missing_files:
        with open(failed_prompts_file, 'w') as f:
            for base_name in sorted(missing_files):
                f.write(prompt_urls[base_name] + '\n')
        print(f"📝 Written {len(missing_files)} missing prompts to: {failed_prompts_file}")
        
        print("\nMissing files (first 20):")
        for i, base_name in enumerate(sorted(missing_files), 1):
            print(f"  {i:3d}. {base_name}")
            if i >= 20 and len(missing_files) > 20:
                print(f"  ... and {len(missing_files) - 20} more")
                break
    else:
        # Remove failed_prompts.txt if it exists and there are no missing files
        if os.path.exists(failed_prompts_file):
            os.remove(failed_prompts_file)
        print("✅ No missing files!")
    
    # Find files without corresponding prompts
    extra_files = result_base_names - prompt_files
    
    print(f"\n✅ Prompts WITH corresponding files: {len(prompt_files) - len(missing_files)}")
    print(f"🔴 Files WITHOUT corresponding prompts: {len(extra_files)}")
    
    if extra_files:
        print("\nExtra files in results folder (not in prompts.txt):")
        for i, base_name in enumerate(sorted(extra_files), 1):
            file_path = os.path.join(results_folder, base_name + '.ply')
            if os.path.exists(file_path):
                size = os.path.getsize(file_path) / (1024 * 1024)
                print(f"  {i}. {base_name}.ply ({size:.1f} MB)")
    
    # Summary statistics
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total prompts:              {len(prompt_files)}")
    print(f"Total files in results:     {len(result_files)}")
    print(f"Missing from results:       {len(missing_files)} ({len(missing_files)/len(prompt_files)*100:.1f}%)")
    print(f"Files without prompts:      {len(extra_files)}")
    print(f"Match rate:                 {(len(prompt_files) - len(missing_files))/len(prompt_files)*100:.1f}%")
    print("=" * 60)

if __name__ == "__main__":
    main()

