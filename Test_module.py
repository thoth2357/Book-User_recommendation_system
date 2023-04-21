from ass_1.load_dataset_module import User_Preference
from similarity_module import *

user_preferences = User_Preference()

# result = euclidean_similarity(user_preferences, '36973', '276688', 'user')
# result2 = euclidean_similarity(user_preferences, '0739307312', '0739307312', 'book')

result3 = cosine_distance(user_preferences, '36973', '276688')
result4 = cosine_distance(user_preferences, '0739307312', '0739307312',)
result_t =cosine_distance(user_preferences, '6889', '276813',)

result5 = pearson_distance(user_preferences, '36973', '276688',)
result6 = pearson_distance(user_preferences, '0739307312', '0739307312',)

# # result7 = jaccard_similarity(user_preferences, '36973', '276688',)
# # result8 = jaccard_similarity(user_preferences, '0739307312', '0739307312',)

result9 = manhattan_distance(user_preferences, '36973', '276688',)
result0 = manhattan_distance(user_preferences, '0739307312', '0739307312',)

result13 = minkowski_distance(user_preferences, '36973', '276688',)
result14 = minkowski_distance(user_preferences, '0739307312', '0739307312',)

result15 = mahalanobis_distance(user_preferences, '36973', '276688',)
result16 = mahalanobis_distance(user_preferences, '0739307312', '0739307312',)

# result11 = n_most_similiar_items(user_preferences, '0739307312', 5,, similarity_measure=cosine_similarity)
# result12 = n_most_similiar_items(user_preferences, '276813', 5,'user', similarity_measure=cosine_similarity)

# print(result, result2)
print(result_t)
print(result3, result4)
print(result5, result6)
# # print(result7, result8)
print(result9, result0)
print(result13, result14)
print(result15, result16)
# print(result11)
# print(result12)


# 1552041778
# 1551665107

#36938
#13273