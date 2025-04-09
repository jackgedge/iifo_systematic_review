import pandas as pd
from serpapi.google_search import GoogleSearch
import requests

# Define exclusion criteria:
exclusion_criteria = {
1:	"Full text not available in English.",
2:	"Studies not focusing on intentional self-ingestion (into the gastrointestinal tract) of foreign object via the oral cavity (mouth) or where unclear if ingested.",
3:	"Studies focussing solely on accidental ingestion.",
4:	"Non-Human/ animal studies.",
5:	"Reviews, editorials, commentaries, and opinion pieces without original empirical data.",
6:	"Duplicate publications or studies with overlapping data sets (the most comprehensive or recent study will be included).",
7:	"Studies focusing on ingestion or co-ingestion of substances (e.g. poisons, medications) rather than physical foreign objects.",
8:	"Ingestions undertaken in controlled environment as part of voluntary study.",
9:	"Ingestions not explicitly stated to be intentional and history not suggestive of deliberate ingestion (i.e. Age < 8, no history of previous ingestions, no psychiatric co-morbidities, not a prisoner/detainee/vulnerable group).",
10:	"Does not meet inclusion criteria.",
11: "Ingestions where death resulted from other means (i.e. suicide)"
}

exclusion_criteria_short = {
1:	"Full text not available in English.",
2:	"No focus on intentional self-ingestion.",
3:	"Sole accidental ingestion focus.",
4:	"Non-Human studies.",
5:	"Reviews, commenteries, etc. without original empirical data.",
6:	"Duplicate publications or overlapping datasets.",
7:	"Ingestion or co-ingestion of substances.",
8:	"Ingested in controlled study.",
9:	"Not explicitly intentional ingestions.",
10:	"Inclusion criteria not met.",
11: "Death occured from by other means (i.e. suicide)."
}

def track_duplicate_removal(stage, end_count, start_count=None, tracking_dict=None):
    """
    Tracks duplicate removal process by adding a record to the tracking dictionary.

    Parameters:
    - stage: Description of the stage of exclusion.
    - start_count: Count of items before processing (optional).
    - end_count: Count of items after processing.
    - tracking_dict: The dictionary to update (default is an empty dictionary).

    Returns:
    - The updated tracking dictionary.
    """
    # define tracking_dict if not provided
    if tracking_dict is None:
        tracking_dict = {}

    # infect start_count if not provided
    if start_count is None:
        if tracking_dict and len(tracking_dict) > 0:
            start_count = tracking_dict[len(tracking_dict) - 1]["Count"].get("End", 0)
        else:
            start_count = 0  # Default to 0 if tracking_dict is empty

    # ensure start_count and end_count are integers
    start_count = int(start_count) if start_count is not None else 0
    end_count = int(end_count) if end_count is not None else 0

    # Define new dictionary to output
    removed = start_count - end_count

    # If removed is negative, set it to 0 or handle it gracefully
    if removed < 0:
        print(f"Warning: Removed count is negative at stage '{stage}'. Check the logic.")
        removed = 0

    new_dict = {
        "Stage": stage,
        "Count": {
            "Start": start_count,
            "End": end_count,
            # Handle the "Start" stage or invalid cases
            "Removed": 0 if stage == "Start" or start_count == 0 else start_count - end_count
        }
    }

    # add new record to tracking_dict
    tracking_dict[len(tracking_dict)] = new_dict

    # print stage details
    print(f"{stage}: Start Count={start_count}, End Count={end_count}, Removed Count={start_count - end_count}")

    # print total number of papers removed
    total_removed = tracking_dict[0]["Count"]["End"] - tracking_dict[len(tracking_dict) - 1]["Count"]["End"]
    print(f"{0 - total_removed} duplicates removed so far.")

    return tracking_dict


def dataframe_to_ris(df, ris_file):
    """
    Converts a pandas DataFrame to RIS format, handling multiple authors.

    Args:
    - df: The pandas DataFrame containing the data.
    - ris_file: Path to the output RIS file.
    """

    # Define mapping of DataFrame columns to RIS fields
    field_mapping = {
        "Title": "T1",              # Title of article     
        "Publication Year": "Y1",   # Publication Year
        "Authors": "AU",            # First Author
        "Publication Title": "JO",  # Title of the Publication
        "Abstract": "AB",           # Abstract
        "DOI": "DO",                # DOI
        "Database": "DB"            # Database name
    }

    with open(ris_file, "w", encoding="utf-8") as file:
        for _, row in df.iterrows():
            file.write("TY  - JOUR\n")  # Assuming all entries are journal articles
            for df_col, ris_field in field_mapping.items():
                if df_col in row and pd.notna(row[df_col]):
                    if ris_field == "AU":  # Handle authors separately
                        authors = row[df_col].split(";")  # Split authors by ';'
                        for author in authors:
                            file.write(f"AU  - {author.strip()}\n")  # Add AU for each author
                    else:
                        # Write other RIS fields
                        file.write(f"{ris_field}  - {row[df_col]}\n")
            file.write("ER  -\n\n")  # End of record


# Define Function to Search Google Scholar
def search_google_scholar(query, api_key, max_results=300):
    """
    A function that performs a google scholar search and returns as pandas dataframe.

    Parameters:
    - query: a string google scholar query
    - api_key: SerpAPI key, available at: https://serpapi.com/
    - max_results. Maximum number of results to be returned.
    
    """

    all_results = []  # store all results here
    start = 0         # start with the first page

    print(f"Searching Google Scholar: {query}")

    # While the length of all_results is less than the maximum permitted:
    while len(all_results) < max_results:
    # Define parameters for searching google scholar
        params = {
        "api_key": api_key,  # SerpAPI key
        "engine": "google_scholar", # google_scholar engine
        "q": query, # define query
        "start": start,
        "num": 20,
        "hl": "en" # set language to english
        }

        # Search google scholar
        search = GoogleSearch(params)
        results = search.get_dict() # get results as dictionary

        # Get organic results
        organic_results = results.get("organic_results", []) # retrieve organic list of results from results

        # Add results to the list
        all_results.extend(organic_results)

        # Check if there are no more results
        if len(organic_results) < 20:
            print("No more results to fetch.")
            break  # exit the loop

        # increment parameter for next page
        start += 20
        print(f"Fetched {len(all_results)} results so far...")

        if len(all_results) == max_results:
            print(f"Maximum number of {max_results} results reached.")

    organic_results = all_results[:max_results]

    # convert organic results to dictionary
    organic_results_dict = {}

    for item in organic_results:
        organic_results_dict[len(organic_results_dict)] = item

    # Create organic results dataframe with predefined columns
    organic_results_df = pd.DataFrame(columns=[
    'Publication Year', 'First Author', 'Summary', 'Authors', 'Publication Title',
    'Title', 'Abstract', 'URL', 'Database', 'Exclude', 'Reason ID',
    'Reason'])

    # create empty list to store rows
    rows = []

    # iterate through organic_results_dict
    for item in organic_results_dict.values():
        # extract information
        title = item.get('title', None)
        abstract = item.get('snippet', None)

        summary = item['publication_info'].get('summary', "Summary not found.")
        if summary:
            authors = summary.split(' - ')[0].strip() if ' - ' in summary else "No Author Listed"
            publication_info = summary.split(' - ')[1].strip() if ' - ' in summary else "No Publication Information"
            publication_title = publication_info.split(',')[0].strip() if ',' in publication_info else None
            year = publication_info.split(',')[-1].strip() if ',' in publication_info else None
        else:
            authors = publication_title = year = None

        # add database specific fields
        database = "Google Scholar"
        exclude = None
        reason_id = None
        reason = None

        # append row as dictionary
        rows.append({
            'Publication Year': year,
            'First Author': f"{authors.split(' ')[-1]}, {authors.split(' ')[0][0]}." if authors else None,
            'Authors': authors,
            'Summary': summary,
            'Publication Title': publication_title,
            'Title': title,
            'Abstract': abstract, 
            'URL': item.get('link', None),
            'Database': database,
            'Exclude': exclude,
            'Reason ID': reason_id,
            'Reason': reason
        })

    organic_results_df = pd.DataFrame(rows).sort_values(by="Publication Year", ascending=True).reset_index(drop=True)

    return organic_results_df


def create_search_query_summary(results):
    
    if not isinstance(results, dict):
        try:
            results = dict()
        except TypeError as e:
            print(f"{e} expected a dictionary, given {type(results)}")

    # Create results dataframe with "Query" and "Num Results" columns
    results_df = pd.DataFrame(columns=["Query", "Num Results"])

    # Initialise list to store rows in 
    rows = []

    # iterate through results dictionary that contains queries and results dataframes from query
    for item in results.values():
        query = item.get('query') # get query
        num_results = len(item.get('results')) # get number of results - max is 300.
        # append row as dictionary
        rows.append({
            "Query": query,
            "Num Results": num_results
            })
    # create dataframe from rows
    results_df = pd.DataFrame(rows)

    # return the results dataframe
    return results_df


# append to all google scholar results dictionary
def append_google_scholar_results_to_dictionary(query, df, results_dict):

    """
    A function that appends query and the resultant dataframe to a dictionary.
    Allows for tracking of queries and for number of results from these queries. 
    """

    if results_dict is None:
        results_dict = {}

    results_dict[len(results_dict)] = {
        "query": query,
        "results": df}
    return results_dict


def export_search_results_to_csvs(results, output_path):
    """
    For use in google_scholar_search
    Function that exports dataframes from queries to CSV.

    Parameters:
        - Results dictionary
    """
    # check results are in dictionary format
    if not isinstance(results, dict):
        raise TypeError(f"Expected a dictionary, but got {type(result).__name__} instead.")

    # export results to csv to inspect
    for n, value in enumerate(results.values()):
        df = value['results']
        output_file = f"{output_path}/google_scholar_results_{n}.csv"
        df.to_csv(output_file, index=False)


# define query to export results from all_results_dict as csv files.
def export_search_result_summary_to_csv(results, output_path):
    """
    For use in google_scholar_search
    Export query and query counts to a CSV file.

    Parameters:
        - results: A pandas DataFrame.
        - output_path: A string representing the output file path (including the file name).
    """
    # Check that results is a pandas dataframe
    if not isinstance(results, pd.DataFrame):
        raise TypeError(f"Expected a DataFrame, but got {type(results).__name__} instead.")
    
    # strip out \n from all cells in the dataframe
    results = results.apply(lambda col: col.map(lambda x: x.replace('\n', '') if isinstance(x, str) else x))
    
    output_file = f"{output_path}/google_scholar_query_results_counts.csv"

    # Save the DataFrame to CSV
    results.to_csv(output_file, index=False)


# Create 10% sample for review by second author
def create_results_sample(df, sample_pct_size=0.05, random_state=42):

    """
    Creates sample of given dataframe based on a percentage.

    Parameters:
    - df (pd.DataFrame): Results dataframe
    - sample_pct_size (float): A percentage as a decimal value between 0 and 1.

    Returns:
    - pd.DataFrame: A DataFrame containing the sampled rows.
    """
    
    # Validate that a dataframe was given
    if not isinstance(df, pd.DataFrame):
        return TypeError(f"Expected DataFrame, was given {type(df)}")
    
    # Validate that percentage given as decimal
    if not sample_pct_size > 0 or not sample_pct_size < 1:
        return ValueError(f"Sample percentage must be a decimal between 0 and 1.")
    
    sample_size = len(df) # Calculate size of given dataframe
    print(f"Given sample size: {sample_size}")  # Print result
    new_sample_size = int(round(sample_size * sample_pct_size)) # Calculate desired sample size.
    
    desired_percentage = int(sample_pct_size * 100) # Calculate desired percentage to display
    print(f"Calculating desired sample size... {desired_percentage}% of {sample_size} = {new_sample_size}") # Print information

    # Create the sample DataFrame
    print("Creating Sample Dataframe")
    sample_df = df.sample(n=new_sample_size, random_state=random_state)  # Use n instead of frac for precise row count
    
    return sample_df


def check_doi_valid(doi):
    """
    Check if a DOI is valid using the Semantic Scholar API.
    
    Returns a tuple (is_valid, title). If the DOI is valid, is_valid is True and title contains the paper title.
    Otherwise, is_valid is False.
    """
    # Construct the API URL. Note the "DOI:" prefix.
    url = f"https://api.semanticscholar.org/graph/v1/paper/DOI:{doi}?fields=title"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            # If title, assume it's valid.
            return True, data.get("title", "No title available")
        else:
            print(f"DOI {doi} returned status code: {response.status_code}")
            return False, None
    except Exception as e:
        print(f"Error checking DOI {doi}: {e}")
        return False, None