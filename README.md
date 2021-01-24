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
 * `matplotlib`, `seaborn`


### Analysis:

 * Model: Linear Regression
 * Featrue engineering: `StandardScaler`,`PolynomialFeatures`,`OneHotEncoder`
 * Cross-Validation
 * Regularization: `Ridge`,`Lasso`,`RidgeCV`,`LassoCV`
 


