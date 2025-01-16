# Depricated Functions

# define a function to query google scholar
def query_google_scholar(google_scholar_query, api_key, max_results=300):

    """
    Query google scholar using SerpAPI
    
    Parameters: 
        - google_scholar_query: a string search query
        - api_key = SerpAPI key, available at: https://serpapi.com/
        - max_results = 300. Set at this level as single author and some evidence says that this is suitable limit.
    
    - Sets language to english
    
    """

    all_results = []  # store all results here
    start = 0         # start with the first page

    while len(all_results) < max_results:
        # define parameters for searching google scholar
        params = {
          "api_key": api_key,  # SerpAPI key
          "engine": "google_scholar", # google_scholar engine
          "q": google_scholar_query, # define query
          "start": start,
          "num": 20,
          "hl": "en" # set language to english
        }

        # search google scholar
        search = GoogleSearch(params)
        results = search.get_dict() # get results as dictionary

        # get organic results
        organic_results = results.get("organic_results", []) # retrieve organic list of results from results

        # add results to the list
        all_results.extend(organic_results)

        # check if there are no more results
        if len(organic_results) < 20:
            print("No more results to fetch.")
            break  # exit the loop

        # increment parameter for next page
        start += 20
        print(f"Fetched {len(all_results)} results so far...")

        if len(all_results) == max_results:
            print(f"Maximum number of {max_results} results reached.")

    return all_results[:max_results]



# define function to retun google scholar results as pandas dataframe
def scholar_to_df(organic_results, all_results_dict):

    """
    A function to transform dictionary output of SerpAPI Google Scholar Query into a
    pandas dataframe.

    Requirements:
        - Pandas

    Usage: 
        - Takes input from query_google_scholar function.
        - Outputs a pandas DataFrame
    """
# convert organic results to dictionary
    organic_results_dict = {}

    for item in organic_results:
        organic_results_dict[len(organic_results_dict)] = item

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