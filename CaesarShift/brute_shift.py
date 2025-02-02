#!/usr/bin/env python3
"""
Script: brute_shift.py.py
Purpose: Decrypt a suspected Caesar cipher by printing all 26 candidate plaintexts. Essentially, brute force substitution methodology.
Usage: python3 brute_shift.py.py <encrypted_file>
"""

import sys

def normalize_text(text):
    """
    Converts the input text to lowercase.
    
    Parameters:
        text (str): The text to be normalized.
        
    Returns:
        str: The lowercase version of the text.
    """
    return text.lower()

def caesar_decrypt(ciphertext, shift):
    plaintext = ""
    for char in ciphertext:
        if char.isalpha():
            # After normalization, all letters are lowercase.
            base = ord('a')
            plaintext += chr((ord(char) - base - shift) % 26 + base)
        else:
            plaintext += char
    return plaintext

def main():
    if len(sys.argv) != 2:
        print("Usage: {} <encrypted_file>".format(sys.argv[0]))
        sys.exit(1)
    
    filename = sys.argv[1]
    try:
        with open(filename, 'r') as file:
            ciphertext = file.read().strip()
    except IOError as e:
        print("Error reading file '{}': {}".format(filename, e))
        sys.exit(1)
    
    # Normalize the ciphertext to lowercase
    ciphertext = normalize_text(ciphertext)
    
    print("Brute-Force Candidate Decryption:")
    for shift in range(26):
        candidate = caesar_decrypt(ciphertext, shift)
        print("Shift {:2d}: {}".format(shift, candidate))

if __name__ == "__main__":
    main()
