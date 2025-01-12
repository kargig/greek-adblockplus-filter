# Reads an input file with UBO rules and returns an output file containing the rules
# sorted by subdomains/domains. It does not change the order of rules within each domain group.
import re

def extract_domain(line):
    """
    Extract the domain from a UBO rule.
    Ignore everything after the domain.tld and consider subdomains.
    """
    match = re.search(r'^(\|\|)?([a-zA-Z0-9.-]+)', line)
    if match:
        return match.group(2).lower()
    return None

def sort_rules_with_comments(input_file, output_file):
    with open(input_file, 'r') as f:
        lines = f.readlines()

    grouped_rules = []
    temp_group = []

    # Group comments with the subsequent rules
    for line in lines:
        line = line.rstrip()
        if line.startswith("!"):  # A comment line
            temp_group.append(line)
        elif extract_domain(line):  # A rule line
            temp_group.append(line)
            grouped_rules.append(temp_group)
            temp_group = []
        else:  # If it's neither, add as is
            grouped_rules.append([line])

    # Sort the grouped rules by domain
    sorted_rules = sorted(
        grouped_rules,
        key=lambda group: extract_domain(group[-1]) or ""
    )

    # Flatten the sorted rules and write to the output file
    with open(output_file, 'w') as f:
        for group in sorted_rules:
            f.write('\n'.join(group) + '\n')

if __name__ == "__main__":
    input_file = "input.txt"  # Replace with your input file path
    output_file = "output.txt"  # Replace with your desired output file path
    sort_rules_with_comments(input_file, output_file)

