import os
import requests
from bs4 import BeautifulSoup

def scrape_approved_bills():
    url = 'https://www.flsenate.gov/Session/Bills/2023'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the table containing the approved bills
    table = soup.find('table', class_='tablesorter')

    # Create a folder to store the bill files
    folder_name = 'FL_2023'
    os.makedirs(folder_name, exist_ok=True)

    # Extract bill details from the table rows
    for row in table.find_all('tr'):
        columns = row.find_all('td')

        # Extract the link to the bill text from the first column
        link = columns[0].find('a')
        if link:
            bill_num = link.text.strip()
            bill_txt_url = 'https://www.flsenate.gov' + link['href']

            # Fetch the bill text page
            bill_response = requests.get(bill_txt_url)
            bill_soup = BeautifulSoup(bill_response.content, 'html.parser')

            # Find the element containing the bill text
            bill_txt_element = bill_soup.find('pre', class_='engrossedText')

            if bill_txt_element:
                # Extract the bill text
                bill_txt = bill_txt_element.text.strip()

                # Store the bill text in a file
                file_name = f'{bill_num}.txt'
                file_path = os.path.join(folder_name, file_name)
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(bill_txt)

                print(f"Bill Number: {bill_num}")
                print(f"Bill text saved to: {file_path}")
                print("-----------------------")

# Call the function to start scraping approved bills and store them in files
scrape_approved_bills()
