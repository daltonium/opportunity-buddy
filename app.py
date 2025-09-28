import time
import random
import pandas as pd
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium_stealth import stealth
from bs4 import BeautifulSoup


def get_url(position, location):
    template = 'https://in.indeed.com/jobs?q={}&l={}'
    position = position.replace(' ', '+')
    location = location.replace(' ', '+')
    return template.format(position, location)


def get_record(card):
    title_tag = card.find('h2', {'class': 'jobTitle'})
    job_title = title_tag.text.strip() if title_tag else 'NOT MENTIONED'

    company_tag = card.find('span', {'data-testid': 'company-name'})
    company = company_tag.text.strip() if company_tag else 'NOT MENTIONED'

    location_tag = card.find('div', {'data-testid': 'text-location'})
    job_location = location_tag.text.strip() if location_tag else 'NOT MENTIONED'

    post_date_tag = card.find('span', {'data-testid': 'myJobsStateDate'})
    post_date = post_date_tag.text.strip() if post_date_tag else 'NOT MENTIONED'

    today = datetime.today().strftime('%Y-%m-%d')

    summary_tag = card.find('div', {'class': 'job-snippet'})
    if not summary_tag:
        summary_tag = card.find('div', {'data-testid': 'job-snippet'})
    summary = summary_tag.text.strip().replace("\n", " ") if summary_tag else 'NOT MENTIONED'

    job_url = "https://in.indeed.com" + card.get('href') if card.get('href') else 'NOT MENTIONED'

    salary_tag = card.find('div', {'data-testid': 'attribute_snippet_testid-salary'})
    if not salary_tag:
        salary_tag = card.find('div', {'class': 'salary-snippet'})
    salary = salary_tag.text.strip() if salary_tag else 'NOT MENTIONED'

    return {
        "JobTitle": job_title,
        "Company": company,
        "Location": job_location,
        "PostDate": post_date,
        "ExtractDate": today,
        "Summary": summary,
        "Salary": salary,
        "JobUrl": job_url
    }


def main(position, location):
    records = []
    url = get_url(position, location)

    # Selenium setup
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--headless")

    driver = webdriver.Chrome(options=options)

    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            # matches a common Intel GPU instead of strange defaults
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            # fixes a subtle rendering difference
            fix_hairline=True,
    )

    driver.get(url)
    time.sleep(5)

    # scroll to half page right after load
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
    time.sleep(2)

    page_num = 1
    while True:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        cards = soup.select("a.tapItem, div.job_seen_beacon")

        print(f"📄 Page {page_num}: Found {len(cards)} jobs")
        for card in cards:
            try:
                records.append(get_record(card))
            except Exception as e:
                print(f"⚠️ Error parsing card: {e}")

        next_btn = soup.find('a', {'data-testid': 'pagination-page-next'})
        if next_btn and next_btn.get('href'):
            next_url = 'https://in.indeed.com' + next_btn['href']
            driver.get(next_url)
            page_num += 1
            time.sleep(random.uniform(3, 6))
            # also scroll halfway on each new page
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
        else:
            break

    driver.quit()

    df = pd.DataFrame(records)
    df.to_csv("results.csv", index=False, encoding="utf-8")

    print(f"✅ Scraped {len(df)} jobs across {page_num} pages into results.csv")


if __name__ == "__main__":
    jobTitle = input("Job Title: ")
    loc = input("Location: ")
    main(jobTitle, loc)
