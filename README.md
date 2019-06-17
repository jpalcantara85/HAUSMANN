## 1. INTRODUCTION

The **GROWTH LAB QUERY** (GLquery) is a local script that runs cloud-based queries on Google BigQuery's environment.

Instead of individually running e.g. 10 separate queries there, you can use a one-line command here - all you need is to change the arguments of the function.


## 2. INSTALLATION

Make sure the packages below are properly installed:

- HAUSMANN: 
```javascript
pip install -e git+https://github.com/jpalcantara85/HAUSMANN#egg=HAUSMANN
```

- bq_helper: 
```javascript
pip install -e git+https://github.com/SohierDane/BigQuery_Helper#egg=bq_helper
```


## 3. USAGE

After installing the necessary packages, type: 
```python
from HAUSMANN import GLquery, GLquery_examples 
```

Then, to learn more about **GLquery** type: 
```python
GLquery_examples()
```


## 4. FUNCTION PARAMETERS

**GLquery** takes the following arguments:
        
- *query (string): choose among one of the options in the next section (see below) (default is "query1")*
        
- *country (string) = format "LL" (default is "US")*
    
- *start_year (string) = format "YYYY" (default is "1790")*

- *end_year (string) = format "YYYY" (default is "2019")*
     
- *min_count (string) = minimum threshold (default is "100")*

- *kind_code (string) = format "LN", see kind codes here: https://www.cas.org/support/documentation/references/patkind (default is "B2")*

- *cpc_code (string) = formant "LNNL", see CPC codes here: https://www.uspto.gov/web/patents/classification/cpc/html/cpc.html (default is "A63F")*
   
- *assignee (string) = any format (case sensitive) (default is "President and Fellows of Harvard College")*

- *keyword (string) = any format (case sensitive) (default is "internet of things")*
    
- *budget (number) = any number (default is 1.000 GB) (queries above value 'budget' will not run; queries below 'budget' will use only the minimum amount of memory necessary to run the query, not the full value of 'budget')*
      
- *output_to_csv (True or False) = output results as .csv file to directory defined at 'my_output_path' (default is False)*
   
- *plot (True of False) = plot results as .pdf file to directory defined at 'my_output_path' (default is False) (implemented for queries 1, 2, 3, 10)*
   
- *ask_before_running (True or False) = given a query size (in GB), asks user input before running the query (default is False)*

    
## 5. QUERIES

As of June/2019, **GLquery** can perform the following queries:
        
- *query1: Number of patent applications by country (takes no inputs)*
        
- *query2: Number of patents published between years X and Y by country (necessary arguments: start_year and end_year)*
      
- *query3: Number of patents published to country Z between years X and Y (necessary arguments: start_year, end_year and country)*
            
- *query4: Which patents country Z published between years X and Y? (necessary arguments: start_year, end_year, country, kind_code)*
            
- *query5: Most common patenting technology areas by year (takes no inputs)*
            
- *query6: Most common patenting technology areas in country Z between years X and Y (necessary arguments: start_year, end_year and country)*
            
- *query7: Inventors with over N patents by country (necessary arguments: min_count)*
            
- *query8: Patent landscaping of technology T between years X and Y" (necessary arguments: start_year, end_year, min_count and cpc_code) (this query returns patents, firms and countries associated with technology T)*
            
- *query9: Which firms is assignee A citing in their patents? (necessary arguments: assignee)*
    
- *query10: Number of patent applications with keyword K in country Z (necessary arguments: country and keyword)*


## 6. OBSERVATIONS:
    
- If you haven't already, you must create a variable named 'my_key_path' to access Google's environment (.json file): 
```python
my_key_path = "/users/NAME_OF_YOUR_FOLDER_HERE/NAME_OF_YOUR_KEY_HERE.json"
```

- If you haven't already, you must create a variable named 'my_output_path' to define your output folder (directory where outputs will be saved): 
```python 
my_output_path = "/Users/NAME_OF_YOUR_FOLDER_HERE"
```


## 7. IMPORTANT CONCEPTS: (under permanent construction)

- *Publication date x filing date x grant date*: patent documents are published (publication date) by patent offices usually 18 months after the date on which a patent application was first filed (filing data) or once a patent has been granted (grant date) for the invention claimed by the patent applicant. Queries in this script always take as reference publication date.
