#!/usr/bin/env python2
#
# This script reads C++ or RST source files and writes all
# multi-line strings into individual files.
# This can be used to extract the Solidity test cases
# into files for e.g. fuzz testing as
# scripts/isolate_tests.py test/libsolidity/*

#!/usr/bin/env python2

"""
This script extracts multi-line strings (test cases) from C++ or RST source files and writes them into individual files.
This is particularly useful for isolating Solidity test cases for fuzz testing.
Usage: scripts/isolate_tests.py test/libsolidity/*
"""

import sys
import re
import os
from os.path import join

def extract_test_cases(file_path):
    """
    Extracts test cases from a given file path.
    
    :param file_path: The path to the source file.
    """
    # Read the file and split lines
    lines = open(file_path, 'rb').read().splitlines()
    
    inside_test_case = False
    delimiter = ''
    test_case = ''
    counter = 1
    test_case_name = ''

    for line in lines:
        if inside_test_case:
            # Check if the end of the test case is reached
            if line.strip().endswith(')' + delimiter + '";'):
                # Write the test case to a file
                with open('%03d_%s.sol' % (counter, test_case_name), 'wb') as file:
                    file.write(test_case)
                counter += 1
                inside_test_case = False
                test_case = ''
            else:
                # Process the line inside the test case
                line = re.sub('^\t\t', '', line)
                line = line.replace('\t', '    ')
                test_case += line + '\n'
        else:
            # Search for the start of a test case
            match = re.search(r'BOOST_AUTO_TEST_CASE\(([^(]*)\)', line.strip())
            if match:
                test_case_name = match.group(1)
            match = re.search(r'R"([^(]*)\($', line.strip())
            if match:
                inside_test_case = True
                delimiter = match.group(1)

if __name__ == '__main__':
    # Extract test cases from the provided path
    source_path = sys.argv[1]
    extract_test_cases(source_path)

