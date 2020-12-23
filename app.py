from flask import Flask, render_template, request

from selenium import webdriver

import json
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'] )   # default is GET only
def index():
    if request.method == 'GET':        
        return render_template("index.html", hotels=[])
    else:    
        # POST
        loc = request.form['search_location']   # to-do: form validation
        response = requests.get(url="http://127.0.0.1:5000/api/" + loc)
        results = response.json()
        return render_template("index.html", hotels=results)


@app.route('/api/<location>')
def scrape_booking(location):
    # start Chrome session
    browser = webdriver.Chrome()

    # opening web site
    url = 'https://www.booking.com/'
    browser.get(url)

    # type in location
    search_input_el = browser.find_element_by_name('ss')
    search_input_el.send_keys(location)

    # click search button
    search_btn_el = browser.find_element_by_css_selector('button.sb-searchbox__button')
    search_btn_el.click()  

    # read results
    list = []
    result_els = browser.find_elements_by_css_selector('div.sr_item')
    for result in result_els:    
        name_el = result.find_element_by_class_name('sr-hotel__name')
        hotel_obj = {}
        hotel_obj['name'] = name_el.text
        list.append(hotel_obj)
        
    # close Chrome session
    browser.quit()

    return json.dumps(list)