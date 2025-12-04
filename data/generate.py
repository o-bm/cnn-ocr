"""
Synthetic data generation of MRZs from passport images
"""
import random 

DIGITS = "0123456789"
LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
ALPHA_NUM = DIGITS + LETTERS

DOC_TYPES = [
    ("P", "<"),  # ordinary passport
    ("P", "D"),  # diplomatic passport (P + subtype D)
    ("P", "S"),  # service/official passport
    ("D", "<"),  # pure 'D' diplomatic passport style
]

DOC_TYPE_WEIGHTS = [85, 8, 5, 2]

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

GIVEN_NAMES = [
    # Common
    "ALEX", "ANNA", "JOHN", "MARIA", "DAVID", "EMMA",
    "NOAH", "LUCAS", "MIA", "LIAM", "OLIVIA", "ETHAN",
    "DANIEL", "SOFIA", "JAMES", "ISABELLA",
    # Global
    "MOHAMMED", "AHMED", "ALI", "SARA", "FATIMA",
    "HUA", "MEI", "WEI", "JUN", "YUNA",    
    # Good letter coverage & uniqueness
    "XAVIER", "QUENTIN", "YARA", "ZOE", "VICTOR",
    "KAYLA", "JACK", "BRUNO", "PEDRO", "LAURA",
]

SURNAMES = [
    # Common Western
    "SMITH", "JOHNSON", "WILLIAMS", "BROWN", "JONES",
    "MILLER", "DAVIS", "GARCIA", "RODRIGUEZ", "MARTINEZ",
    "HERNANDEZ", "LOPEZ", "GONZALEZ", "WILSON", "TAYLOR",
    
    # European variety
    "SCHMIDT", "SCHNEIDER", "MULLER", "WAGNER", "HOFMANN",
    "DUBOIS", "MOREAU", "LEROY", "ROUSSEAU", "FERRARI",
    "ROSSI", "RICCI", "CONTI", "ROMANO",
    
    # Asian variety
    "KIM", "LEE", "PARK", "CHOI", "NGUYEN", "TRAN", "PHAM",
    "SATO", "SUZUKI", "TANAKA",
    
    # Good letter coverage
    "XAVIER", "QUINN", "ZIMMERMAN", "VEGA", "YOUNG", "KING",
    "FOX", "JACKSON", "BAKER", "CARTER",
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


def generate_doc_type():
    """
    Generate a random document type
    """
    type, subtype = random.choices(DOC_TYPES, weights=DOC_TYPE_WEIGHTS)[0]
    return f"{type}{subtype}"


def generate_name():
    """
    Generate a random name
    """
    surname = random.choice(SURNAMES)
    r = random.random()
    if r < 0.70:
        given_count = 1
    elif r < 0.95:
        given_count = 2
    else:
        given_count = 3
    given_names = [random.choice(GIVEN_NAMES) for _ in range(given_count)]
    return surname, given_names


def generate_document_number():
    """
    Generate a random document number
    """
    r = random.random()
    if r < 0.7:
        return "".join(random.choices(DIGITS, k=9))
    elif r < 0.9:
        return "".join(random.choices(LETTERS, k=1)) + "".join(random.choices(DIGITS, k=8))
    else:
        return "".join(random.choices(LETTERS, k=2)) + "".join(random.choices(DIGITS, k=7))


def generate_personal_number():
    """
    Generate a random personal number
    """
    r = random.random()
    if r < 0.6:
        return ""
    elif r < 0.8:
        length = random.randint(3, min(7, 14))
    else:
        length = random.randint(8, 14)
    return "".join(random.choice(ALPHA_NUM) for _ in range(length))


def check_digit(data):
    """
    The check digits permit readers to verify that data in the MRZ is correctly interpreted
    """
    weights = [7, 3, 1]
    checksum = 0
    for i in range(len(data)):
        if data[i] in DIGITS:
            value = int(data[i])
        elif data[i] in LETTERS:
            value = ord(data[i]) - ord('A') + 10
        else:
            value = 0 # < 
        checksum += value * weights[i % 3]
    return checksum % 10


def build_mrz(): 
    """
    Build a valid MRZ string
    """
    doc_code = generate_doc_type()

    issuing = random.choice(NATIONALITY_CODES)

    surname, given_names = generate_name()
    name_block = surname + "<<" + "<".join(given_names)
    name_block = name_block.replace(" ", "<")
    max_len = 39
    name_block = name_block[:max_len].ljust(max_len, "<")

    line1 = f"{doc_code}{issuing}{name_block}"
    
    assert len(line1) == 44
    
    doc_number = generate_document_number()
    doc_number_cd = check_digit(doc_number)

    nationality = issuing

    dob = generate_date(1900, 2025)
    expiry_date = generate_date(dob.year + random.randint(15, 60))
    dob = str(dob)
    expiry_date = str(expiry_date)
    dob_cd = check_digit(dob)
    expiry_date_cd = check_digit(expiry_date)
    
    sex = generate_sex()
    pn = generate_personal_number()
    pn_field = pn.ljust(14, "<")
    pn_cd = check_digit(pn_field)

    composite_input = (
        doc_number + str(doc_number_cd) +
        dob + str(dob_cd) +
        expiry_date + str(expiry_date_cd) +
        pn_field + str(pn_cd)
    )
    composite_cd = check_digit(composite_input)

    line2 = (
        f"{doc_number}{doc_number_cd}"
        f"{nationality}"
        f"{dob}{dob_cd}"
        f"{sex}"
        f"{expiry_date}{expiry_date_cd}"
        f"{pn_field}{pn_cd}{composite_cd}"
    )

    assert len(line2) == 44

    return line1, line2
    
if __name__ == "__main__":
   for _ in range(10000):
    line1, line2 = build_mrz()
    print(line1+ "\n" + line2 + "\n")