#!/usr/bin/env python

import argparse
import re
import sys


def header_to_text(text):
    # "#### **Black Tentacles**" -> "Black Tentacles"
    return text.lstrip('#').strip().strip('*').strip()


def check_duration_length(line):
    # "**Duration:** Concentration, up to 1 minute Squirming, ebony tentacles..."
    duration_match = re.search(r'\*\*Duration:\*\*\s+(.+)', line)
    if duration_match:
        duration_content = duration_match.group(1)
        if len(duration_content.split()) > 5:
            return f"Duration value has more than 5 words, likely contains description: '{line}'"


def check_srd(lines):
    TESTS_TABLE = {
        # match on          check with
        '**Duration':       check_duration_length,
    }

    error_messages = []
    for index, line in enumerate(lines):
        for match, checker in TESTS_TABLE.items():
            if match in line:
                message = checker(line)
                if message:
                    context = 'file'
                    for prev in range(index - 1, -1, -1):
                        if lines[prev].startswith('#'):
                            context = header_to_text(lines[prev])
                            break
                    error_messages.append(f"{context}, {index}:\n{message}\n")
    if error_messages:
        raise ValueError('\n'.join(error_messages))


def main():
    parser = argparse.ArgumentParser(description='Clean SRD markdown format')
    parser.add_argument('markdown', help='Input markdown file')
    args = parser.parse_args()

    try:
        with open(args.markdown, 'r', encoding='utf-8') as f:
            content = f.readlines()

        check_srd(content)

    except FileNotFoundError as e:
        print(f"Error: File not found - {e}", file=sys.stderr)
        sys.exit(1)

    except Exception as e:
        print(f"{e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
