# Redbus Data Scraping with Selenium & Dynamic Filtering using Streamlit

## Project Overview

This project aims to scrape bus route data from the Redbus website, store it in a SQL database, and create a Streamlit application for dynamic data filtering and analysis.

### Project Components

- **Web Scraping with Selenium**: A Python script to scrape bus data from Redbus.
- **Database Interaction**: Store the scraped data in a SQL database.
- **Streamlit Application**: A web application for dynamic data filtering and visualization.

## Project Structure
redbus-data-scraping/
│
├── redbus_scrape.py # Script for scraping data from Redbus
├── streamlit.py # Streamlit application script for data filtering and visualization
└── schema.sql # SQL script to create and populate the database


## Features

- **Bus Routes Name**: The start and end locations of each bus journey.
- **Bus Routes Link**: A link to the route details.
- **Bus Name**: The name of the bus or service provider.
- **Bus Type (Sleeper/Seater/AC/Non-AC)**: The type of bus, indicating seating arrangements and comfort level.
- **Departing Time**: The scheduled departure time of the bus.
- **Duration**: The total duration of the journey.
- **Reaching Time**: The expected arrival time at the destination.
- **Star Rating**: A rating provided by passengers.
- **Price**: The cost of the ticket.
- **Seat Availability**: The number of seats available at the time of data scraping.

## Setup Instructions

### Prerequisites

- Python 3.x
- Selenium
- Streamlit
- SQL Database (MySQL)

### Installing Dependencies

Install the required Python packages using `pip`:

```bash
pip install -r requirements.txt

##Usage

## Data Scraping:
-->The redbus_scrape.py script scrapes data from the Redbus website and stores it in the SQL database.

## Data Filtering and Visualization:
-->The streamlit.py script runs a Streamlit application that allows users to filter and visualize the scraped data.
