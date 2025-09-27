# Trie-Based Vietnamese Address Finder

This project implements a Trie data structure to efficiently store and search Vietnamese addresses with built-in error tolerance. It can handle typos in address names such as missing characters, replaced characters, or inserted characters.

## Project Structure

```
.
├── main.py          # Main script with Solution class and trie creation functions
├── trie.py          # Trie data structure implementation
├── test.py          # Test script to evaluate performance on test data
├── dataset/         # Directory containing address data
│   ├── address.txt  # Full address data
│   ├── district.txt # District names
│   ├── province.txt # Province names
│   └── ward.txt     # Ward names
├── contest/         # Contest test data
│   └── public.json  # Public test cases
└── README.md        # This file
```

## Key Features

- **Error-tolerant search**: Can find correct addresses even with typos
- **Fast prefix search**: Efficiently finds all addresses starting with a given prefix
- **Case-insensitive matching**: Maintains original capitalization in results
- **Right-to-left search**: Optimized for Vietnamese address format
- **Sliding windows Longest Match**: Advanced algorithm for precise component detection
- **Text preprocessing**: Handles non-Vietnamese characters and punctuation
- **Reusable design**: The Trie implementation can be used for other applications

## How It Works

### Trie Data Structure

A Trie (or prefix tree) is a tree-like data structure that stores strings in a way that allows for efficient prefix-based lookup. Each node in the tree represents a character in a string, and paths from the root to a marked node represent complete words.

### Error Tolerance Approach

To handle typos, we generate variants of each address name and insert them into the Trie, mapping back to the original correct address. We handle three types of errors:

1. **Character deletion**: e.g., "Hà Đông" → "Hà Đng"
2. **Character substitution**: e.g., "Hà Nội" → "Hà Nộc"
3. **Character insertion**: e.g., "Long An" → "Lonbg An"

### Text Preprocessing

Input text is preprocessed before searching:
1. Converting to lowercase and removing leading/trailing whitespaces
2. Replacing non-Vietnamese characters (j → i, z → s, w → v, f → ph)
3. Removing pre and post punctuation
4. Normalizing whitespace within the text

### Sliding Windows Longest Match Algorithm

Our updated implementation uses a sliding windows approach with a Longest Match algorithm to precisely extract address components:

1. **Segmentation**: The address is first split by commas to separate potential components
2. **Right-to-Left Processing**: We process segments from right to left, which matches the natural order of Vietnamese addresses (province at the end)
3. **Multi-Pass Processing**: Three separate passes are conducted for province, district, and ward identification
4. **Sliding Window Technique**: For each segment, we slide a window from the rightmost word, gradually expanding leftward to find the longest matching phrase
5. **Remnant Preservation**: Unmatched portions of segments are preserved and forwarded to subsequent passes
6. **Sequential Matching**: Address components are identified in order: province → district → ward

This approach offers several advantages:
- More accurate extraction of address components
- Better handling of complex or ambiguous address formats
- Precise identification of administrative boundaries
- Ability to correctly process addresses with irregular formatting

### Case-Insensitive Matching with Original Case Preservation

When inserting data into the Trie:
- We store the original word with its capitalization preserved
- We also store a lowercase version to ensure case-insensitive matching
- This allows us to match user input regardless of capitalization while returning properly formatted results

## How to Run

### Prerequisites

- Python 3.6 or higher
- Pandas (for test result analysis)
- Dataset files in the correct format (one address per line)

### Running the Code

1. Make sure your dataset files are in the `dataset` directory
2. Run the main script:

```bash
python main.py
```

### Running the Tests

To evaluate the performance on the test dataset:

```bash
python test.py
```

This will:
- Load test cases from `contest/public.json`
- Process each address using our Solution class
- Calculate accuracy and execution time statistics
- Generate a `test_results.xlsx` file with detailed results

### Using the Trie in Your Own Code

```python
from main import Solution

# Initialize the Solution class which creates the tries
solution = Solution()

# Process an address
address = "123 Đường ABC, Phường Phú Mỹ, Quận 7, TP. Hồ Chí Minh"
result = solution.process(address)

print(f"Province: {result['province']}")  # Outputs: "Hồ Chí Minh"
print(f"District: {result['district']}")  # Outputs: "7"
print(f"Ward: {result['ward']}")          # Outputs: "Phú Mỹ"
```

Alternatively, you can use the individual trie creation functions:

```python
from main import create_province_trie, create_district_trie, create_ward_trie, preprocess_text

# Create the tries from datasets
dataset_path = "dataset"
province_trie = create_province_trie(dataset_path)
district_trie = create_district_trie(dataset_path)
ward_trie = create_ward_trie(dataset_path)

# Search for an address (even with typos)
province_name = "Hà Nộc"  # Typo for "Hà Nội"
processed_query = preprocess_text(province_name)
is_found, value, _ = province_trie.search(processed_query)

if is_found:
    print(f"Did you mean: {value}?")  # Will output: Did you mean: Hà Nội?
else:
    print("Province not found")
```

## Performance Considerations

- The Trie structure provides O(m) time complexity for lookup operations, where m is the length of the key
- Sliding windows Longest Match algorithm improves extraction accuracy with O(n²) complexity for each segment, where n is the number of words
- Right-to-left search improves accuracy for typical Vietnamese address formats
- Generating all possible variants increases memory usage but greatly improves error tolerance
- Case-insensitive matching with preservation of original capitalization adds minimal overhead
- For very large datasets, consider limiting the number of variants or implementing more sophisticated error models

## Extending the Project

- Add support for more complex error models
- Implement fuzzy searching with edit distance calculations
- Add an autocomplete feature based on the Trie structure
- Integrate with a web or GUI interface for easier interaction
- Include more context-aware parsing (e.g., recognize common address patterns)
- Add support for abbreviations (Tp. → Thành phố, Q. → Quận, etc.)