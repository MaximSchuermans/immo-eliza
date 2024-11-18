<h1 align="center">ImmoEliza: Data Scraper</h1> <br>
<p align="center">
  <a href="https://becode.org/" target="_blank">BeCode</a> learning project.
</p>
<p align="center">AI & Data Science Bootcamp</p>

<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li> <a href="#installation">Installation</a></li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contributors">Contributors</a></li>
    <li><a href="#timeline">Timeline</a></li>
  </ol>
</details>

## **About The Project**
This project is the first step towards creating a machine learning model to predict real estate prices in Belgium.

The initial task is to gather the data that will be used to train and test the machine learning model. We collect information from [Immoweb](immoweb.be) on over 10,000 properties to create a dataset about the Belgian real estate market.

The dataset is stored as a `csv` with the following columns:
* Locality
* Type of property (House/apartment)
* Subtype of property (Bungalow, Chalet, Mansion, ...)
* Price
* Number of rooms
* Living Area
* Fully equipped kitchen (Yes/No)
* Furnished (Yes/No)
* Open fire (Yes/No)
* Terrace (Yes/No)
* If yes: Area
* Garden (Yes/No)
* If yes: Area
* Surface of the land
* Surface area of the plot of land
* Number of facades
* Swimming pool (Yes/No)
* State of the building (New, to be renovated, ...)

### Additional Notes
* The Type of Sale tag consistently returned only false values, so this column was not included in the dataset.
* We added two additional columns, Disabled Access and Lift, as they are of particular interest for further analysis.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With
List of frameworks/libraries used in this project.

* [![selenium](https://img.shields.io/badge/Selenium-Automation-yellow)](https://selenium.dev/) 
* [![selenium.webdriver.support.ui.WebDriverWait](https://img.shields.io/badge/WebDriverWait-Module-yellow)](https://selenium.dev/) 
* [![selenium.webdriver.support.expected_conditions](https://img.shields.io/badge/expected_conditions-Module-yellow)](https://selenium.dev/)
* [![selenium.webdriver.common.by.By](https://img.shields.io/badge/By-Module-yellow)](https://selenium.dev/) 
* [![requests](https://img.shields.io/badge/Requests-HTTP-blue)](https://docs.python-requests.org/) 
* [![requests.Session](https://img.shields.io/badge/requests.Session-HTTP%20Session-blue)](https://docs.python-requests.org/) 
* [![threading](https://img.shields.io/badge/threading-Module-green)](https://docs.python.org/3/library/threading.html) 
* [![concurrent.futures](https://img.shields.io/badge/concurrent.futures-Module-green)](https://docs.python.org/3/library/concurrent.futures.html) 
* [![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup-HTML%20Parsing-brightgreen)](https://www.crummy.com/software/BeautifulSoup/) 
* [![json](https://img.shields.io/badge/JSON-Data-orange)](https://docs.python.org/3/library/json.html) 
* [![pandas](https://img.shields.io/badge/pandas-Dataframe-blue)](https://pandas.pydata.org/) 
* [![time](https://img.shields.io/badge/time-Time%20Functions-red)](https://docs.python.org/3/library/time.html) 
* [![tqdm](https://img.shields.io/badge/tqdm-Progress%20Bar-blue)](https://tqdm.github.io/) 

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## **Installation**
1. Clone the immo-eliza repository
2. Install the required libraries by running pip install -r requirements.txt

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## **Usage**
1. To get the urls from the immoweb execute `python3 url_scraper.py`
2. To get the data from the urls `python3 data_scraper.py`
3. To clean the obtained data run `python3 cleaning.py`

## **Contributors**
The project's contributors (in alphabetical order):
* Manel Boubakeur - https://github.com/ManelBouba
* Maxim Schuermans - https://github.com/MaximSchuermans
* Jessica Rojas - https://github.com/jessrojasal

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## **How We Work**
* Parallel Work: During the first two days of the project, we worked individually—while helping each other—to find our own solutions for scraping the URLs. Then, we selected the best parts of each person’s code to create our unified URL and data scraper.
* Testing: We tested both scrapers and identified areas for improvement.
* Implementing Improvements: We addressed each improvement in separate branches. When someone resolved an issue, we merged the solution into the main branch.


## **Timeline**
12 Nov 2024 - project initiated 
15 Nov 2024 - project concluded

<p align="right">(<a href="#readme-top">back to top</a>)</p>
