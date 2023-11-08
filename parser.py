import time
import undetected_chromedriver as uc
import json


from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


driver = uc.Chrome()


def collect_all_courses():
    
    page_link = 'https://www.udemy.com/courses/search/?p=1&q=AI&src=ukw'
    page_number = 1
    courses_to_pars = []
    while True:
        pages_of_site = []
        driver.get(page_link)
        while True:
            try:
                WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[2]/div/div/header/h1'))

                )
                break
            except:
                driver.refresh()
        
        container = driver.find_element(By.CLASS_NAME,
                                                'course-list--container--FuG0T')
        courses = container.find_elements(By.CLASS_NAME,
                                                       'course-card-title-module--title--2C6ac')
        for info in courses:
            href_of_container = info.find_element(By.TAG_NAME, 'a')
            href_of_container = href_of_container.get_attribute('href')
            courses_to_pars.append(href_of_container)

        navigations_container = driver.find_element(By.XPATH,
                                                    '/html/body/div[1]/div[2]/div/div/div/nav')
        links_in_navigation = navigations_container.find_elements(By.TAG_NAME, 'a')
        for href in links_in_navigation:
            pages_of_site = (href.get_attribute('href'))

        try:
            if pages_of_site[-1] != page_link:
                page_number = pages_of_site
                print('Переходим к следующей странице:  ' + str(page_number))
        except:
            (print('Ошибка перехода на следующую страницу'))
            break
        page_link = page_number


    with open('courses.json', "w") as file:
        json.dump(courses_to_pars, file, indent=2)
    return courses_to_pars


def parse_the_course_rates(courses_to_pars):
    for course in courses_to_pars[:1]:
        print('---------------------')
        result_for_json = [1,2,3]
        result_for_json[0] = course
        try:
            list_of_revievs = []
            json_list_of_lists = []
            with open('persons.json', 'w') as file:
                json.dump(json_list_of_lists, file, indent=2)
            driver.get(course)
            time.sleep(5)
            try:
                WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.ID, 'reviews'))
                )
                print('Есть отзывы')
            except:
                driver.refresh()


            result = driver.find_element(By.CLASS_NAME, 'star-rating-module--star-wrapper--VHfnS')\
                .find_element(By.CLASS_NAME, 'ud-sr-only')
            print('На курсе: ' + str(result.text))
            button_revievs = driver.find_element(By.XPATH, "//button[@data-purpose='show-reviews-modal-trigger-button']")
            print("Нашел кнопку 'Показать все отзывы'")
            button_revievs.click()
            time.sleep(2)
            try:
                load_more = driver.find_element(By.XPATH, '/html/body/div[12]/div/div[2]/div[2]/div[2]/button')
                for i in range(999):
                    load_more.click()
            except:
                print('Прокликал отзывы')
            container_otzivov = driver.find_element(By.XPATH, '/html/body/div[12]/div/div[2]/div[2]/div[2]/ul')
            list_otzivov = container_otzivov.find_elements(By.TAG_NAME, 'li')
            time.sleep(4)
            for otziv in list_otzivov:
                try:
                    otziv_kostil = {
                        "name_otziv": otziv.find_element(By.TAG_NAME, 'p').text,
                        "stars_otziv": otziv.find_element(By.CLASS_NAME, 'ud-sr-only').text,
                        "time_otziv": otziv.find_element(By.CLASS_NAME, 'review--time-since--37KF5').text,
                        "text_otziv": otziv.find_element(By.CLASS_NAME, 'show-more-module--content--cjTh0').text
                    }
                    list_of_revievs.append(otziv_kostil)
                except:
                    pass
            t_or_f = True
            result_for_json[1] = t_or_f
            result_for_json[2] = list_of_revievs
        except:
            try:
                t_or_f = False
                result_for_json[1] = t_or_f
                if driver.find_element(By.CLASS_NAME, 'styles--rating-wrapper--ajCRv').find_elements(By.TAG_NAME, 'span')[1] == '(0 оценок)':
                    print("нет отзывов")
                else:
                    print('нет письменных отзывов')
            except:
                print('ОШИБКА')
                print(course)

        with open('persons.json', "r") as file:
            json_list_of_lists = json.load(file)
        json_list_of_lists.append(result_for_json)
        with open('persons.json', "w") as f:
            json.dump(json_list_of_lists, f, indent=2)


#collect_all_courses()
print('первая часть закончена')
with open('courses.json', "r") as file:
    courses = json.load(file)
parse_the_course_rates(courses)
print('вторая часть закончена')


