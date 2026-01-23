import sys
import json
from pathlib import Path

def inventory_files(base_rep):
    files_list = []
    path_obj = Path(base_rep)
    for file in path_obj.rglob("*"):
        if file.is_file():
            files_list.append([str(file), file.stat().st_size])
    return files_list

def sort_and_filter(files_list, limit=100, min_size=1048576):
    sorted_list = sorted(files_list, key=lambda x: x[1], reverse=True)
    filtered_list = [f for f in sorted_list if f[1] >= min_size]
    return filtered_list[:limit]

def save_to_json(data, filename="data.json"):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        rep = sys.argv[1]
        data = inventory_files(rep)
        clean_data = sort_and_filter(data)
        save_to_json(clean_data)