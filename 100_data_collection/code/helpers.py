import pandas as pd

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

    # define new dictionary to output
    new_dict = {
        "Stage": stage,
        "Count": {
            "Start": start_count,
            "End": end_count,
            "Removed": start_count - end_count
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
