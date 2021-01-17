from bs4 import BeautifulSoup
import requests
from IPython.core.display import display, HTML

# get detailed data from individual movie webpage

def get_movie_detail(soup):
    """
    Getting detailed data from individual movie webpage
    """
    
    headers=['movie_title', 'rating', 'vote', 'certificate', 'genre', 'release_date', 'metascore', 'keywords','budget',\
            'opening_weekend_usa','gross_usa','gross_world','runtime','director','link_d','writer','link_w',\
             'star','link_s','distributor','language','country']
    
    # find movie title
    title = " ".join(soup.find('h1').text.split()[:-1]) ## problem?
    
    # find rating
    rating = float(soup.find('span',attrs={'itemprop':'ratingValue'}).text)
    
    # find vote (rating count)
    vote = int(soup.find('span',attrs={'itemprop':'ratingCount'}).text.replace(',',''))
    
    # find content rating
    certificate = soup.find('div', class_="subtext").text.split()[0]
    
    # find list of genre
    genre_list=[]
    for genres in soup.find('div', class_="subtext").find_all('a')[:-1]:
        genre_list.append(genres.text)
        
    # find release date
    date_pre = soup.find('div', class_="subtext").find_all('a')[-1].text.split('(')[0]
    date = pd.to_datetime(date_pre) ## why is it Timestamp? format ='%d-%B-%Y'
    
    # find metascorre
    if soup.find('div',class_="metacriticScore score_favorable titleReviewBarSubItem") is not None:
        meta = int(soup.find('div',class_="metacriticScore score_favorable titleReviewBarSubItem").text.strip('\n'))
    else:
        meta = np.nan
        
        
    # find plot keywords
    keyword_list=[]
    for keywords in soup.find('div', class_="article", id="titleStoryLine").\
    find('div', class_="see-more inline canwrap").find_all('a')[:-1]:
        keyword_list.append(keywords.text.strip(' '))
        
    
    
    # find budget, opening weekend USA, gross USA, cumulative worldwide gross
    # assign default value:
    budget, opening, gross_usa, gross_cw, distributor = np.nan, np.nan, np.nan, np.nan, np.nan
    for line in soup.find('div', class_="article", id="titleDetails").find_all('h4'):        
        if "Budget:" in line:
            budget = int(''.join(s for s in line.next_sibling if s.isdigit()))
        if "Opening Weekend USA:" in line:
            opening = int(''.join(s for s in line.next_sibling if s.isdigit()))
        if "Gross USA:" in line:
            gross_usa = int(''.join(s for s in line.next_sibling if s.isdigit()))
        if "Cumulative Worldwide Gross:" in line:
            gross_cw = int(''.join(s for s in line.next_sibling if s.isdigit()))
        if "Production Co:" in line:
            distributor = line.findNext().text.replace(' ','')

        
    # find runtime
    runtime = np.nan
    try:
        runtime = int(soup.find_all('time')[-1].text.strip(' min'))
    except:
        pass
        
        
        
        
    # find director
    director= np.nan
    director = soup.find('div',class_="credit_summary_item").find('a').text
    link_d = soup.find('div',class_="credit_summary_item").find('a').get('href')
    
    # find writer
    writer = np.nan
    writer_line = soup.find_all('div',class_="credit_summary_item")[1].find_all('a')
    link_w = [w.get('href') for w in writer_line]
    writer = [w.text for w in writer_line]
    if '1 more credit' in writer:
        writer.remove('1 more credit')
        link_w.pop()
        
    # find star
    star = np.nan
    star_line = soup.find_all('div',class_="credit_summary_item")[2].find_all('a')
    link_s = [s.get('href') for s in star_line]
    star = [s.text for s in star_line]
    if 'See full cast & crew' in star:
        star.remove('See full cast & crew')
        link_s.pop()
    
    
    
    # find language
    language= np.nan
    t= []
    matching = []
    for div in soup.find('div', class_="article", id="titleDetails").find_all('div'):
        t.append(div.text.replace('\n','').replace(' ',''))
    
    matching = [s for s in t if 'Language:' in s]
    language = matching[0].replace(':',' ').replace('|',' ').split(' ')[1:]
    
    
    # find country
    country= np.nan
    t= []
    matching = []
    for div in soup.find('div', class_="article", id="titleDetails").find_all('div'):
        t.append(div.text.replace('\n','').replace(' ',''))
    
    matching = [s for s in t if 'Country:' in s]
    country = matching[0].replace(':',' ').replace('|',' ').split(' ')[1:]
    
        
    movie_dict = dict(zip(headers, [title,
                                    rating,
                                    vote,
                                   certificate,
                                   genre_list,
                                   date,
                                   meta,
                                   keyword_list,
                                   budget,
                                   opening,
                                   gross_usa,
                                   gross_cw,
                                   runtime,
                                   director,
                                    link_d,
                                    writer,
                                    link_w,
                                    star,
                                    link_s,
                                   distributor,
                                   language,
                                   country]))
    
    return movie_dict