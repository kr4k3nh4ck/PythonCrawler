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
main_league = {}

for element in country_list:
    new_element = element.replace('"', "").split(">")
    if len(new_element) == 1:
        new_element.append("")
    country_keys.append(new_element[0])
    country_values.append(new_element[1])

country_dict = dict(zip(country_keys, country_values))

"""League Names, Logos and URLs"""

for key in country_dict:
    league_name_list = []
    league_logo_list = []
    league_url_list = []
    try:
        main[str(country_dict[key])] = []
        a = int(key)
        if a==174:
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
                    main[str(country_dict[key])].append({"League_Name":league_name, "League_Logo":league_logo, "League_URL":league_url_pattern})

                    club_name_list = []
                    club_logo_list = []
                    club_url_list = []

            league_dict = dict(zip(league_name_list,league_url_list))
            for league_key in league_dict:
                try:

                    club_page = requests.get(league_dict[league_key], headers={'User-Agent': 'Custom'})
                    club_page_content = BeautifulSoup(club_page.content, 'html.parser')
                    club_table = club_page_content.find("table", attrs={"class":"items"})
                    column_len_of_table = len(club_table.find("thead").findAll("th"))
                    if column_len_of_table == 6 or column_len_of_table == 10:
                        main_league[league_key] = []
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
                            main_league[str(league_key)].append({"Club_Name":club_name, "Club_Logo":club_logo, "Club_URL": club_url_pattern})
                    else:
                        pass

                except Exception as e:
                    print("Club_Name"+ club_name, "Club_Logo" +club_logo, "Club_URL"+  club_url_pattern)
                    print(league_key)
                    print(e)


    except Exception as e:
        print(e)
        pass
#print(main)
print(main_league)