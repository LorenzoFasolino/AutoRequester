from selenium import webdriver

driver = webdriver.Chrome("./chromedriver")

with open("Top 50 Alexa sites/top-1m.csv") as reader:

    line = reader.readline()
    while line != '':
        driver.get("http://"+line)
        headlines = driver.find_elements_by_class_name("story-heading")
        for headline in headlines:
            print(headline.text.strip())
        line = reader.readline()



