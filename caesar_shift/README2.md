Overview

This Python program is designed to decrypt texts that have been encrypted using a substitution cipher. The decryption is performed using a hill-climbing algorithm that iteratively searches for the optimal decryption key based on quadgram scoring. The script handles various encrypted messages and runs until a plausible English plaintext is found. Additionally, it caches decryption results based on file hashes to prevent redundant processing on subsequent runs.
Features

    File I/O: Reads an encrypted text file and writes the decrypted message to a new file.
    Substitution Cipher Decryption: Uses a hill-climbing algorithm to explore different key mappings.
    Quadgram Scoring: Evaluates the likelihood of a decryption being valid English by summing quadgram log probabilities.
    Caching: Uses SHA‑256 file hashes to cache results, saving time on repeated decryption attempts.
    Flexibility: Can decrypt various messages encrypted with substitution ciphers that use different keys.

Requirements

    Python 3.x
    A text file containing the encrypted message.
    (Optional) A quadgrams.txt file with quadgram frequencies for improved scoring. If not provided, a minimal default dictionary is used.

Usage

    Clone the Repository or Download the Script:

git clone <repository-url>
cd <repository-directory>

Prepare Your Encrypted File:

Place your encrypted text file in the project directory.

Run the Program:

Execute the script by specifying your encrypted file as an argument:

    python decrypt.py your_encrypted_file.txt

    The program will:
        Compute the file's SHA‑256 hash.
        Check if the file has already been processed (using a JSON cache).
        If not cached, perform decryption using the hill-climbing algorithm.
        Write the decrypted text to a new file named your_encrypted_file.txt.decrypted.txt.

    Review the Output:

    Open the generated .decrypted.txt file to view the decrypted message.

Customization

    Quadgram Data:
    For improved accuracy, supply a comprehensive quadgrams.txt file with real-world quadgram frequencies.
    Algorithm Parameters:
    You can adjust the number of hill-climbing restarts and iterations by modifying the restarts and iterations parameters in the solve_substitution function.

Additional Information

The code includes detailed inline comments explaining the reasoning behind each major component. The hill-climbing algorithm and quadgram scoring approach are inspired by well-established cryptanalysis techniques, as discussed in sources like the Practical Cryptography website citePracticalCryptography2024.