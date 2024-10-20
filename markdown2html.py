#!/usr/bin/python3
"""
markdown2html.py - A script to convert Markdown to HTML.

This script takes two arguments: a Markdown file and an output HTML file.
It converts headings, lists, paragraphs, bold, emphasis, and custom syntax 
for MD5 hashing and character removal.

Usage:
    ./markdown2html.py README.md README.html
"""
import sys
import os
import re
import hashlib

def usage():
    """ Print usage """
    print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)

def file_missing(filename):
    """ Print missing file message """
    print(f"Missing {filename}", file=sys.stderr)

def convert_to_md5(text):
    """ Convert text inside [[ ]] to its MD5 hash """
    return hashlib.md5(text.encode()).hexdigest()

def remove_c_from_text(text):
    """ Remove 'c' or 'C' from the text inside (( )) """
    return text.replace('c', '').replace('C', '')

def process_markdown_line(line):
    """
    Parse a markdown line and return the corresponding HTML.
    Supports headings, unordered lists, ordered lists, bold, emphasis,
    MD5 hashing, and 'c'/'C' removal.
    """
    # Heading conversion
    heading_match = re.match(r'^(#{1,6}) (.*)', line)
    if heading_match:
        heading_level = len(heading_match.group(1))
        content = heading_match.group(2)
        return f"<h{heading_level}>{content}</h{heading_level}>"

    # Unordered list
    if re.match(r'^- (.*)', line):
        return f"<li>{line[2:]}</li>", 'ul'
    
    # Ordered list
    if re.match(r'^\* (.*)', line):
        return f"<li>{line[2:]}</li>", 'ol'
    
    # Bold text
    line = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', line)
    
    # Emphasis text
    line = re.sub(r'__(.*?)__', r'<em>\1</em>', line)

    # Custom MD5 conversion
    line = re.sub(r'\[\[(.*?)\]\]', lambda m: convert_to_md5(m.group(1)), line)

    # Remove 'c' or 'C'
    line = re.sub(r'\(\((.*?)\)\)', lambda m: remove_c_from_text(m.group(1)), line)

    # Paragraph and line break
    if not line.strip():
        return "", "newline"
    return line

def main():
    """ Main function to handle argument parsing and file conversion. """
    # Check argument count
    if len(sys.argv) < 3:
        usage()
        sys.exit(1)

    markdown_file = sys.argv[1]
    html_file = sys.argv[2]

    # Check if the markdown file exists
    if not os.path.isfile(markdown_file):
        file_missing(markdown_file)
        sys.exit(1)

    # Read the markdown file
    with open(markdown_file, 'r') as md:
        lines = md.readlines()

    html_lines = []
    list_type = None

    for line in lines:
        line = line.rstrip()

        html_line, tag_type = process_markdown_line(line)
        
        if tag_type == "ul":
            if list_type != "ul":
                if list_type:
                    html_lines.append(f"</{list_type}>")
                html_lines.append("<ul>")
            list_type = "ul"
        
        elif tag_type == "ol":
            if list_type != "ol":
                if list_type:
                    html_lines.append(f"</{list_type}>")
                html_lines.append("<ol>")
            list_type = "ol"
        
        elif tag_type == "newline":
            if list_type:
                html_lines.append(f"</{list_type}>")
                list_type = None
            html_lines.append("<p>")
        else:
            if list_type:
                html_lines.append(f"</{list_type}>")
                list_type = None
            html_lines.append(html_line)

    if list_type:
        html_lines.append(f"</{list_type}>")

    # Write to the HTML file
    with open(html_file, 'w') as html:
        html.write('\n'.join(html_lines))

    sys.exit(0)

if __name__ == "__main__":
    main()
