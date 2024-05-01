from bs4 import BeautifulSoup
import requests

_base_link1 = "https://usfonline.admin.usf.edu/pls/prod/bwckschd.p_disp_detail_sched?term_in="
_base_link2 = "&crn_in="

def check_available(crn, term):

    if(crn == "00000"):
          return 0
    if(crn == "00001"):
          return 3
    
    full_link = _base_link1 + term + _base_link2 + crn  #add course number and term to url

    #get html content for url
    try:
        response = requests.get(full_link)
        html = BeautifulSoup(response.text, 'html.parser')
        soup = html.find('table',class_="datadisplaytable")

        seat_areas = soup.find('table',class_="datadisplaytable")

        #find all rows within seating area
        rows = seat_areas.find_all('tr')

        #find all td elements 
        td_elements = (rows[0].find_all('td',class_='dddefault'))

        if len(td_elements) >=3:
                remaining_seats = int(td_elements[2].get_text(strip=True))
        
        return remaining_seats
    
    except Exception as e:
            print(f"Error: {e}")
            return -1
