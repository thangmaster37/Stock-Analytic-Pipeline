from time import sleep
from selenium import webdriver
# from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service

from webdriver_manager.chrome import ChromeDriverManager
from tqdm import tqdm
import pandas as pd
import logging, logging.handlers
import datetime
import connection_utils
    

# declare logging
logging.basicConfig(level=logging.DEBUG, filename="crawl_data_stock/logs/log-crawl-data.log", format='%(asctime)s %(levelname)s:%(message)s')
logging.disable(logging.DEBUG)

logger = logging.getLogger(__name__)

# declare variable STMP Handler, initialized with the from and to addresses and subject line of the email.
smtp_handler = logging.handlers.SMTPHandler(mailhost=('smtp.gmail.com', 587),
                                            fromaddr='hungnguyenjr9@gmail.com',
                                            toaddrs=['hungnq.cdc@gmail.com',
                                                     'hung.nq183760@sis.hust.edu.vn'],
                                            subject='Error in Crawl-Data-Tool',
                                            credentials=(
                                                'hungnguyenjr9@gmail.com',
                                                'wlpgtalknxstpftp'),
                                            secure=())
logger.addHandler(smtp_handler)


def crawl_sections_data(driver, section):
    """
    This function takes as 2 input parameters the Web Driver and the name of the stock item section, and crawls the data of stock codes and prices. 

    Parameters:
    driver : the instance of WebDriver 
    section (String): A input string describes the name of the stock section like ABC, DEF, GHI, ...

    Returns:
    this function doesn't return anything
    
    """

    # Call selenium function to click on button by xpath
    xpath = '//div[@id="' + section +'"]/p'
    driver.find_element(By.XPATH, xpath).click()
    sleep(3)


    try:
        # Call selenium function to fill all rows in stock table
        # Each element corresponds to a line describing a stock
        # wait 10 seconds before looking for element
        items = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//div/table/tbody/tr'))
        )

    except:
        # else return function
        print(f"Error! Cannot find any stock in {section} section.\n")
        logger.error("Error! Cannot find any stock in {section} section.")
        return
    

    # Notice to user
    print(f"Crawl {len(items)} items in {section} section")

    result = []
    for item in tqdm(items):
        try:
            # Get the stock code
            stockCode = item.find_element(By.XPATH, './/td/div/div/span').text

            # If can't get the code for some reason, skip this iteration
            if not stockCode:
                continue

            # Get the stock prices
            referencePrice = item.find_element(By.XPATH, './/td[4]/div').text.replace(",","")
            if not referencePrice:
                referencePrice = 0

            cellingPrice = item.find_element(By.XPATH, './/td[5]/div').text.replace(",","")
            if not cellingPrice:
                cellingPrice = 0

            floorPrice = item.find_element(By.XPATH, './/td[6]/div').text.replace(",","")
            if not floorPrice:
                floorPrice = 0

            price = item.find_element(By.XPATH, './/td[14]/div').text.replace(",","")
            if not price:
                price = 0

            volume = item.find_element(By.XPATH, './/td[15]/div').text.replace(",","")
            if not volume:
                volume = 0

            totalVolume = item.find_element(By.XPATH, './/td[16]/div').text.replace(",","")
            if not totalVolume:
                totalVolume = 0

            totalValue = item.find_element(By.XPATH, './/td[17]/div').text.replace(",","")
            if not totalValue:
                totalValue = 0

            highestPrice = item.find_element(By.XPATH, './/td[26]/div').text.replace(",","")
            if not highestPrice:
                highestPrice = 0

            lowerPrice = item.find_element(By.XPATH, './/td[27]/div').text.replace(",","")
            if not lowerPrice:
                lowerPrice = 0

            averagePrice = item.find_element(By.XPATH, './/td[28]/div').text.replace(",","")
            if not averagePrice:
                averagePrice = 0

            referencePrice = float(referencePrice)
            cellingPrice = float(cellingPrice)
            floorPrice = float(floorPrice)
            price = float(price)
            volume = float(volume)
            totalVolume = float(totalVolume)
            totalValue = float(totalValue)
            highestPrice = float(highestPrice)
            lowerPrice = float(lowerPrice)
            averagePrice = float(averagePrice)

            # Create element that contains stock information: code, prices
            stock_item = {
                'stock-code': stockCode,
                'reference-price': referencePrice,
                'celling-price': cellingPrice,
                'floor-price': floorPrice,
                'price': price,
                'volume': volume,
                'total-volume': totalVolume,
                'total-value': totalValue,
                'highest-price': highestPrice,
                'lowest-price': lowerPrice,
                'average-price': averagePrice,
            }

            # push that element to the last of the stock item list
            result.append(stock_item)
        
        except Exception as e:
            # There has some wrong with crawling data
            print(f"Error! Failed when crawling a stock in {section} section.\n")

            # log this error
            logger.error(f"Failed when crawling crawl a stock in {section} section. Error: {e}")

            return

        # end loop

    # End function
    print("Done!\n")
    return result

    # crawl
def crawl(url):
    """
    This function crawls stock data from the `url` link

    Parameters:
    url : the website link that needs to crawl

    Returns:
    this function doesn't return anything
    
    """

    # Access to url
    try:
        print(f"Access the url {url} ...\n")

        # initialize the Firefox driver
        # options = Options()
        # options.headless = True
        # options.page_load_strategy = 'eager'
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

        # access the url
        driver.get(url)   

        # set implicit wait is 5s
        driver.implicitly_wait(5)

    except Exception as e:
        # There has some wrong with url connection problem
        print("Can\'t access the url. Please check your operation and try again.")

        # log that cannot access the url
        logger.error(f"Failed to access the url {url}. \nError: {e}")

        # shutdown app
        exit(0)
        
    print('\n______________________ CRAWL DATA ______________________')

    sections = ['ABC', 'DEF', 'GHI', 'JKL', 'MNO', 'PQR', 'STUV', 'WXYZ']

    # contains stock data
    data = []

    # crawl listed stock from sections
    print("Crawl listed stocks")
    driver.find_element(By.XPATH, "//div[2]/div[2]/div/div/div").click()
    for section in sections:
        res = crawl_sections_data(driver, section)
        data.extend(res)
    
    print("=====================")

    # crawl upcom stock
    print("Crawl upcom stocks")
    driver.find_element(By.XPATH, "//div[2]/div[3]/div/div/div").click()
    for section in sections:
        res = crawl_sections_data(driver, section)
        data.extend(res)


    # Finishing crawl data. Print the total number of stocks
    print(f"Completed. We have crawled {len(data)} stocks")
    print("======================================")

    # close web browser
    driver.close()

    # End function
    return data

def export_file(data):

    """
    The function takes 1 input parameter of stock data in an array, from which to export the data to csv format.

    Parameters:
    data (list): A list data of stock codes and prices.

    Returns:
    this function doesn't return anything
    
    """

    print("\n______________________ SAVE DATA TO FILE ______________________")

    # export data to file as csv format
    try:
        df = pd.DataFrame(data)
        df.to_csv('data/stock.csv', index = None, header=True)

        print("Exported data to file csv")

    except Exception as e:
        print("Cannot export data to csv file.\n")
        logger.error(f"Failed to export data to csv file. Error: {e}")

    # End function
    return

if __name__ == '__main__':
    # website link needs to crawl
    url = "https://banggia.hnx.vn"  

    # Create stock-list to contain the stock-object
    # Each item contains infomation of 1 stock such as code, prices
    stock_list = []

    # Start
    print("Starting application ... \n")
    stock_list = crawl(url)
    export_file(stock_list)
    # save_database(stock_list)
