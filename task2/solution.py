import requests
from bs4 import BeautifulSoup
import csv
from collections import defaultdict
from urllib.parse import urljoin
import logging

CYRILLIC_LETTERS = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЭЮЯ'

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


def is_cyrillic_letter(letter):
    """Check if the letter is a Cyrillic character."""
    return letter.upper() in CYRILLIC_LETTERS


def get_animals_from_page(url):
    """
    Get a list of animals from a single category page.

    Args:
        url (str): URL of the Wikipedia category page

    Returns:
        tuple: (list of animal names, bool indicating if page contains any Cyrillic names)
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        content_div = soup.find('div', id='mw-pages')
        if not content_div:
            return [], False

        excluded_items = {
            'Следующая страница',
            'Предыдущая страница',
            'Случайная страница в категории',
            'PetScan',
            'Дерево категорий',
            'Список ниже может не отражать последних изменений.'
        }

        # Find main container with the list
        mw_category = content_div.find('div', class_='mw-category')
        if not mw_category:
            return [], False

        animals = []
        has_cyrillic = False

        for link in mw_category.find_all('a'):
            text = link.text.strip()
            if text and text not in excluded_items:
                if is_cyrillic_letter(text[0]):
                    animals.append(text)
                    has_cyrillic = True
                elif has_cyrillic:
                    # If we've already seen Cyrillic letters and now we're seeing non-Cyrillic,
                    # it means we've reached the end of the Cyrillic section
                    logger.info("Reached non-Cyrillic section, stopping further processing")
                    return animals, False

        return animals, True
    except Exception as e:
        logger.error(f"Error processing page {url}: {e}")
        return [], False


def get_next_page_url(soup, base_url):
    """
    Get URL of the next page.

    Args:
        soup (BeautifulSoup): Parsed HTML of current page
        base_url (str): Base URL for relative path resolution

    Returns:
        str or None: URL of next page if exists, None otherwise
    """
    next_link = soup.find('a', string='Следующая страница')
    if next_link:
        return urljoin(base_url, next_link['href'])
    return None


def count_animals_by_letter():
    """
    Main function for counting animals by their first letter.

    Returns:
        dict: Dictionary with counts of animals for each Cyrillic letter
    """
    base_url = 'https://ru.wikipedia.org/wiki/Категория:Животные_по_алфавиту'
    animals_by_letter = defaultdict(int)
    current_url = base_url
    page_count = 0
    total_animals = 0

    while current_url:
        page_count += 1
        logger.info(f"Processing page {page_count}: {current_url}")

        try:
            response = requests.get(current_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            # Get animals from current page
            animals, continue_processing = get_animals_from_page(current_url)

            if animals:
                total_animals += len(animals)
                # Count animals for each letter
                for animal in animals:
                    if animal and len(animal) > 0:
                        first_letter = animal[0].upper()
                        if is_cyrillic_letter(first_letter):
                            animals_by_letter[first_letter] += 1

            # If we've finished processing Cyrillic letters -> stop
            if not continue_processing:
                break

            # Get next page URL
            current_url = get_next_page_url(soup, base_url)


        except Exception as e:
            logger.error(f"An error occurred: {e}")
            break

    logger.info(f"Pages processed: {page_count}")
    logger.info(f"Total animals found: {total_animals}")
    return animals_by_letter


def save_to_csv(data, filename='beasts.csv'):
    """
    Save data to CSV file.

    Args:
        data (dict): Dictionary with letter counts
        filename (str): Output filename
    """
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            # Sort letters according to Cyrillic alphabet
            for letter in CYRILLIC_LETTERS:
                if letter in data:
                    writer.writerow([letter, data[letter]])
    except Exception as e:
        logger.error(f"During saving file \"{filename}\" an error occurred:\n{e}")
        raise
    else:
        logger.info(f"\"{filename}\" is successfully saved")


def main():
    logger.info("Starting data collection...")
    animals_count = count_animals_by_letter()
    save_to_csv(animals_count)
    logger.info("Data has been successfully collected")


if __name__ == "__main__":
    main()
