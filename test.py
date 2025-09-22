import os
import json
import time
import string
import pandas as pd

# Import the Solution class from main.py
from main import Solution

# Normalization functions for handling equivalent names
def to_same(groups):
    same = {ele: k for k, v in groups.items() for ele in v}
    return same

# Define groups for normalization (similar to GettingStarted.ipynb)
groups_province = {}
groups_district = {'hòa bình': ['Hoà Bình', 'Hòa Bình'], 'kbang': ['Kbang', 'KBang'], 'quy nhơn': ['Qui Nhơn', 'Quy Nhơn']}
groups_ward = {'ái nghĩa': ['ái Nghĩa', 'Ái Nghĩa'], 'hòa bình': ['Hoà Bình', 'Hòa Bình']}
# Add number normalizations (01 = 1, etc.)
groups_ward.update({1: ['1', '01'], 2: ['2', '02'], 3: ['3', '03'], 4: ['4', '04'], 5: ['5', '05'], 
                    6: ['6', '06'], 7: ['7', '07'], 8: ['8', '08'], 9: ['9', '09']})

same_province = to_same(groups_province)
same_district = to_same(groups_district)
same_ward = to_same(groups_ward)

def normalize(text, same_dict):
    return same_dict.get(text, text)

def run_tests():
    # Path to the test file
    test_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "contest", "public.json")
    
    # Load test data
    print(f"Loading test data from {test_file_path}...")
    with open(test_file_path, 'r', encoding='utf-8') as file:
        test_data = json.load(file)
    print(f"Loaded {len(test_data)} test cases.\n")
    
    # Initialize Solution from main.py
    print("Initializing Solution class...")
    solution = Solution()
    print("Solution initialized successfully.\n")
    
    # Prepare results storage
    results = []
    timer = []
    correct_count = 0
    
    # Process each test case
    print("Processing test cases...")
    for test_idx, data_point in enumerate(test_data):
        address = data_point["text"]
        
        # Get expected answer
        answer = data_point["result"]
        answer["province_normalized"] = normalize(answer["province"], same_province)
        answer["district_normalized"] = normalize(answer["district"], same_district)
        answer["ward_normalized"] = normalize(answer["ward"], same_ward)
        
        # Process the address using the Solution class
        start_time = time.perf_counter_ns()
        result = solution.process(address)
        end_time = time.perf_counter_ns()
        execution_time = end_time - start_time
        timer.append(execution_time)
        
        # Normalize results
        result["province_normalized"] = normalize(result["province"], same_province)
        result["district_normalized"] = normalize(result["district"], same_district)
        result["ward_normalized"] = normalize(result["ward"], same_ward)
        
        # Check correctness
        province_correct = int(answer["province_normalized"] == result["province_normalized"])
        district_correct = int(answer["district_normalized"] == result["district_normalized"])
        ward_correct = int(answer["ward_normalized"] == result["ward_normalized"])
        total_correct = province_correct + district_correct + ward_correct
        
        correct_count += total_correct
        
        # Store results
        results.append([
            test_idx,
            address,
            answer["province"],
            result["province"],
            answer["province_normalized"],
            result["province_normalized"],
            province_correct,
            answer["district"],
            result["district"],
            answer["district_normalized"],
            result["district_normalized"],
            district_correct,
            answer["ward"],
            result["ward"],
            answer["ward_normalized"],
            result["ward_normalized"],
            ward_correct,
            total_correct,
            execution_time / 1_000_000_000,  # Convert to seconds
        ])
        
        # Print progress for every 100 test cases
        if (test_idx + 1) % 100 == 0:
            print(f"Processed {test_idx + 1}/{len(test_data)} test cases...")
    
    # Calculate statistics
    total_tests = len(test_data) * 3  # province, district, ward for each test
    accuracy = correct_count / total_tests
    score_out_of_10 = round(accuracy * 10, 2)
    
    max_time_sec = round(max(timer) / 1_000_000_000, 4) if timer else 0
    avg_time_sec = round((sum(timer) / len(timer)) / 1_000_000_000, 4) if timer else 0
    
    # Create summary DataFrame
    summary = pd.DataFrame(
        [[correct_count, total_tests, score_out_of_10, max_time_sec, avg_time_sec]],
        columns=['Correct', 'Total', 'Score /10', 'Max Time (sec)', 'Avg Time (sec)']
    )
    
    # Create detailed results DataFrame
    columns = [
        'ID', 'Text', 
        'Expected Province', 'Extracted Province', 'Expected Province Normalized', 'Extracted Province Normalized', 'Province Correct',
        'Expected District', 'Extracted District', 'Expected District Normalized', 'Extracted District Normalized', 'District Correct',
        'Expected Ward', 'Extracted Ward', 'Expected Ward Normalized', 'Extracted Ward Normalized', 'Ward Correct',
        'Total Correct', 'Time (sec)'
    ]
    
    details = pd.DataFrame(results, columns=columns)
    
    # Print summary
    print("\n" + "="*50)
    print(f"Test Results Summary:")
    print("="*50)
    print(summary)
    print("\nDetailed province results:")
    province_stats = details.groupby('Province Correct').size()
    print(f"Correct: {province_stats.get(1, 0)}, Incorrect: {province_stats.get(0, 0)}")
    
    print("\nDetailed district results:")
    district_stats = details.groupby('District Correct').size()
    print(f"Correct: {district_stats.get(1, 0)}, Incorrect: {district_stats.get(0, 0)}")
    
    print("\nDetailed ward results:")
    ward_stats = details.groupby('Ward Correct').size()
    print(f"Correct: {ward_stats.get(1, 0)}, Incorrect: {ward_stats.get(0, 0)}")
    
    # Save results to Excel
    excel_file = "test_results.xlsx"
    with pd.ExcelWriter(excel_file, engine='xlsxwriter') as writer:
        summary.to_excel(writer, sheet_name='Summary', index=False)
        details.to_excel(writer, sheet_name='Details', index=False)
    
    print(f"\nResults saved to {excel_file}")

if __name__ == "__main__":
    run_tests()