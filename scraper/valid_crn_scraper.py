from bs4 import BeautifulSoup
import requests

_base_link1 = "https://usfonline.admin.usf.edu/pls/prod/bwckschd.p_disp_detail_sched?term_in="
_base_link2 = "&crn_in="

def check_available(crn, term):

    full_link = _base_link1 + term + _base_link2 + crn  #add course number and term to url
    ret_dict = {
                "valid": 0,
                "course_info": None
                }

    #get html content for url
    try:
        response = requests.get(full_link)
        html = BeautifulSoup(response.text, 'html.parser')
        soup = html.find('table',class_="datadisplaytable")

        #append course prefix + number to dictionary
        ret_dict['course_info'] = soup.find('th',class_="ddlabel").get_text().split('-')[2]
        ret_dict['valid'] = 1

        return ret_dict
    
    #if course doesnt exsist or error scraping will except and return
    except Exception as e:
            return ret_dict

#test functions
if __name__ == "__main__":
      check_available('86730','202408')