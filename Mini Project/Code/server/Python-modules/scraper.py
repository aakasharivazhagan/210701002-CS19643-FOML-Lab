from bs4 import BeautifulSoup;
import requests;
import json
import re;
import os;

main_text = requests.get('https://www.tn.gov.in/scheme/department_wise/', verify=False).text;
main_soup = BeautifulSoup(main_text, 'lxml');
maine = main_soup.find_all('div', class_='scheme_list');
main_links = [];
for div in maine:
    p_tag = div.find('p')
    if p_tag:
        a_tag = p_tag.find('a')
        if a_tag and 'href' in a_tag.attrs:
            href_value = a_tag['href']
            main_links.append(href_value)
            print(f"Found href: {href_value}")
        


for m_link in main_links:
    html_text = requests.get(m_link, verify=False).text;
    soup = BeautifulSoup(html_text, 'lxml');

    full = soup.find_all('div', class_='scheme_lst');
    links = [];
    for div in full:
        p_tag = div.find('p')
        if p_tag:
            a_tag = p_tag.find('a')
            if a_tag and 'href' in a_tag.attrs:
                href_value = a_tag['href']
                links.append(href_value)
                print(f"Found href: {href_value}")
            
    for slink in links:
        spage_text = requests.get(slink, verify=False).text;
        soup = BeautifulSoup(spage_text, 'lxml');
        full = soup.find_all('span', class_='right_column');
        
        ext_data = [];
        for f in full:
            ext_data.append(f.text);

        extracted_data = {
            'concerned_dept' :ext_data[0],
            'concerned_dist' :ext_data[1],
            'org_name'       :ext_data[2],
            'name'           :ext_data[3],
            'associated'     :ext_data[4],
            'sponsered_by'   :ext_data[5],
            'funding_pattern':ext_data[6],
            'beneficiaries'  :ext_data[7],
            'benefits'       :ext_data[8],
            'income'         :ext_data[9],
            'age'            :ext_data[10],
            'community'      :ext_data[11],
            'other'          :ext_data[12],
            'how'            :ext_data[13],
            'introduced_on'  :ext_data[14],
            'valid_upto'     :ext_data[15],
            'desc'           :ext_data[17],
        }
        if(len(ext_data)==20):
            anchor = full[19].find('a');
            onclick = anchor.get('onclick');

            pattern = re.compile(r"tnportal_window\('([^']+)'\)")
            match = pattern.search(onclick)
            if match:
                url = match.group(1)
            else:
                url = "No URL found."

            extracted_data['dummy_field'] = ext_data[18];
            extracted_data['download_link'] =url ;
        
        json_data = json.dumps(extracted_data, indent=2)
        file_path=r'..\Datasets\raw_data.json';
     #  file_path=os.path.join('G:','AI-Chatbot-Project','chat-bot','server','Datasets','raw_data.json');
        try:
            with open(file_path, 'r') as file:
                existing_data = json.load(file)

            if not isinstance(existing_data, list):
                existing_data = [existing_data]  

        except FileNotFoundError:
            existing_data = []

        existing_data.append(extracted_data)
        with open(file_path, 'w') as file:
            json.dump(existing_data, file, indent=2)
        print(f"JSON data appended to {file_path}")
    
    