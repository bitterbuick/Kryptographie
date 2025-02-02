Title: Caesar Cipher Decryption and Performance Comparison

Description:
-------------
This package includes three scripts:
  1. caesar_bruteforce.py
     - Reads an encrypted file and prints all 26 candidate plaintexts using a simple brute-force approach.
  2. caesar_frequency.py
     - Uses chi-squared frequency analysis to dynamically determine the best Caesar cipher shift.
  3. compare_decryption_methods.py
     - Compares the runtime and memory usage of the brute-force and frequency analysis methods.

Restrictions Met:
-------------------
- No external decryption tools are used; all cryptographic analysis is implemented in the scripts.
- No static, hard-coded substitution keys are used; keys are derived dynamically from the ciphertext.

English Letter Frequencies:
---------------------------
The frequencies used for the chi-squared analysis are based on:
  1. Kucera, H., & Francis, W. N. (1967). Computational Analysis of Present-Day American English.
  2. Norvig, P. (2009). How to Write a Spelling Corrector. Retrieved from http://norvig.com/spell-correct.html
  3. Wikipedia: Letter Frequency. Retrieved from https://en.wikipedia.org/wiki/Letter_frequency

How to Run:
-----------
1. Ensure Python 3 is installed.
2. Save each script with its respective filename.
3. Create an encrypted text file (e.g., encrypted.txt) containing the ciphertext.

To run each script:
  - Brute-Force Decryption:
      ```python3 caesar_bruteforce.py encrypted.txt```
  - Frequency Analysis Decryption:
      ```python3 caesar_frequency.py encrypted.txt```
  - Performance Comparison:
      ```python3 compare_decryption_methods.py encrypted.txt```

Expected Output:
----------------
- **caesar_bruteforce.py**: Lists all 26 shifts with candidate plaintexts.
- **caesar_frequency.py**: Displays the determined shift, chi-squared score, and the best decrypted message.
- **compare_decryption_methods.py**: 
    - Prints the runtime (in seconds) and memory usage (in KB) for both methods.
    - Shows all candidates from the brute-force approach.
    - Displays the best candidate selected by the frequency analysis method.

Performance Comparison Details:
-------------------------------
- **Timing**: Measured using time.perf_counter() before and after function execution.
- **Memory**: Measured using resource.getrusage() (ru_maxrss) before and after function calls.
- The differences are minimal given the small search space (26 shifts), but the comparison demonstrates
  that the frequency analysis introduces a slight overhead due to additional computations.
  
Additional Notes:
-----------------
- The provided memory measurement method works on Unix-based systems. For Windows, consider using 'psutil'.
- The scripts assume the ciphertext consists of lowercase alphabetic characters.
- For further customization or integration, refer to the in-code comments.

Author: Adam W Freeman
Date: 02-Feb-2025
