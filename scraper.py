"""File is intended for reading information from the 'https://www.investopedia.com' site."""


import aiohttp
import asyncio
from bs4 import BeautifulSoup


class Scraper:
    """Scraps information from site."""

    DATA = {'first_names_list': None,
            'last_names_list': None, 'ages_list': None}

    def __init__(self, url):
        self.url = url
        self.event_loop = asyncio.new_event_loop()
        self.tasks = [self.event_loop.create_task(self.async_parse())]
        self.event_loop.run_until_complete(asyncio.wait(self.tasks))

    async def async_parse(self):
        """Sends a request to the site."""

        async with aiohttp.ClientSession() as session:
            async with session.get(self.url) as req:
                data = await req.text()
                self.async_parse_data(data)

    def async_parse_data(self, data):
        """Reads information from html"""

        soup = BeautifulSoup(data, 'lxml')
        persons = soup.find_all(
            'h2', {'class': 'comp mntl-sc-block finance-sc-block-heading mntl-sc-block-heading'})
        persons = persons[:-1]
        persons_first_name = []
        persons_last_name = []
        for person in persons:
            name = person.find('span').text.split(".")[1].strip().split()
            persons_first_name.append(name[0])
            persons_last_name.append(name[1])

        persons_age = soup.find_all(
            'ul', {'class': 'comp mntl-sc-block finance-sc-block-html mntl-sc-block-html'})
        persons_age = [person_age.find_all('li')[0].text.split(" ")[
            1] for person_age in persons_age]

        Scraper.DATA = {'first_names_list': persons_first_name,
                        'last_names_list': persons_last_name, 'ages_list': persons_age}
