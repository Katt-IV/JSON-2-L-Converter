import json
import os
import glob

def convert_json_to_jsonl(input_directory, output_directory):
    """
    Reads JSON files from input_directory, converts them to JSONL, 
    and saves them to output_directory. Drops corrupted files.
    """
    os.makedirs(output_directory, exist_ok=True)
    
    # Find all .json files in the input directory
    json_files = glob.glob(os.path.join(input_directory, '*.json'))
    
    for file_path in json_files:
        filename = os.path.basename(file_path)
        output_path = os.path.join(output_directory, filename.replace('.json', '.jsonl'))
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            with open(output_path, 'w', encoding='utf-8') as f_out:
                # If the JSON contains a list of objects, write each object on a new line
                if isinstance(data, list):
                    for item in data:
                        f_out.write(json.dumps(item) + '\n')
                # If it's a single dictionary/object, write it as one line
                else:
                    f_out.write(json.dumps(data) + '\n')
                    
        except (json.JSONDecodeError, UnicodeDecodeError):
            # File is corrupted or not valid JSON; drop it and move to the next
            print(f"Dropped corrupted file: {filename}")
            continue