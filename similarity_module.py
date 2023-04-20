def helper_function(user_preference, id_1, id_2):
    """
    A helper function to form a feature dictionary for two users based on their book ratings.

    Args:
        user_preference (dict): A dictionary containing user preferences and book information.
        id_1 (int): The id of the first user.
        id_2 (int): The id of the second user.

    Returns:
        A tuple of dictionaries containing features for the two users, where each dictionary maps a book to a list of features.

    Raises:
        KeyError: If the user_preference dictionary does not contain necessary keys.
        ValueError: If the input arguments are not valid or a common set of rated books cannot be found.

    """
    try:
        user1_rated_books = user_preference['Ratings'][id_1]
        user2_rated_books = user_preference['Ratings'][id_2]
        common_rated_books = set(user1_rated_books.keys()).intersection(user2_rated_books.keys())

        if not common_rated_books:
            raise ValueError('No common books found between the users')

        common_rated_books_features = {}
        book_na = []

        # Get book features for the common books
        for book in common_rated_books:
            try:
                common_rated_books_features[book] = user_preference['Books'][book]
            except KeyError:
                book_na.append(book)

        # Form the features for the users
        user1_features = {}
        user2_features = {}

        for book in common_rated_books:
            if book not in book_na:
                user1_features[book] = [
                    int(common_rated_books_features[book]['Book-Title']),
                    int(common_rated_books_features[book]['Book-Author']),
                    int(common_rated_books_features[book]['Year-Of-Publication']),
                    int(user1_rated_books[book]['book-ratings'].replace('"', ""))
                ]
                user2_features[book] = [
                    int(common_rated_books_features[book]['Book-Title']),
                    int(common_rated_books_features[book]['Book-Author']),
                    int(common_rated_books_features[book]['Year-Of-Publication']),
                    int(user2_rated_books[book]['book-ratings'].replace('"', ""))
                ]

        if not user1_features or not user2_features:
            raise ValueError('No valid common books found between the users')

        return user1_features, user2_features

    except KeyError:
        raise KeyError('Necessary keys not found in user_preference dictionary')
    except (TypeError, ValueError) as e:
        raise ValueError('Invalid input arguments:', e)



