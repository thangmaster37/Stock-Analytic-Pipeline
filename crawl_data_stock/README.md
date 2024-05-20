# Python-crawl-data-tool

## Table of Contents
- [Description](#description)
- [Main features](#main-features)
- [Implementation Guide](#implemention-guide)
- [User Guide](#user-guide)
- [Release](#release)
- [Author](#author)


## Description

This tool uses Python Selenium to crawl data of stock and price from website https://banggia.hnx.vn/. Each stock includes data as code, prices, total volume, total value. After that, all data is exported into 1 file formats csv. And all data is saved to database.

### I. Python Selenium

Selenium is a free (open source) test automation suite for web applications across different browsers and platforms, with a focus on automating web-based applications. Selenium toolkit has 4 components: Selenium Integrated Development Environment (IDE), Selenium Remote Control (RC), WebDriver, Selenium Grid in which WebDriver is the most appreciated. In particular, Selenium WebDriver is compatible with almost all popular web browsers and supports most of today's popular programming languages. In file selenium-crawl-hnx.py, I use Selenium WebDriver tool on Python programming language.

Selenium WebDriver creates a driver to control the brower. This driver is responsible for sending launch commands and then interacting directly with browsers. To interact with elements in the browser, it is necessary to find the element through Xpath.

To determine the Xpath of elements on the web page, I use an extension called [https://chrome.google.com/webstore/detail/selenium-ide/mooikfkahbdckldjjndioackbalphokd](Selenium IDE). This extension records all web page manipulation actions and records the address of the object just executed. For example, if you click on a data box on a web page, the extension will record the onclick event and the corresponding address of that button.

Then, when you have the Xpath, call the find_element function to let the driver identify the element and then execute the job of getting data or other events such as clicking on the object.

Example:
```python
    driver.find_element(By.XPATH, "//div[2]/div[3]/div/div/div")
```


### II. Functions in file crawl-stock-hnx.py

On the website [https:\\banggia.hnx.vn](https:\\banggia.hnx.vn), stock codes are divided into 2 types, listed stocks and unlisted stocks (upcom stock). Each stock page is further divided into smaller sections by ticker name, which are 'ABC', 'DEF', 'GHI', 'JKL', 'MNO', 'PQR', 'STUV', ' WXYZ'.


**1. Function crawl(url):**

This function creates a driver that controls access to url = [https:\\banggia.hnx.vn](https:\\banggia.hnx.vn). Then crawl the data on the listed and unlisted stock items. For each of the above, call the crawl_sections_data function to get data from the smaller sections of the web page.

The input parameter is the url of the website to be crawled.

This function returns a list of stock data

**2. Function crawl_sections_data(driver, section)** 

Parameters:

driver : the instance of WebDriver 

section (String): A input string describes the name of the stock section like ABC, DEF, GHI, ...

This function get all rows of data in the table. Each row contains information of a stock.
Each stock with such fields will be stored in a dictionary as follows:

* `stock-code`: the code name of stock
* `reference-price`: reference price
* `celling-price`: price ceiling
* `floor-price`: floor price
* `price`: selling price
* `volume`: volume
* `total-volume`: total volume
* `total-value`: total value
* `highest-price`: highest selling price
* `lowest-price`: lowest selling price
* `average-price`: average selling price

This function returns a list of stock data that crawl on the group

**3. Function export_data(data):**

This function saves data to file format csv

Parameters:

data: a list structure containing data of stock codes.


**4. Function save_database(data):**

This function creates connection to mysql database server by using the function `getConnection()` in the file `connection_utils.py`. For each stock code, search the database to find that stock (select_query). If it doesn't exist, do a new insert (insert_query). If it already exists, execute the update (update_query).

Parameters:

data: a list structure containing data of stock codes.


**5. Function getConnection() in file connection_utils.py :**

This function creates a new connection to the mysql database with the information fields as host address, username, password, database name.

Returns a connection.


### III. Web API

I use nodejs to build Web API server. Then push the server to a free site called heroku.com.
The server provides an api at: `http://vnindex.herokuapp.com/getStockInfo?code={code}` with the code being the stock code entered by the user

Example:
```php
    http://vnindex.herokuapp.com/getStockInfo?code=BCC
```



## Main features

- Crawl listed stock and upcom stock data 
- Export to csv file
- Export documentation as html format
- Save all data to mysql database
- Log to file and send warning email when an error occurs
- Provide API to get the detail information of the stock

## Implementation Guide

1. Enviroment require: python. 
- In windows, you can download an install python in [`https://www.python.org/downloads/`](https://www.python.org/downloads/)


2. Libraries require: selenium, pandas, PyMySQL
- Install python libraries: turn on your terminal and type `pip install -r requirements.txt`


## User Guide

1. Excecute

- Clone repository
- Turn on your terminal and `cd` into this folder `Python-crawl-data-tool.`
- Run command on your terminal: `python selenium-crawl-hnx.py`
- Data exported to file: `stock-hnx-csv.csv` (csv format)
- Data is saved to `vnindex` mysql database

2. If you want to read the documentation: 
- In your terminal, direct to this folder, type: `python -m pydoc -w .\selenium-crawl-hnx.py`
- documentation is exported to file `selenium-crawl-hnx.html`. You can watch it on browser.

3. If you want to get the stock information, use the API: `http://vnindex.herokuapp.com/getStockInfo?code= + stock_code`



## Release: 

- Version 0.4 updated on Nov 14, 2021
- Version 0.5 updated on Nov 21, 2021
- Version 0.6 updated on Dec 5, 2021
- Version 0.7 updated on Jan 7, 2022
- Version 0.9 updated on Jan 20, 2022
- Version 1.0 released on Jan 22, 2022


# Author
- Nguyễn Quang Hưng
- Facebook: https://www.facebook.com/hungnq.SoICT
- Email: nguyenquanghung.ktmt@gmail.com
- LinkedIn: https://www.linkedin.com/in/hungnq-soict