# goit-pythonweb-hw-04

Asynchronous file sorter that reads all files from a source folder recursively and distributes them into subfolders by file extension.

## How to run

**1. Create and activate virtual environment**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Run the script**
```bash
python main.py <source_folder> <output_folder>
```

**Example:**
```bash
python main.py test_source test_output
```