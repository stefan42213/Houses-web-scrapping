from urllib.request import urlopen
import pandas as pd
from unidecode import unidecode
import re
import aiohttp
import asyncio


# Class collecting link to single Announcement and then collecting all data by web html
class Announcement():
    def __init__(self, link):
        self.link = link
        self.html = None
        self.price = ""
        self.size = ""
        self.rooms = ""
        self.description = ""
        self.rent = ""

    # Get the HTML content of the page
    def get_page_html(self):
        page = urlopen(self.link)
        html_bytes = page.read()
        self.html = html_bytes.decode("utf-8")

    # Find price in web html
    def finding_price(self):
        #We are looking for </h3> end because here is value of house hidden and we saving text in variable
        end_text = '</h3>'
        end_Index = self.html.find(end_text)
        price = self.html[end_Index - 14:end_Index - 3]

        #Removing spaces and replacing ',' with '.'
        for i in price:
            if(i == ' '):
                pass
            elif(i == ','):
                self.price+= '.'
            else:
                self.price+=i

        #Here we are trying to remove useless signs from text because we are getting some larger text from page for example not only price but some trash values before
        # it isnt that easy to remove those values in downloading because for every annoucmment those are different. So now we are making func whitch delete first element
        #from our string until we got value we can convert to float
        x=1
        while len(self.price) != 0:
            self.price = self.price[x:]
            try:
                float(self.price)
                break
            except ValueError:
                continue


    # Find the size of the house using web html
    def finding_size(self):
        # Find the beginning of the string
        to_find = self.html.find('<p class="css-b5m1rv er34gjf0">Powierzchnia:')
        self.size = self.html[to_find + 45:to_find + 60]

        # Remove unnecessary characters from the end until we get a value we can convert to float
        x = 1
        while len(self.size) != 0:
            self.size = self.size[:-x]
            try:
                float(self.size)
                break
            except ValueError:
                continue

    # Find the number of rooms in the web html file
    def finding_rooms_number(self):
        # Find the beginning of the string
        to_find = self.html.find('<p class="css-b5m1rv er34gjf0">Liczba pokoi:')
        self.rooms = self.html[to_find + 45:to_find + 54]

        # Remove unnecessary characters from the end until we get a value we can convert to float
        x = 1
        while len(self.rooms) != 0:
            self.rooms = self.rooms[:-x]
            try:
                float(self.rooms)
                break
            except ValueError:
                continue

    # Find rent price of the Announcement
    def finding_the_rent(self):
        to_find = self.html.find('Czynsz (dodatkowo):')
        if to_find == -1:
            self.rent = 0
        else:
            # 19 is the length of "Czynsz (dodatkowo):" and 24 is to get some more data
            self.rent = self.html[to_find + 19: to_find + 26]
            x = 1
            while len(self.rent) != 0:
                self.rent = self.rent[:-x]
                try:
                    float(self.rent)
                    break
                except ValueError:
                    continue

    # Find the description of Announcement and remove <br>
    def finding_description(self):
        text_beginning = 'class="css-1t507yq er34gjf0">'
        to_find = self.html.find(text_beginning)

        closing_desc_hr = self.html.find("</div>", to_find)
        if closing_desc_hr != -1:
            description = self.html[to_find + len(text_beginning): closing_desc_hr]
            self.description = description.replace('<br />', '')
        else:
            self.description = "No description"


                        ### Functions ###




# Collect town names in Poland from the database and return them as an array
def get_city_names():
    data = pd.read_csv('pl.csv')
    towns = data['city'].to_numpy()
    return towns


# Search for a text sequence that best matches the user-provided value
def city_recognition(towns, data):
    best_score = 0
    closest_elem = ''
    data = data.lower()

    for elem in towns:
        current_score = 0
        elem = elem.lower()

        for i, (char_elem, char_data) in enumerate(zip(elem, data)):
            if char_elem == char_data:
                current_score += 1
            else:
                try:
                    if elem[i - 1] == data[i] or elem[i] == data[i - 1] or elem[i] == data[i + 1] or elem[i + 1] == \
                            data[i]:
                        current_score += 0.5
                except IndexError:
                    pass

        if current_score > best_score:
            best_score = current_score
            closest_elem = elem

    return closest_elem


# Get the page with the location provided by the user
def get_html(location, how_many_pages):
    html = []
    for i in range(how_many_pages):
        if i == 0:
            page = urlopen(f'https://www.olx.pl/nieruchomosci/{location}/')
            html_bytes = page.read()
            html.append(html_bytes.decode("utf-8"))
        else:
            page = urlopen(f'https://www.olx.pl/nieruchomosci/{location}/?page={i + 1}')
            html_bytes = page.read()
            html.append(html_bytes.decode("utf-8"))
    return html


# Get all links to announcements from OLX from the given page
def getting_all_links_from_olx(html_pages):
    olx_links = []
    for html in html_pages:
        matches = re.findall(r'href\s*=\s*["\'](.*?\.html)["\']', html)
        matches = matches[1:]  # Ignore the first match, as it is not relevant
        for link in matches:
            if link.startswith('/d'):
                olx_links.append(f'https://olx.pl{link}')
    return olx_links


# Remove Polish symbols
def without_polish_symbols(city):
    return unidecode(city)


def getting_links_from_database():
    data = pd.read_csv('nieruchomosci.csv')
    offers_in_database = data['Link'].to_numpy()
    return offers_in_database


#Removing all unactive links from database


# Define an asynchronous function to check the status of a link
async def check_link(session, link, index):
    try:
        # Use aiohttp to asynchronously get the response from the link
        async with session.get(link) as response:
            # Check if the response has an HTTP error status
            response.raise_for_status()
        # If no error occurred, the link is active, return None
        return None
    except aiohttp.ClientError as e:
        # If an error occurred, return the index of the inactive link
        return index

# Define an asynchronous function to check multiple links concurrently
async def deleting_data_async():
    # Read links from a CSV file using pandas
    links = pd.read_csv('nieruchomosci.csv')['Link']

    # List to store indices of inactive links
    unactive_link_indices = []

    # List to store asynchronous tasks
    tasks = []

    # Create an aiohttp ClientSession to manage HTTP connections
    async with aiohttp.ClientSession() as session:
        # Iterate through the links, create tasks for each link, and append them to the tasks list
        for i, link in enumerate(links, start=1):
            tasks.append(check_link(session, link, i))

        # Execute the tasks concurrently and gather the results
        unactive_link_indices = await asyncio.gather(*tasks)

    # Filter out None values (indicating active links) and keep only indices of inactive links
    unactive_link_indices = [index for index in unactive_link_indices if index is not None]

    # Return the array of indices for inactive links
    return unactive_link_indices


def delete_links_from_db(indices_to_remove):
    df = pd.read_csv('nieruchomosci.csv')

    # Convert 1-indexed indices to 0-indexed
    indices_to_remove_0indexed = [index - 1 for index in indices_to_remove]

    # Filter DataFrame and drop rows with inactive links
    filtered_df = df.drop(indices_to_remove_0indexed)

    # Save the filtered DataFrame back to the CSV file
    filtered_df.to_csv('nieruchomosci.csv', index=False)

