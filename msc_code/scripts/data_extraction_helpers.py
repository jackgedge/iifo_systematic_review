# Scripts to assist with data extraction

class Paper:
    def __init__(self, data):
        """
        Initialise a Paper instance with a flexible dictionary-based structure.
        
        :param data: Dictionary containing paper metadata and any nested information.
        """
        self.data = data
    
    def __str__(self):
        """Returns a formatted string representation of the paper."""
        id = self.data.get("Study_ID", "Unknown ID")
        title = self.data.get("Title", "Unknown Title")
        authors = ", ".join(self.data.get("Authors", ["Unknown Author"]))
        journal = self.data.get("Journal", "Unknown Journal")
        year = self.data.get("Year", "Unknown Year")
        doi = self.data.get("DOI", None)
        
        paper_info = f"{title} by {authors}, {journal}, {year}"
        if doi:
            paper_info += f" (DOI: {doi})"
        return paper_info
    
    def to_dict(self):
        """Returns the paper details as a dictionary."""
        return self.data
    
    def cite(self, style="APA"):
        """Returns a citation string based on the specified style."""
        title = self.data.get("Title", "Unknown Title")
        authors = ", ".join(self.data.get("Authors", ["Unknown Author"]))
        journal = self.data.get("Journal", "Unknown Journal")
        year = self.data.get("Year", "Unknown Year")
        doi = self.data.get("DOI", "No DOI")
        
        if style == "APA":
            return f"{authors} ({year}). {title}. {journal}. DOI: {doi}"
        elif style == "MLA":
            return f"{authors}. \"{title}.\" {journal}, {year}, DOI: {doi}."
        else:
            return "Citation style not supported."
    
    @classmethod
    def from_dict(cls, data):
        """Creates a Paper instance from a dictionary."""
        return cls(data)