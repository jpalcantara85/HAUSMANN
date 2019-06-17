##############################################################################################################################################################

# Insert here your key to access Google's environment (.json file)"

my_key_path = "/Users/jpalcantara/Desktop/Growth Lab/Patents/My Project 1-1e3a04e30599.json"

# Define here your output folder (directory where outputs will be saved):

my_output_path = "/Users/jpalcantara/Desktop/Growth Lab/Patents/"

##############################################################################################################################################################

def GLquery(query = "query1", 
            country = "US", 
            start_year = "1790", 
            end_year = "2019", 
            min_count = "100", 
            kind_code = "B2", 
            cpc_code = "A63F", 
            assignee = "President and Fellows of Harvard College", 
            keyword = "internet of things",
            budget = 1000,
            output_to_csv = False,
            plot = False,
            ask_before_running = False):   

    
    import bq_helper
    from bq_helper import BigQueryHelper
    import os
    import re
    from pathlib import Path
    import sys
    import seaborn as sns        
    import matplotlib.pyplot as plt
    from matplotlib.pyplot import figure

    
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = my_key_path
    
    
    patents = bq_helper.BigQueryHelper(active_project = "patents-public-data", dataset_name = "patents")
    bq_assistant = BigQueryHelper("patents-public-data", "patents")
    
    
    temp_path = Path(my_output_path)
    
    print ("Country selected: {}.".format(country))
    print ("Period selected: from {} to {}.".format(start_year, end_year))
    
    
    def replace(string, substitutions):
        substrings = sorted(substitutions, key = len, reverse = True)
        regex = re.compile('|'.join(map(re.escape, substrings)))
        return regex.sub(lambda match: substitutions[match.group(0)], string)
    
    
    def query_selector(query):
        switcher = {
            "query1": """
            -- "Number of publications by country"
            
            SELECT COUNT(*) AS cnt, country_code
            FROM (
                SELECT ANY_VALUE(country_code) AS country_code
                FROM `patents-public-data.patents.publications`
                GROUP BY application_number)
            GROUP BY country_code
            ORDER BY cnt DESC
            """,
            
            
            "query2": replace("""
            -- "Number of patents published between years X and Y by country"
            
            SELECT country_code,
            COUNT(DISTINCT publication_number) AS publications
            FROM `patents-public-data.patents.publications`
            WHERE publication_date >= XXXX0000 
            AND publication_date < YYYY0000
            AND application_kind = 'A'
            GROUP BY country_code
            ORDER BY publications DESC
            """, {"XXXX": start_year, "YYYY": end_year}),
           
            
            "query3": replace("""
            -- "Number of patents granted to country Z between years X and Y"
            
            SELECT FLOOR(grant_date/10000) as datum,
            COUNT(DISTINCT publication_number) as publications
            FROM `patents-public-data.patents.publications`
            WHERE country_code = 'ZZZZ'
            AND publication_date >= XXXX0000
            AND publication_date <= YYYY0000
            AND application_kind = 'A'
            GROUP BY datum, application_kind
            ORDER BY application_kind, datum
            """, {"XXXX": start_year, "YYYY": end_year, "ZZZZ": country}),


            "query4": replace("""
            -- "Which patents country Z published between years X and Y"
            
            SELECT publication_number
            FROM `patents-public-data.patents.publications`
            WHERE country_code = 'ZZZZ'
            AND publication_date >= XXXX0000
            AND publication_date <= YYYY0000
            AND application_kind = 'A'
            AND kind_code = 'BBBB'
            """, {"XXXX": start_year, "YYYY": end_year, "ZZZZ": country, "BBBB": kind_code}),
           
            
            "query5": """
            -- "Most common patenting technology areas by year"
            
            CREATE TEMPORARY FUNCTION highest_moving_avg(yearcnt ARRAY<STRUCT<filing_year INT64, cnt INT64>>)
            RETURNS STRUCT<filing_year INT64, avg INT64>
            LANGUAGE js AS \"""
            let avg = 0;
            let a = 1.0;
            let highest = {filing_year: -1, avg: -1};
            for (let x of yearcnt) {
                    avg = a * x.cnt + (1 - a) * avg;
                    if (avg > highest.avg) {
                            highest = {filing_year: x.filing_year, avg: avg};}
                    }
                    return highest;
                \""";
                
            WITH patent_cpcs AS (
                SELECT cd.parents,
                CAST(FLOOR(filing_date/10000) AS INT64) AS filing_year
                FROM (
                    SELECT ANY_VALUE(cpc) AS cpc, ANY_VALUE(filing_date) AS filing_date
                    FROM `patents-public-data.patents.publications`
                    WHERE application_number != ""
                    GROUP BY application_number), UNNEST(cpc) AS cpcs
                JOIN `patents-public-data.cpc.definition` cd ON cd.symbol = cpcs.code
                WHERE cpcs.first = TRUE AND filing_date > 0)

            SELECT c.title_full, cpc_group, best_year.*
            FROM (
                SELECT cpc_group, highest_moving_avg(ARRAY_AGG(STRUCT<filing_year INT64, cnt INT64>(filing_year, cnt) ORDER BY filing_year ASC)) AS best_year
                FROM (
                    SELECT cpc_group, filing_year, COUNT(*) AS cnt
                    FROM (
                        SELECT cpc_parent AS cpc_group, filing_year
                        FROM patent_cpcs, UNNEST(parents) AS cpc_parent)
                    GROUP BY cpc_group, filing_year
                    ORDER BY filing_year DESC, cnt DESC)
                GROUP BY cpc_group)
            JOIN `patents-public-data.cpc.definition` c ON cpc_group = c.symbol
            WHERE c.level = 5
            ORDER BY best_year.filing_year ASC;
            """,


            "query6": replace("""
            -- "Most common patenting technology areas in country Z between years X and Y"
            
            CREATE TEMPORARY FUNCTION highest_moving_avg(yearcnt ARRAY<STRUCT<filing_year INT64, cnt INT64>>)
            RETURNS STRUCT<filing_year INT64, avg INT64>
            LANGUAGE js AS \"""
            let avg = 0;
            let a = 1.0;
            let highest = {filing_year: -1, avg: -1};
            for (let x of yearcnt) {
                    avg = a * x.cnt + (1 - a) * avg;
                    if (avg > highest.avg) {
                            highest = {filing_year: x.filing_year, avg: avg};}
                    }
                    return highest;
                \""";
                
            WITH patent_cpcs AS (
                SELECT cd.parents,
                CAST(FLOOR(filing_date/10000) AS INT64) AS filing_year
                FROM (
                    SELECT ANY_VALUE(cpc) AS cpc, ANY_VALUE(filing_date) AS filing_date
                    FROM `patents-public-data.patents.publications`
                    WHERE application_number != ""
                    AND country_code = 'ZZZZ'
                    AND grant_date >= XXXX0000
                    AND grant_date <= YYYY0000
                    GROUP BY application_number), UNNEST(cpc) AS cpcs
                JOIN `patents-public-data.cpc.definition` cd ON cd.symbol = cpcs.code
                WHERE cpcs.first = TRUE AND filing_date > 0)

            SELECT c.title_full, cpc_group, best_year.*
            FROM (
                SELECT cpc_group, highest_moving_avg(ARRAY_AGG(STRUCT<filing_year INT64, cnt INT64>(filing_year, cnt) ORDER BY filing_year ASC)) AS best_year
                FROM (
                    SELECT cpc_group, filing_year, COUNT(*) AS cnt
                    FROM (
                        SELECT cpc_parent AS cpc_group, filing_year
                        FROM patent_cpcs, UNNEST(parents) AS cpc_parent)
                    GROUP BY cpc_group, filing_year
                    ORDER BY filing_year DESC, cnt DESC)
                GROUP BY cpc_group)
            JOIN `patents-public-data.cpc.definition` c ON cpc_group = c.symbol
            WHERE c.level = 5 
            ORDER BY best_year.filing_year ASC;
            """, {"XXXX": start_year, "YYYY": end_year, "ZZZZ": country}),


            "query7": replace("""
            -- "Inventors with over N patents by country"
            
            WITH temp1 AS (
            SELECT DISTINCT PUB.country_code,
            PUB.application_number AS patent_number, inventor_name
            FROM `patents-public-data.patents.publications` PUB
            CROSS JOIN
            UNNEST(PUB.inventor) AS inventor_name
            WHERE PUB.grant_date >= 1790000
            AND PUB.country_code IS NOT NULL
            AND PUB.application_number IS NOT NULL
            AND PUB.inventor IS NOT NULL)
            SELECT * FROM (
            SELECT temp1.country_code AS country, temp1.inventor_name AS inventor,
            COUNT(temp1.patent_number) AS count_of_patents
            FROM temp1
            GROUP BY temp1.country_code, temp1.inventor_name)
            WHERE count_of_patents >= NNNN
            """, {"NNNN": min_count}),


            "query8": replace("""
            -- "Patent landscaping of technology T between years X and Y" 
            
            SELECT SUM(year_cnt) AS total_count, assignee_name,
            ARRAY_AGG(STRUCT<cnt INT64, filing_year INT64, countries STRING>(year_cnt, filing_year, countries) ORDER BY year_cnt DESC LIMIT 1)[SAFE_ORDINAL(1)] AS Number_of_patents_under_this_CPC_code_Peak_year_Top_countries
            FROM (
                SELECT SUM(year_country_cnt) AS year_cnt, assignee_name, filing_year, STRING_AGG(country_code ORDER BY year_country_cnt DESC LIMIT 5) AS countries
                FROM (
                    SELECT COUNT(*) AS year_country_cnt, a.name AS assignee_name, CAST(FLOOR(filing_date/10000) AS INT64) AS filing_year, apps.country_code
                    FROM (
                        SELECT ANY_VALUE(assignee_harmonized) AS assignee_harmonized, ANY_VALUE(filing_date) AS filing_date, ANY_VALUE(country_code) AS country_code
                        FROM `patents-public-data.patents.publications` AS pubs
                        WHERE (SELECT MAX(TRUE) FROM UNNEST(pubs.cpc) AS c WHERE REGEXP_CONTAINS(c.code, "TTTT"))
                        AND publication_date >= XXXX0000
                        AND publication_date <= YYYY0000
                        GROUP BY application_number) AS apps, UNNEST(assignee_harmonized) AS a
                    WHERE filing_date > 0
                    GROUP BY a.name, filing_year, country_code)
                GROUP BY assignee_name, filing_year)
            GROUP BY assignee_name
            ORDER BY total_count DESC
            LIMIT NNNN
            """, {"XXXX": start_year, "YYYY": end_year, "NNNN": min_count, "TTTT": cpc_code}),

            "query9": replace("""
            -- "Which firms is assignee A citing in their patents?"
            
            SELECT citing_assignee,
            COUNT(*) AS num_cites, citing_cpc_subclass, cpcdef.title_full AS citing_cpc_title
            FROM (
                SELECT pubs.publication_number AS citing_publication_number, cite.publication_number AS cited_publication_number, citing_assignee_s.name AS citing_assignee, SUBSTR(cpcs.code, 0, 4) AS citing_cpc_subclass
                FROM `patents-public-data.patents.publications` AS pubs, UNNEST(citation) AS cite, UNNEST(assignee_harmonized) AS citing_assignee_s, UNNEST(cpc) AS cpcs
                WHERE cpcs.first = TRUE) AS pubs
                JOIN (
                    SELECT publication_number AS cited_publication_number, cited_assignee_s.name AS cited_assignee
                    FROM `patents-public-data.patents.publications`, UNNEST(assignee_harmonized) AS cited_assignee_s) AS refs ON pubs.cited_publication_number = refs.cited_publication_number
                JOIN `patents-public-data.cpc.definition` AS cpcdef ON cpcdef.symbol = citing_cpc_subclass
                WHERE cited_assignee = "AAAA" AND citing_assignee != "AAAA"
                GROUP BY cited_assignee, citing_assignee, citing_cpc_subclass, cpcdef.title_full
                ORDER BY num_cites DESC
                """, {"AAAA": assignee}),


            "query10": replace("""
            --  Number of patent applications with keyword K in country Z             
            
            WITH Patent_Matches AS (
                SELECT PARSE_DATE('%Y%m%d', SAFE_CAST(ANY_VALUE(patentsdb.filing_date) AS STRING)) AS Patent_Filing_Date, patentsdb.application_number AS Patent_Application_Number,
                ANY_VALUE(abstract_info.text) AS Patent_Title,
                ANY_VALUE(abstract_info.language) AS Patent_Title_Language
                FROM `patents-public-data.patents.publications` AS patentsdb,
                UNNEST(abstract_localized) AS abstract_info
                WHERE
                LOWER(abstract_info.text) LIKE '%KKKK%'
                AND patentsdb.country_code = 'ZZZZ'
                GROUP BY Patent_Application_Number),
            Date_Series_Table AS (
                SELECT day, 0 AS Number_of_Patents
                FROM UNNEST (GENERATE_DATE_ARRAY(
                    (SELECT MIN(Patent_Filing_Date) FROM Patent_Matches),
                    (SELECT MAX(Patent_Filing_Date) FROM Patent_Matches))) AS day)
            SELECT SAFE_CAST(FORMAT_DATE('%Y-%m',Date_Series_Table.day) AS STRING) AS Patent_Date_YearMonth, COUNT(Patent_Matches.Patent_Application_Number) AS Number_of_Patent_Applications
            FROM Patent_Matches
            RIGHT JOIN Date_Series_Table
            ON Patent_Matches.Patent_Filing_Date = Date_Series_Table.day
            GROUP BY Patent_Date_YearMonth
            ORDER BY Patent_Date_YearMonth
            """, {"ZZZZ": country, "KKKK": keyword}),
            }
        return switcher.get(query, "Invalid query") 

    print ("Estimated query size: {} GB.".format(bq_assistant.estimate_query_size(query_selector(query))))

    def kenvelo(question, answer = "no"):
    
        range_of_choices = {"yes": True, "y": True, "": True, "no": False, "n": False}
        
        if answer is None:
            prompt = "[Y/N]"
        
        elif answer == "yes":
            prompt = "[Y/N]"
        
        elif answer == "no":
            prompt = "[Y/N]"
        
        else:
            raise ValueError("Answer '%s' is invalid.")
    
        while True:
            sys.stdout.write(question + prompt)
            choice = input().lower()
            
            if answer is not None and choice == '':
                return range_of_choices[answer]
            
            elif choice in range_of_choices:
                return range_of_choices[choice]
            
            else:
                sys.stdout.write("Please answer any variation of 'yes' or 'no'. ")
    
  
    while ask_before_running is False or kenvelo("Run query? "):
    
        def plot_query1():
            figure(num = None, figsize = (24, 16), facecolor = 'w', edgecolor = 'k')         
            sns.set(context = 'paper', style = 'ticks', font_scale = 0.9)
            sns.barplot(x = 'country_code', y = 'cnt', data = patents.query_to_pandas_safe(query_selector("query1"), max_gb_scanned = bq_assistant.estimate_query_size(query_selector("query1"))))
            plt.title("Number of publications by country", loc = 'left', fontsize = 24, style = 'oblique')
            plt.ylabel('# of publications (log)', fontsize = 14) 
            plt.xlabel('Country', fontsize = 14)
            plt.yscale('log')     
            sns.despine(offset = 10, trim = True);
            plt.savefig(my_output_path + "query1" + '.pdf', orientation = 'landscape', bbox_inches = 'tight')
            plt.show()
        
        
        def plot_query2():
            figure(num = None, figsize = (24, 16), facecolor = 'w', edgecolor = 'k')
            sns.set(context = 'paper', style = 'ticks', font_scale = 0.9)
            sns.barplot(x = 'country_code', y = 'publications', data = patents.query_to_pandas_safe(query_selector("query2"), max_gb_scanned = bq_assistant.estimate_query_size(query_selector("query2"))))
            plt.title("Number of patents published between years {} and {} by country".format(start_year, end_year), loc = 'left', fontsize = 24, style = 'oblique')
            plt.ylabel('# of publications')
            plt.xlabel('Country')
            plt.yscale('log')
            sns.despine(offset = 10, trim = True);
            plt.savefig(my_output_path + "query2" + '.pdf', orientation = 'landscape', bbox_inches = 'tight')
            plt.show()
     
        
        def plot_query3():
            figure(num = None, figsize = (24, 16), facecolor = 'w', edgecolor = 'k')
            sns.set(context = 'paper', style = 'ticks', font_scale = 0.9)
            sns.barplot(x = 'datum', y = 'publications', data = patents.query_to_pandas_safe(query_selector("query3"), max_gb_scanned = bq_assistant.estimate_query_size(query_selector("query3"))))
            plt.title("Number of patents granted to country {} between years {} and {}".format(country, start_year, end_year), loc = 'left', fontsize = 24, style = 'oblique')
            plt.ylabel('# of patents', fontsize = 14)
            plt.xlabel('')
            sns.despine(offset = 10, trim = True);
            plt.savefig(my_output_path + "query3" + '.pdf', orientation = 'landscape', bbox_inches = 'tight')
            plt.show()    
        
        
        def plot_query10():
            figure(num = None, figsize = (24, 16), facecolor = 'w', edgecolor = 'k')         
            sns.set(context = 'paper', style = 'ticks', font_scale = 0.9)
            sns.barplot(x = 'Patent_Date_YearMonth', y = 'Number_of_Patent_Applications', data = patents.query_to_pandas_safe(query_selector("query10"), max_gb_scanned = bq_assistant.estimate_query_size(query_selector("query10"))))
            plt.title("Number of patent applications of technology {} in country {}".format(keyword, country), loc = 'left', fontsize = 24, style = 'oblique')
            plt.ylabel('# of applications', fontsize = 14) 
            plt.xlabel('Date', fontsize = 14)     
            sns.despine(offset = 10, trim = True);
            plt.savefig(my_output_path + "query10" + '.pdf', orientation = 'landscape', bbox_inches = 'tight')
            plt.show()        
        
    
        def plotter(query):
            if query == "query1":
                plot_query1()
                query = "query2"
            
            elif query == "query2":
                plot_query2()
                query = "query3"
            
            elif query == "query3":
                plot_query3()
                query = "query10"
            
            elif query == "query10":
                plot_query10()
            
            else: print('\033[1m' + "Sorry, this query doesn't output graphs (yet)." + '\033[0m')
    
    
        if output_to_csv and plot:
            return patents.query_to_pandas_safe(query_selector(query), max_gb_scanned = min(budget, bq_assistant.estimate_query_size(query_selector(query)))).to_csv(Path(temp_path, query + '.csv'), index = False, encoding = "utf-8"), plotter(query)        
            
        if output_to_csv:
            return patents.query_to_pandas_safe(query_selector(query), max_gb_scanned = min(budget, bq_assistant.estimate_query_size(query_selector(query)))).to_csv(Path(temp_path, query + '.csv'), index = False, encoding = "utf-8")
        
        if plot:
            return plotter(query)
        
        else:
            return patents.query_to_pandas_safe(query_selector(query), max_gb_scanned = min(budget, bq_assistant.estimate_query_size(query_selector(query))))

        if kenvelo("You will use", bq_assistant.estimate_query_size(query_selector(query)), "GB in this query. Continue? ") is False:
            break
 
##############################################################################################################################################################

def GLquery_examples():

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