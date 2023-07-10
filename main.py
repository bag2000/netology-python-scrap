import requests
import bs4
import fake_headers
import re

headers = fake_headers.Headers('firefox', os='win')
headers_dict = headers.generate()

response = requests.get('https://spb.hh.ru/search/vacancy?text=Python+django+flask&salary=&area=1&area=2&ored_clusters=true', headers=headers_dict)
html_data = response.text
main_html = bs4.BeautifulSoup(html_data, 'lxml')
job_openings = main_html.findAll('a', class_='serp-item__title')

list_job_openings = []
for vacancy in job_openings:

    response = requests.get(vacancy['href'], headers=headers_dict)
    html_data = response.text
    main_html = bs4.BeautifulSoup(html_data, 'lxml')
    salary = main_html.find('span', class_='bloko-header-section-2 bloko-header-section-2_lite')
    pattern = re.compile('[<a-z\s=\"-2_]+[>]?(от)?\s?(<!-- -->)?([0-9 ]+)?(<!-- -->)?\s(<!-- -->)?(₽)?(<span class=\"vacancy-salary-compensation-type\">)?\s?(<!-- -->)?(на руки)?(</span></span>)?')
    pattern_repl = r"\1 \3\6 \9 "
    salary = re.sub(pattern, pattern_repl, str(salary)).replace('</span></span>', '')

    if salary[0] != 'о':
        salary = 'нет'

    company = main_html.find('span', class_='vacancy-company-name')
    company = str(company).replace('</span></a></span>', '').replace('<!-- -->', '').split('>')[3]

    keywords = main_html.find('div', class_='bloko-tag-list')

    list_job_openings.append({
        'title': list(vacancy)[0],
        'link': vacancy['href'],
        'salary': salary,
        'company': company
    })


for vacancy in list_job_openings:
    title = vacancy['title']
    link = vacancy['link']
    salary = vacancy['salary']
    vacancy = vacancy['company']
    print(f'Название: {title}, ссылка: {link}, зарплата: {salary}, компания: {vacancy}')
