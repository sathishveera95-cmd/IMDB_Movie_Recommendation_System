import re
import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException


URL = "https://www.imdb.com/search/title/?title_type=feature&release_date=2024-01-01,2024-12-31"


def start_driver():

    options = webdriver.ChromeOptions()

    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    driver.get(URL)

    WebDriverWait(driver,20).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR,"li.ipc-metadata-list-summary-item")
        )
    )

    return driver


def scrape_movies(driver,start_index,movie_data):

    movies = driver.find_elements(
        By.CSS_SELECTOR,
        "li.ipc-metadata-list-summary-item"
    )

    new_movies = movies[start_index:]

    print(f"Processing {len(new_movies)} new movies")

    for movie in new_movies:

        try:
            title = movie.find_element(
                By.CSS_SELECTOR,
                "h4.ipc-title__text"
            ).text

            title = re.sub(r"^\d+\.\s*","",title)

        except:
            title = ""

        try:
            storyline = movie.find_element(
                By.CSS_SELECTOR,
                "div.ipc-html-content-inner-div"
            ).text

        except:
            storyline = ""

        movie_data.append({
            "Movie Name":title,
            "Storyline":storyline
        })

    return len(movies)


def click_load_more(driver):

    old_count = len(
        driver.find_elements(
            By.CSS_SELECTOR,
            "li.ipc-metadata-list-summary-item"
        )
    )

    driver.execute_script(
        "window.scrollTo(0,document.body.scrollHeight);"
    )

    try:

        button = WebDriverWait(driver,20).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//span[contains(text(),'50 more')]"
                )
            )
        )

        driver.execute_script(
            "arguments[0].click();",
            button
        )

    except:

        try:

            button = driver.find_element(
                By.XPATH,
                "//span[contains(text(),'50 more')]"
            )

            driver.execute_script(
                "arguments[0].click();",
                button
            )

        except:
            return False

    try:

        WebDriverWait(driver,30).until(
            lambda d:
            len(
                d.find_elements(
                    By.CSS_SELECTOR,
                    "li.ipc-metadata-list-summary-item"
                )
            ) > old_count
        )

        new_count = len(
            driver.find_elements(
                By.CSS_SELECTOR,
                "li.ipc-metadata-list-summary-item"
            )
        )

        print(f"Loaded : {old_count} -> {new_count}")

        return True

    except TimeoutException:

        print("Movie count did not increase.")

        return False


def save_csv(movie_data):

    df = pd.DataFrame(movie_data)

    df.to_csv(
        "dataset/imdb_movies_2024.csv",
        index=False,
        encoding="utf-8"
    )

    print("\n=====================================")
    print(f"Movies Scraped : {len(df)}")
    print("CSV Saved Successfully")
    print("=====================================")


def main():

    driver = start_driver()

    movie_data = []

    processed = 0

    while True:

        processed = scrape_movies(
            driver,
            processed,
            movie_data
        )

        print(f"Collected : {len(movie_data)}")

        success = click_load_more(driver)

        if not success:
            break

    save_csv(movie_data)

    driver.quit()


if __name__ == "__main__":
    main()