import pandas as pd
import re

def load_data(file_path):
    """Load raw data from a CSV or Excel file."""
    if file_path.endswith('.csv'):
        return pd.read_csv(file_path)
    elif file_path.endswith(('.xls', '.xlsx')):
        return pd.read_excel(file_path)
    else:
        raise ValueError("Unsupported file format. Please use CSV or Excel.")

# Define MSP-related keywords
MSP_KEYWORDS = {
    "Service-Based MSP Keywords": [
        "Remote IT Support", "Managed Cloud Solutions", "IT Outsourcing", "IT Service Management", "Virtual CIO"
    ],
    "Specialized MSP Offerings": [
        "Disaster Recovery Services", "Cyber Threat Management", "Endpoint Security Provider", "Cloud Backup Solutions",
        "Managed Firewall Provider", "Compliance & Security Management"
    ],
    "Industry-Specific MSP Terms": [
        "Healthcare IT Services", "Legal IT Support", "Financial IT Services", "Government IT Support", "Education IT Solutions"
    ]
}

# Flatten keyword list for easy searching
ALL_KEYWORDS = [kw.lower() for category in MSP_KEYWORDS.values() for kw in category]

def filter_msp_leads(df):
    """Filter leads based on MSP-related keywords."""
    def keyword_match(text):
        if pd.isna(text):
            return False
        text_lower = str(text).lower()
        return any(re.search(rf'\b{kw}\b', text_lower) for kw in ALL_KEYWORDS)

    # Apply filtering across relevant columns
    relevant_columns = ['Company Name', 'Industry', 'Description', 'Services']
    df['MSP Match'] = df[relevant_columns].apply(lambda row: any(keyword_match(row[col]) for col in relevant_columns), axis=1)
    
    return df[df['MSP Match']]

def clean_data(df):
    """Clean and standardize data for CRM upload."""
    df = df.drop_duplicates()
    df = df.dropna(subset=['Company Name', 'Email', 'Phone'])  # Keep only essential fields
    df = df.rename(columns=lambda x: x.strip().title())
    return df

def save_to_excel(df, output_path):
    """Save filtered leads to an Excel file."""
    df.to_excel(output_path, index=False)
    print(f"Filtered leads saved to {output_path}")

if __name__ == "__main__":
    input_file = "raw_leads.xlsx"  # Change this as needed
    output_file = "filtered_msp_leads.xlsx"
    
    data = load_data(input_file)
    filtered_data = filter_msp_leads(data)
    cleaned_data = clean_data(filtered_data)
    save_to_excel(cleaned_data, output_file)
