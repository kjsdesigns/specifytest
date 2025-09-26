# Timestamp Management Guide

## Overview

The Specify framework uses **ISO 8601 timestamps** as the sole versioning mechanism for tracking changes to specifications and detecting implementation staleness. This guide explains when and how to update timestamps.

## Core Principle

> **Every time you save a modification to a specification file, you MUST update the `hash_timestamp` field to the current UTC time.**

This simple rule enables the framework to automatically detect when implementations need updates.

## Timestamp Format

### Required Format
```yaml
hash_timestamp: YYYY-MM-DDTHH:MM:SSZ
```

### Format Details
- **YYYY**: 4-digit year
- **MM**: 2-digit month (01-12)
- **DD**: 2-digit day (01-31)
- **T**: Literal character 'T' separating date and time
- **HH**: 2-digit hour in 24-hour format (00-23)
- **MM**: 2-digit minute (00-59)
- **SS**: 2-digit second (00-59)
- **Z**: Literal character 'Z' indicating UTC timezone

### Valid Examples
```yaml
hash_timestamp: 2024-01-15T10:30:00Z
hash_timestamp: 2024-12-31T23:59:59Z
hash_timestamp: 2025-09-26T14:22:30Z
```

### Invalid Examples
```yaml
hash_timestamp: 2024-01-15  # Missing time component
hash_timestamp: 2024-01-15T10:30:00  # Missing Z
hash_timestamp: 2024-01-15 10:30:00Z  # Space instead of T
hash_timestamp: 01-15-2024T10:30:00Z  # Wrong date format
hash_timestamp: 2024-01-15T10:30:00+00:00  # Use Z, not +00:00
```

## When to Update Timestamps

### ALWAYS Update When:

1. **Changing Requirements**
   - Adding new fields
   - Removing fields
   - Modifying field types or validation rules
   - Changing business rules
   - Updating validation criteria

2. **Modifying Content**
   - Changing descriptions
   - Updating examples
   - Adding/removing sections
   - Clarifying ambiguous language
   - Fixing errors or inconsistencies

3. **Structural Changes**
   - Reordering sections
   - Adding new sections
   - Removing obsolete sections
   - Changing relationships to other specs

4. **Metadata Changes**
   - Changing status (draft → ready → active)
   - Adding/removing related spec IDs
   - Updating any frontmatter fields (except hash_timestamp itself)

### DO NOT Update When:

1. **Formatting Only**
   - Fixing typos in comments
   - Adjusting whitespace
   - Reformatting code blocks (without content changes)
   - Fixing markdown formatting

2. **Non-Content Changes**
   - Adding TODO comments
   - Adding internal notes (not part of spec)
   - Updating file permissions
   - Moving files (unless path changes affect references)

### Gray Areas (Use Judgment):

1. **Minor Clarifications**
   - If clarification doesn't change meaning → Don't update
   - If clarification reveals new requirement → Update

2. **Adding Examples**
   - Substantive examples that aid understanding → Update
   - Trivial examples that restate existing content → Consider updating

3. **Reorganizing Without Changes**
   - Pure reorganization for readability → Don't update
   - Reorganization that changes semantic meaning → Update

## How to Update Timestamps

### Manual Process

1. **Get Current UTC Time**

   **macOS/Linux:**
   ```bash
   date -u +"%Y-%m-%dT%H:%M:%SZ"
   ```

   **Windows PowerShell:**
   ```powershell
   (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
   ```

   **Online:**
   - Visit https://www.timeanddate.com/worldclock/timezone/utc
   - Format as ISO 8601

2. **Update the File**
   ```yaml
   hash_timestamp: 2025-09-26T14:30:00Z  # ← Replace with current time
   ```

3. **Save the File**

### Using Scripts

#### Quick Update Script (Bash)
```bash
#!/bin/bash
# update-timestamp.sh - Update timestamp in a spec file

FILE="$1"
if [ -z "$FILE" ]; then
    echo "Usage: $0 <spec-file>"
    exit 1
fi

TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
sed -i.bak "s/hash_timestamp: .*/hash_timestamp: $TIMESTAMP/" "$FILE"
echo "Updated $FILE timestamp to $TIMESTAMP"
```

Usage:
```bash
chmod +x update-timestamp.sh
./update-timestamp.sh /specs/test-cases/TC-001.yaml
```

#### Quick Update Script (Python)
```python
#!/usr/bin/env python3
# update-timestamp.py - Update timestamp in a spec file

import sys
import re
from datetime import datetime, timezone

def update_timestamp(file_path):
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    with open(file_path, 'r') as f:
        content = f.read()

    updated = re.sub(
        r'hash_timestamp: \d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z',
        f'hash_timestamp: {timestamp}',
        content
    )

    with open(file_path, 'w') as f:
        f.write(updated)

    print(f"Updated {file_path} timestamp to {timestamp}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 update-timestamp.py <spec-file>")
        sys.exit(1)

    update_timestamp(sys.argv[1])
```

Usage:
```bash
python3 update-timestamp.py /specs/test-cases/TC-001.yaml
```

### Editor Integration

#### VS Code Snippet
Add to your `.vscode/settings.json` or user snippets:
```json
{
  "Insert Timestamp": {
    "prefix": "timestamp",
    "body": ["hash_timestamp: ${CURRENT_YEAR}-${CURRENT_MONTH}-${CURRENT_DATE}T${CURRENT_HOUR}:${CURRENT_MINUTE}:${CURRENT_SECOND}Z"],
    "description": "Insert ISO 8601 UTC timestamp"
  }
}
```

#### Vim/Neovim
Add to your `.vimrc` or `init.vim`:
```vim
" Insert current UTC timestamp
inoremap <C-t> <C-R>=strftime("%Y-%m-%dT%H:%M:%SZ", localtime() - timezone())<CR>
```

#### Emacs
Add to your `.emacs` or `init.el`:
```elisp
(defun insert-utc-timestamp ()
  "Insert current UTC timestamp in ISO 8601 format"
  (interactive)
  (insert (format-time-string "%Y-%m-%dT%H:%M:%SZ" nil t)))

(global-set-key (kbd "C-c t") 'insert-utc-timestamp)
```

## Implementation Timestamp References

### In Test Files

When implementing a test from a spec, include ONLY the timestamp:

**Python (pytest):**
```python
def test_user_login():
    """
    Implements: /specs/test-cases/TC-001.yaml
    Case Timestamp: 2024-01-15T10:30:00Z
    """
    # Test implementation
```

**JavaScript (Jest):**
```javascript
describe('User Login', () => {
  test('valid credentials', () => {
    /*
     * Implements: /specs/test-cases/TC-001.yaml
     * Case Timestamp: 2024-01-15T10:30:00Z
     */
    // Test implementation
  });
});
```

**Go:**
```go
func TestUserLogin(t *testing.T) {
    // Implements: /specs/test-cases/TC-001.yaml
    // Case Timestamp: 2024-01-15T10:30:00Z

    // Test implementation
}
```

### In Source Code

For implementations referenced by specs:

```python
class UserAuthentication:
    """
    Implements: /specs/concepts/C-001/spec.md
    Spec Timestamp: 2024-01-15T10:30:00Z
    """
    def login(self, username, password):
        # Implementation
        pass
```

## Staleness Detection

### How It Works

1. **Specification Updated**: `hash_timestamp` changes from `2024-01-15T10:30:00Z` to `2024-01-20T14:00:00Z`

2. **Implementation Has Old Timestamp**: Test still references `2024-01-15T10:30:00Z`

3. **Staleness Script Detects**:
   ```bash
   ./specify/scripts/check-staleness.sh
   ```

4. **Output Shows**:
   ```
   CRITICAL (>30 days stale):
     tests/test_auth.py → TC-001.yaml (35 days stale)
       Case: 2024-01-20T14:00:00Z
       Impl: 2024-01-15T10:30:00Z
   ```

5. **Developer Updates**: Review spec changes, update implementation, update timestamp reference

### Priority Levels

- **CRITICAL**: > 30 days stale
- **HIGH**: 7-30 days stale
- **MEDIUM**: 1-7 days stale
- **LOW**: < 1 day stale

## Best Practices

### DO:
✓ Update timestamp immediately when saving meaningful changes
✓ Use UTC timezone always (Z suffix)
✓ Use consistent ISO 8601 format
✓ Include timestamp references in all implementations
✓ Run staleness checks before commits
✓ Update implementation timestamps when updating code

### DON'T:
✗ Forget to update after spec changes
✗ Use local time instead of UTC
✗ Use non-standard date formats
✗ Update timestamp for formatting-only changes
✗ Batch update timestamps without reviewing each file
✗ Leave stale implementations unaddressed

## Workflow Integration

### Pre-Commit Checklist
Before committing spec changes:
1. [ ] Did I update the `hash_timestamp`?
2. [ ] Is the timestamp in correct ISO 8601 format?
3. [ ] Is the timestamp in UTC (ends with Z)?
4. [ ] Did I run `check-staleness.sh`?
5. [ ] Did I update affected implementations?

### Code Review Checklist
When reviewing spec changes:
1. [ ] Is `hash_timestamp` updated?
2. [ ] Is timestamp format valid?
3. [ ] Are changes substantial enough to warrant timestamp update?
4. [ ] Are related implementations flagged for update?

## Troubleshooting

### Invalid Timestamp Format
**Error**: Validation script reports invalid timestamp

**Solution**:
1. Check format matches: `YYYY-MM-DDTHH:MM:SSZ`
2. Ensure UTC timezone (`Z` suffix)
3. Verify all components are 2-digits (except year)

### False Staleness Warnings
**Problem**: Implementation flagged as stale but is current

**Causes**:
1. Implementation timestamp reference not updated
2. Clock skew between systems
3. Timestamp format mismatch

**Solution**:
1. Verify implementation timestamp matches current spec
2. Ensure both use identical format
3. Update implementation timestamp reference

### Missing Timestamps
**Error**: Spec file has no `hash_timestamp`

**Solution**:
1. Add field to YAML frontmatter
2. Set to current UTC time
3. Commit the update

## Migration from Other Systems

### From Version Numbers
If migrating from traditional version numbers (v1.0.0):
1. Set `hash_timestamp` to file's last modification time
2. Convert to UTC if necessary
3. Use ISO 8601 format
4. Going forward, update on every save

### From Git Commit Dates
```bash
# Get last commit timestamp for a file
git log -1 --format="%aI" path/to/spec.md
```

Convert to `YYYY-MM-DDTHH:MM:SSZ` format and use as initial timestamp.

### From Content Hashes
If previously using MD5/SHA hashes:
1. Remove hash fields
2. Add `hash_timestamp` field
3. Set to current or last-modified time
4. Update constitution reference

## Validation

### Validate Timestamp Format
```bash
python3 .specify/scripts/validate-specs.py /specs/
```

### Manual Validation
```bash
# Check if timestamp matches ISO 8601 format
grep "hash_timestamp:" spec.yaml | grep -E "[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z"
```

## FAQ

**Q: Do I update timestamps for typo fixes?**
A: Generally no, unless the typo changes meaning.

**Q: What if I forget to update the timestamp?**
A: Update it now with current time. The gap will be visible in staleness reports.

**Q: Can I backdate a timestamp?**
A: No. Always use current time. Backdating defeats staleness detection.

**Q: Do Plans and Tasks use timestamps?**
A: Plans use Git SHA and plan_created timestamp. Tasks reference Case timestamps.

**Q: What timezone should I use?**
A: Always UTC (indicated by Z suffix). Never use local time.

**Q: How precise should timestamps be?**
A: Second precision is sufficient. Don't worry about milliseconds.

**Q: Can I use automated timestamp updates?**
A: Manual updates are recommended to ensure intentional changes. Automation can hide unintended modifications.

## Summary

The timestamp system is intentionally simple:
1. Update `hash_timestamp` when saving meaningful spec changes
2. Use ISO 8601 UTC format: `YYYY-MM-DDTHH:MM:SSZ`
3. Reference timestamps in implementations
4. Run staleness checks regularly
5. Keep implementations current

This approach provides temporal awareness without complex versioning systems.