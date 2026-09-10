# Distance Learning 3: Operating Systems

Python solution for processing CSV files with prime number calculations using multi-threading and semaphores.

## 📋 Overview

A high-performance CSV processing system that:
- Processes 6 CSV files containing 60,000 numbers concurrently
- Identifies prime numbers and performs mathematical operations
- Enforces resource access control using semaphores
- Manages file permissions and system-level operations

**Built with:** Multi-threading, semaphores, subprocess management, and OS-level file operations.

## 🚀 Quick Start

```bash
# Clone and setup
git clone https://github.com/einkaf/Concurrent-File-Processing-System.git
cd filename
mkdir data && cd data

# Copy required scripts
cp /calc.sh /gencsv.sh .
chmod +x *.sh

# Generate test data
./gencsv.sh

# Run the application
cd ..
python3 solution.py
```

## 🔧 Features

| Feature | Description |
|---|---|
| **Concurrent Processing** | Multi-threaded file handling for 6 CSV files |
| **Resource Control** | Semaphore-based access limiting for external scripts |
| **Prime Detection** | Efficient primality testing algorithm |
| **Subprocess Integration** | Seamless external script execution |
| **Permission Management** | Proper file and directory permission handling |
| **High Performance** | Process 60,000 numbers efficiently |

## 📁 Project Structure

```
distance-learning-3/
├── solution.py          # Main application
├── calc.sh              # External calculation utility
├── gencsv.sh            # Data generation utility
├── data/                # Input/output directory
│   ├── 1-10000.csv      # Input files (6 total)
│   └── 2-20000.csv      # Output files (6 total)
└── README.md            # This file
```



## 🔐 Initial Configuration

```bash
# Create project directory with proper permissions
mkdir -p project/data
chmod 700 project

# Set up executable permissions
chmod +x solution.py
chmod +x calc.sh gencsv.sh

# Output files get restricted permissions (read/write only)
chmod 600 data/*.csv
```

## 🧵 Threading & Semaphore Pattern

```python
import threading

# Limit calc.sh to 2 concurrent calls
CALC_SEMAPHORE = threading.Semaphore(2)

def process_file(filename):
    """Process one CSV file in a thread."""
    for number in read_csv(filename):
        if is_prime(number):
            with CALC_SEMAPHORE:
                result = subprocess.run(['./calc.sh', str(number), '2'])
    write_output(filename)

# Spawn threads for each file
threads = []
for file in input_files:
    t = threading.Thread(target=process_file, args=(file,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()
```

## 🧪 Verification

```bash
# Check code quality
pylint solution.py

# Verify output file permissions
ls -l 2*.csv

# Should show: -rw------- (600 permissions)
```

## 📝 Code Quality

- **Comments:** Comprehensive documentation for all functions
- **Naming conventions:** UPPERCASE constants, snake_case for variables
- **Indentation:** PEP 8 - 4 spaces
- **Docstrings:** All functions documented
- **Linting:** Pass pylint checks

## 🐛 Troubleshooting

| Issue | Solution |
|---|---|
| "Permission denied" on scripts | Run `chmod +x calc.sh gencsv.sh` |
| Import errors | Ensure Python 3.7+ installed |
| Slow performance | Check system resources, verify threading works |
| Semaphore bottleneck | Verify initialization before thread spawn |
| File permission errors | Check `chmod 600` on output files |
