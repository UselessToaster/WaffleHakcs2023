import os
import requests
from bs4 import BeautifulSoup


def scrape_approved_bills():
    url = 'https://www.flsenate.gov/Session/Bills/2023'
    html = requests.get(url)
    soup = BeautifulSoup(html.content, 'html.parser')


    # Find the table containing the approved bills
    table = soup.find('table', class_='width100 clickableRows tbl')

    if table:
        # Create a folder to store the bill files
        folder_name = 'FL_2023'
        os.makedirs(folder_name, exist_ok=True)

        # Find the tbody element within the table
        tbody = table.find('tbody')

        if tbody:
            # Extract bill details from the table rows within tbody
            for row in tbody.find_all('tr'):
                columns = row.find_all('th')

                # Extract the link to the bill text from the first column
                link = columns[0].find('a')
                print(link)
                if link:
                    bill_num = link.text.strip()
                    bill_pg_url = 'https://www.flsenate.gov' + link['href']

                    # Fetch the bill text page
                    bill_html = requests.get(bill_pg_url)
                    bill_soup = BeautifulSoup(bill_html.content, 'html.parser')

                    print(f"Bill Number: {bill_num}")
                    print(f"Bill Text URL: {bill_pg_url}")

                    # Find the element containing the bill text
                    bill_txt_elem = bill_soup.find('span', class_='bold', text='Bill Text:').find_next('a')

                    if bill_txt_elem:
                        # Extract the bill text
                        bill_txt_url = 'https://www.flsenate.gov' + bill_txt_elem['href']
                        bill_txt_html = requests.get(bill_txt_url)
                        bill_txt_soup = BeautifulSoup(bill_txt_html.content, 'html.parser')
                        bill_txt = bill_txt_soup.get_text()

                        # Store the bill text in a file
                        file_name = f'{bill_num}.txt'
                        file_path = os.path.join(folder_name, file_name)
                        with open(file_path, 'w', encoding='utf-8') as file:
                            file.write(bill_txt)

                        print(f"Bill text saved to: {file_path}")
                        print("-----------------------")
        else:
            print("No tbody element found.")

    else:
        print("Table not found.")

# Call the function to start scraping approved bills and store them in files
scrape_approved_bills()
