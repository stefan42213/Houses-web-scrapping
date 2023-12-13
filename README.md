In this advanced iteration, our application leverages the power of web scraping to meticulously extract data from a myriad of OLX announcements, carefully selecting and downloading only the freshest listings while adeptly culling inactive links. The primary objective of this sophisticated program transcends mere data extraction; it strives to establish a seamless user-server communication paradigm. The focal point is to facilitate users in their quest for the ideal abode by implementing dynamic filtering mechanisms that cater to individual preferences and requirements.

This intelligent system is not merely confined to gathering data; it aspires to redefine the house-hunting experience. The incorporation of cutting-edge artificial intelligence marks a pivotal phase in the evolution of our application. As the user interacts with the system, the AI component comes into play, analyzing and interpreting textual descriptions with finesse. The ultimate goal is to discern nuanced preferences and subtle requirements, enabling the system to recommend the optimal housing options that align perfectly with the user's needs.

Picture this: a user-friendly interface that not only presents a curated selection of homes but also engages in a dialogue with the user, refining and reshaping its recommendations based on real-time feedback. The AI-driven recommendation engine dives deep into the intricacies of each listing, drawing insights that go beyond mere keywords. It seeks to understand the essence of what makes a home the perfect fit for an individual.

Moreover, this innovative application is future-proof, constantly adapting and learning from user interactions to enhance its recommendation accuracy. As users engage with the system, providing feedback and refining their preferences, the AI algorithm evolves, becoming increasingly attuned to the subtleties of individual tastes and lifestyle choices.

In essence, what began as a simple web scraping tool has blossomed into a comprehensive, user-centric housing solution that seamlessly integrates advanced technologies. Our application not only transforms the house-hunting journey but also sets a new standard for personalized and intelligent digital experiences. Welcome to the future of home discovery, where every recommendation is a step closer to finding the perfect home.

Overview

This Python project is a web scraper designed to extract real estate data from OLX announcements. It focuses on obtaining information such as price, size, number of rooms, rent, description, and link for each property. The collected data is stored in a CSV file for further analysis.
Features

Web scraping of OLX announcements for real estate information.
User interaction for adding or deleting data.
Automatic recognition of town names to refine the search.
Asynchronous checking of link statuses for data cleanup.

Decencies

     pip install urllib pandas unidecode re aiohttp asyncio
Choose an operation:
        Enter 1 to add new real estate data.
        Enter 2 to delete inactive data.

Provide input:
        When adding data, enter the city and the number of pages to scrape.
        When deleting data, the script will automatically identify and remove inactive links.

Review input:
        The processed data is appended to the 'nieruchomosci.csv' file.
        Deletion results are printed, showing the number of offers successfully removed.

Class Annoucment:

This class represents a single OLX announcement and provides methods to extract various details such as price, size, rooms, rent, and description.
Functions

    process_links(x, links_we_have, city):
  Processes the links obtained from OLX, extracts real estate details, and returns a map of the processed data.

    city_recognition(towns, data):
  Recognizes the user-provided city name, matching it to a town name from the database.

    get_html(location, how_many_pages):
  Retrieves HTML pages containing real estate announcements based on the user-provided location and number of pages.

    getting_all_links_from_olx(html_pages):
  Extracts all links to real estate announcements from OLX pages.

    without_polish_symbols(city):
  Removes Polish symbols from a given city name.

    getting_links_from_database():
  Retrieves links from the 'nieruchomosci.csv' database.

    check_link(session, link, index):
  Asynchronous function to check the status of a link.

    deleting_data_async():
  Asynchronously checks the status of multiple links and returns indices of inactive links.

     delete_links_from_db(indices_to_remove):
  Deletes inactive links from the 'nieruchomosci.csv' database.
