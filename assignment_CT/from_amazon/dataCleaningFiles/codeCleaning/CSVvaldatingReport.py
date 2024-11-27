import pandas as pd
import numpy as np

# Load CSV file
file_path = './CurrentWorkingFile/corrected_data_lowercase_brands.csv'  # Update with the correct file path
data = pd.read_csv(file_path)

# Initialize report dictionary to store validation results
report = {}

# 1. Check Data Types
def check_data_types(df):
    expected_types = {
        'Brand': str,
        'Price': np.int64,
        'Rating': float,
        'Rating_Count': np.int64,
        'Best_Seller_Rank_Home_Improvement': np.int64,
        'Best_Seller_Rank_Home_Security': np.int64,
        'Product_Title': str,
        'Product_URL': str
    }
    mismatches = []
    for column, expected_type in expected_types.items():
        if not pd.api.types.is_dtype_equal(df[column].dtype, expected_type):
            mismatches.append((column, df[column].dtype, expected_type))
    return mismatches

report['data_type_mismatches'] = check_data_types(data)

# 2. Check for Missing Values
missing_values = data.isnull().sum()
report['missing_values'] = missing_values[missing_values > 0].to_dict()

# 3. Detect Outliers in Numerical Data (e.g., Price, Rating)
outliers = {
    'Price': data[~data['Price'].between(0, 100000)].shape[0],
    'Rating': data[~data['Rating'].between(0, 5)].shape[0],
    'Rating_Count': data[data['Rating_Count'] < 0].shape[0],
    'Best_Seller_Rank_Home_Improvement': data[data['Best_Seller_Rank_Home_Improvement'] <= 0].shape[0],
    'Best_Seller_Rank_Home_Security': data[data['Best_Seller_Rank_Home_Security'] <= 0].shape[0]
}
report['outliers'] = {k: v for k, v in outliers.items() if v > 0}

# 4. Ensure Uniqueness of Product URLs
duplicate_urls = data.duplicated(subset=['Product_URL']).sum()
report['duplicate_urls'] = duplicate_urls

# 5. Validate Rank Columns
invalid_ranks = {
    'Best_Seller_Rank_Home_Improvement': data[~data['Best_Seller_Rank_Home_Improvement'].between(1, 1e6)].shape[0],
    'Best_Seller_Rank_Home_Security': data[~data['Best_Seller_Rank_Home_Security'].between(1, 1e6)].shape[0]
}
report['invalid_ranks'] = {k: v for k, v in invalid_ranks.items() if v > 0}

# 6. Cross-Verify Brand Names for Consistency
# Convert all brand names to lowercase for uniformity and count unique brands
data['Brand'] = data['Brand'].str.lower()
unique_brands = data['Brand'].nunique()
report['unique_brands_count'] = unique_brands

# Print report
for key, value in report.items():
    print(f"{key}: {value}")

# Provide a summary of the CSV readiness
issues = {k: v for k, v in report.items() if v}
if issues:
    print("\nThe CSV file has issues that need to be addressed before analysis:")
    for key, value in issues.items():
        print(f"{key}: {value}")
else:
    print("\nThe CSV file is ready for analysis.")
