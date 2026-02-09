#!/usr/bin/env python3
"""
Create GitHub Labels from planning/labels.yaml

Usage:
  python scripts/create-github-labels.py              # Create all labels
  python scripts/create-github-labels.py --dry-run    # Preview without creating
"""

import os
import sys
import yaml
import argparse
import subprocess
from pathlib import Path

WORKSPACE_ROOT = Path('/home/runner/work/morpheus-press/morpheus-press')

# Label color mapping
LABEL_COLORS = {
    'area: setup': 'e99695',
    'area: backend': '0366d6',
    'area: ml': '5319e7',
    'area: ingestion': 'd4c5f9',
    'area: image-gen': 'fbca04',
    'area: comic': 'bfdadc',
    'area: distribution': 'c2e0c6',
    'area: ecommerce': '0e8a16',
    'area: release': 'fef2c0',
    'priority:p0': 'b60205',
    'priority:p1': 'd93f0b',
    'priority:p2': 'fbca04',
    'priority:p3': 'c5def5',
    'status:triage': 'ededed',
    'status:ready': '0e8a16',
    'status:in-progress': 'fbca04',
    'status:blocked': 'b60205',
    'status:done': '0e8a16',
    'Task': '0075ca',
    'Feature': 'a2eeef',
    'Bug': 'd73a4a',
    'auto-generated': 'fef2c0',
    'from-planning': 'c5def5',
    'milestone-complete': '0e8a16',
}

def load_labels():
    """Load labels from planning/labels.yaml"""
    labels_path = WORKSPACE_ROOT / 'planning/labels.yaml'
    
    if not labels_path.exists():
        print(f"❌ Labels file not found: {labels_path}")
        sys.exit(1)
    
    with open(labels_path, 'r') as f:
        data = yaml.safe_load(f)
    
    all_labels = []
    
    # Issue types
    for issue_type in data.get('issueTypes', []):
        all_labels.append(issue_type)
    
    # Label categories
    for category, labels in data.get('labels', {}).items():
        all_labels.extend(labels)
    
    # Add special labels
    all_labels.extend(['auto-generated', 'from-planning', 'milestone-complete'])
    
    return all_labels

def get_existing_labels():
    """Get existing GitHub labels"""
    try:
        result = subprocess.run(
            ['gh', 'api', '/repos/neutrico/morpheus-press/labels', '--jq', r'.[].name'],
            capture_output=True, text=True, check=False
        )
        
        if result.returncode == 0 and result.stdout.strip():
            return set(result.stdout.strip().split('\n'))
        return set()
    except Exception as e:
        print(f"⚠️  Could not fetch existing labels: {e}")
        return set()

def create_label(name, color, description, dry_run=False):
    """Create a single label"""
    if dry_run:
        print(f"   Would create: {name} (#{color})")
        return True
    
    try:
        result = subprocess.run(
            ['gh', 'api', '/repos/neutrico/morpheus-press/labels',
             '-f', f'name={name}',
             '-f', f'color={color}',
             '-f', f'description={description}'],
            capture_output=True, text=True, check=True
        )
        print(f"   ✅ Created: {name}")
        return True
    except subprocess.CalledProcessError as e:
        # Check if label already exists
        if 'already_exists' in e.stderr:
            print(f"   ⚠️  Already exists: {name}")
            return False
        print(f"   ❌ Failed to create {name}: {e.stderr}")
        return False

def update_label(name, color, description, dry_run=False):
    """Update an existing label"""
    if dry_run:
        print(f"   Would update: {name} (#{color})")
        return True
    
    try:
        result = subprocess.run(
            ['gh', 'api', f'/repos/neutrico/morpheus-press/labels/{name}', '--method', 'PATCH',
             '-f', f'new_name={name}',
             '-f', f'color={color}',
             '-f', f'description={description}'],
            capture_output=True, text=True, check=True
        )
        print(f"   🔄 Updated: {name}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"   ❌ Failed to update {name}: {e.stderr}")
        return False

def generate_description(label_name):
    """Generate description for a label"""
    descriptions = {
        'area: setup': 'Infrastructure and project setup',
        'area: backend': 'Backend API and services',
        'area: ml': 'Machine learning and AI',
        'area: ingestion': 'Book ingestion pipeline',
        'area: image-gen': 'Image generation with Stable Diffusion',
        'area: comic': 'Comic assembly and layout',
        'area: distribution': 'Distribution channels',
        'area: ecommerce': 'E-commerce and payments',
        'area: release': 'Release and deployment',
        'priority:p0': 'Critical priority',
        'priority:p1': 'High priority',
        'priority:p2': 'Medium priority',
        'priority:p3': 'Low priority',
        'status:triage': 'Needs triage',
        'status:ready': 'Ready for implementation',
        'status:in-progress': 'Currently being worked on',
        'status:blocked': 'Blocked by dependencies',
        'status:done': 'Completed',
        'Task': 'Development task',
        'Feature': 'New feature or enhancement',
        'Bug': 'Bug report',
        'auto-generated': 'Auto-generated by automation',
        'from-planning': 'Created from planning system',
        'milestone-complete': 'Milestone completion celebration',
    }
    return descriptions.get(label_name, '')

def main():
    parser = argparse.ArgumentParser(description='Create GitHub Labels from planning')
    parser.add_argument('--dry-run', action='store_true', help='Preview without creating')
    parser.add_argument('--update', action='store_true', help='Update existing labels')
    args = parser.parse_args()
    
    print("🏷️  GitHub Labels Management")
    print("=" * 50)
    
    # Load labels
    labels = load_labels()
    print(f"\n📋 Found {len(labels)} labels in planning/labels.yaml")
    
    # Get existing labels
    existing = get_existing_labels() if not args.dry_run else set()
    print(f"📋 Found {len(existing)} existing labels in GitHub")
    
    if args.dry_run:
        print("\n🔍 DRY RUN MODE - No changes will be made\n")
    
    # Create/update labels
    created = 0
    updated = 0
    skipped = 0
    
    print("\n🏷️  Processing labels...")
    for label in labels:
        color = LABEL_COLORS.get(label, 'ededed')
        description = generate_description(label)
        
        if label in existing:
            if args.update:
                if update_label(label, color, description, args.dry_run):
                    updated += 1
            else:
                print(f"   ⏭️  Skipped (exists): {label}")
                skipped += 1
        else:
            if create_label(label, color, description, args.dry_run):
                created += 1
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Summary:")
    print(f"   ✅ Created: {created}")
    if args.update:
        print(f"   🔄 Updated: {updated}")
    print(f"   ⏭️  Skipped: {skipped}")
    print(f"   📋 Total: {len(labels)}")
    
    if args.dry_run:
        print("\n💡 Run without --dry-run to actually create labels")

if __name__ == '__main__':
    main()
