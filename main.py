#!/usr/bin/env python3.13t
"""
Process CSV files, check prime numbers, transform them using calc.sh,
and write the results to new CSV files.

Steps:
- Read six generated CSV files (x-y.csv), each with numbers.
- Check which numbers are prime.
- For each prime, call calc.sh to add 2 (limited to 2 parallel calls).
- Check if the new number is prime.
- Write all resulting prime numbers to new files 2x-2y.csv, sorted ascending.
- Set output file permissions to rw------- (600).
"""

import csv
import threading
from threading import Semaphore
import subprocess
import os

# List of input CSV files to process
FILE_PATHS = [
    "1-10000.csv",
    "10001-20000.csv",
    "20001-30000.csv",
    "30001-40000.csv",
    "40001-50000.csv",
    "50001-60000.csv",
]

# Semaphore to limit concurrent accesses to calc.sh to 2
CALC_SEMAPHORE = Semaphore(2)


def is_prime(number):
    """Return True if the given number is a prime number, otherwise False."""
    if number <= 1:
        return False
    if number <= 3:
        return True
    if number % 2 == 0 or number % 3 == 0:
        return False

    i = 5
    while i * i <= number:
        if number % i == 0 or number % (i + 2) == 0:
            return False
        i += 6

    return True


def process_row(row):
    """
    Process a single CSV row.

    Steps:
    - Convert values to integers.
    - Check which numbers are prime.
    - For each prime, call calc.sh (+2) and check if the new number is prime.
    - Return a list of resulting prime numbers.
    """
    numbers = [int(value) for value in row]

    # Check which numbers are prime
    prime_numbers = [number for number in numbers if is_prime(number)]

    new_primes = []
    for prime in prime_numbers:
        # Limit concurrent calc.sh calls
        with CALC_SEMAPHORE:
            result = subprocess.run(
                ["./calc.sh", str(prime)],
                check=True,
                capture_output=True,
                text=True,
            )
            new_value = int(result.stdout.strip())
            if is_prime(new_value):
                new_primes.append(new_value)

    return new_primes


def process_file(file_path):
    """
    Process a single CSV file.

    Steps:
    - Read all rows and process them.
    - Collect all resulting prime numbers.
    - Sort them and write to a new CSV file (2x-2y.csv).
    - Set file permissions to rw------- (600).
    """
    split_name_array = file_path.replace(".csv", "").split("-")
    first_number_int = int(split_name_array[0])
    second_number_int = int(split_name_array[1])
    output_file_path = f"{first_number_int*2}-{second_number_int*2}.csv"

    all_results = []

    with open(file_path, "r", encoding="utf-8") as input_file:
        reader = csv.reader(input_file)
        for row in reader:
            row_results = process_row(row)
            all_results.extend(row_results)

    all_results.sort()

    with open(output_file_path, "w", newline="", encoding="utf-8") as output_file:
        writer = csv.writer(output_file)
        for value in all_results:
            writer.writerow([value])

    os.chmod(output_file_path, 0o600)
    print(f"Processed {file_path} -> {output_file_path} (mode 600 set)")


def main():
    """
    Run processing threads for all CSV files concurrently.

    Each CSV file is processed in its own thread.
    """
    threads = []

    for file_path in FILE_PATHS:
        thread = threading.Thread(target=process_file, args=(file_path,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    print("All files processed.")


if __name__ == "__main__":
    main()