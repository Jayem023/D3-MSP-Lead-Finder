# lead_finder.py - A simple script to filter MSP leads

def process_leads(data):
    """Filter leads that belong to the MSP industry."""
    qualified_leads = [lead for lead in data if lead.get("industry") == "MSP"]
    return qualified_leads

if __name__ == "__main__":
    # Sample data to test the script
    sample_data = [
        {"name": "ABC IT", "industry": "MSP", "email": "contact@abcit.com"},
        {"name": "XYZ Corp", "industry": "Finance", "email": "info@xyzcorp.com"}
    ]

    print("Qualified MSP Leads:")
    print(process_leads(sample_data))
