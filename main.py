"""Imports information into the database using the created 'User' class(form), receives, modifies and deletes the imported information."""


from form import User
from scraper import Scraper


def main():
    """Test"""

    scraper = Scraper(
        'https://www.investopedia.com/articles/investing/012715/5-richest-people-world.asp')
    storage = scraper.DATA

    first_name = storage['first_names_list']
    last_name = storage['last_names_list']
    age = storage['ages_list']

    for idx, person in enumerate(first_name):
        User.Storage.insert(
            first_name=first_name[idx], last_name=last_name[idx], age=age[idx])

    print(User.Storage.get_by_field(first_name='Elon'))
    User.Storage.update('first_name = "Elon"', 'age = "30"')
    print(User.Storage.get_by_field(first_name='Elon'))
    User.Storage.insert(first_name='Mane', last_name='Vardazaryan', age='23')
    print(User.Storage.get_by_field(first_name='Mane'))
    User.Storage.delete(first_name='Mane')
    print(User.Storage.get_by_field(first_name='Mane'))


if __name__ == '__main__':
    main()
