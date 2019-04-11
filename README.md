# Recommendation_atSparseDomain
Recommendation at sparse domain using transfer learning from a related domain
The set of python program manipulates the tourism data crawled from Tripadvisor.com to make cross domain tourist attraction recommendation.

* attr_latent.py - Reads the crawled tourist attraction details and creates unique records for tourist attraction.
* res_latent.py - Reads the crawled restaurant details and creates unique records for restaurants.
* user_latent.py - Reads the crawled user details and creates unique records for users.
* split.py - Creates the test and train data for recommendation of tourist attaction.
* test_code.py - Performs unsupervised transfer learning technique for getting user's restaurant affinity for recommendation of tourist attraction.
