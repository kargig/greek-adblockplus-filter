# Reads an input file with UBO rules and returns an output file containing the rules
# sorted by subdomains/domains. It does modify the order of rules within each domain group.
import re

def sort_urls_in_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split content by comments or blank lines to maintain blocks
    blocks = re.split(r'(\n\s*!\s*[^\n]*|^\s*$)', content, flags=re.MULTILINE)

    sorted_content = ""

    for block in blocks:
        if block.strip().startswith("!") or block.strip() == "":
            # Keep comments and blank lines as they are
            sorted_content += block
        else:
            # Sort lines within a block of URLs
            urls = block.strip().split("\n")
            urls = sorted(urls, key=lambda x: re.search(r'\|\|([^/]+)', x).group(1) if re.search(r'\|\|([^/]+)', x) else x)
            sorted_content += "\n".join(urls) + "\n"

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(sorted_content)

if __name__ == "__main__":
    input_file = "input.txt"  # Replace with your input file name
    output_file = "output.txt"  # Replace with your desired output file name
    sort_urls_in_file(input_file, output_file)
    print(f"Sorted content has been written to {output_file}.")

