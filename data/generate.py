"""
Synthetic data generation of MRZs from passport images
"""
import random 

SEX_CODES = ["M", "F", "<"]

NATIONALITY_CODES = [
    # North America
    "USA", "CAN", "MEX",
    # South America
    "BRA", "ARG", "COL", "CHL", "PER",
    # Europe (big + letter coverage)
    "GBR", "IRL", "FRA", "DEU", "ESP", "PRT",
    "ITA", "NLD", "BEL", "CHE", "AUT", "SWE",
    "NOR", "FIN", "DNK", "POL", "CZE", "GRC",
    # Asia
    "CHN", "JPN", "KOR", "IND", "PAK", "THA",
    # Middle East
    "SAU", "ARE", "QAT", "IRQ", "IRN",
    # Africa
    "ZAF", "EGY", "KEN", "NGA",
    # Oceania
    "AUS", "NZL",
    # Special
    "XXX",   # stateless / unknown
]

class Date:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    def __str__(self):
        """
        Return the date in YYMMDD format 
        """
        yy = self.year % 100
        return f"{yy:02d}{self.month:02d}{self.day:02d}"


def is_leap_year(year):
    """
    Check if a year is a leap year
    """
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
    
def generate_date(start_year, end_year=None):
    """
    Generate a random Date object
    """
    year = random.randint(start_year, end_year) if end_year else start_year
    month = random.randint(1, 12)
    if month == 2:
        if is_leap_year(year):
            max_days = 29
        else:
            max_days = 28
    elif month in [4, 6, 9, 11]:
        max_days = 30
    else:
        max_days = 31
    day = random.randint(1, max_days)
    return Date(year, month, day)

def generate_sex():
    """
    Generate a random sex code
    """
    r = random.random()
    return "M" if r < 0.49 else "F" if r < 0.98 else "<"

def main():
    birthdate = generate_date(1900, 2025)
    expirydate = generate_date(birthdate.year + random.randint(15, 60))
    nationality = random.choice(NATIONALITY_CODES)
    print(birthdate)
    print(expirydate)

if __name__ == "__main__":
    main()