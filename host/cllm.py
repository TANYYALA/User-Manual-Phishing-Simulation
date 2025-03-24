import google.generativeai as genai
import pandas as pd
import os
import time

# Initialize Gemini API Key
genai.configure(api_key="AIzaSyCl4kydhpekfITQKCjMHuBnxYlcYCp6Buc")

# Enhanced email generation prompt template
email_prompt_template = """
You are a highly skilled professional email designer, known for creating detailed and comprehensive HTML email templates. Each email should meet the following criteria:

### Email Specifications:
1. **HTML Structure**:
    - Use `<html>`, `<head>`, and `<body>` tags for each email.
    - Include design elements like `<div>`, `<table>`, `<ul>`, and `<img>` for variety.
    - Apply inline or embedded CSS for polished styling.
2. **Content**:
    - Write a **large, detailed body** with at least 500 words or 5 paragraphs.
    - Start with a professional greeting: "Dear {recipient},"
    - Expand the main body with context, explanations, and engaging details.
    - Include elements like bullet points or tables where appropriate.
3. **Call-to-Action**:
    - Include styled buttons or links (e.g., "Verify Now" or "Learn More").
    - Ensure all links in the email, including the call-to-action links, redirect to: https://nithin1207v.github.io/phishing-awareness/?id=ngit.cyberguard
4. **Signature**:
    - End with a professional closing: "Sincerely," followed by "[Your Name], [Your Position]."
5. **No Placeholders**:
    - Each email should be a complete and stand-alone HTML template.

### Task:
Generate exactly 1 complete email template in HTML format for the following details:
- **Subject**: {subject}
- **Purpose**: {purpose}
- **Recipient**: {recipient}

Ensure the template is professional, detailed, and aligns with the provided input details.
"""

# Categories and Prompts
categories = {
    "Banking": [
        ("Verify Your Account Details to Avoid Disruption", "To ensure account continuity by prompting verification.", "Customer"),
        ("Your Bank Statement is Ready for Download", "To inform the recipient about their account statement availability.", "Customer"),
        ("New Security Alert: Confirm Your Login Activity", "To notify the recipient about unusual login activity.", "Customer")
    ],
    "E-commerce": [
        ("Exclusive Offer: Limited-Time Discount Just for You!", "To inform the customer about a personalized discount.", "Shopper"),
        ("Order Shipped: Track Your Package Now", "To provide shipment tracking details.", "Customer"),
        ("Abandoned Cart Reminder: Complete Your Purchase Today!", "To remind the customer about unpurchased items in their cart.", "Shopper")
    ],
    "Insurance": [
        ("Renew Your Policy Before Expiration", "To remind the customer to renew their insurance policy.", "Policyholder"),
        ("Claim Approved: Next Steps & Payout Details", "To inform the customer about their claim approval.", "Policyholder"),
        ("Exclusive Health Insurance Plans for You", "To promote new health insurance plans.", "Customer")
    ],
    "Healthcare": [
        ("Your Upcoming Appointment Reminder", "To notify the patient about their scheduled appointment.", "Patient"),
        ("Lab Test Results Available Online", "To inform the patient that their test results are ready.", "Patient"),
        ("Annual Health Checkup: Schedule Today", "To encourage the patient to book their annual checkup.", "Patient")
    ]
}

# Initialize model
model = genai.GenerativeModel("gemini-1.5-flash-8b")

# Define output file path
output_file = "C:\\Users\\gumma\\OneDrive\\Desktop\\email_templates.xlsx"

def safe_write_to_excel(output_file, new_df):
    max_retries = 5  # Number of retries
    retry_delay = 3  # Seconds to wait before retrying
    
    for attempt in range(max_retries):
        try:
            with pd.ExcelWriter(output_file, mode='a', if_sheet_exists='overlay') as writer:
                new_df.to_excel(writer, index=False, sheet_name="Templates", header=False)
            print(f"Email templates appended to {output_file}")
            return  # Exit the function if successful
        except PermissionError:
            print(f"Permission denied. Retrying in {retry_delay} seconds... ({attempt + 1}/{max_retries})")
            time.sleep(retry_delay)  # Wait and retry
    
    print(f"Failed to write to {output_file} after {max_retries} attempts. Please close the file and try again.")

def generate_email_templates():
    data = []
    
    for category, prompts in categories.items():
        for subject, purpose, recipient in prompts:
            try:
                print(f"Generating Email for {category} - {subject}...")
                prompt = email_prompt_template.format(subject=subject, purpose=purpose, recipient=recipient)
                result = model.generate_content([prompt])
                email_body = result.text.strip()
                data.append([category, subject, email_body])
                print(f"Email for {category} - {subject} saved.")
            except Exception as e:
                print(f"Error generating email for {category} - {subject}: {e}")
    
    # Convert to DataFrame
    new_df = pd.DataFrame(data, columns=["Category", "Subject", "Template"])
    
    # Write to Excel with safe retry logic
    safe_write_to_excel(output_file, new_df)

# Run email generation
generate_email_templates()
