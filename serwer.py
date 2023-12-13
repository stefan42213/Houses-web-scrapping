from geting_data import *
from functools import lru_cache

# Function to process links and create a map
@lru_cache(maxsize=None)
def process_links(x, links_we_have, city):
    prices = []
    rents = []
    sizes = []
    types = []  # Avoid using type as a variable name, as it's a reserved keyword
    rooms = []
    descriptions = []
    links = []
    cities = []
    how_many_links_added = 1
    for i in range(len(x)):
        if x[i] in links_we_have:
            continue
        else:
            ogloszenie = Announcement(x[i])
            ogloszenie.get_page_html()
            ogloszenie.finding_price()
            ogloszenie.finding_size()
            ogloszenie.finding_rooms_number()
            ogloszenie.finding_the_rent()
            ogloszenie.finding_description()

            # Check if the price is a non-empty string before converting to float
            if ogloszenie.price and ogloszenie.price.strip():
                price = float(ogloszenie.price)
            else:
                price = 0.0  # Set a default value or handle it as needed

            prices.append(price)
            sizes.append(ogloszenie.size)
            rooms.append(ogloszenie.rooms)
            rents.append(ogloszenie.rent)
            types.append('Buy' if price > 50000 else 'Rent')
            descriptions.append(ogloszenie.description)
            links.append(x[i])  # Add the current link
            cities.append(city)
            print(f'{how_many_links_added}. link data collected')
            how_many_links_added+=1

    # Create a map of processed data
    data_map = {
        'Price': prices,
        'Rent': rents,
        'Size': sizes,
        'Rooms': rooms,
        'Type': types,
        'Town': cities,
        'Description': descriptions,
        'Link': links
    }

    return data_map


if __name__ == '__main__':

    i = input("1-Add , 2-Delete \n")

    if (i=='1'):
    # Get user input
        input_by_user = input("Podaj miasto dla którego mam sprawdzić ogłoszenia: ")
        how_many_sites = input("Podaj ile stron ogłoszeń mam przeszukać: ")

    # Process city name and get links
        city = city_recognition(get_city_names(), input_by_user)
        links = getting_all_links_from_olx(get_html(without_polish_symbols(city), int(how_many_sites)))

    # Process links and add to the database
        links_we_have = getting_links_from_database()
        add_to_database = process_links(tuple(links), tuple(links_we_have), city)

    # Create a DataFrame and append to CSV
        df = pd.DataFrame(add_to_database)
        df.to_csv('nieruchomosci.csv', mode='a', index=False, header=False)

    # Print a success message
        print(f"Data appended successfully. We added {len(add_to_database['Link'])} offers")

    elif(i=='2'):
        inactive_indices = asyncio.run(deleting_data_async())
        delete_links_from_db(inactive_indices)
        print(f"Deleted successfully {len(inactive_indices)} offers")