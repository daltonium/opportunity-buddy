# 🕵️‍♂️ Indeed Job Scraper (Selenium + BeautifulSoup)

This project is a **job scraper** for [Indeed India](https://in.indeed.com/).  
It uses **Selenium**, **BeautifulSoup**, and **Pandas** to extract job postings, including job title, company, location, post date, salary, and job description snippets.  
The results are saved into a CSV file (`results.csv`).

---

## 🚀 Features
- Scrapes job postings from Indeed India.
- Collects:
  - Job Title
  - Company
  - Location
  - Post Date
  - Extract Date
  - Job Summary
  - Salary (if available)
  - Job URL
- Saves results in `results.csv`.
- Bypasses basic bot detection using [`selenium-stealth`](https://pypi.org/project/selenium-stealth/).
- Handles multiple pages with random delays to mimic human behavior.

---

## 📦 Requirements

Make sure you have Python **3.8+** installed.  
selenium
selenium-stealth
beautifulsoup4
pandas
