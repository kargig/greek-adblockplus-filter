# Reads an input file with UBO rules and returns an output file containing rules
# that point to non-existent URLs.
import re
import requests

# Input and output file paths
INPUT_FILE = "input.txt"
OUTPUT_FILE_ERRORS = "output.txt"

def is_valid_url(url):
    """
    Checks if the given URL exists by making a HEAD request.
    Returns the response status code or None if there's an error.
    """
    try:
        response = requests.head(url, timeout=5)
        print(f"Trying URL: {url} - Response Code: {response.status_code}")
        return response.status_code
    except requests.RequestException as e:
        print(f"Trying URL: {url} - Error: {e}")
        return None

def extract_exact_file_url(rule):
    """
    Extracts the exact URL from the UBO rule for rules that point to specific files.
    Returns None if the rule points to directories or includes wildcards.
    """
    # Match rules that end with a file name and extension, avoiding directories or wildcards
    match = re.match(r"^\|\|([^\/\^\*]+)(\/.*\/[^\/\*\?]+?\.[a-zA-Z0-9]+)\$", rule)
    if match:
        return f"https://{match.group(1)}{match.group(2)}".strip("$")
    return None

def process_rules(input_file, error_file):
    """
    Reads UBO rules from input_file, validates exact file URL rules,
    and writes rules with response codes > 400 to error_file.
    """
    error_rules = []

    with open(input_file, "r") as file:
        rules = file.readlines()

    for rule in rules:
        rule = rule.strip()
        if rule.startswith("||") and not "*" in rule:
            url = extract_exact_file_url(rule)
            if url:
                status_code = is_valid_url(url)
                if status_code and status_code > 400:
                    error_rules.append(rule)

    with open(error_file, "w") as file:
        file.writelines(f"{rule}\n" for rule in error_rules)

    print(f"Processing complete. Error rules saved to {error_file}")

if __name__ == "__main__":
    process_rules(INPUT_FILE, OUTPUT_FILE_ERRORS)
