import requests
from bs4 import BeautifulSoup
import pandas as pd
from progressbar import progressbar
import numpy as np



def download_athlete_information_via_standings(season:int, gender:str, competition:int=2819, nation:str='all'):
    df_standings_schema = {
            "rank":[],
            "name":[],
            "team":[],
            "points":[]
        }
    df_athlete_schema = {
        "born":[],
        "nation":[],
        "height":[],
        "weight":[],
        "skis":[],
        "boots":[],
        "poles":[]
    }

    starting_point=__get_starting_response(season, gender, competition, nation)
    searching_index=["rank", "name", "team", "time"]
    for result_item in progressbar(starting_point.find("div", class_=f"results-wrapper gender-{gender}").find_all('div')):
        for key, index in zip(df_standings_schema, searching_index):
            index_item = result_item.find('span', class_=index)
            if index_item:
                df_standings_schema[key].append(index_item.text)
            else:
                df_standings_schema[key].append(index_item.text)
            a_tag = result_item.find('a')
        if a_tag:
            link = a_tag['href']
            athlete_infos = __handle_athlete_page(link)
            combined_values = athlete_infos[1]|athlete_infos[2]
            df_athlete_schema['nation'].append(athlete_infos[0])
            for key, value in combined_values.items():
                df_athlete_schema[key].append(value)
    combined_schema = df_standings_schema | df_athlete_schema
    df = pd.DataFrame(combined_schema)
    df.to_csv(f"./data/{season}/{gender}_athlete_information.csv", index=False)

def __handle_athlete_page(link:str):
    response_athlete = requests.get(link)
    soup_athlete = BeautifulSoup(response_athlete.text, "html.parser")
    name_nationality_item = soup_athlete.find('div', class_ = "name-nationality")
    nationality=__extract_nation(name_nationality_item)
    athlete_information = soup_athlete.find('div', class_="born-height-weight")
    equipment_information = soup_athlete.find('div', class_="skis-boots-poles")
    athlete_values = __extract_athlete_information(athlete_information)
    equipment_values = __extract_equipment_information(equipment_information)
    return (nationality, athlete_values, equipment_values)

def __get_starting_response(season:int, gender:str, competition:int=2819, nation:str='all'):
    response = requests.get(f"https://skiclassics.com/results/standings/?season={season}&comp={competition}&gender={gender}&nation={nation}")
    return BeautifulSoup(response.text, "html.parser")

def __extract_nation(result_item):
    nation = np.nan
    if result_item:
        img_tag = result_item.find('img')
        if img_tag:
            nation = img_tag.get('alt')
    return nation

def __extract_athlete_information(soup):  
    athlete_values:dict = {"born": np.nan, "height":np.nan, "weight": np.nan}
    searching_index = ["borndate data", "height data", "weight data"]
    if soup:
        for key, index in zip(athlete_values, searching_index):
            value = soup.find('span', class_=index)
            if value:
                athlete_values[key] = value.text
    return athlete_values

def __extract_equipment_information(soup):
    equipment_values = {"skis": np.nan, "boots":np.nan, "poles":np.nan}
    searching_index = ["skis data", "boots data", "poles data"]
    if soup:
        for key, index in zip(equipment_values, searching_index):
            value = soup.find('span', class_=index)
            if value:
                equipment_values[key] = value.text
    return equipment_values

"""
def download_athlete_information_via_pro_teams():
    df_athlete_schema:dict = {
        "name": [],
        "team": [],
        "born":[],
        "nation":[],
        "height":[],
        "weight":[],
        "skis":[],
        "boots":[],
        "poles":[]

    }
    start_response = requests.get("https://skiclassics.com/pro-teams/")
    soup_pro_teams_list = BeautifulSoup(start_response.text, 'html.parser')
    teams_item_container = soup_pro_teams_list.find('div', class_ = "container team-container grid-mobile-2")
    for team_container in teams_item_container.find_all('div', class_ = "item team-item pro-team-item"):
        link_a_tag = team_container.find('a')
        if not link_a_tag:
            break
        link = link_a_tag['href']
        teampage_response = requests.get(link)
        teampage_soup = BeautifulSoup(teampage_response.text, "html.parser")
        athletes_container = teampage_soup.find('div', class_="container content-container team-members grid-mobile-2 grid-desktop-3")
        for athlete in athletes_container.find_all('div', class_ ='container-item'):
            link_a_tag = athlete.find('a')
            if link_a_tag:
                athletepage_link = link_a_tag['href']
                df_athlete_schema['team'].append(team_name)
                athlete_response =  __handle_athlete_page(athletepage_link)
                combined_values = athlete_response[1]|athlete_response[2]
                df_athlete_schema['nation'].append(athlete_response[0])
                for key, value in combined_values.items():
                    df_athlete_schema[key].append(value)
    df = pd.DataFrame(df_athlete_schema)
    df.to_csv("./data/2025/all_athletes.csv")"""

if __name__ == "__main__":
    #download_athlete_information_via_pro_teams()
    download_athlete_information_via_standings(2024, 'W')