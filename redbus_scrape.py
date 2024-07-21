import time
import mysql.connector
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from datetime import datetime
from selenium.common.exceptions import NoSuchElementException


# Connect to the MySQL database
def get_database_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345678",
        database="Redbus"
    )


# Create the table if it doesn't already exist
def create_table(cursor):
    query = """
    CREATE TABLE IF NOT EXISTS bus_routes (
        id INT PRIMARY KEY AUTO_INCREMENT,
        route_name TEXT,
        route_link TEXT,
        busname TEXT,
        bustype TEXT,
        departing_time TEXT,
        duration TEXT,
        reaching_time TEXT,
        star_rating FLOAT,
        price DECIMAL,
        seats_available TEXT
    )
    """
    cursor.execute(query)


#Initializes the WebDriver
def get_driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    return driver


#Scrapes the current page for bus routes and links
def scrape_current_page(driver, bus_list, max_scroll_attempts=3):
    scrolling = True
    scroll_attempts = 0

    while scrolling and scroll_attempts < max_scroll_attempts:
        old_page_source = driver.page_source

        body = driver.find_element(By.TAG_NAME, "body")
        body.send_keys(Keys.PAGE_DOWN)

        time.sleep(2)

        new_page_source = driver.page_source

        if new_page_source == old_page_source:
            scrolling = False

        scroll_attempts += 1

    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located(
            (By.XPATH, "//div[@class='D117_main D117_container']/div[@class='route_link']")
        )
    )

    for bus in driver.find_elements(
            By.XPATH, "//div[@class='D117_main D117_container']/div[@class='route_link']"):
        route_name = bus.find_element(By.CSS_SELECTOR, "a.route").text
        route_link = bus.find_element(By.CSS_SELECTOR, "a.route").get_attribute('href')

        bus_list.append({
            'route': route_name,
            'link': route_link
        })


#Clicks the next page button to navigate to the next page
def click_next_page(driver, current_page):
   
    try:
        next_page = driver.find_element(
            By.XPATH, f"//div[@class='DC_117_pageTabs ' and text()='{current_page + 1}']")
        driver.execute_script("arguments[0].scrollIntoView(true);", next_page)  # Scroll to the element
        time.sleep(1)  # Wait for the scroll to complete
        driver.execute_script("arguments[0].click();", next_page)  # Click using JavaScript
        time.sleep(2)
    except Exception as e:
        print(f"Error clicking next page: {e}")


#Scrapes the bus details for each route in the bus list
def scrape_bus_details(driver, cursor, bus_list):
    
    for bus in bus_list:
        try:
            driver.get(bus['link'])

            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//div[@class='clearfix bus-item']"))
            )

            for bus_detail in driver.find_elements(
                    By.XPATH, "//div[@class='clearfix bus-item']/div[@class='clearfix bus-item-details']/div[@class='clearfix row-one']"):
                try:
                    busname = bus_detail.find_element(
                        By.XPATH, ".//div[@class='travels lh-24 f-bold d-color']").text
                    bustype = bus_detail.find_element(
                        By.XPATH, ".//div[@class='bus-type f-12 m-top-16 l-color evBus']").text
                    departing_time = bus_detail.find_element(
                        By.XPATH, ".//div[@class='dp-time f-19 d-color f-bold']").text
                    duration = bus_detail.find_element(
                        By.XPATH, ".//div[@class='dur l-color lh-24']").text
                    reaching_time = bus_detail.find_element(
                        By.XPATH, ".//div[@class='bp-time f-19 d-color disp-Inline']").text

                    star_rating_str = bus_detail.find_element(
                        By.XPATH, ".//div[@class='rating-sec lh-24']").text
                    star_rating = float(star_rating_str.split()[0]) if star_rating_str else 0.0

                    price_str = bus_detail.find_element(By.XPATH, ".//div[@class='fare d-block']").text
                    price = int(price_str.replace('INR', '').replace(',', '').strip()) if price_str else 0

                    try:
                        seat_availability_str = bus_detail.find_element(
                            By.XPATH, ".//div[@class='seat-left m-top-30']").text
                        seats_available = int(seat_availability_str.split()[0]) if seat_availability_str else 0
                    except NoSuchElementException:
                        seats_available = 0

                    cursor.execute("""
                    INSERT INTO bus_routes (
                        route_name, route_link, busname, bustype, departing_time, duration, reaching_time, star_rating, price, seats_available
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                                   (bus['route'], bus['link'], busname, bustype, departing_time,
                                    duration, reaching_time, star_rating, price, seats_available))

                except NoSuchElementException as e:
                    print(f"Error scraping bus details: {e}")
                except ValueError as ve:
                    print(f"Error converting data: {ve}")

        except Exception as e:
            print(f"Error scraping bus details: {e}")


#Main function to execute the scraping and database insertion process
def main():
    
    con = get_database_connection()
    cursor = con.cursor()
    create_table(cursor)

    driver = get_driver()

    urls = [
        'https://www.redbus.in/online-booking/apsrtc/?utm_source=rtchometile',
        'https://www.redbus.in/online-booking/ksrtc-kerala/?utm_source=rtchometile',
        'https://www.redbus.in/online-booking/tsrtc/?utm_source=rtchometile',
        'https://www.redbus.in/online-booking/ktcl/?utm_source=rtchometile',
        'https://www.redbus.in/online-booking/rsrtc/?utm_source=rtchometile',
        'https://www.redbus.in/online-booking/south-bengal-state-transport-corporation-sbstc/?utm_source=rtchometile',
        'https://www.redbus.in/online-booking/hrtc/?utm_source=rtchometile',
        'https://www.redbus.in/online-booking/astc/?utm_source=rtchometile',
        'https://www.redbus.in/online-booking/uttar-pradesh-state-road-transport-corporation-upsrtc/?utm_source=rtchometile',
        'https://www.redbus.in/online-booking/wbtc-ctc/?utm_source=rtchometile',
    ]

    for url in urls:
        driver.get(url)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='D117_main D117_container']"))
        )

        bus_list = []
        current_page = 1
        total_pages = len(driver.find_elements(By.XPATH, "//div[@class='DC_117_pageTabs ']")) + 1

        while current_page <= total_pages:
            scrape_current_page(driver, bus_list)
            if current_page < total_pages:
                click_next_page(driver, current_page)
            current_page += 1

        scrape_bus_details(driver, cursor, bus_list)
        con.commit()

    cursor.close()
    con.close()

    driver.quit()
    print("Data scraped and inserted into MySQL successfully.")


if __name__ == "__main__":
    main()
