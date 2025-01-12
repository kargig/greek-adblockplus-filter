# Reads an input file with UBO rules and returns an output file containing domains
# and UBO rules that point to non-existent domains.

import re
import dns.resolver

def parse_domains_from_rules(file_path):
    """
    Extract unique domains/subdomains from UBO rules. rules are in the form of:
    www.domain.gr##.foo.bar in such a case, extract www.domain.gr
    add the domain to a dictionary with the domain as the key and the rule as the value
    prevent duplicates by checking if the domain already exists in the dictionary
    """
    domains = {}
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('!') or not line:  # Ignore comments or empty lines
                continue
            # Extract domain using regex
            match = re.search(r'([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', line)
            if match:
                domain = match.group(1)
                if domain not in domains:
                    domains[domain] = []
                domains[domain].append(line)
    return domains

def check_domain_exists(domain):
    """
    Check if a domain exists in DNS.
    """
    try:
        dns.resolver.resolve(domain, 'A')
        return True
    except dns.resolver.NXDOMAIN:
        return False
    except Exception:
        return True  # Treat as existing in case of temporary DNS issues

def main():
    input_file = 'input.txt'
    output_file = 'output.txt'

    domains = parse_domains_from_rules(input_file)
    non_existent_domains = {}

    # Check each domain only once
    for domain in domains:
        if not check_domain_exists(domain):
            non_existent_domains[domain] = domains[domain]

    # Write results to output file
    with open(output_file, 'w') as f:
        for domain, rules in non_existent_domains.items():
            f.write(f"{domain}\n")
            for rule in rules:
                f.write(f"  {rule}\n")

    print(f"Non-existent domains and associated rules written to {output_file}.")

if __name__ == '__main__':
    main()
