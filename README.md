# Project 2: Regression - Adapting to Succeed?
###### Weeks 2 and 3

## Backstory:

Using information we scrape from the web, build linear regression models from which we can learn about movies adapted from novels and predict whether an adaptaion will success.

### Data:

 * **acquisition**: web scraping
 * **storage**: flat files
 * **sources**:
  - movie: [IMDb](https://www.imdb.com/)
  - book: [goodreads](https://www.goodreads.com/), [fictionDB](https://www.fictiondb.com/), [Google](https://www.google.com/)


### Target variable:
Opening weekend box office (U.S.)
### Features:
<ins>*Movie*</ins>
  - MPAA rating
  - release year
  - release seaon
  - director
    - number of directed films then
    - average rating of directed films then
    - average gross then
  - cast
    - number of participated films then
    - average rating of participated films then
    - average gross then
  - writer: with original author or not
  - genre
  - distributor
  - language
  - country
  
<ins>*Book*<ins/>
  - first published year
  - years from movie release
  - page
  - author
    - number of publications then
    - visibility
  - book visibility
 
  
 

  

### Skills:

 * basics of the web (requests, HTML, CSS, JavaScript)
 * web scraping (`BeautifulSouop`, `selenium`)
 * `numpy` and `pandas`
 * `statsmodels`, `scikit-learn`


### Analysis:

 * linear regression is required, other regression methods are optional


## Deliverable/communication:

 * organized project repository
 * slide presentation
 * visual and oral communication in presentations
 * write-up of process and results


### Design:

 * iterative design process
 * "MVP"s and building outward
 * [stand-ups/scrums](https://en.wikipedia.org/wiki/Scrum_(software_development)) (1 minute progress updates to the class)


## More information:

We'll learn about web scraping using two popular tools - BeautifulSoup and Selenium. You must know the very basics of HTML. We can also evolve the way we use Jupyter notebooks; during this project, we begin to use the notebook as a development scratchpad, where we test things out through interactive scripting, but then solidify our work in python modules with reusable functions and classes.

We'll practice using linear regression. We'll have a first taste of feature selection, this time based on our intuition and some trial and error, and we'll build and refine our models.

This project will give you the freedom to challenge yourself, no matter your skill level. Find your boundaries and push them a little further. We are very excited to see what you will learn and do for Project Luther!
