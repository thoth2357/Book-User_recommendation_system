def user_preferences() -> dict:
    """Load book ratings and book information from CSV files and organize them into a dictionary of user preferences.

    Returns:
        A dictionary with two keys: 'Books' and 'Ratings'. The value for 'Books' is another dictionary containing book
        information for each book in the dataset, keyed by ISBN. The value for 'Ratings' is another dictionary containing
        the book ratings for each user in the dataset, keyed by user ID. Each value in 'Ratings' is itself a dictionary,
        keyed by ISBN, containing the book rating for that user and book.
    """
    user_preference = {'Books': {}, 'Ratings': {}}

    with open('Book-Ratings.csv', 'r', encoding='ISO-8859-1') as ratings_file:
        print('Loading Book-Ratings.csv')
        # Skip the header row
        next(ratings_file)
        for line in ratings_file:
            row = line.strip().split(',')
            user_id = row[0]
            isbn = row[1]
            book_rating = row[2]
            if user_id not in user_preference['Ratings']:
                user_preference['Ratings'][user_id] = {isbn: {'book-ratings': book_rating}}
            elif isbn not in user_preference['Ratings'][user_id]:
                user_preference['Ratings'][user_id][isbn] = {'book-ratings': book_rating}

        print('Done loading Book-Ratings.csv')

    with open('Books-encoded.csv', 'r', encoding='ISO-8859-1') as books_file:
        print('Loading Books-encoded.csv')
        # Skip the header row
        next(books_file)
        for line in books_file:
            row = line.strip().split(',')
            isbn = row[0]
            book_title = row[1]
            book_author = row[2]
            publisher = row[3]
            year_of_publication = row[4]
            if isbn not in user_preference['Books']:
                user_preference['Books'][isbn] = {
                    'Book-Title': book_title,
                    'Book-Author': book_author,
                    'Publisher': publisher,
                    'Year-Of-Publication': year_of_publication
                }

        print('Done loading Books-encoded.csv')

    return user_preference

# g = user_preferences()
# print(len(g))
# print(g.keys())
# # print(g['Ratings'])
# print(g['Books']['0374157065'])
# print(g['Ratings']['276726'])