# Resume-Parser-Using-AI
Developed an AI-powered resume parser that extracts key information like name, contact, skills, education, and experience from resumes using Natural Language Processing (NLP). Utilized Python, spaCy, and regex to process and structure unstructured resume data into a readable format. 


step1: install important libraries
📚 Libraries Used
spaCy – For NLP tasks like tokenization and entity recognition

pdfminer.six – To extract text from PDF files

docx2txt – To extract text from DOCX files

pandas – For handling structured data (CSV, tables)

re – Python’s built-in regular expression module (used for pattern matching like emails or phone numbers)

step2: Change the Path of the file according to your system
step 3: start with login.py file having all information related to it like _username password_ also for parsing resume
step 4:in **data.py** file you must have to update your mysql password for data connection.
step 5 : **main.py** file is running and you have to select the resume and upload on it 
step6: you can message this person directly via mail through email button
step7:You can store the interested candidate into your Recorded database for further


Details working of it
1. Upload Resume File
User uploads a resume in PDF or DOCX format.

2. Extract Raw Text
The tool uses:

pdfminer.six to extract text from PDF files, or

docx2txt for DOCX files.

3. Clean and Preprocess Text
Removes extra spaces, special characters, or line breaks.

Prepares the text for NLP processing.

4. Natural Language Processing
Uses spaCy to:

Tokenize the text

Identify named entities (like names, locations, etc.)

Extract key sections like Education, Skills, Experience

5. Extract Specific Information
Uses regular expressions (re) and rules to extract:

📧 Email

📞 Phone number

🧠 Skills

🎓 Education

👤 Name (optional: from filename or content)

6. Structure the Data
The extracted data is organized into a structured format:

JSON

CSV

or displayed in the web interface

7. Display / Export
The final result is shown on a web page (using Flask/Streamlit) or saved to a file.



Images that helps you a lot
<img width="1069" height="789" alt="Screenshot 2025-07-31 203915" src="https://github.com/user-attachments/assets/91fd6ad6-77ce-4e54-bd51-0a9420e515db" />

<img width="1485" height="901" alt="Screenshot 2025-07-31 204230" src="https://github.com/user-attachments/assets/63b38fd2-a325-486b-ae44-62f797c41e20" />

<img width="1910" height="1045" alt="Screenshot 2025-07-31 204141" src="https://github.com/user-attachments/assets/0679b5e9-b262-425f-b576-78cd385a1254" />
<img width="476" height="267" alt="Screenshot 2025-07-31 204153" src="https://github.com/user-attachments/assets/73a2da07-69c2-48e0-85a5-f715caf0b16f" />
<img width="191" height="204" alt="Screenshot 2025-07-31 204214" src="https://github.com/user-attachments/assets/5a7d8f5c-e852-4af3-8ced-22dd0c7f1cfd" />

<img width="1485" height="901" alt="Screenshot 2025-07-31 204230" src="https://github.com/user-attachments/assets/7adcce5f-0194-46bb-881c-2ae62bc81f55" />

thankyou for watch







 wo
