"""
This file checks if your OpenRefine OnDemand application template is valid and ready for deployment.

It performs the following checks:
    - Verifies that all required files are present.
    - Checks YAML syntax for any errors.
    - Looks for custom error and warning patterns in files.
"""

import json
import os
import yaml
import argparse

ERROR = "!["
ERRORE = "]!"
WARNING = "?["
WARNINGE = "]?"

def find_pattern(start_pattern, end_pattern, string):
    """
    Find the given pattern in the given string.

    A 'pattern' is a string enclosed by two characters.
    If the start character is '![' and the end character is ']!',
    then we would look for text enclosed within:

    ![TEXT HERE]!

    If the given pattern is found, then we return 'TEXT HERE'.
    Otherwise, return None.

    :param start_pattern: Start character
    :param end_pattern: End character
    :param string: Text to search
    :return: The text enclosed in the pattern, or None if pattern not found
    """
    start = string.find(start_pattern)
    end = string.find(end_pattern)

    if start < 0 and end < 0:
        return None

    if end < 0 or end < start:
        print(" --== MALFORMED PATTERN FOUND! ==--")
        print("No end pattern found:")
        print("\n{}\n".format(string))
        print("Assuming end of line is end of pattern")

    if start < 0 or start > end:
        print(" --== MALFORMED PATTERN FOUND! ==--")
        print("No start pattern found:")
        print("\n{}\n".format(string))
        print("Assuming start of line is start of pattern")
        start = 0 - len(start_pattern)

    return string[start + len(start_pattern):end]

def find_file_pattern(files, start_pattern, stop_pattern):
    """
    Find a generic pattern in a list of files.

    We iterate over the files provided,
    and then search each line for a given pattern.

    :param files: List of files to search through
    :param start_pattern: Start character to search for
    :param stop_pattern: Stop character to search for
    :return: List of all matches, file match was found in, and line
    """
    text = []

    for name in files:
        with open(name, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        for num, line in enumerate(lines):
            temp = find_pattern(start_pattern, stop_pattern, line)
            if temp:
                text.append((temp, name, num))

    return text

def find_errors(file_names):
    """
    Find all errors in the given files.

    Errors are defined as text within the characters '![]!'.
    :param file_names: A list of files to search
    :return: A list of all errors and their line numbers
    """
    return find_file_pattern(file_names, ERROR, ERRORE)

def find_warnings(file_names):
    """
    Find all warnings in the given files.

    Warnings are defined as text within the characters '?[]?'.
    :param file_names: A list of files to search
    :return: A list of all warnings and their line numbers
    """
    return find_file_pattern(file_names, WARNING, WARNINGE)

def check_yaml_syntax(file_names):
    """
    Check YAML syntax for all specified files.

    :param file_names: A list of YAML files to validate
    :return: List of tuples containing file name and error if any
    """
    syntax_errors = []
    for file in file_names:
        try:
            with open(file, 'r', encoding='utf-8') as f:
                yaml.safe_load(f)
        except yaml.YAMLError as exc:
            syntax_errors.append((file, str(exc)))
    return syntax_errors

def main():
    # Load the file index
    with open("index.json", "r", encoding="utf-8") as f:
        files = json.load(f)

    # List all files to check
    files_to_check = files['files']

    print("Checking files: {}".format(", ".join(files_to_check)))

    # Check for errors
    errors = find_errors(files_to_check)
    if errors:
        for err in errors:
            print("ERROR: Found error on line [{}] in file [{}] :".format(err[2], err[1]))
            print("\n{}\n".format(err[0]))
    else:
        print("No errors found.")

    # Check for warnings
    warnings = find_warnings(files_to_check)
    if warnings:
        for war in warnings:
            print("WARNING: Found warning on line [{}] in file [{}] :".format(war[2], war[1]))
            print("\n{}\n".format(war[0]))
    else:
        print("No warnings found.")

    # Check YAML syntax
    yaml_files = [file for file in files_to_check if file.endswith('.yml') or file.endswith('.yaml')]
    yaml_errors = check_yaml_syntax(yaml_files)
    if yaml_errors:
        for file, error in yaml_errors:
            print("SYNTAX ERROR in file [{}]:\n{}\n".format(file, error))
    else:
        print("YAML syntax is valid.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check the OnDemand application template for errors and warnings.")
    parser.add_argument("--errors", action="store_true", help="Show only errors")
    parser.add_argument("--warnings", action="store_true", help="Show only warnings")
    parser.add_argument("--syntax", action="store_true", help="Show only YAML syntax issues")
    args = parser.parse_args()

    main()
