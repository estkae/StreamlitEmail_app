import csv
import parameters
from time import sleep
from parsel import Selector
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import pandas as pd


def scrape(search_query, password, username):
    all_results = []
    writer = csv.writer(open(parameters.result_file, 'w'))
    writer.writerow(['name', 'phone', 'job_title', 'schools', 'location', 'ln_url'])
    options = Options ()
    # options.add_argument ("--headless")
    options.add_argument ("--no-sandbox")
    options.add_argument ("--disable-dev-shm-usage")
    options.add_argument ("--disable-gpu")
    options.add_argument ("--disable-features=NetworkService")
    options.add_argument ("--window-size=1920x1080")
    options.add_argument ("--disable-features=VizDisplayCompositor")
    driver = webdriver.Chrome (options=options , service_log_path='selenium.log')

    # driver = webdriver.Chrome ('./chromedriver')  # Optional
    # driver = webdriver.Chrome('/Users/karlestermann/PycharmProjects/QlikCoreGui/node_modules/electron-chromedriver/bin/chromedriver')
    # driver = webdriver.Chrome('chromedriver')
    #driver.maximize_window()
    sleep(0.5)

    driver.get('https://www.linkedin.com/')
    sleep(5)

    driver.find_element_by_xpath('//a[text()="Einloggen"]').click()
    sleep(3)

    username_input = driver.find_element_by_name('session_key')
    username_input.send_keys(username)
    sleep(0.5)

    password_input = driver.find_element_by_name('session_password')
    password_input.send_keys(password)
    sleep(0.5)

    # click on the sign in button
    driver.find_element_by_xpath('//button[text()="Einloggen"]').click()
    sleep(5)

    driver.get('https://www.google.com/')
    sleep(5)

    search_input = driver.find_element_by_name('q')
    search_input.send_keys(search_query)
    sleep(1)

    search_input.send_keys(Keys.RETURN)
    sleep(3)

    profiles = driver.find_elements_by_xpath('//*[@class="yuRUbf"]/a[1]')
    print("Google Vor",profiles)
    profiles = [profile.get_attribute('href') for profile in profiles]
    print("Google Nach",profiles)
    for profile in profiles:
        # print(profile)
        driver.get(profile)
        sleep(5)

        sel = Selector(text=driver.page_source)
        # print("Sel1",sel)

        name = sel.xpath('//title/text()').extract_first().split(' | ')[0]
        job_title = sel.xpath('//h2/text()').extract_first().strip()
        schools = ', '.join(sel.xpath('//*[contains(@class, "pv-entity__school-name")]/text()').extract())
        location = sel.xpath('//*[@class="t-16 t-black t-normal inline-block"]/text()').extract_first()
        if location:
           location=sel.xpath('//*[@class="t-16 t-black t-normal inline-block"]/text()').extract_first().strip()
        ln_url = driver.current_url
        if driver.find_element_by_xpath('//*[text()="Kontaktinformationen"]'):
           driver.find_element_by_xpath('//*[text()="Kontaktinformationen"]').click ()
        sleep (1)
        sel = Selector (text=driver.page_source)
        phone = sel.xpath('//span[contains(@class, "t-14 t-black t-normal")]/text()').extract_first()
        if phone:
           phone=sel.xpath('//span[contains(@class, "t-14 t-black t-normal")]/text()').extract_first().strip()
        # driver.find_element_by_xpath ('//*[text()="Verwerfen"]').click()
        # sleep (1)


        # print ("Phone" , phone)

        print('\n')
        print(name)
        print(job_title)
        print(schools)
        print(location)
        print(phone)
        print(ln_url)
        print('\n')

        try:
            driver.find_element_by_xpath('//*[text()="Mehr…"]').click()
            sleep(1)

            driver.find_element_by_xpath('//*[text()="Kontaktinformationen"]').click()
            sleep(1)

            #driver.find_element_by_xpath('//*[text()="Senden"]').click()
            #sleep(1)
        except:
            pass

        writer.writerow([name, phone, job_title, schools, location, ln_url])
        result = [name, phone, job_title, schools, location, ln_url]
        all_results.append (result)

    result_df = pd.DataFrame (all_results)
    result_df.columns = ['name', 'phone','job_title', 'schools', 'location', 'ln_url']

    driver.quit()
    # print(result_df)
    return result_df
