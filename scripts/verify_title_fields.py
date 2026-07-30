#!/usr/bin/env python3
"""
DEPRECATED: This script has been renamed to verify_canonical_profile.py.
Please use verify_canonical_profile.py directly.
"""
import sys
import subprocess
import pathlib

def main():
    print("WARNING: verify_title_fields.py is deprecated and will be removed in a future release.", file=sys.stderr)
    print("WARNING: Please use verify_canonical_profile.py instead.\n", file=sys.stderr)
    
    script_dir = pathlib.Path(__file__).parent
    new_script = script_dir / "verify_canonical_profile.py"
    
    sys.exit(subprocess.call([sys.executable, str(new_script)] + sys.argv[1:]))

if __name__ == "__main__":
    main()
