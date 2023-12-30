import pandas as pd
from notion_client import Client

# TODO: As an improvement, update these to be environment variables (they should not be hardcoded)
notion_token = "secret_DQVjotqX2yqrKnWina3H5YgFJWH9tecBhjAZ1lG4A1u"
database_id = "2e807af3c29548c5887c35e1456c003d"
notion = Client(auth=notion_token)

# Normalize book title capitlization by capitalizing the first letter of each word
def normalize_titles(s):
    t = []
    for temp in s.split(' '): t.append(temp.capitalize())
    return ' '.join(t)

# Process ratings to remove duplicate ratings, get average ratings and number of favorites
def process_ratings(df):
    df['book_title'] = df['book_title'].str.strip().apply(normalize_titles)
    df['member'] = df['member'].str.strip().str.lower()
    df['book_rating'] = pd.to_numeric(df['book_rating'])
    # If there are duplicates, only keep the last rating for each member and book
    df = df.drop_duplicates(subset=['member', 'book_title'], keep='last')
    # Mark a book as a favorite if a member has rated it 5
    df['is_favorite'] = df['book_rating'] == 5
    
    result_df = df.groupby('book_title').agg(
        average_rating=('book_rating', 'mean'),
        favorites=('is_favorite', 'sum')
    ).reset_index()

    # Round average rating to two decimal points
    result_df['average_rating'] = result_df['average_rating'].round(2)

    return result_df

def read_database():
    existing_books = notion.databases.query(database_id).get("results")
    return existing_books

def write_data(row, existing_book_titles):
    # If the book does not already exist in the database, create a new record
    # TODO: As an improvement, if the record already exists in the database, we can update the record instead of skipping it
    if row['book_title'] not in existing_book_titles:
        notion.pages.create(
            **{
                "parent": {
                    "database_id": database_id
                },
                "properties": {
                    "Book Title": {"title": [{"text": {"content": row['book_title']}}]},
                    "Rating": {"number": row['average_rating']},
                    "Favorites": {"number": row['favorites']}
                }
            }
        )

def main():
    df = pd.read_csv('data/ratings.csv', header=None, names=['book_title', 'member', 'book_rating'])
    result_df = process_ratings(df)
    existing_books = read_database()
    existing_book_titles = []
    
    # From the existing records in the database, get the existing book titles
    for res in existing_books:
        book_title = res.get('properties', {}).get('Book Title', {}).get('title', [{}])[0].get('text', {}).get('content', '')
        existing_book_titles.append(book_title)
    
    for index, row in result_df.iterrows():
        write_data(row, existing_book_titles)

if __name__ == '__main__':
    main()
