"""
Synthetic data generation of MRZs from passport images
"""
import random 


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


def main():
    birthdate = generate_date(1900, 2025)
    expirydate = generate_date(birthdate.year + random.randint(15, 60))

if __name__ == "__main__":
    main()