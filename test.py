from selenium import webdriver
driver = webdriver.Chrome("/Users/roberta/Documents/1.Università/RetiGeografiche/Task/3/chromedriver")
driver.get("https://www.nytimes.com")
headlines = driver.find_elements_by_class_name("story-heading")
for headline in headlines:
    print(headline.text.strip())
