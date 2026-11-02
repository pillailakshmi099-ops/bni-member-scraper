
import requests
import time
import pandas as pd

from bs4 import BeautifulSoup
from urllib.parse import urljoin

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# ==========================================
# CONFIGURATION
# ==========================================

BASE_URL = "https://bni-mumbainortheast.in"

MEMBER_LIST_PAGE = (
    BASE_URL + "/mumbai-north-east-millionaire/en-IN/memberlist"
)

LIST_URL = (
    BASE_URL + "/bnicms/v3/frontend/memberlist/display"
)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/156.0.0.0 Safari/537.36"
    ),
    "X-Requested-With": "XMLHttpRequest",
    "Referer": MEMBER_LIST_PAGE
}


# ==========================================
# STEP 1: SCRAPE MEMBER LIST USING REQUESTS
# ==========================================

def scrape_member_list():

    session = requests.Session()
    session.headers.update(HEADERS)

    payload = {
        "parameters": (
            "chapterName=3889&regionIds=22034&chapterWebsite=1"
        ),
        "languages[availableLanguages][0][type]": "published",
        "languages[availableLanguages][0][url]":
            "http://bni-mumbainortheast.in/"
            "mumbai-north-east-millionaire/en-IN/memberlist",
        "languages[availableLanguages][0][descriptionKey]":
            "English (IN)",
        "languages[availableLanguages][0][id]": "47",
        "languages[availableLanguages][0][localeCode]": "en_IN",
        "languages[activeLanguage][id]": "47",
        "languages[activeLanguage][localeCode]": "en_IN",
        "languages[activeLanguage][descriptionKey]": "English (IN)",
        "languages[activeLanguage][cookieBotCode]": "en",
        "cmsv3": "true",
        "website_type": "3",
        "website_id": "11099",
        "mappedWidgetSettings": (
            '[{"key":113,"name":"Member Names","value":"Member Names"},'
            '{"key":117,"name":"Profession/Specialty",'
            '"value":"Profession/Specialty"},'
            '{"key":118,"name":"Company","value":"Company"},'
            '{"key":119,"name":"Showing","value":"Showing"},'
            '{"key":120,"name":"to","value":"to"},'
            '{"key":121,"name":"of","value":"of"},'
            '{"key":122,"name":"entries","value":"entries"},'
            '{"key":304,"name":"Zero Records","value":"Zero Records"},'
            '{"key":343,"name":"Phone","value":"Phone"},'
            '{"key":344,"name":"Send Mail","value":"Send Mail"}]'
        ),
        "pageMode": "Live_Site"
    }

    print("Fetching BNI member list...")

    response = session.post(
        LIST_URL,
        data=payload,
        timeout=30
    )

    response.raise_for_status()

    soup = BeautifulSoup(response.text, "lxml")

    rows = soup.select("table#chapterListTable tbody tr")

    print("Rows detected:", len(rows))

    members = []

    for row in rows:

        cells = row.find_all("td")

        if len(cells) < 4:
            continue

        name_tag = cells[0].find("a")

        if not name_tag:
            continue

        name = name_tag.get_text(strip=True)

        profile_link = name_tag.get("href", "")

        profile_url = urljoin(
            MEMBER_LIST_PAGE,
            profile_link
        )

        member = {
            "Member Name": name,
            "Company": cells[1].get_text(strip=True),
            "Profession/Specialty": cells[2].get_text(strip=True),
            "Phone": cells[3].get_text(strip=True),
            "Address": "Not Available",
            "Profile URL": profile_url
        }

        members.append(member)

    print("Total members retrieved:", len(members))

    return members


# ==========================================
# STEP 2: CONFIGURE OPTIMIZED SELENIUM
# ==========================================

def create_driver():

    options = Options()

    # Run Chrome in the background
    options.add_argument("--headless=new")

    # Optimize browser performance
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-extensions")

    # Load pages faster
    options.page_load_strategy = "eager"

    # Block unnecessary images
    prefs = {
        "profile.managed_default_content_settings.images": 2
    }

    options.add_experimental_option(
        "prefs",
        prefs
    )

    driver = webdriver.Chrome(options=options)

    driver.set_page_load_timeout(30)

    return driver



# ==========================================
# STEP 3: EXTRACT CLEAN ADDRESS FROM PROFILE
# ==========================================

def extract_address_from_profile(driver, member):

    try:

        profile_url = member["Profile URL"]

        # Open member profile
        driver.get(profile_url)

        # Wait for address section
        address_element = WebDriverWait(
            driver,
            12
        ).until(
            EC.presence_of_element_located(
                (
                    By.CSS_SELECTOR,
                    ".widgetMemberCompanyDetail .textHolder h6"
                )
            )
        )

        # Extract text line by line
        lines = address_element.get_attribute(
            "innerText"
        ).splitlines()

        lines = [
            line.strip()
            for line in lines
            if line.strip()
        ]

        if not lines:
            return None

        # Normalize text for comparison
        member_name = member["Member Name"].strip().lower()
        company_name = member["Company"].strip().lower()

        cleaned_lines = []

        for line in lines:

            line_lower = line.strip().lower()

            # Skip member name
            if line_lower == member_name:
                continue

            # Skip company name
            if line_lower == company_name:
                continue

            # Skip common titles attached to names
            if line_lower.startswith(
                (
                    "mr. ",
                    "mrs. ",
                    "ms. ",
                    "miss ",
                    "dr. ",
                    "mr ",
                    "mrs ",
                    "ms ",
                    "dr "
                )
            ):
                continue

            cleaned_lines.append(line.strip())

        # Join remaining lines as address
        address = ", ".join(cleaned_lines).strip()

        if address:
            return address

        return None

    except Exception as error:

        print(
            "Address extraction failed for",
            member["Member Name"],
            ":",
            str(error)[:150]
        )

        return None


# ==========================================
# STEP 4: SCRAPE ADDRESSES USING SELENIUM
# ==========================================

def scrape_all_addresses(members):

    if not members:
        return members

    driver = create_driver()

    total = len(members)

    try:

        for index, member in enumerate(
            members,
            start=1
        ):

            print(
                f"[{index}/{total}] "
                f"Fetching address: "
                f"{member['Member Name']}"
            )

            # Retry if the profile fails
            for attempt in range(1, 4):

                address = extract_address_from_profile(
                    driver,
                    member
                )

                if address:

                    member["Address"] = address

                    print("Address found!")

                    break

                print(
                    f"Retry {attempt}/3 for "
                    f"{member['Member Name']}"
                    )

                time.sleep(0.5)

            # Move to next member

    finally:

        # Always close browser after scraping
        driver.quit()

    # ==========================================
    # SUMMARY
    # ==========================================

    successful = sum(
        1 for member in members
        if member["Address"] != "Not Available"
    )

    missing = [
        member["Member Name"]
        for member in members
        if member["Address"] == "Not Available"
    ]

    print("\n========== SCRAPING SUMMARY ==========")

    print("Total members:", total)

    print("Addresses retrieved:", successful)

    print("Addresses missing:", len(missing))

    if missing:

        print("\nMembers with missing addresses:")

        for name in missing:
            print("-", name)

    print("\nScraping completed!")

    return members


# ==========================================
# STEP 5: SAVE TO EXCEL
# ==========================================

def save_to_excel(members):

    if not members:

        print("No data available to save.")

        return

    df = pd.DataFrame(members)

    filename = "FAST_BNI_Mumbai_North_East_Members.xlsx"

    df.to_excel(
        filename,
        index=False,
        engine="openpyxl"
    )

    print("\nExcel file successfully created!")

    print("Filename:", filename)

    print("Total records:", len(df))


# ==========================================
# MAIN PROGRAM
# ==========================================

if __name__ == "__main__":

    all_members = scrape_member_list()

    if all_members:

        all_members = scrape_all_addresses(
            all_members
        )

        save_to_excel(all_members)
