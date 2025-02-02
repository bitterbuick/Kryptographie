#!/usr/bin/env python3
"""
Script: compare_decryption_methods.py
Purpose:
  Compare two Caesar cipher decryption methods:
    1. Brute-Force Candidate Generation.
    2. Frequency Analysis Decryption.
  Measures runtime and memory usage.
Usage:
  python3 compare_decryption_methods.py <encrypted_file>
  
Note: The resource module is used for memory measurements on Unix-based systems.
"""

import sys
import string
import time
import resource

ENGLISH_FREQ = {
    'a': 8.167, 'b': 1.492, 'c': 2.782, 'd': 4.253, 'e': 12.702,
    'f': 2.228, 'g': 2.015, 'h': 6.094, 'i': 6.966, 'j': 0.153,
    'k': 0.772, 'l': 4.025, 'm': 2.406, 'n': 6.749, 'o': 7.507,
    'p': 1.929, 'q': 0.095, 'r': 5.987, 's': 6.327, 't': 9.056,
    'u': 2.758, 'v': 0.978, 'w': 2.360, 'x': 0.150, 'y': 1.974,
    'z': 0.074
}

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
            base = ord('a')
            plaintext += chr((ord(char) - base - shift) % 26 + base)
        else:
            plaintext += char
    return plaintext

def chi_squared_score(text):
    filtered_text = "".join(filter(str.isalpha, text.lower()))
    if not filtered_text:
        return float('inf')
    
    letter_counts = {letter: 0 for letter in string.ascii_lowercase}
    for char in filtered_text:
        if char in letter_counts:
            letter_counts[char] += 1

    chi_sq = 0.0
    total = len(filtered_text)
    for letter in string.ascii_lowercase:
        observed = letter_counts[letter]
        expected = ENGLISH_FREQ[letter] / 100 * total
        if expected > 0:
            chi_sq += (observed - expected) ** 2 / expected
    return chi_sq

def brute_force_candidates(ciphertext):
    candidates = []
    for shift in range(26):
        candidate = caesar_decrypt(ciphertext, shift)
        candidates.append((shift, candidate))
    return candidates

def frequency_analysis_decrypt(ciphertext):
    best_shift = None
    best_score = float('inf')
    best_plaintext = ""
    for shift in range(26):
        candidate = caesar_decrypt(ciphertext, shift)
        score = chi_squared_score(candidate)
        if score < best_score:
            best_score = score
            best_shift = shift
            best_plaintext = candidate
    return best_shift, best_score, best_plaintext

def measure_time(func, *args, **kwargs):
    start = time.perf_counter()
    result = func(*args, **kwargs)
    elapsed = time.perf_counter() - start
    return result, elapsed

def measure_memory(func, *args, **kwargs):
    mem_before = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    result = func(*args, **kwargs)
    mem_after = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return result, mem_after - mem_before

def main():
    if len(sys.argv) != 2:
        print("Usage: {} <encrypted_file>".format(sys.argv[0]))
        sys.exit(1)
    
    filename = sys.argv[1]
    try:
        with open(filename, 'r') as f:
            ciphertext = f.read().strip()
    except IOError as e:
        print("Error reading file '{}': {}".format(filename, e))
        sys.exit(1)
    
    # Normalize ciphertext to lowercase
    ciphertext = normalize_text(ciphertext)
    
    # Brute-force method
    print("=== Brute-Force Candidate Generation ===")
    candidates, time_brute = measure_time(brute_force_candidates, ciphertext)
    _, mem_brute = measure_memory(brute_force_candidates, ciphertext)
    print("Time: {:.6f} seconds".format(time_brute))
    print("Memory change: {} KB".format(mem_brute))
    for shift, candidate in candidates:
        print("Shift {:2d}: {}".format(shift, candidate))
    
    # Frequency analysis method
    print("\n=== Frequency Analysis Decryption ===")
    (best_shift, best_score, best_plaintext), time_freq = measure_time(frequency_analysis_decrypt, ciphertext)
    _, mem_freq = measure_memory(frequency_analysis_decrypt, ciphertext)
    print("Time: {:.6f} seconds".format(time_freq))
    print("Memory change: {} KB".format(mem_freq))
    print("Best candidate:")
    print("  Determined Shift: {:2d}".format(best_shift))
    print("  Chi-squared Score: {:.2f}".format(best_score))
    print("  Decrypted Message:")
    print(best_plaintext)

if __name__ == "__main__":
    main()
