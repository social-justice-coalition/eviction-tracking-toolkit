# historic-court-data-scraping

### Purpose

To analyze and capture previous eviction cases, we used Historic High Court Data from the SAFLII. The Southern African Legal Information Institute (SAFLII) is an online repository of legal information from South Africa, and we chose the databases: South Africa: Western Cape High Court, Cape Town to get the cases about ‘Prevention of Illegal Eviction’ from 1993 to 2018. By scraping each case using BeautifulSoup and extracting the information by using SpaCy and Regex packages, we generate an Excel file of structured historic data that gives an overview of court decisions in the post-apartheid era.

The code can be adjusted and used for future years to update the database, but this may be a challenge without knowledge of Python or JupyterNotebooks. This is an ongoing project.

----

### Process

This code has two main components: the first piece checks if there was any case about ‘Prevention of Illegal Eviction’ in a specific year; the second piece extracts the information from each case into the larger dataset.

Users need to put in a year after 1993 (in the future, users can also put in the other later year, but for this project, we only consider these 26 years), the code will use BeautifulSoup to scrape each link of all the cases in that year, and open it to find out if the keywords: ‘Prevention of Illegal Eviction’ is contained within the case. If it finds the keywords, it will print out the link of the cases, otherwise it will show out 'no case about PIE'.

For the second part, if in the previous step we received any relative link, the code will continue using BeautifulSoup to open the text of the case and SpaCy and Regex to extract the title of the case title, judgment date, case number, ERF number, heard date and address. After gathering all the information from a year, that year's dataset is added to a larger, multi-year dataset. Finally, convert the multi-year dataset to an excel file for easy readability. The result is a complete dataset of court decisions from the Western Cape that contain the keywords.
