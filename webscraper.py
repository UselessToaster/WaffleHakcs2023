import os
import requests
from bs4 import BeautifulSoup

base_url = 'https://www.flsenate.gov'

def main():
    url = 'https://www.flsenate.gov/Session/Bills/2023'
    html = requests.get(url)
    soup = BeautifulSoup(html.content, 'html.parser')

    # First page
    scrape_bills_page(url)

    # Iterate through every page on the website
    nxt_pg = soup.find('a', class_='next')
    while nxt_pg:
        next_url = base_url + nxt_pg['href']
        print(next_url)
        scrape_bills_page(next_url)

        html = requests.get(next_url)
        soup = BeautifulSoup(html.content, 'html.parser')
        nxt_pg = soup.find('a', class_='next')

def scrape_bills_page(url):
    html = requests.get(url)
    soup = BeautifulSoup(html.content, 'html.parser')

    # Find the table containing the bills
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

                # Extract the link to the bill page from the first column
                link = columns[0].find('a')
                if link:
                    bill_num = link.text.strip()
                    bill_pg_url = base_url + link['href']

                    # Fetch the bill text page
                    bill_html = requests.get(bill_pg_url)
                    bill_soup = BeautifulSoup(bill_html.content, 'html.parser')

                    print(f"Bill Number: {bill_num}")
                    print(f"Bill Text URL: {bill_pg_url}")

                    # Find the element containing the bill text
                    bill_txt_elem = bill_soup.find('span', class_='bold', text='Bill Text:').find_next('a')

                    if bill_txt_elem:
                        # Extract the bill text
                        bill_txt_url = base_url + bill_txt_elem['href']
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


main()
