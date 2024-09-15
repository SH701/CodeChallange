from playwright.sync_api import sync_playwright
import time
from bs4 import BeautifulSoup
import csv

class Scrap:
    def __init__(self):
        self.p = sync_playwright().start()
        self.browser = self.p.chromium.launch(headless=False) 
        self.page = self.browser.new_page()
    
    def scrap(self, keyword):
        self.jobs_db = []  
        self.page.goto(f"https://www.wanted.co.kr/search?query={keyword}&tab=position")

        for _ in range(5):
            time.sleep(3)
            self.page.keyboard.press("End")

        content = self.page.content()
        soup = BeautifulSoup(content, "html.parser")
        jobs = soup.find_all("div", class_="JobCard_container__REty8")

        for job in jobs:
            link = f"https://www.wanted.co.kr{job.find('a')['href']}"
            title = job.find("strong", class_="JobCard_title__HBpZf").text
            company_name = job.find("span", class_="JobCard_companyName__N1YrF").text
            reward = job.find("span", class_="JobCard_reward__cNlG5").text
            job_info = {
                "title": title,
                "company_name": company_name,
                "reward": reward,
                "link": link
            }
            self.jobs_db.append(job_info)
    
    def save_to_csv(self, keyword):
        filename = f"{keyword}_jobs.csv"
        with open(filename, "w", newline='', encoding='utf-8-sig') as file:
            writer = csv.writer(file)
            writer.writerow(["Title", "Company", "Reward", "Link"])
            for job in self.jobs_db:
                writer.writerow(job.values())

    def close(self):
        self.browser.close()
        self.p.stop()

if __name__ == "__main__":
    scraper = Scrap()
    keywords = ["python", "js", "flutter"]
    try:
        for keyword in keywords:
            scraper.scrap(keyword)
            scraper.save_to_csv(keyword)
    finally:
        scraper.close()