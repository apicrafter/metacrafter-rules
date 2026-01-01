#!/usr/bin/env python3
"""
Script to automatically identify potentially wide rules that may generate false positives.

This script analyzes YAML rule files and identifies patterns that are likely to be too broad:
- Rules with Word(alphanums, min=X, max=Y) where range > 10
- Rules with Word(nums, max=N) where N <= 6 without fieldrule
- Rules with text matches of length <= 3 without fieldrule
- Rules matching common patterns (years, short codes) without fieldrule
"""

import os
import re
import sys
import yaml
import argparse
from pathlib import Path
from typing import List, Dict, Any, Tuple


def extract_word_patterns(rule_text: str) -> List[Dict[str, Any]]:
    """Extract Word() patterns from PyParsing rule text."""
    patterns = []
    
    # Match Word(alphanums, min=X, max=Y) or Word(alphanums, exact=N)
    alphanum_pattern = r'Word\(alphanums[^)]*\)'
    for match in re.finditer(alphanum_pattern, rule_text):
        pattern_text = match.group(0)
        min_val = None
        max_val = None
        exact_val = None
        
        min_match = re.search(r'min\s*=\s*(\d+)', pattern_text)
        if min_match:
            min_val = int(min_match.group(1))
        
        max_match = re.search(r'max\s*=\s*(\d+)', pattern_text)
        if max_match:
            max_val = int(max_match.group(1))
        
        exact_match = re.search(r'exact\s*=\s*(\d+)', pattern_text)
        if exact_match:
            exact_val = int(exact_match.group(1))
            min_val = max_val = exact_val
        
        patterns.append({
            'type': 'alphanums',
            'min': min_val,
            'max': max_val,
            'exact': exact_val,
            'text': pattern_text
        })
    
    # Match Word(nums, max=N) or Word(nums, exact=N)
    nums_pattern = r'Word\(nums[^)]*\)'
    for match in re.finditer(nums_pattern, rule_text):
        pattern_text = match.group(0)
        min_val = None
        max_val = None
        exact_val = None
        
        min_match = re.search(r'min\s*=\s*(\d+)', pattern_text)
        if min_match:
            min_val = int(min_match.group(1))
        
        max_match = re.search(r'max\s*=\s*(\d+)', pattern_text)
        if max_match:
            max_val = int(max_match.group(1))
        
        exact_match = re.search(r'exact\s*=\s*(\d+)', pattern_text)
        if exact_match:
            exact_val = int(exact_match.group(1))
            min_val = max_val = exact_val
        
        patterns.append({
            'type': 'nums',
            'min': min_val,
            'max': max_val,
            'exact': exact_val,
            'text': pattern_text
        })
    
    return patterns


def analyze_rule(rule_id: str, rule: Dict[str, Any], file_path: str) -> List[Dict[str, Any]]:
    """Analyze a single rule for potential width issues."""
    issues = []
    rule_type = rule.get('type', 'unknown')
    match_type = rule.get('match', 'unknown')
    rule_text = rule.get('rule', '')
    has_fieldrule = 'fieldrule' in rule
    is_imprecise = rule.get('imprecise', 0) == 1
    
    # Skip if already marked as imprecise
    if is_imprecise:
        return issues
    
    # Only analyze data rules (field rules are less problematic)
    if rule_type != 'data':
        return issues
    
    # Check for broad alphanumeric patterns
    if match_type == 'ppr' and 'Word(alphanums' in rule_text:
        patterns = extract_word_patterns(rule_text)
        for pattern in patterns:
            if pattern['type'] == 'alphanums':
                if pattern['exact'] is not None:
                    # Exact patterns are usually fine
                    continue
                if pattern['min'] is not None and pattern['max'] is not None:
                    range_size = pattern['max'] - pattern['min']
                    if range_size > 10:
                        issues.append({
                            'severity': 'high',
                            'issue': f"Very broad alphanumeric range: {pattern['min']}-{pattern['max']} (range: {range_size})",
                            'pattern': pattern['text'],
                            'has_fieldrule': has_fieldrule,
                            'rule_id': rule_id,
                            'file': file_path
                        })
                    elif pattern['min'] is not None and pattern['min'] <= 3:
                        issues.append({
                            'severity': 'medium',
                            'issue': f"Short alphanumeric pattern (min={pattern['min']}) may match common codes",
                            'pattern': pattern['text'],
                            'has_fieldrule': has_fieldrule,
                            'rule_id': rule_id,
                            'file': file_path
                        })
    
    # Check for numeric patterns without fieldrule
    if match_type == 'ppr' and 'Word(nums' in rule_text:
        patterns = extract_word_patterns(rule_text)
        for pattern in patterns:
            if pattern['type'] == 'nums':
                if pattern['max'] is not None and pattern['max'] <= 6 and not has_fieldrule:
                    issues.append({
                        'severity': 'high',
                        'issue': f"Short numeric pattern (max={pattern['max']}) without fieldrule constraint",
                        'pattern': pattern['text'],
                        'has_fieldrule': False,
                        'rule_id': rule_id,
                        'file': file_path
                    })
                elif pattern['min'] is not None and pattern['max'] is not None:
                    range_size = pattern['max'] - pattern['min']
                    if range_size > 5 and not has_fieldrule:
                        issues.append({
                            'severity': 'medium',
                            'issue': f"Wide numeric range ({pattern['min']}-{pattern['max']}) without fieldrule",
                            'pattern': pattern['text'],
                            'has_fieldrule': False,
                            'rule_id': rule_id,
                            'file': file_path
                        })
    
    # Check for short text matches without fieldrule
    if match_type == 'text':
        text_values = rule_text.split(',')
        maxlen = rule.get('maxlen', None)
        minlen = rule.get('minlen', None)
        
        if minlen is not None and minlen <= 3 and not has_fieldrule:
            issues.append({
                'severity': 'high',
                'issue': f"Short text match (minlen={minlen}) without fieldrule constraint",
                'pattern': f"Text match with {len(text_values)} values",
                'has_fieldrule': False,
                'rule_id': rule_id,
                'file': file_path
            })
        elif maxlen is not None and maxlen <= 3 and not has_fieldrule:
            issues.append({
                'severity': 'high',
                'issue': f"Short text match (maxlen={maxlen}) without fieldrule constraint",
                'pattern': f"Text match with {len(text_values)} values",
                'has_fieldrule': False,
                'rule_id': rule_id,
                'file': file_path
            })
    
    # Check for year patterns without fieldrule
    if match_type == 'ppr' and ('1001' in rule_text or '2199' in rule_text or 'year' in rule_id.lower()):
        if not has_fieldrule:
            issues.append({
                'severity': 'high',
                'issue': "Year pattern without fieldrule constraint",
                'pattern': rule_text[:100] if len(rule_text) > 100 else rule_text,
                'has_fieldrule': False,
                'rule_id': rule_id,
                'file': file_path
            })
    
    return issues


def analyze_yaml_file(file_path: Path) -> List[Dict[str, Any]]:
    """Analyze a single YAML file for wide rules."""
    all_issues = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        if not data or 'rules' not in data:
            return all_issues
        
        for rule_id, rule in data['rules'].items():
            issues = analyze_rule(rule_id, rule, str(file_path))
            all_issues.extend(issues)
    
    except Exception as e:
        print(f"Error analyzing {file_path}: {e}", file=sys.stderr)
    
    return all_issues


def main():
    parser = argparse.ArgumentParser(
        description='Analyze rule files for potentially wide rules that may generate false positives'
    )
    parser.add_argument(
        'rules_dir',
        type=str,
        nargs='?',
        default='rules',
        help='Directory containing rule YAML files (default: rules)'
    )
    parser.add_argument(
        '--severity',
        choices=['low', 'medium', 'high', 'all'],
        default='all',
        help='Minimum severity level to report (default: all)'
    )
    parser.add_argument(
        '--format',
        choices=['text', 'json', 'csv'],
        default='text',
        help='Output format (default: text)'
    )
    
    args = parser.parse_args()
    
    rules_dir = Path(args.rules_dir)
    if not rules_dir.exists():
        print(f"Error: Rules directory '{rules_dir}' does not exist", file=sys.stderr)
        return 1
    
    # Find all YAML files
    yaml_files = list(rules_dir.rglob('*.yaml'))
    
    if not yaml_files:
        print(f"No YAML files found in {rules_dir}", file=sys.stderr)
        return 1
    
    # Analyze all files
    all_issues = []
    for yaml_file in yaml_files:
        issues = analyze_yaml_file(yaml_file)
        all_issues.extend(issues)
    
    # Filter by severity
    severity_order = {'low': 0, 'medium': 1, 'high': 2}
    if args.severity != 'all':
        min_severity = severity_order[args.severity]
        all_issues = [
            issue for issue in all_issues
            if severity_order.get(issue['severity'], 0) >= min_severity
        ]
    
    # Sort by severity and file
    all_issues.sort(key=lambda x: (severity_order.get(x['severity'], 0), x['file'], x['rule_id']), reverse=True)
    
    # Output results
    if args.format == 'json':
        import json
        print(json.dumps(all_issues, indent=2))
    elif args.format == 'csv':
        import csv
        import sys
        writer = csv.DictWriter(sys.stdout, fieldnames=['severity', 'file', 'rule_id', 'issue', 'pattern', 'has_fieldrule'])
        writer.writeheader()
        for issue in all_issues:
            writer.writerow({
                'severity': issue['severity'],
                'file': issue['file'],
                'rule_id': issue['rule_id'],
                'issue': issue['issue'],
                'pattern': issue['pattern'],
                'has_fieldrule': issue['has_fieldrule']
            })
    else:
        # Text format
        if not all_issues:
            print("No potentially wide rules found.")
            return 0
        
        print(f"Found {len(all_issues)} potentially wide rules:\n")
        
        current_file = None
        for issue in all_issues:
            if issue['file'] != current_file:
                current_file = issue['file']
                print(f"\n{current_file}:")
                print("=" * 80)
            
            severity_marker = {
                'high': '!!!',
                'medium': '!!',
                'low': '!'
            }.get(issue['severity'], '?')
            
            print(f"\n{severity_marker} [{issue['severity'].upper()}] {issue['rule_id']}")
            print(f"   Issue: {issue['issue']}")
            print(f"   Pattern: {issue['pattern']}")
            print(f"   Has fieldrule: {issue['has_fieldrule']}")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())

