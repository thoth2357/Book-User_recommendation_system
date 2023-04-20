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



def euclidean_similarity(user_preference, id_1, id_2, similarity_type):
    """
    Computes the Euclidean distance between users or books based on their features.
    """
    if similarity_type == 'user':
        user1_features, user2_features = helper_function(user_preference, id_1, id_2)
        if user1_features is not None and user2_features is not None:
            distances = []
            for book in user1_features:
                if book in user2_features:
                    features1 = user1_features[book]
                    features2 = user2_features[book]
                    distance_squared = sum([(a - b) ** 2 for a, b in zip(features1, features2)]) ** 0.5
                    distances.append(distance_squared)
            if distances:
                return sum(distances) / len(distances)
            else:
                return None
        else:
            return None
    elif similarity_type == 'book':
        try:
            features1 = [
                int(user_preference['Books'][id_1]['Book-Title']),
                int(user_preference['Books'][id_1]['Book-Author']),
                int(user_preference['Books'][id_1]['Year-Of-Publication'])
            ]
            features2 = [
                int(user_preference['Books'][id_2]['Book-Title']),
                int(user_preference['Books'][id_2]['Book-Author']),
                int(user_preference['Books'][id_2]['Year-Of-Publication'])
            ]
            distance_squared = sum([(a - b) ** 2 for a, b in zip(features1, features2)]) ** 0.5
            return distance_squared
        except KeyError:
            print('Book ISBN not found. Check inputs.')
            return None
    else:
        print('Invalid similarity type. Choose "user" or "book".')
        return None

def cosine_similarity(user_preference, id_1, id_2, type_):
    '''
    Computes the cosine similarity between books or users. Cosine similarity is commonly used in document similarity 
    and text mining.
    '''
    if type_ == 'user':
        # Get features for both users
        user1_features, user2_features = helper_function(user_preference, id_1, id_2)

        # If there are common books between the users, compute cosine similarity
        if user1_features and user2_features:
            cosine_similarities = []
            for book, features1 in user1_features.items():
                features2 = user2_features.get(book)
                if features2:
                    # Compute dot product and norm
                    dot_product = sum([a * b for a, b in zip(features1, features2)])
                    norm_features1 = sum([a ** 2 for a in features1]) ** 0.5
                    norm_features2 = sum([a ** 2 for a in features2]) ** 0.5
                    
                    # Compute cosine similarity
                    cosine_similarity = dot_product / (norm_features1 * norm_features2)
                    cosine_similarities.append(cosine_similarity)

            # Compute the average cosine similarity across all common books
            if cosine_similarities:
                return sum(cosine_similarities) / len(cosine_similarities)
            else:
                return None
        else:
            return None

    elif type_ == 'book':
        try:
            # Retrieve features for the two books
            features1 = [
                int(user_preference['Books'][id_1]['Book-Title']),
                int(user_preference['Books'][id_1]['Book-Author']),
                int(user_preference['Books'][id_1]['Year-Of-Publication'])
            ]
            features2 = [
                int(user_preference['Books'][id_2]['Book-Title']),
                int(user_preference['Books'][id_2]['Book-Author']),
                int(user_preference['Books'][id_2]['Year-Of-Publication'])
            ]

            # Compute dot product and norm
            dot_product = sum([a * b for a, b in zip(features1, features2)])
            norm_features1 = sum([a ** 2 for a in features1]) ** 0.5
            norm_features2 = sum([a ** 2 for a in features2]) ** 0.5

            # Compute cosine similarity
            cosine_similarity = dot_product / (norm_features1 * norm_features2)
            return cosine_similarity
        except KeyError:
            print('Book isbn not found..Check inputs')
    else:
        return None



def pearson_similarity(user_preference, id_1, id_2, similarity_type):
    '''
    Computes the Pearson correlation between the books or users
    '''
    x_y = []
    x_x = []
    y_y = []

    if similarity_type == 'user':
        feature_calculation = []
        user1_rated_books = user_preference['Ratings'][id_1] if id_1 in user_preference['Ratings'] else None
        user2_rated_books = user_preference['Ratings'][id_2] if id_2 in user_preference['Ratings'] else None

        if user1_rated_books is not None and user2_rated_books is not None:
            common_rated_books = set(user1_rated_books.keys()).intersection(user2_rated_books.keys())
            
            if common_rated_books:
                for book in common_rated_books:
                    try:
                        common_rated_books_features = user_preference['Books'][book]
                        user1_rating = int(user1_rated_books[book]['book-ratings'].replace('"', ""))
                        user2_rating = int(user2_rated_books[book]['book-ratings'].replace('"', ""))

                        for i in range(3):
                            x_y.append(common_rated_books_features[list(common_rated_books_features.keys())[i]] * common_rated_books_features[list(common_rated_books_features.keys())[i]])
                            x_x.append(common_rated_books_features[list(common_rated_books_features.keys())[i]] * common_rated_books_features[list(common_rated_books_features.keys())[i]])
                            y_y.append(common_rated_books_features[list(common_rated_books_features.keys())[i]] * common_rated_books_features[list(common_rated_books_features.keys())[i]])

                        # pearson formula 
                        numerator = (3 * (user1_rating * user2_rating)) - (sum(common_rated_books_features.values()) * (user1_rating + user2_rating))
                        denominator = (((3 * sum(x_x)) - (sum(common_rated_books_features.values()) ** 2)) * ((3 * sum(y_y)) - (sum(common_rated_books_features.values()) ** 2))) ** 0.5
                        cofficient  = numerator / denominator
                        feature_calculation.append(cofficient)
                    except KeyError:
                        continue

                if feature_calculation:
                    return sum(feature_calculation) / len(feature_calculation)

        else:
            print('User id not found..Check inputs')

    elif similarity_type == 'book':
        try:
            book1_features = [
                int(user_preference['Books'][id_1]['Book-Title']),
                int(user_preference['Books'][id_1]['Book-Author']),
                int(user_preference['Books'][id_1]['Year-Of-Publication'])
            ]
            book2_features = [
                int(user_preference['Books'][id_2]['Book-Title']),
                int(user_preference['Books'][id_2]['Book-Author']),
                int(user_preference['Books'][id_2]['Year-Of-Publication'])
            ]
            for i in range(3):
                x_y.append(book1_features[i] * book2_features[i])
                x_x.append(book1_features[i] * book1_features[i])
                y_y.append(book2_features[i] * book2_features[i])

            # pearson formula 
            numerator = (3 * sum(x_y)) - (sum(book1_features) * sum(book2_features))
            denominator = (((3 * sum(x_x)) - (sum(book1_features) ** 2)) * ((3 * sum(y_y)) - (sum(book2

