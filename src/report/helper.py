from datetime import datetime



cube_end_date = datetime(2003, 1, 1)
youth_end_date = datetime(1998,1,1)
normal_end_date = datetime(1985, 1, 1)

def get_age_group(borndate:datetime)->str:
    age_category = "vet"
    if borndate > cube_end_date:
        age_category = "cube"
    if (borndate < cube_end_date) & (borndate > youth_end_date):
        age_category = "youth"
    if (borndate < youth_end_date) & (borndate > normal_end_date):
        age_category = "normal"
    return age_category