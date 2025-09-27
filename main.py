import os
import string
import re
import unicodedata

# Use the existing Trie structure from trie.py
from trie import Trie

def preprocess_text(text):
    """
    Preprocess the input text according to the following rules:
    1. Lower text, remove pre and post white-space
    2. Handle common Vietnamese address abbreviations
    3. Remove non-Vietnamese characters (j, z, w, ...)
    4. Remove pre and post punctuation
    
    Args:
        text: The input text string
        
    Returns:
        The preprocessed text string
    """
    # 1. Convert to lowercase and remove leading/trailing whitespaces
    text = text.lower().strip()
    
    # 2. Handle common Vietnamese address abbreviations
    text = text.replace('thành phố', "").replace('tp', "").replace('phố', "").replace('hcm', "hồ chí minh").replace(' hn', " hà nội ")
    text = text.replace('tỉnh', "").replace(' t ', " ").replace('huyện', "").replace(' h ', " ")
    text = text.replace('xã', "").replace(' x ', " ").replace('phường', "").replace(' p ', " ")
    
    # 3. Remove non-Vietnamese characters (j, z, w, ...)
    # Create a mapping of characters to be replaced
    non_viet_chars = {
        'j': 'i',
        'z': 's',
        'w': 'v',
        'f': 'ph',
    }
    
    for char, replacement in non_viet_chars.items():
        text = text.replace(char, replacement)
    
    # 4. Remove pre and post punctuation
    text = text.strip(string.punctuation)
    
    # Additional cleaning: normalize whitespace within the text
    text = ' '.join(text.split())
    
    return text

def generate_variants(word, max_variants=2000):
    """
    Generate variants of the word with the following cases:
    1. Missing character (deletion)
    2. Replaced character (substitution)
    3. Inserted character (insertion)
    4. Missing spaces (concatenation)
    
    Args:
        word: The original word
        max_variants: Maximum number of variants to generate to prevent memory issues
        
    Returns:
        A list of word variants
    """
    variants = set()
    
    # Original word
    variants.add(word)
    
    # Case 1: Missing character (deletion)
    for i in range(len(word)):
        # Skip deletion of spaces to maintain word boundaries
        if word[i] == ' ':
            continue
        variant = word[:i] + word[i+1:]
        variants.add(variant)
        if len(variants) > max_variants:
            return list(variants)
    
    # Case 2: Replaced character (substitution)
    for i in range(len(word)):
        # Skip replacing spaces to maintain word boundaries
        if word[i] == ' ':
            continue
        for char in string.ascii_lowercase + 'áàảãạăắằẳẵặâấầẩẫậđéèẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵ':
            if char != word[i]:
                variant = word[:i] + char + word[i+1:]
                variants.add(variant)
                if len(variants) > max_variants:
                    return list(variants)
    
    # Case 3: Inserted character (insertion)
    for i in range(len(word) + 1):
        for char in string.ascii_lowercase + 'áàảãạăắằẳẵặâấầẩẫậđéèẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵ':
            variant = word[:i] + char + word[i:]
            variants.add(variant)
            if len(variants) > max_variants:
                return list(variants)
    
    # Case 4: Missing spaces (concatenation)
    if ' ' in word:
        # Create a variant with all spaces removed
        no_space_variant = word.replace(' ', '')
        variants.add(no_space_variant)
        
        # Create variants with some spaces removed
        words = word.split()
        if len(words) > 1:
            for i in range(len(words) - 1):
                # Join words at position i and i+1
                concatenated = words.copy()
                concatenated[i] = concatenated[i] + concatenated[i+1]
                concatenated.pop(i+1)
                variants.add(' '.join(concatenated))
    
    return list(variants)

def insert_with_variants(trie, word, value=None):
    """
    Insert a word and its variants into the trie
    
    Args:
        trie: The Trie to insert into
        word: The word to insert
        value: Value associated with the word
    """
    # First insert the original word
    trie.insert(word, value)
    
    # Also insert the lowercase version to ensure case-insensitive matching
    lowercase_word = word.lower()
    if lowercase_word != word:
        trie.insert(lowercase_word, value)
    
    # Generate and insert variants based on the lowercase version
    # to ensure we capture all potential typos
    variants = generate_variants(lowercase_word)
    for variant in variants:
        # Insert variants but mark them as the original word
        # This ensures searches for variants find the original word
        trie.insert(variant, value)

def create_ward_trie(data_path):
    """
    Create a Trie tree from ward.txt file
    
    Args:
        data_path: Path to the dataset directory
        
    Returns:
        A Trie tree containing all ward names and their variants
    """
    ward_trie = Trie()
    file_path = os.path.join(data_path, "ward.txt")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                ward_name = line.strip()
                if ward_name:  # Skip empty lines
                    # Insert the original word without preprocessing
                    insert_with_variants(ward_trie, ward_name, ward_name)
        
        print(f"Ward Trie created successfully with data from {file_path}")
        return ward_trie
    except Exception as e:
        print(f"Error creating Ward Trie: {str(e)}")
        return None

def create_district_trie(data_path):
    """
    Create a Trie tree from district.txt file
    
    Args:
        data_path: Path to the dataset directory
        
    Returns:
        A Trie tree containing all district names and their variants
    """
    district_trie = Trie()
    file_path = os.path.join(data_path, "district.txt")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                district_name = line.strip()
                if district_name:  # Skip empty lines
                    # Insert the original word without preprocessing
                    insert_with_variants(district_trie, district_name, district_name)
        
        print(f"District Trie created successfully with data from {file_path}")
        return district_trie
    except Exception as e:
        print(f"Error creating District Trie: {str(e)}")
        return None

def create_province_trie(data_path):
    """
    Create a Trie tree from province.txt file
    
    Args:
        data_path: Path to the dataset directory
        
    Returns:
        A Trie tree containing all province names and their variants
    """
    province_trie = Trie()
    file_path = os.path.join(data_path, "province.txt")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                province_name = line.strip()
                if province_name:  # Skip empty lines
                    # Insert the original word without preprocessing
                    insert_with_variants(province_trie, province_name, province_name)
        
        print(f"Province Trie created successfully with data from {file_path}")
        return province_trie
    except Exception as e:
        print(f"Error creating Province Trie: {str(e)}")
        return None

# Solution class for testing according to GettingStarted.ipynb requirements
class Solution:
    def __init__(self):
        # List province, district, ward file paths
        self.province_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dataset", "province.txt")
        self.district_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dataset", "district.txt")
        self.ward_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dataset", "ward.txt")
        
        # Create the trie data structures for each administrative level
        self.province_trie = self._create_province_trie()
        self.district_trie = self._create_district_trie()
        self.ward_trie = self._create_ward_trie()
        
    def _create_province_trie(self):
        """
        Create a Trie tree from province.txt file
        
        Returns:
            A Trie tree containing all province names and their variants
        """
        province_trie = Trie()
        
        try:
            with open(self.province_path, 'r', encoding='utf-8') as file:
                for line in file:
                    province_name = line.strip()
                    if province_name:  # Skip empty lines
                        # Insert the original word without preprocessing
                        insert_with_variants(province_trie, province_name, province_name)
            
            return province_trie
        except Exception as e:
            print(f"Error creating Province Trie: {str(e)}")
            return Trie()
    
    def _create_district_trie(self):
        """
        Create a Trie tree from district.txt file
        
        Returns:
            A Trie tree containing all district names and their variants
        """
        district_trie = Trie()
        
        try:
            with open(self.district_path, 'r', encoding='utf-8') as file:
                for line in file:
                    district_name = line.strip()
                    if district_name:  # Skip empty lines
                        # Insert the original word without preprocessing
                        insert_with_variants(district_trie, district_name, district_name)
            
            return district_trie
        except Exception as e:
            print(f"Error creating District Trie: {str(e)}")
            return Trie()
    
    def _create_ward_trie(self):
        """
        Create a Trie tree from ward.txt file
        
        Returns:
            A Trie tree containing all ward names and their variants
        """
        ward_trie = Trie()
        
        try:
            with open(self.ward_path, 'r', encoding='utf-8') as file:
                for line in file:
                    ward_name = line.strip()
                    if ward_name:  # Skip empty lines
                        # Insert the original word without preprocessing
                        insert_with_variants(ward_trie, ward_name, ward_name)
            
            return ward_trie
        except Exception as e:
            print(f"Error creating Ward Trie: {str(e)}")
            return Trie()
    
    def process(self, address_text):
        """
        Extract address, performing three separate searches for each administrative level.
        """
        result = {
            "province": "",
            "district": "",
            "ward": ""
        }
        
        # 1. preprocess text
        processed_text = preprocess_text(address_text)
        
        # 2. split string by comma
        segments = [s.strip() for s in processed_text.split(',') if s.strip()]
        
        # TEMP variable to hold unmatched segments
        unmatched_segments = list(segments)
        
        # =================================================================
        # FIND PROVINCE (PROVINCE)
        # =================================================================
        segments_after_province_pass = []
        for segment in reversed(unmatched_segments):
            words = segment.split()
            found = False
            for i in range(len(words)):
                phrase = " ".join(words[i:])
                print("phrase:", phrase)
                # Apply preprocessing to phrase before searching
                processed_phrase = preprocess_text(phrase)
                print("processed_phrase:", processed_phrase)
                is_found, value, _ = self.province_trie.search(processed_phrase)
                if is_found and not result["province"]:
                    result["province"] = value
                    # Store the remaining part for next passes
                    remaining_part = " ".join(words[:i])
                    if remaining_part:
                        segments_after_province_pass.insert(0, remaining_part)
                    found = True
                    break
            if not found:
                segments_after_province_pass.insert(0, segment)
        unmatched_segments = segments_after_province_pass

        # =================================================================
        # FIND DISTRICT (DISTRICT)
        # =================================================================
        segments_after_district_pass = []
        for segment in reversed(unmatched_segments):
            words = segment.split()
            found = False
            for i in range(len(words)):
                phrase = " ".join(words[i:])
                # Apply preprocessing to phrase before searching
                processed_phrase = preprocess_text(phrase)
                is_found, value, _ = self.district_trie.search(processed_phrase)
                if is_found and not result["district"]:
                    result["district"] = value
                    remaining_part = " ".join(words[:i])
                    if remaining_part:
                        segments_after_district_pass.insert(0, remaining_part)
                    found = True
                    break
            if not found:
                segments_after_district_pass.insert(0, segment)
        unmatched_segments = segments_after_district_pass

        # =================================================================
        # FIND WARD (WARD)
        # =================================================================
        segments_after_ward_pass = []
        for segment in reversed(unmatched_segments):
            words = segment.split()
            found = False
            for i in range(len(words)):
                phrase = " ".join(words[i:])
                # Apply preprocessing to phrase before searching
                processed_phrase = preprocess_text(phrase)
                is_found, value, _ = self.ward_trie.search(processed_phrase)
                if is_found and not result["ward"]:
                    result["ward"] = value
                    remaining_part = " ".join(words[:i])
                    if remaining_part:
                        segments_after_ward_pass.insert(0, remaining_part)
                    found = True
                    break
            if not found:
                segments_after_ward_pass.insert(0, segment)
        unmatched_segments = segments_after_ward_pass
        
        return result

# Example usage:
if __name__ == "__main__":
    dataset_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dataset")
    
    # Create Trie trees for each dataset
    ward_trie = create_ward_trie(dataset_path)
    district_trie = create_district_trie(dataset_path)
    province_trie = create_province_trie(dataset_path)
    
    # Example of searching in the tries with exact words
    if ward_trie:
        test_ward = "Phú Mỹ"
        processed_query = preprocess_text(test_ward)
        is_found, value, word = ward_trie.search(processed_query)
        if is_found:
            print(f"Found ward: {value}")
        else:
            print(f"Ward '{test_ward}' not found")
    
    # Example of searching in the tries with typos
    if district_trie:
        test_district = "Hà Đng"  # Missing 'o' from "Hà Đông"
        processed_query = preprocess_text(test_district)
        is_found, value, word = district_trie.search(processed_query)
        if is_found:
            print(f"Typo detected: '{test_district}' is probably '{value}'")
        else:
            print(f"District '{test_district}' not found")
    
    # Test with non-Vietnamese characters
    if province_trie:
        test_province = "Hồ Chí Minh."  # With punctuation
        processed_query = preprocess_text(test_province)
        print(f"Original: '{test_province}', Processed: '{processed_query}'")
        is_found, value, word = province_trie.search(processed_query)
        if is_found:
            print(f"Found province: '{value}'")
        else:
            print(f"Province '{test_province}' not found")
        
        # Test with j, z, w characters
        test_province_with_j = " Hồ Zhí Minh "  # With 'z' instead of 'ch'
        processed_query = preprocess_text(test_province_with_j)
        print(f"Original: '{test_province_with_j}', Processed: '{processed_query}'")
        is_found, value, word = province_trie.search(processed_query)
        if is_found:
            print(f"Found province: '{value}'")
        else:
            print(f"Province '{test_province_with_j}' not found")
        
        # Test with . characters
        test_province_with_dot = "T Giang"  # With punctuation
        processed_query = preprocess_text(test_province_with_dot)
        print(f"Original: '{test_province_with_dot}', Processed: '{processed_query}'")
        is_found, value, word = province_trie.search(processed_query)
        if is_found:
            print(f"Found province: '{value}'")
        else:
            print(f"Province '{test_province_with_dot}' not found")
        
    

    # Test the Solution class
    # print("\nTesting Solution class:")
    # solution = Solution()
    # address = "284DBis Ng Văn Giáo, P3, Mỹ Tho, T.Giang."
    # result = solution.process(address)
    # print(f"Input: {address}")
    # print(f"Extracted: Province={result['province']}, District={result['district']}, Ward={result['ward']}")