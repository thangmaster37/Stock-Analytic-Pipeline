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
        options = Options()
        options.headless = True
        options.page_load_strategy = 'eager'
        driver = webdriver.Firefox(options=options)
        
        # access the url
        driver.get(url)   
