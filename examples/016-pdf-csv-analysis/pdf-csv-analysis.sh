# First, install the Google Generative AI library and httpx (for downloading files)
$ pip install google-genai httpx pandas

# Then run the program with Python
$ python pdf_csv_analysis.py
PDF Analysis Result:
 The main company mentioned in the invoice is Sunny Farm.
CSV Analysis Result:
 Okay, I've analyzed the provided data. Here's a summary of its contents:
**Data Format:**
*   The data appears to be in CSV (Comma Separated Values) format.
*   The first line is a header row defining the fields.
*   Each subsequent line represents a record containing information about a person.
**Fields Present:**
The data includes the following fields for each person:
1.  **first\_name:** The person's first name.
2.  **last\_name:** The person's last name.
3.  **company\_name:** The name of the company they are associated with.
4.  **address:** The street address.
5.  **city:** The city.
6.  **county:** The county.
7.  **state:** The state.
8.  **zip:** The zip code.
9.  **phone1:** The primary phone number.
10. **phone2:** A secondary phone number.
11. **email:** The email address.
12. **web:** The website address (presumably for the associated company).
