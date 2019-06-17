print(

"""
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

### Examples of queries ###

# This example returns the most recent number of patent applications per country
Example1 = GLquery("query1")


# This example will not run because "budget" is lower necessary memory to run this query
Example2 = GLquery("query1", budget = 1)


# This example will demand you to answer any variation of 'yes' or 'no' in the console
Example3 = GLquery(ask_before_running = True) 


# This example returns a dataset named query1.csv and a plot named query1.pdf in your destination folder
Example4 = GLquery("query1", output_to_csv = True, plot = True) 


# This query returns the number of published patents for each year between 1890 and 1930 per country          
Example5 = GLquery("query2", start_year = "1890", end_year = "1930")


# This query returns the number of patents China published for each year between 1870 and 2010
Example6 = GLquery("query3", start_year = "1970", end_year = "2010", country = "CN")


# This query returns which patents Brazil published between 1970 and 1990
Example7 = GLquery("query4", start_year = "1960", end_year = "1990", country = "BR", kind_code = "B1")


# This query returns the most common patenting technology areas per year 
Example8 = GLquery("query5")


# This query returns the most common patenting technology areas in Great Britain for each year between 1790 and 1900
Example9 = GLquery("query6", start_year = "1790", end_year = "1900", country = "GB")


# This query returns inventors with over 1000 inventions by country of origin
Example10 = GLquery("query7", min_count = "1000")


# This query returns how many patents, which firms and what countries are interested in technology Y02A ("TECHNOLOGIES FOR ADAPTATION TO CLIMATE CHANGE") between years 1990 and 2019
Example11 = GLquery("query8", start_year = "1990", end_year = "2019", cpc_code = "Y02A")


# This query returns which firms and what technologies Amazon is citing in their patents
Example12 = GLquery("query9", assignee = "AMAZON TECH INC")


# This query returns patent applications with keyword "internet of things" in China
Example13 = GLquery("query10", country = "CN", keyword = "internet of things")

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
""")