import google.generativeai as genai
import os
import re
import nltk
import pandas as pd
from textblob import TextBlob
from io import StringIO
import json
import random


nltk.download('punkt')

# Initialize Gemini API Key
genai.configure(api_key="AIzaSyA0CGp14csv72KDQk_KEyV4SD1TkvlrqtQ")

# Function to clean and analyze text
def clean_and_analyze_text(text):
    """Cleans input text and ensures professional tone."""
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)  # Remove non-ASCII characters
    text = re.sub(r'\s+', ' ', text).strip()  # Remove extra whitespace
    sentiment = TextBlob(text).sentiment

    if sentiment.polarity < -0.2:
        if sentiment.subjectivity > 0.5:
            text = "This content might be too subjective. Consider making it more objective. " + text
    
    return text

# Function to clean unwanted phrases
def clean_unwanted_phrases(text):
    """Remove unwanted phrases related to links."""
    unwanted_phrases = ["Phishing Awareness", "phishing awareness", "cyberguard", "nithin1207v", "ngit.cyberguard"]

    for phrase in unwanted_phrases:
        pattern = rf'(?<!href=")\b{re.escape(phrase)}\b(?!")'
        text = re.sub(pattern, '', text, flags=re.IGNORECASE)

    text = re.sub(r'\s+', ' ', text).strip()  # Clean extra spaces
    return text

# Function to train the LLM with extracted templates
def train_llm_with_templates(file_path='C:\\Users\\gumma\\OneDrive\\Desktop\\New folder\\wb\\wb\\web view\\web\\full_email_templates.csv'):
    df = pd.read_csv('C:\\pishing\\front end\\host\\host\\full_email_templates.csv')

    model = genai.GenerativeModel("gemini-1.5-flash-8b")
    training_data = ""

    for _, row in df.iterrows():
        training_data += f"Category: {row['Category']}\nEmail Body: {row['Email Body']}\n\n"

    return model, training_data
# ✅ Function to generate a random product/order ID
def generate_random_id():
    return str(random.randint(10000000000, 99999999999))

# Email prompt template
email_prompt_template = """
You are a highly skilled professional email designer, known for creating detailed and comprehensive HTML email templates. Each email should meet the following criteria:

### Email Specifications:
1. **HTML Structure**:
    - Use `<html>`, `<head>`, and `<body>` tags for each email.
    - Include design elements like `<div>`, `<table>`, `<ul>`, and `<img>` for variety.
    - Apply inline or embedded CSS for polished styling.
    - **Avoid any phishing-like language or overly urgent messaging.**
    
    - **Do not include company logos, branding banners, or any placeholder images.**
2. **Content**:
*Use a neutral, professional, and friendly tone.**
    - Write a **large, detailed body** with at least 200 words or 2 paragraphs.
    - Start with a professional greeting: "Dear {recipient},"
    - Expand the main body with context, explanations, and engaging details.
    - **Do not add any generic branding elements such as "Company Logo" at the top.**
    - Include elements like bullet points or tables where appropriate.
    - **DO NOT MENTION any delivery dates like "Expected Delivery Date," "Delivered by [date]," or similar.**
    - If you need to mention an order number, generate a random 10-12 digit number like {random_id}.
     Include useful details in a **helpful, reassuring** way.
**Call-to-Action:**
    - If a CTA is needed, **use soft language**, such as:
      - `"Visit Our Website"` instead of `"Click Here to Confirm"`
      - `"Check Your Account Settings"` instead of `"Update Your Information"`
    - ensure that the button is placed at the middle or in new line of the template, rather than being in the middle of the text. 
    - the redirection of the button should only redirect to "https://teamy-labs.github.io/phishing-awareness-/?id={email.split("@")[0]}"
    - DO NOT generate multiple buttons or secondary links like:
      - "View Order Details"
      - "Check Delivery Date"
      - "Track Shipment"
    - **Ensure there is ONLY ONE CTA button per email.**
4. **Signature**:
    - End with a professional closing: "Sincerely," followed by "[Your Name], [Your Position]."
5. **No Placeholders**:
    - Each email should be a complete and stand-alone HTML template.
    - **Ensure no unnecessary placeholders such as "Company Logo" appear anywhere in the email.**
6. **Important Restrictions**:
    - **DO NOT** include explanations, analysis, or additional commentary after the email body.
    - **DO NOT** add any "Explanation of Changes" or security notes at the end.
    - The email must **end with the signature** and **nothing else**.
7. **Personalized Details**:
    - Include dynamic placeholders:
      - "Dear {name}," (recipient's name)
      - Location: {address}
      - Department: {department}
      
    - Ensure these placeholders are replaced dynamically for each recipient.
### Task:
Generate exactly 1 complete email template in HTML format for the following details:
- **Subject**: {subject}
- **Purpose**: {purpose}
- **Recipient**: {recipient}

Ensure the template is professional, detailed, and aligns with the provided input details.
"""
def modify_email_links(email_body, email_id):
    """Dynamically replace the phishing-awareness URL with userID"""
    user_id = email_id.split('@')[0]
    updated_email_body = email_body.replace(
        'https://teamy-labs.github.io/phishing-awareness/', 
        f'https://teamy-labs.github.io/phishing-awareness-/?id={user_id}'
    )
    return updated_email_body






# Function to generate email templates based on trained model
import concurrent.futures

def generate_templates(model, training_data, category, email_details):
    """Generates 5 email templates per prompt using the trained LLM in parallel."""

    category_prompts = {
        "Banking": [
            ("Account Update: Review Your Information", "To ensure your account details remain up-to-date.", "Customer"),
            ("Your Monthly Bank Statement is Now Available", "To inform the recipient about their latest statement.", "Customer"),
            ("Login Activity Notification: Your Recent Access", "To provide a summary of recent login activity for security awareness.", "Customer")
        ],

        "Delivery": [
            ("Track Your Order – Delivery Scheduled Soon", "To inform the recipient about the status of their order and provide tracking details for transparency and assurance regarding the delivery schedule.", "Customer"),
            ("Delivery Confirmation Required – Verify Your Details", "To prompt the recipient to confirm or update their delivery details to ensure the successful and timely arrival of their package.", "Customer"),
            ("Your Package Is on the Way – Expected Delivery Date", "To notify the recipient that their package has been shipped and provide the estimated delivery date to manage their expectations", "Customer")
        ],
        "Retail": [
            ("Exclusive Offers Just for You!", "To promote special discounts and offers.", "Customer"),
            ("Your Order Has Been Shipped", "To confirm shipment of a customer's order.", "Customer"),
            ("New Arrivals: Check Out the Latest Trends", "To inform customers about new products.", "Customer")
        ],
        "Technology": [
            ("Your Subscription Renewal Notice", "To remind users about upcoming subscription renewals.", "User"),
            ("New Software Update Available", "To notify users of the latest software updates.", "User"),
            ("Join Our Tech Webinar for Free", "To invite users to attend a technology-related webinar.", "User")
        ],
        "Education": [
            ("Upcoming Semester Enrollment Reminder", "To remind students to enroll for the next semester.", "Student"),
            ("Important Exam Schedule Update", "To notify students about changes in the exam schedule.", "Student"),
            ("Scholarship Opportunities You Shouldn't Miss", "To inform students about available scholarships.", "Student")
        ]
    }
    print(f"DEBUG: Input email details: {email_details}")
    if category not in category_prompts:
        print(f"❌ Error: No prompts found for category '{category}'")
        return {}

    print(f"🚀 Generating email templates for category: {category}")

    # Initialize emails dictionary
    emails = {detail["email"]: [] for detail in email_details}  # Use email as the key

    # Function to generate a single email template
    def generate_email(email_detail, subject, purpose, recipient):
        try:
            # Extract recipient details
            email = email_detail.get("email", "N/A")
            name = email_detail.get("name", "N/A")
            address = email_detail.get("address", "N/A")
            department = email_detail.get("department", "N/A")
       

            # Validate required fields
            if not name:
                name = "User"
            if not address:
                address = "N/A"
            if not department:
                department = "N/A"
            
            


            # ✅ Generate a random common American name
            common_names = [
                "David Parker", "Emily Ross", "Robert Green", "Sarah Thompson", 
                "James Carter", "Jessica Moore", "Daniel Scott", "Amanda White",
                "John Taylor", "Laura Martinez"
            ]

            # ✅ Generate a random professional position
            professional_positions = [
                "Customer Service Manager", "Delivery Support Executive",
                "Account Manager", "Subscription Coordinator",
                "Billing Department Head", "Customer Experience Officer",
                "Corporate Communications Lead", "Relationship Manager"
            ]

            # ✅ Randomly pick a name and position
            random_name = random.choice(common_names)
            random_position = random.choice(professional_positions)



            # Debug details
            print(f"DEBUG: Extracted details for email: {email}")
            print(f"DEBUG: Name: {name}, Address: {address}, Department: {department}")

            subject = subject.replace("Verify", "Review").replace("Confirm", "Check").replace("Security Alert", "Login Notification")
            # Construct the prompt
            prompt = f"""
            {email_prompt_template}

            Generate exactly 1 complete email template in HTML format for the following details:
            - **Subject**: {subject}
            - **Purpose**: {purpose}
            - **Recipient**: {recipient}
            - **Name**: {name}
            - **Address**: {address}
            - **Department**: {department}
            

            Ensure:
            - No logos, no placeholders.
            - Use `<a href>` button style with the embedded email ID.
            - Follow my exact training data template for consistency.
            - Avoid giving clear instructions like "verify your email" but rather use neutral tones.
            - Ensure {name}, {address}, {department} are part of the email body.
            - Write a **large, detailed body** with at least 200 words or 2 paragraphs.
            """
            print(f"DEBUG: Prompt for email: {email}\n{prompt}")

            # Generate email content
            result = model.generate_content([prompt])
            if not hasattr(result, 'text') or not result.text:
                print(f"❌ Error: Model returned empty response for email: {email}")
                return None

            email_body = result.text.strip()
            print(f"DEBUG: Raw email body returned by model for {email}:\n{email_body}")
            

            # Replace placeholders with actual details
            print(f"DEBUG: Replacing placeholders in email body for {email}")
            email_body = email_body.replace("{name}", name or "Dear Valued Customer")
            email_body = email_body.replace("{address}", address or "N/A")
            email_body = email_body.replace("{department}", department or "N/A")

            # ✅ Automatically replace any placeholder with real values
            email_body = re.sub(r"\[Your Name\]", random_name, email_body)
            email_body = re.sub(r"\[Your Position\]", random_position, email_body)
            email_body = re.sub(r"\[.*?\]", "", email_body)  # Remove any remaining placeholders

             # ✅ Remove unexpected triple quotes like '''html and '''
            email_body = re.sub(r"^'''.*?html|'''$", "", email_body, flags=re.MULTILINE).strip()
            email_body = re.sub(r"^'''html|'''$", "", email_body, flags=re.IGNORECASE).strip()
            
            # ✅ Ensure only one CTA button exists
            email_body = re.sub(r'<a\s+href="[^"]*".*?</a>', '', email_body, flags=re.DOTALL)  # Remove existing buttons
            # ✅ Dynamically generate the embedded URL for "Visit Our Website"
            email_body = re.sub(r'<a\s*href="[^"]*"\s*class="button">.*?</a>', '', email_body)  # Remove any existing buttons

            # ✅ Inject a clean button without any wrapping <a>
            email_body += f"""
            <p style="text-align:center;">
            <a href="https://teamy-labs.github.io/phishing-awareness-/?id={email.split('@')[0]}" 
                style="padding:10px 20px; background-color:#4CAF50; color:white; text-decoration:none; border-radius:5px;">
                View Your Account Overview
            </a>
            </p>
            """
            




            # ✅ Remove any unwanted empty <a> tags injected by Gemini
            email_body = re.sub(r'<a\s*href="https://teamy-labs.github.io/phishing-awareness-/">\s*</a>', '', email_body)



            print(f"DEBUG: Final email body for {email}:\n{email_body}")

            return email, subject, email_body

        except Exception as e:
            print(f"❌ Error generating template for {email}: {e}")
            return None

    # Use ThreadPoolExecutor to handle parallel email generation
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_email = {
            executor.submit(generate_email, detail, subject, purpose, recipient): detail["email"]
            for detail in email_details
            for subject, purpose, recipient in category_prompts[category]
        }

        for future in concurrent.futures.as_completed(future_to_email):
            result = future.result()
            if result:
                email, subject, body = result
                emails[email].append((subject, body))  # Append subject-body pairs

    print(f"✅ Successfully generated {sum(len(templates) for templates in emails.values())} email templates.")
    return emails