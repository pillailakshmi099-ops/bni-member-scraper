# 📊 BNI Member Directory Web Scraper

A Python-based web scraping application designed to extract, organize, and export member information from the **BNI Mumbai North East Member Directory**.

The application uses **Requests, BeautifulSoup, and Selenium** for data extraction and **Streamlit** to provide an interactive web interface. Users can retrieve member details, search records, and download the collected information in Excel format.

## 🌐 Live Application

[**Launch BNI Member Directory Web Scraper**](https://bni-member-scraper.streamlit.app/)

## 📌 Project Overview

The BNI Member Directory Web Scraper automates the process of collecting member information from an online business directory.

Manually visiting individual member profiles and recording their details can be time-consuming. This application simplifies the process by extracting member information, retrieving available addresses from profile pages, and organizing the results into a structured dataset.

The project demonstrates practical implementation of web scraping, browser automation, data processing, and web application deployment using Python.

## ✨ Features

- **Automated Data Extraction:** Retrieves member information from the BNI Mumbai North East directory.
- **Profile-Based Address Extraction:** Uses Selenium to visit individual member profiles and collect available address information.
- **Interactive Web Interface:** Provides a simple interface built using Streamlit.
- **Search Functionality:** Allows users to search records by member name or company.
- **Data Visualization:** Displays extracted records in an organized table.
- **Summary Metrics:** Shows the total number of members and successfully retrieved addresses.
- **Excel Export:** Allows users to download extracted records in `.xlsx` format.
- **Error Handling:** Handles scraping errors and unavailable profile information.
- **Cloud Deployment:** Accessible through Streamlit Community Cloud.

## 🛠️ Technologies Used

| Technology | Purpose |
|:---|:---|
| Python | Core programming language |
| Requests | Fetches HTML content from the member directory |
| BeautifulSoup | Parses HTML and extracts member information |
| Selenium | Automates browser interactions to retrieve profile addresses |
| Pandas | Organizes extracted data into structured DataFrames |
| OpenPyXL | Exports member records to Excel format |
| Streamlit | Creates the interactive web application |
| Git & GitHub | Version control and source code management |
| Streamlit Community Cloud | Hosts and deploys the application |

## ⚙️ How It Works

### Step 1: Fetch Member Directory

The application sends an HTTP request to the BNI Mumbai North East directory using the Requests library.

### Step 2: Extract Member Information

BeautifulSoup parses the HTML response and extracts member names, company names, professions, phone numbers, and profile links.

### Step 3: Retrieve Member Addresses

Selenium launches a headless Chrome/Chromium browser and visits individual member profiles to extract available address information.

### Step 4: Process Extracted Data

The extracted records are stored as Python dictionaries and converted into a Pandas DataFrame.

### Step 5: Display Results

Streamlit displays the extracted information in an interactive table with search functionality and summary metrics.

### Step 6: Export to Excel

Users can download the extracted records as an Excel file for further analysis and authorized use.

## ⚠️ Challenges Faced

### Dynamic Profile Information

Some member information, particularly addresses, required browser-based extraction.

Solution: Integrated Selenium to access individual profile pages and retrieve address details.

### Browser Compatibility During Deployment

Selenium initially encountered ChromeDriver compatibility and dependency issues in the cloud environment.

Solution: Configured Chromium and ChromeDriver dependencies for Linux-based deployment while maintaining local compatibility.

### Handling Missing Data

Some profiles may not contain accessible address information.

Solution: Implemented exception handling, retries, and a default Not Available value for missing addresses.

## 📚 Key Learning Outcomes

Through this project, I gained practical experience in:

- Extracting structured information from web pages using web scraping techniques.
- Working with HTTP requests and HTML parsing.
- Implementing browser automation using Selenium.
- Processing and organizing data using Pandas.
- Developing interactive web applications using Streamlit.
- Exporting structured data into Excel format using OpenPyXL.
- Managing source code and version control using Git and GitHub.
- Deploying Python applications using Streamlit Community Cloud.
- Identifying and resolving dependency, debugging, and browser compatibility issues.
