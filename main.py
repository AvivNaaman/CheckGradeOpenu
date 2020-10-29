# Author: Aviv Naaman, @AvivNaaman, 2020
# A script to check whether grades are in @ OpenU. NOT OFFICIAL!

# Required modules:
#  * pip install selenium
#  * @ https://selenium-python.readthedocs.io/installation.html#drivers:
#    1) Download firefox ("Gecko") driver for win
#    2) Extract the content into C:\Windows\System32 Folder
# YOU ARE READY!

import time
import argparse
import logging


def get_grades_url(course_num, semester, teach_center, teach_group):
    return "https://sheilta.apps.openu.ac.il/pls/dmyopt2/course_info_2.ZIUNMATALA?p_kurs=" + str(
        course_num) + "&p_semester=" + str(semester) + "&p_MERKAZ_LIMUD=" + str(
        teach_center) + "&p_KVUTZAT_LIMUD=" + str(teach_group) + "&p_KOD_PEILUT_KURS=01"


def login(driver, username, password, idnum, sleep):
    username_field = driver.find_element_by_id("p_user")
    pwd_field = driver.find_element_by_id("p_sisma")
    idnum_field = driver.find_element_by_id("p_mis_student")
    username_field.send_keys(username)
    pwd_field.send_keys(password)
    idnum_field.send_keys(str(idnum))
    logging.debug("Waiting for authentication request to finish...")
    driver.find_element_by_xpath("/html/body/div/div[1]/div[1]/form/fieldset/input[1]").click()  # Submit
    time.sleep(sleep)  # Wait For Authentication End


def build_argv_parser():
    logging.debug("Building command line arguments parser")
    p = argparse.ArgumentParser(description="""
    Check For Grades @ OpenU
    Read the argument description below or the documentation!
    """)
    p.add_argument("--sleep", "-s", required=False, help="The time to wait before initiating another request.",
                   default=5, type=int)
    creds = p.add_argument_group("Credentials - REQUIRED")
    creds.add_argument("--userName", required=True, help="Your user name")
    creds.add_argument("--pwd", required=True, help="Your password")
    creds.add_argument("--id", required=True, help="Your ID number")
    courseinfo = p.add_argument_group("Course Information - REQUIRED")
    courseinfo.add_argument("--course", required=True, help="Course number, such as 20109 or 04101")
    courseinfo.add_argument("--semester", required=True, help="Semester, Formatted as yyyy[a|b|c] (e.g. 2021a)")
    courseinfo.add_argument("--group", required=True, help="Group number (e.g. 81)")
    courseinfo.add_argument("--center", required=True, help="Teaching center number (e.g. 780)")
    logging.debug("DONE Building command line arguments parser")
    return p

def process_grades_page(driver):
    from selenium.common.exceptions import NoSuchElementException
    # Now we're @ Grades page. Let's find the exam's grade:
    grades_table = driver.find_element_by_xpath("/html/body/table[1]/tbody/tr[3]/td/table")
    for row in reversed(grades_table.find_elements_by_css_selector("tr")):
        cells = row.find_elements_by_tag_name("td")
        if (len(str(cells[2].text).strip()) > 0):
            try:
                grade = str(cells[5].find_element_by_css_selector("a").text)
                while True:
                    time.sleep(0.35)
                    print('Grade found! You Got ' + grade)
            except NoSuchElementException:
                print("No grade found.")



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logging.info("Starting...")
    parser = build_argv_parser()
    parsed_vars = vars(parser.parse_args())
    logging.debug("The command line arguments are: " + str(parsed_vars))
    sleep = parsed_vars["sleep"]
    try:
        from selenium import webdriver
        from selenium.common.exceptions import WebDriverException
    except:
        logging.critical("Selenium module not found. Please install it using the command 'python -m pip install selenium'.")
        exit(1)
    logging.info("Initializing browser...")
    try:
        logging.debug("Trying to start edge...")
        driver = webdriver.Edge()
    except WebDriverException as edgeException:
        logging.debug("Trying to start edge...failed.")
        try:
            logging.debug("Trying to start firefox...")
            driver = webdriver.Firefox()
        except WebDriverException as firefoxException:
            logging.debug("Trying to start firefox...failed.")
            try:
                logging.debug("Trying to start chrome...")
                driver = webdriver.Chrome()
            except WebDriverException as chromeException:
                logging.debug("Trying to start chrome...failed.")
                logging.critical("""Neither edge, nor firefox and chrome drivers are installed.
                Please download one of the drivers and put it in the C:\Windows\System32 folder and then run again.
                Choose one and download:
                """)
                logging.critical(edgeException.msg)
                logging.critical(firefoxException.msg)
                logging.critical(chromeException.msg)

    logging.info("Browser initialized.")
    logging.info("Starting request loop.")
    url = get_grades_url(parsed_vars["course"], parsed_vars["semester"], parsed_vars["center"], parsed_vars["group"]
                         )
    logging.debug("Grades page URL is: '" + url + "'")

    while True:
        logging.debug("Requesting URL...")
        driver.get(url)
        logging.info("Waiting for request to finish...")
        time.sleep(sleep)
        logging.debug("Request finished. Checking if redirected to login page:")
        if ((not driver.current_url == url) and "login" in driver.current_url):
            logging.info("Redirected to login page. Logging in...")
            login(driver, parsed_vars["userName"], parsed_vars["pwd"], parsed_vars["id"], sleep)
            if ((not driver.current_url == url) and "login" in driver.current_url):
                logging.critical("Authentication failed. Credentials are probably wrong. Check & Re-run.")
                exit(1)
            driver.get(url)  # After login, page is redirected to sheilta's main page, we'd like to view grades!
            time.sleep(sleep)
            logging.info("Authentication Succeeded. ")
        process_grades_page(driver)
        logging.info("Waiting before checking again..")
        time.sleep(600) # Wait before checking again
        logging.log("Checking again...")
