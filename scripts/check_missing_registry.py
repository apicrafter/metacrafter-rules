#!/usr/bin/env python3
"""
Script to find rule keys that are missing from metacrafter-registry.
"""

import os
import sys
import yaml
import json
from pathlib import Path
from collections import defaultdict

try:
    import yaml
except ImportError:
    print("PyYAML is required. Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

# Add parent directory to path for imports if needed
sys.path.insert(0, str(Path(__file__).parent.parent))

def load_all_rule_keys(rules_dir):
    """Extract all 'key' values from all YAML rule files."""
    rule_keys = set()
    rule_files = []
    
    rules_path = Path(rules_dir)
    if not rules_path.exists():
        print(f"Rules directory not found: {rules_dir}")
        return rule_keys, rule_files
    
    # Find all YAML files
    for yaml_file in rules_path.rglob("*.yaml"):
        if yaml_file.name.endswith('.yaml_'):
            continue  # Skip backup files
        
        try:
            with open(yaml_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                
            if data and 'rules' in data:
                for rule_name, rule_data in data['rules'].items():
                    if isinstance(rule_data, dict) and 'key' in rule_data:
                        key = rule_data['key']
                        rule_keys.add(key)
                        rule_files.append({
                            'key': key,
                            'rule_name': rule_name,
                            'file': str(yaml_file.relative_to(rules_path)),
                            'name': rule_data.get('name', ''),
                        })
        except Exception as e:
            print(f"Error processing {yaml_file}: {e}", file=sys.stderr)
    
    return rule_keys, rule_files

def load_registry_datatypes(registry_jsonl_path, registry_yaml_dir=None):
    """Load all datatype IDs from registry JSONL file and optionally YAML files."""
    datatype_ids = set()
    
    # Load from JSONL
    if os.path.exists(registry_jsonl_path):
        try:
            with open(registry_jsonl_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        datatype = json.loads(line)
                        if 'id' in datatype:
                            datatype_ids.add(datatype['id'])
                    except json.JSONDecodeError as e:
                        print(f"Error parsing JSON line: {e}", file=sys.stderr)
        except Exception as e:
            print(f"Error reading registry file: {e}", file=sys.stderr)
    else:
        print(f"Registry JSONL file not found: {registry_jsonl_path}")
    
    # Also load from YAML files if directory provided
    if registry_yaml_dir and os.path.exists(registry_yaml_dir):
        yaml_path = Path(registry_yaml_dir)
        for yaml_file in yaml_path.rglob("*.yaml"):
            try:
                with open(yaml_file, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                    if data and isinstance(data, dict) and 'id' in data:
                        datatype_ids.add(data['id'])
            except Exception as e:
                print(f"Error loading YAML {yaml_file}: {e}", file=sys.stderr)
    
    return datatype_ids

def main():
    # Default paths
    script_dir = Path(__file__).parent
    rules_dir = script_dir.parent / "rules"
    registry_dir = script_dir.parent.parent / "metacrafter-registry"
    registry_jsonl = registry_dir / "data" / "datatypes_latest.jsonl"
    registry_yaml = registry_dir / "data" / "datatypes"
    
    # Allow override via command line
    if len(sys.argv) > 1:
        rules_dir = Path(sys.argv[1])
    if len(sys.argv) > 2:
        registry_jsonl = Path(sys.argv[2])
    if len(sys.argv) > 3:
        registry_yaml = Path(sys.argv[3])
    
    print(f"Loading rules from: {rules_dir}")
    print(f"Loading registry from: {registry_jsonl}")
    if registry_yaml.exists():
        print(f"Also checking YAML sources: {registry_yaml}")
    print()
    
    # Load rule keys
    rule_keys, rule_files = load_all_rule_keys(rules_dir)
    print(f"Found {len(rule_keys)} unique rule keys in {len(list((rules_dir).rglob('*.yaml')))} rule files")
    
    # Load registry datatypes (from both JSONL and YAML)
    registry_ids = load_registry_datatypes(registry_jsonl, registry_yaml)
    print(f"Found {len(registry_ids)} datatypes in registry (JSONL + YAML)")
    print()
    
    # Find missing keys
    missing_keys = rule_keys - registry_ids
    missing_keys_sorted = sorted(missing_keys)
    
    # Group by file
    missing_by_file = defaultdict(list)
    for rule_info in rule_files:
        if rule_info['key'] in missing_keys:
            missing_by_file[rule_info['file']].append(rule_info)
    
    # Print results
    if missing_keys:
        print(f"Found {len(missing_keys)} rule keys missing from registry:")
        print("=" * 80)
        
        for key in missing_keys_sorted:
            print(f"\nKey: {key}")
            print("  Found in rules:")
            for rule_info in rule_files:
                if rule_info['key'] == key:
                    print(f"    - {rule_info['file']}: {rule_info['rule_name']} ({rule_info['name']})")
    else:
        print("✓ All rule keys are present in the registry!")
    
    # Also show keys that exist in registry but not in rules (for reference)
    extra_in_registry = registry_ids - rule_keys
    if extra_in_registry and len(extra_in_registry) < 50:  # Only show if not too many
        print(f"\n\nNote: {len(extra_in_registry)} datatypes in registry have no corresponding rules")
        print("(This is normal - not all registry entries need rules)")
    
    return 0 if not missing_keys else 1

if __name__ == "__main__":
    sys.exit(main())

