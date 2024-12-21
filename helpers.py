def track_duplicate_removal(stage, end_count, start_count=None, tracking_dict=None):
   """
   Tracks duplicate removal process by adding a record to the tracking dictionary.
   
   Parameters:
   - stage: Description of the stage of exclusion.
   - start_count: Count of items before processing.
   - end_count: Count of items after processing.
   - tracking_dict: The dictionary to update (default is an empty dictionary).
   
   Returns:
   - The updated tracking dictionary.
   """

   if tracking_dict is None:  # If there is no tracking dictionary:
      tracking_dict = {}      # Create one

   # Infer start_count from the previous stage if it's None
   if start_count is None and len(tracking_dict) > 0:                      # If start_count is 0
      start_count = tracking_dict[len(tracking_dict) - 1]["Count"]["End"]  # Use the previous end count.


   # Validate inputs
   if end_count is None or start_count < 0 or end_count < 0:
      raise ValueError("Start and End counts must be non-negative integers.")

   
   new_dict = {                              # Define new dictionary to output
      "Stage": stage,                        
      "Count": {
         "Start": start_count,
         "End": end_count,
         "Removed": start_count - end_count
      }
   }

   # Add to tracking dictionary
   tracking_dict[len(tracking_dict)] = new_dict

   # Print/log the stage details
   print(f"{stage}: Start={start_count}, End={end_count}, Removed={start_count - end_count}")

   # Print the total number of papers removed.
   print(f'{tracking_dict[min(tracking_dict.keys())]["Count"]["Start"] - tracking_dict[max(tracking_dict.keys())]["Count"]["End"]} duplicates removed so far.')

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
