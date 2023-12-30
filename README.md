# book-ratings

## Overview
Thanks for taking the time to look through my take home assessment! This program reads book ratings from the provided `ratings.csv`, aggregates the information, and populates a notion database with the results. The Notion database used for this program can be found [here](https://power-occupation-87a.notion.site/2e807af3c29548c5887c35e1456c003d?v=f707bfb9046746e2be33743fa518897e).

This program is deterministic, meaning that it will always achieve the same result. An existing database will not create duplicate rows.

## Setup
This program uses two libraries: [Pandas](https://github.com/pandas-dev/pandas) and [Notion Client](https://github.com/ramnes/notion-sdk-py).
To install these libraries, run the following commands:
```
pip install pandas
```
```
pip install notion-client
```

## Usage
To run the program, run the following command from the command line:
```
python3 main.py
```
To run the tests, run the following command from the command line:
```
python3 unit_tests.py
```

## Improvements
If I had more time to work on this project, there are some improvements I would make which have been indicated in the code as TODO comments.

Firstly, I would make a virtual environment and I wouldn't hardcode the secrets/tokens, I would store them as environment variables instead. For this assessment since I will just be running it on my system and recording a video, I left the tokens hardcoded.

I would also improve the way I check for existing book records. Right now, my approach is that I query the database for all existing records, then I iterate through these records and I grab the book titles and add it to a list. When adding rows to the database, if the book title already exists in this list, I just skip it and I don't add it to the database. This is to ensure determinism.
 I think this works for the use case of this assessment, but there could be edge cases where the database has old records that have outdated average ratings and number of favorites. In this case, we don't want to skip the records entirely, instead we should update their average rating and favorites. 
 
 We could update the book if it already exists, however this may make uneccessary API calls since the rating/favorites might be the same, which means we don't need to update it. This would be the simplest to build off of my current approach. 
 
 Another way is to check if the rating and number of favorites are the same as well, if they are, the whole record is the same and we should skip it. We only update the record if it is not the same as the existing one. This would be the best solution but it will require more modification to my code since we need to also get the average rating and number of favorites and compare them. I would still choose this approach because it is the most efficient for a large scale and it does not require too much extra work.

## Questions
### Was there anything you got stuck on, and if so what did you do to resolve it?
- #### Understanding the structure of the database objects from the Notion API and how to work with them
  - At first, I struggled to get the existing book titles from the database query so I could check if the books were already in the database to make the program deterministic. To overcome this, I printed out the results of the database query and looked at the structure to understand how I could get the information I needed from the object.
- #### Writing tests
  - I'm not too familiar with unit testing in Python so I struggled with mocking objects, especially the Notion Client. I overcame this by reading documentation about the [unittest.mock library](https://docs.python.org/3/library/unittest.mock.html) and understanding how to use patch to mock objects for my tests.

### Do you have any suggestions for improving the API documentation to make it clearer or easier to use?
A suggestion I have is to make sure the documentation is consistent and up-to-date. For example, when I was looking for the database ID, on this page: [Working with Databases,](https://developers.notion.com/docs/working-with-databases) under "Where can I find my database's ID?" it says that the database ID is a 36 character long string. However, the database ID is a 32 character long string. Since I couldn't find a 36 character string, I ended up searching on Google "Notion database id" where I found this page: [Retrieve a Database,](https://developers.notion.com/reference/retrieve-a-database) which says that the database ID is a 32 character string. I used this page to understand how to get the database ID. Perhaps this page could be linked somewhere in the Working with Databases page.