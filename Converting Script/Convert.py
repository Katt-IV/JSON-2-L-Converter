import json
import argparse
from pathlib import Path

def convert_json_to_jsonl(input_dir, output_dir, recursive=False):
    """
    Reads JSON files from input_dir, converts them to JSONL, 
    and saves them to output_dir. Drops corrupted files.
    """
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    
    # Ensure output directory exists
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Determine search pattern based on whether recursive is true
    search_pattern = '**/*.json' if recursive else '*.json'
    json_files = list(input_path.glob(search_pattern))
    
    stats = {"success": 0, "corrupted": 0, "errors": 0}

    print(f"Found {len(json_files)} JSON files to process...")

    for file_path in json_files:
        # If recursive, preserve the directory structure in the output folder
        relative_path = file_path.relative_to(input_path)
        out_file_path = output_path / relative_path.with_suffix('.jsonl')
        
        # Ensure the subdirectories exist in the output folder
        out_file_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            with open(out_file_path, 'w', encoding='utf-8') as f_out:
                if isinstance(data, list):
                    for item in data:
                        f_out.write(json.dumps(item) + '\n')
                else:
                    f_out.write(json.dumps(data) + '\n')
                    
            stats["success"] += 1
            
        except (json.JSONDecodeError, UnicodeDecodeError):
            print(f"Dropped corrupted file: {file_path.name}")
            stats["corrupted"] += 1
        except Exception as e:
            print(f"Error processing {file_path.name}: {e}")
            stats["errors"] += 1

    # Print final summary
    print("\n--- Conversion Summary ---")
    print(f"Successfully converted: {stats['success']}")
    print(f"Dropped (corrupted):    {stats['corrupted']}")
    print(f"Failed (other errors):  {stats['errors']}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert JSON files to JSONL and drop corrupted files.")
    parser.add_argument("-i", "--input", required=True, help="Path to the input directory containing JSON files.")
    parser.add_argument("-o", "--output", required=True, help="Path to the output directory.")
    parser.add_argument("-r", "--recursive", action="store_true", help="Search for JSON files in subdirectories.")
    
    args = parser.parse_args()
    
    convert_json_to_jsonl(args.input, args.output, args.recursive)