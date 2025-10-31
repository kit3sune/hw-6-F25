
# Your name: 
# Your student id:
# Your email:
# Who or what you worked with on this homework (including generative AI like ChatGPT):
# If you worked with generative AI also add a statement for how you used it.  
# e.g.: 
# Asked Chatgpt hints for debugging and suggesting the general structure of the code


import requests
import json
import unittest
import os

# TO DO: 
# assign this variable to your API key
# if you are doing the extra credit, assign API_KEY to the return value of your get_api_key function
API_KEY = ''

def load_json(filename):
    '''
    opens file file, loads content as json object

    ARGUMENTS: 
        filename: name of file to be opened

    RETURNS: 
        json dictionary OR an empty dict if the file could not be opened 
    '''
    pass


def create_cache(dict, filename):
    '''
    Encodes dictonary into JSON format and writes
    the JSON to filename to save the search results

    ARGUMENTS: 
        filename: the name of the file to write a cache to
        dict: cache dictionary

    RETURNS: 
        None
    '''
    pass


def search_movie(movie):
    '''
    creates API request
    ARGUMENTS: 
        movie: title of the movie you're searching for 

    RETURNS: 
        tuple with the response text and url OR None if the 
        request was unsuccessful
    '''
    pass

    

def update_cache(movies, cache_file):
    '''
    Iterates through a list of movies, adds their data to the cache.
    checks if a movie already exists in the cache before making an API request.
    only counts successful new API requests in the success_count.

    ARGUMENTS: 
        movies: a list of movies to get data for 
        cache_file: the file that has cached data 

    RETURNS: 
        A string saying the percentage of movies we successfully got data for 
    '''
    pass
    
    


def get_highest_box_office_by_year(year, cache_file): 
    '''
    gets the movie with the highest box office total for a given year

    ARGUMENTS: 
        year: the year we want to find the highest grossing film for 
        cache_file: the file that has cached data 

    RETURNS:
        a tuple with the title and box office amount
    '''
    pass

def get_genres_above_cutoff(cutoff, cache_file):
    '''
    finds the most common movie genres

    ARGUMENTS: 
        cutoff: the cutoff for how many films a genre must 
                be associated with
        cache_file: the file that has cached data 

    RETURNS:
        a list of tuples with the the genres and counts
    '''
    pass

# EXTRA CREDIT
def get_api_key(filename):
    '''
    loads in API key from file 

    ARGUMENTS:  
        file: file that contains your API key
    
    RETURNS:
        your API key
    '''
    pass

def recommend_similar_movies(movie_title, cache_file):
    '''
    Recommends movies that share at least one genre with the given movie

    ARGUMENTS: 
        movie_title: the title of the movie we're looking for recommendations for
        cache_file: the file that has cached data 

    RETURNS:
        EITHER a list of movie titles that share at least one genre with movie_title
        OR an error message if the movie can't be found, has no genre information, or no similar movies
    '''
    pass


class TestHomework6(unittest.TestCase):
    def setUp(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.filename = dir_path + '/' + "cache.json"

        with open('movies.txt', 'r') as f: 
            movies = f.readlines()
            
        for i in range(len(movies)): 
            movies[i] = movies[i].strip()
        self.movies = movies

        # NOTE: if you already have a cache file, setUp will open it
        # otherwise, it will cache all movies to use that in the test cases 
        if not os.path.isfile(self.filename):
            self.cache = update_cache(self.movies, 'cache.json')
        else:
            self.cache = load_json(self.filename)

        self.url = "http://www.omdbapi.com/"


    def test_load_and_create_cache(self):
        test_dict = {'test': [1, 2, 3]}
        create_cache(test_dict, 'test_cache_load_json.json')

        test_dict_cache = load_json('test_cache_load_json.json')
        self.assertEqual(test_dict_cache, test_dict)
        os.remove('test_cache_load_json.json')

        test_dict_2 = {'test_2': {'test_3': ['a', 'b', 'c']}}
        create_cache(test_dict_2, 'test_cache_load_json_2.json')
        
        test_dict_2_cache = load_json('test_cache_load_json_2.json')
        self.assertEqual(test_dict_2_cache, test_dict_2)
        os.remove('test_cache_load_json_2.json')


    def test_search_movie(self):
        # testing valid movies
        for movie in ['Mean Girls', 'Pulp Fiction', 'Forrest Gump']:
            movie_data = search_movie(movie)
            movie = movie.replace(" ", "+")
            self.assertEqual(type(movie_data[0]), dict)
            self.assertTrue(movie in movie_data[1])

        # testing invalid movie 
        invalid_movie_data = search_movie('fake movie 123')
        self.assertEqual(invalid_movie_data, None)


    def test_update_cache(self):
        test_movies = ['Mean Girls', 'Pulp Fiction', 'Forrest Gump']
        test_resp = update_cache(test_movies, 'test_cache_movies.json')
        self.assertTrue(test_resp == "Cached data for 100% of movies" or test_resp == "Cached data for 100.0% of movies")
        test_cache = load_json('test_cache_movies.json')
        self.assertIsInstance(test_cache, dict)
        self.assertEqual(len(list(test_cache.keys())), 3)

        for _, data in test_cache.items():
            if data['Ratings']:
                self.assertEqual(type(data['Ratings']), list)
                self.assertEqual(type(data['Ratings'][0]), dict)

        # checking it won't cache duplicates
        test_resp_2 = update_cache(test_movies, 'test_cache_movies.json')
        self.assertTrue(test_resp_2 == "Cached data for 0% of movies" or test_resp_2 == "Cached data for 0.0% of movies")        
        self.assertEqual(len(list(test_cache.keys())), 3)
        os.remove('test_cache_movies.json')


    def test_get_highest_box_office_per_year(self):
        test_1 = get_highest_box_office_by_year(2005, 'cache.json')
        self.assertEqual(test_1, ("Harry Potter and the Goblet of Fire", 290469928))
        test_2 = get_highest_box_office_by_year(2019, 'cache.json')
        self.assertEqual(test_2, ('Little Women', 108101214))
        test_3 = get_highest_box_office_by_year(2012, 'cache.json')
        self.assertEqual(test_3, ('The Avengers', 623357910))
        test_4 = get_highest_box_office_by_year(1990, 'cache.json')
        self.assertEqual(test_4, 'No films found')


    def test_get_genres_above_cutoff(self):
        test_1 = get_genres_above_cutoff(16, 'cache.json')
        self.assertEqual(len(test_1), 1)
        test_2 = get_genres_above_cutoff(5, 'cache.json') 
        self.assertEqual(len(test_2), 6)
        test_3 =  get_genres_above_cutoff(0, 'cache.json')
        self.assertEqual(len(test_3), 17)
        test_4 = get_genres_above_cutoff(1, 'cache.json')
        self.assertEqual(len(test_4), len(test_3))
        self.assertEqual(test_4['Drama'], 16)
        self.assertEqual(test_4['Short'], 1)


    # UNCOMMENT TO TEST EXTRA CREDIT
    '''
    
    def test_get_api_key(self):                     
        hidden_key = get_api_key('api_key.txt')
        self.assertEqual(API_KEY, hidden_key)

    def test_recommend_similar_movies(self):
        # Updated test case to use a movie that's definitely in the cache
        test_1 = recommend_similar_movies("Titanic", 'cache.json')
        self.assertTrue(isinstance(test_1, list))
        self.assertTrue(len(test_1) > 0)  # There should be recommendations for Titanic
        self.assertEqual(test_1, ['Little Women', 'Top Gun: Maverick', 'La La Land', 'Whiplash',
                                   '12 Years a Slave', 'Life of Pi', 'The Help', 'Killers of the Flower Moon', 
                                   'Oppenheimer', 'The Lord of the Rings: The Fellowship of the Ring', 'Braveheart', 
                                   'Clueless', '10 Things I Hate About You', 'Gone with the Wind', 'Casablanca', 'Parasite'])
        
        test_2 = recommend_similar_movies("NonexistentMovie", 'cache.json')
        self.assertEqual(test_2, "'NonexistentMovie' is not in the cache.")
    '''
    
    
def main():
    '''
    Note that your cache file will be called 
    cache.json and will be created in your current directory

    Make sure you are in the directory you want to be work in 
    prior to running
    '''
    #######################################
    # DO NOT CHANGE THIS 
    # this code loads in the list of movies and 
    # removes whitespace for you!
    with open('movies.txt', 'r') as f: 
        movies = f.readlines()
        
    for i in range(len(movies)): 
        movies[i] = movies[i].strip()
    #resp = cache_all_movies(movies, 'cache.json')
        
    # DO NOT CHANGE THIS 
    #######################################


if __name__ == "__main__":
    main()
    unittest.main(verbosity = 2)