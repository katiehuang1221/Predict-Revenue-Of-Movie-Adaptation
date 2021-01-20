import numpy as np
import pandas as pd

def director_value(movie):
    """
    input: movie (each row in all_data_df)
    output: 
        - film_count: number of movies directed before the movie of interest
        - avg_rating: average rating of movies directed before the movie of interest
        - avg_gross: gross per movie before the movie of interest
    """
    
    movie_title = movie.movie_title
    director = movie.director
    year = movie.release_date

    headers = ['movie_title','director','film_count_d','avg_rating_d','avg_gross_d']
    
    # Assign default values
    film_count,avg_rating,avg_gross = 0, director_rating_mean, director_gross_mean
    
    doi_df = director_df[(director_df.director == director) & (director_df.year < year)]
    
    # Fill NaN with director's mean
    doi_df[['rating','gross_usa']].apply(lambda x: x.fillna(x.mean(),axis=0))
    
    # If there's still NaN, fill with all directors' mean
    doi_df[['rating']] = doi_df[['rating']].apply(lambda x: x.fillna(director_rating_mean,axis=0))
    doi_df[['gross_usa']] = doi_df[['gross_usa']].apply(lambda x: x.fillna(director_gross_mean,axis=0))
    
   
    if doi_df.shape[0] == 0:
        film_count,avg_rating,avg_gross = 0, director_rating_mean, director_gross_mean
    else:
        
    
    
        film_count = doi_df.shape[0]

        
        avg_rating = doi_df['rating'].mean()
        if avg_rating == np.nan:
            avg_rating = director_rating_mean

        try:
            avg_gross = int(doi_df['gross_usa'].mean())
        except ValueError:
            avg_gross = director_gross_mean
        
    
    director_value = dict(zip(headers, [movie_title,director,film_count,avg_rating,avg_gross]))
    
    return director_value



def actor_value(actor,year):
    """
    input: actor name and (release) year of the movie of interest
    output: 
        - film_count: number of movies the actor was in before the movie of interest
        - avg_rating: average rating of movies the actor was in before the movie of interest
        - avg_gross: gross per movie before the movie of interest
    """
    
    aoi_df = actor_df[(actor_df.actor == actor) & (actor_df.year.dt.year < year)].copy()
    
    # Fill NaN with actor's mean
    values={'rating':aoi_df.rating.mean(), 'gross_usa':aoi_df.gross_usa.mean()}
    aoi_df.fillna(value=values,inplace=True)
    
    # If there's still NaN, fill with all actors' mean
    values={'rating':actor_rating_mean, 'gross_usa':actor_gross_mean}
    aoi_df.fillna(value=values,inplace=True)
        
    
    # If there's no movie prior to movie of interest  
    if aoi_df.shape[0] == 0:
        film_count,avg_rating,avg_gross = 0, actor_rating_mean, actor_gross_mean
        
    else:
        
        film_count = aoi_df.shape[0]
        
        avg_rating = aoi_df['rating'].mean()
        avg_gross = aoi_df['gross_usa'].mean()

        
    
    actor_value = [film_count, avg_rating, avg_gross]
    
    print(actor,actor_value)
    
    return actor_value,aoi_df




def get_cast(movie):
    """
    input: movie (each row in all_data_df)
    output: 
        - film_count: number of movies directed before the movie of interest
        - avg_rating: average rating of movies directed before the movie of interest
        - avg_gross: gross per movie before the movie of interest
    """
    
    movie_title = movie.movie_title
    year = movie.release_year
    actors = movie.actor
    lead = actors[0]
    
    film_counts = []
    ratings = []
    grosses = []
    
    for actor in actors:
        result = actor_value(actor,year)
        film_counts.append(result[0])
        ratings.append(result[1])
        grosses.append(result[2])
        
    avg_film_count = np.mean(film_counts)
    avg_rating = np.mean(ratings)
    avg_gross = np.mean(grosses)    
    
    
    lead_result = actor_value(lead,year)
    

    headers = ['movie_title','cast','avg_film_count_c','avg_rating_c','avg_gross_c',\
              'avg_film_count_l','avg_rating_l','avg_gross_l']

        
    
    cast_info = dict(zip(headers, [movie_title,actors,avg_film_count,avg_rating,avg_gross,\
                                  lead_result[0],lead_result[1],lead_result[2]]))
    
    return cast_info