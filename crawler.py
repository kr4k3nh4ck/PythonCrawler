import requests
import scrapy
from bs4 import BeautifulSoup
import sys

get_country_page = requests.get('https://www.transfermarkt.com.tr/site/dropDownLaender',  headers={'User-Agent': 'Custom'})
get_country_json = get_country_page.json()

get_country_json = get_country_json[27:]
country_list = get_country_json.replace("<option value=", "").replace("></option>", "</option>").replace("</option>", "+").split("+")
country_list = country_list[:-1]
country_keys = []
country_values = []

main = {}


for element in country_list:
    new_element = element.replace('"', "").split(">")
    if len(new_element) == 1:
        new_element.append("")
    country_keys.append(new_element[0])
    country_values.append(new_element[1])

country_dict = dict(zip(country_keys, country_values))

"""League Names, Logos and URLs"""
league_name_list = []
league_logo_list = []
league_url_list = []
for key in country_dict:
    try:
        main[str(country_dict[key])] = []
        a = int(key)
        if a==40:
            payload =int(key)
            league_page = requests.post("https://www.transfermarkt.com.tr/wettbewerbe/national/wettbewerbe/" + str(a), headers={'User-Agent': 'Custom'})
            league_page_content = BeautifulSoup(league_page.content, 'html.parser')
            league_table = league_page_content.find("table", attrs={"class":"items"})
            league_table_body= league_table.find("tbody")
            all_leagues_tr = league_table_body.findAll("tr")
            for league_cols in all_leagues_tr:
                league = league_cols.findAll("td", attrs={"class":r"hauptlink"})
                if len(league) == 2:
                    league_name = league[0].find("img")["alt"]
                    league_name_list.append(league_name)
                    league_logo = league[0].find("img")["src"].replace("tiny", "normal")
                    league_logo_list.append(league_logo)
                    league_url = ((league[0]).findAll("a")[1])["href"]
                    league_url_pattern = r"https://www.transfermarkt.com.tr" + league_url
                    league_url_list.append(league_url_pattern)

                    #It should be done at the at
                    main[str(country_dict[key])].append({"Legaue_Name":league_name,"Legaue_Logo":league_logo,"Legaue_URL":league_url_pattern})

                    club_name_list = []
                    club_logo_list = []
                    club_url_list = []

                    """URL PATTERM VE ÜLKE ADIYLA DİCT OLUŞTURUP İÇİNDE DÖN!"""

                    if league_url_pattern=="https://www.transfermarkt.com.tr/1-bundesliga/startseite/wettbewerb/L1":
                        club_page = requests.get(league_url_pattern, headers={'User-Agent': 'Custom'})
                        club_page_content = BeautifulSoup(club_page.content, 'html.parser')
                        club_table = club_page_content.find("table", attrs={"class":"items"})
                        club_table_body = club_table.find("tbody")
                        all_clubs_tr = club_table_body.findAll("tr")
                        for club_cols in all_clubs_tr:
                            club = club_cols.findAll("td", attrs={"class":r"zentriert no-border-rechts"})[0].find("a")
                            club_name = club.find("img")["alt"]
                            club_name_list.append(club_name)
                            club_logo = club.find("img")["src"].replace("tiny", "normal")
                            club_logo_list.append(club_logo)
                            club_url = club["href"]
                            club_url_pattern = r"https://www.transfermarkt.com.tr" + club_url



    except Exception as e:
        pass
#print(main)