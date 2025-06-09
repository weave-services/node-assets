import json
import csv
import os

SCHEMA_DIR = os.path.join('node-list', 'node-schemas')
OUTPUT_CSV = 'nodes_endpoints.csv'


def extract_options(options, prefix='-> '):
    rows = []
    for opt in options:
        label = opt.get('label') or opt.get('name') or ''
        desc = opt.get('description', '')
        rows.append((prefix + label, desc))
        if isinstance(opt.get('options'), list):
            # recursively add nested options
            rows.extend(extract_options(opt['options'], prefix + '-> '))
    return rows


def process_schema(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    node_label = data.get('label', os.path.splitext(os.path.basename(path))[0])
    description = data.get('description', '')
    rows = [(node_label, node_label, 'parent', description)]
    if isinstance(data.get('actions'), list):
        for action in data['actions']:
            if isinstance(action.get('options'), list):
                for endpoint, desc in extract_options(action['options']):
                    rows.append((node_label, endpoint, 'child', desc))
    return rows


def main():
    records = []
    for fname in sorted(os.listdir(SCHEMA_DIR)):
        if not fname.endswith('.json'):
            continue
        path = os.path.join(SCHEMA_DIR, fname)
        records.extend(process_schema(path))

    with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Node Name', 'Status', 'Endpoint', 'Method', 'Relationship', 'Description'])
        for node_label, endpoint, rel, desc in records:
            writer.writerow([node_label, '', endpoint, '', rel, desc])

if __name__ == '__main__':
    main()
