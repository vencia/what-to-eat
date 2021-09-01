from selenium import webdriver
import datetime
import locale

locale.setlocale(locale.LC_ALL, "de_DE.utf8")


def get_kit_mensa_plan():
    driver.get('https://www.sw-ka.de/en/essen/?view=ok&STYLE=popup_plain&c=adenauerring')
    today_table = driver.find_element_by_xpath('//*[@id="platocontent"]/table')
    rows = today_table.find_elements_by_xpath('tbody/tr')
    meal_plan = []
    for row in rows:
        row = row.find_elements_by_xpath('td')
        if len(row) > 0:
            assert len(row) == 2  # line & meals
            line = row[0].text.split('\n')[0]
            meal_infos = [x.split('\n')[0].strip() for x in row[1].text.split(']') if '€' in x]
            if len(meal_infos) > 0:
                for meal_info in meal_infos:
                    meal_info[-2:] == ' €'
                    meal_info = meal_info[:-2]
                    meal_info = meal_info.rsplit(' ', 1)
                    price = locale.atof(meal_info[-1], float)
                    meal = meal_info[0].rsplit('(', 1)[0].strip()
                    meal_plan.append({'meal': meal, 'price': price, 'line': line})
    return meal_plan


def get_mri_plan():
    driver.get('https://casinocatering.de/speiseplan/')
    today = datetime.datetime.today().strftime('%A, %d. %B %Y')
    cols = driver.find_elements_by_class_name('elementor-widget-wrap')
    meal_plan = None
    for col in cols:
        divs = col.find_elements_by_xpath('div/div')
        if len(divs) == 2:  # day & meals
            day = divs[0].text
            meals = divs[1].text.split('\n')
            if day == today:
                meals = [x.replace('•', '').rsplit('(', 1)[0].strip() for x in meals]
                meal_plan = [{'meal': x} for x in meals]
    return meal_plan


if __name__ == '__main__':
    driver = webdriver.Chrome(executable_path='chromedriver_linux64/chromedriver')
    driver.delete_all_cookies()
    mensa_plan = get_kit_mensa_plan()
    print('mensa')
    print('-----------------')
    print(mensa_plan)
    print('-----------------')
    mri_plan = get_mri_plan()
    print('mri')
    print('-----------------')
    print(mri_plan)
    print('-----------------')
