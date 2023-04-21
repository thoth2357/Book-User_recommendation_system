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

def cosine_similarity(user_preference, id_1, id_2, similarity_type):
    '''
    Computes the cosine similarity between books or users. Cosine similarity is commonly used in document similarity 
    and text mining.
    '''
    if similarity_type == 'user':
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

    elif similarity_type == 'book':
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
    """
    Computes the Pearson correlation between the books or users.
    """
    x_y = []
    x_x = []
    y_y = []
    
    if similarity_type == 'user':
        feature_calculation = []
        user1_features, user2_features = helper_function(user_preference, id_1, id_2)
        
        if user1_features is not None and user2_features is not None:
            for key in user1_features:
                feature1 = user1_features.get(key)
                feature2 = user2_features.get(key)
                
                for i, j in enumerate(feature1):
                    x_y.append(feature1[i] * feature2[i])
                    x_x.append(feature1[i] * feature1[i])
                    y_y.append(feature2[i] * feature2[i])

                numerator = (len(feature1) * sum(x_y)) - sum(feature1) * sum(feature2)
                denominator = (((len(feature1) * sum(x_x)) - (sum(feature1) ** 2)) * ((len(feature1) * sum(y_y)) - (sum(feature2) ** 2))) ** 0.5
                coefficient = numerator / denominator
                feature_calculation.append(coefficient)
                
            return sum(feature_calculation) / len(feature_calculation)
        
        else:
            print('No common books found between the users')
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
            for i, j in enumerate(features1):
                x_y.append(features1[i] * features2[i])
                x_x.append(features1[i] * features1[i])
                y_y.append(features2[i] * features2[i])

            numerator = (len(features1) * sum(x_y)) - sum(features1) * sum(features2)
            denominator = (((len(features1) * sum(x_x)) - (sum(features1) ** 2)) * ((len(features1) * sum(y_y)) - (sum(features2) ** 2))) ** 0.5
            coefficient = numerator / denominator
            return coefficient
        
        except KeyError:
            print('Book ISBN not found. Check inputs.')
            return None
    else:
        print('Invalid type of similarity. Please enter either "user" or "book".')
        return None

def jaccard_similarity(user_preference, id_1, id_2, similarity_type):
    """
    Compute the Jaccard similarity between two sets of data. The higher the number, the more similar the two sets of data.
    """
    if similarity_type == 'user':
        feature_calculation = []
        try:
            user1_rated_books = user_preference['Ratings'][id_1]
            user2_rated_books = user_preference['Ratings'][id_2]
            common_rated_books = set(user1_rated_books.keys()).intersection(user2_rated_books.keys())
            if common_rated_books:
                common_rated_books_features = {}
                book_na = []
                for book in common_rated_books:
                    try:
                        common_rated_books_features[book] = user_preference['Books'][book]
                    except KeyError:
                        book_na.append(book)
                for book in common_rated_books:
                    if book not in book_na:
                        user1_features = [
                            int(common_rated_books_features[book]['Book-Title']),
                            int(common_rated_books_features[book]['Book-Author']),
                            int(common_rated_books_features[book]['Year-Of-Publication']),
                            int(user1_rated_books[book]['book-ratings'].replace('"', ""))
                        ]
                        user2_features = [
                            int(common_rated_books_features[book]['Book-Title']),
                            int(common_rated_books_features[book]['Book-Author']),
                            int(common_rated_books_features[book]['Year-Of-Publication']),
                            int(user2_rated_books[book]['book-ratings'].replace('"', ""))
                        ]
                        intersections = len(list(set(user1_features).intersection(user2_features)))
                        union = (len(user1_features) + len(user2_features)) - intersections
                        result = float(intersections) / union
                        feature_calculation.append(result)
                if len(feature_calculation) == 0:
                    print('No common books found between the users')
                    return None
                return sum(feature_calculation) / len(feature_calculation)
            else:
                print('No common books found between the users')
                return None
        except KeyError:
            print('Wrong user id..Check inputs')
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
            intersections = len(list(set(features1).intersection(features2)))
            union = (len(features1) + len(features2)) - intersections
            return float(intersections) / union
        except KeyError:
            print('Wrong book isbn..Check inputs')

def manhattan_similarity(user_preference, id_1, id_2, feature_type):
    """
    Measures the Manhattan similarity between two users or two books.
    """
    if feature_type == "user":
        # Get features for the two users
        user1_features, user2_features = helper_function(user_preference, id_1, id_2)
        if user1_features is None or user2_features is None:
            return None
        # Calculate the Manhattan distance between the two users
        distance = sum(abs(a - b) for _, (a, _, _, b) in user1_features.items() & user2_features.items())
        return distance / len(user1_features)
    
    elif feature_type == "book":
        # Get features for the two books
        try:
            feature1 = [
                int(user_preference["Books"][id_1]["Book-Title"]),
                int(user_preference["Books"][id_1]["Book-Author"]),
                int(user_preference["Books"][id_1]["Year-Of-Publication"]),
            ]
            feature2 = [
                int(user_preference["Books"][id_2]["Book-Title"]),
                int(user_preference["Books"][id_2]["Book-Author"]),
                int(user_preference["Books"][id_2]["Year-Of-Publication"]),
            ]
            # Calculate the Manhattan distance between the two books
            distance = sum(abs(a - b) for a, b in zip(feature1, feature2))
            return distance
        except KeyError:
            print("Book ID not found. Check inputs.")
            return None
    else:
        print("Invalid feature type. Choose either 'user' or 'book'.")
        return None
    

def get_n_most_similar_items(user_preference, id_1, n, item_type, similarity_measure):
    """
    Returns the n most similar items to the given item (book or user).
    """
    if item_type == 'user':
        try:
            similarity_scores = []
            for user_id in user_preference['Ratings']:
                if user_id != id_1:
                    similarity = similarity_measure(user_preference, id_1, user_id, item_type)
                    if similarity is not None:
                        similarity_scores.append((user_id, similarity))
            similarity_scores.sort(key=lambda x: x[1], reverse=True)
            return similarity_scores[:n]
        except KeyError:
            print('User ID not found in user preference')
    elif item_type == 'book':
        try:
            similarity_scores = []
            for book_id in user_preference['Books']:
                if book_id != id_1:
                    similarity = similarity_measure(user_preference, id_1, book_id, item_type)
                    if similarity is not None:
                        similarity_scores.append((book_id, similarity))
            similarity_scores.sort(key=lambda x: x[1], reverse=True)
            return similarity_scores[:n]
        except KeyError:
            print('Book ISBN not found in user preference')

