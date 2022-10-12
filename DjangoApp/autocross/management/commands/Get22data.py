from  django.core.management.base import  BaseCommand
from ...models import Run_data, Event,Best_run_data, Run_notes
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz
import requests
import logging
import re
import os
import datetime

class Command(BaseCommand):
    def handle(self, *args, **options):
        print('command: Get22data') 
        main()
        print('Finished')       

def main():
    #%(asctime)s:%(levelname)s:
    #logging file
    #logging.basicConfig(filename='test.log', level = logging.DEBUG,
                        #format='%(message)s')

    current_results_url = 'https://ccsportscarclub.org/autocross/schedule/'
    page = requests.get(current_results_url)
    soup = BeautifulSoup(page.text, 'html.parser')

    #get a list of all links on the web page    
    url_fulltag_list = soup.find_all('a')

    #creating a list of urls which contains files or msreg
    #these urls will be the only ones we need to look through    
    url_notag_list = delete_tags(url_fulltag_list) 
    
    #writing to files
    location = ''
    length = len(url_notag_list)
    for i in range(length):
        #gets raw data
        if url_notag_list[i].find('_raw') != -1:            
            write_to_files(9,location, url_notag_list[i])

        #gets pax data           
        if url_notag_list[i].find('_pax') != -1:            
            write_to_files(11,location, url_notag_list[i])

        #gets location
        if url_notag_list[i].find('msreg') != -1:
            if (length - i) > 1:            
                new_page = requests.get(url_notag_list[i])
                new_soup = BeautifulSoup(new_page.text, 'html.parser')
                location = new_soup.find('div',{'class':'section__description section__description_s'}).text
                

    # start reading in files to prepare to compare
    #must be absolute path
    #import os /os.getcwd()
    dir_list = os.listdir(path='C:\\Users\\BlahKyle\\Documents\\IT391Proj\\DjangoApp\\autocross\\management\\commands\\files\\')
    indexx = 0
    dir_length = len(dir_list)    
    while indexx < dir_length:
        curr_path = dir_list[indexx]
        k_index = indexx + 1
        # Full path = cone-slayer-saturday-04-23-2022_pax.txt
        #sub_path = cone-slayer-saturday-04-23-2022
        #gets the sub path
        split_list = re.split('_pax|_raw', curr_path)
        sub_path = split_list[0]        
        #holds the paths associated with curr_path
        #by matching with sub_path
        filePathList = []
        #holds the index of the last file found k
        k_holder = 0

        while k_index < dir_length:
            if dir_list[k_index].find(sub_path) != -1:
                filePathList.append(dir_list[k_index])
                k_holder = k_index
            k_index += 1
        if k_holder == 0:
            indexx+=1
        else:
            indexx = k_holder +1

        raw_path = ""
        pax_path = ""
        fin_path = ""
        filePathList.append(curr_path)
        for path in filePathList:
            if path.find('_raw') != -1:
                raw_path = path
            if path.find('_pax') != -1:
                pax_path = path
            if path.find('_fin') != -1:
                fin_path = path
        raw_data_list = read_files(raw_path)
        pax_data_list = read_files(pax_path)
        #fin_data_list = []        

        #Creating an event instance into the database
        datelist=raw_data_list[1][0].split('-')
        month = int(datelist[0])
        day =  int(datelist[1])
        year = int(datelist[2])
        event_date = datetime.date(year,month,day)
        event_instance = Event(date=event_date,location=raw_data_list[0][0], name = raw_data_list[2][0])
        event_instance.save()        
        
        #Start comparing files
        #name index 4 for pax
        #name index 4 for raw        
        for index in range(3,len(raw_data_list)):
            raw_name = raw_data_list[index][4].lower()
            ratio_limit = 90
            pindex = 3
            while pindex < len(pax_data_list):
                pax_name = pax_data_list[pindex][4].lower()
                ratio = fuzz.ratio(raw_name,pax_name)
                if ratio > ratio_limit:                                        
                    #Create Run data instance
                    class_name = raw_data_list[index][2]
                    car_num = raw_data_list[index][3]
                    driver_name = raw_data_list[index][4]
                    car_model = raw_data_list[index][5]
                    time = raw_data_list[index][6]
                    cones_hit = -1
                    
                    run_data_instance = Run_data(class_name=class_name,car_num = int(car_num),driver_name=driver_name,car_model = car_model,
                                                    time=time,cones_hit=int(cones_hit),event_id =event_instance)
                    run_data_instance.save()

                    #Create Best Run Data instance and                    
                    raw_class_position = raw_data_list[index][1]
                    pax_class_position = pax_data_list[pindex][1]
                    pax_time = pax_data_list[pindex][8]                    

                    best_run_data_instance = Best_run_data(run_id=run_data_instance, raw_class_position= int(raw_class_position), pax_class_position=int(pax_class_position),
                                                            pax_time=pax_time)                    
                    best_run_data_instance.save()
                    pindex= len(pax_data_list)+1
                else:
                    if pindex == len(pax_data_list) -1:
                        pindex = 2
                        ratio_limit = ratio_limit -5
                pindex+=1       
    
    # end of while loop

def read_files(path):
    '''Reads file line by line, splits the string
    , returns a list of lists of stripped strings'''
    #must be absolute path
    #import os /os.getcwd()
    my_file = open('C:\\Users\\BlahKyle\\Documents\\IT391Proj\\DjangoApp\\autocross\\management\\commands\\files\\'+path,'r')
    lines = my_file.readlines()
    data_list =  []
    for line in lines:
        newLine = re.split(r"[\n|]", line)
        data_list.append(newLine)
    my_file.close()
    return data_list
    


def write_to_files(num_fields, location, url):
    '''Takes in the number of data fields, a location, and a URL
    /  writes table contents of url to files'''
    #get file name and open a file
    filename = get_filename(url).lower()
    #must be absolute path
    #import os /os.getcwd()
    my_file = open('C:\\Users\\BlahKyle\\Documents\\IT391Proj\\DjangoApp\\autocross\\management\\commands\\files\\'+filename+'.txt', 'w') 
    #soup it up
    new_page = requests.get(url)
    new_soup = BeautifulSoup(new_page.text, 'html.parser')

    #get event name
    event_name = ""
    f_list = filename.split('-')
    for word in f_list:
        if True in [char.isdigit() for char in word]:
            pass
        else:
            event_name += word+' '
    # get date Only works with 2022 results
    date= re.findall(r'\d+', filename)
    date = '-'.join(date)
       
    #find all table data
    td_find = new_soup.find_all('td')

    #writing to file intervals of num_fields 
    my_file.write(location.strip() + '\n') 
    my_file.write(date + '\n')
    my_file.write(event_name + '\n')   
    count = 1
    for td in td_find:
        if count % num_fields == 0:
            #td_list.append('\n')
            my_file.write(td.text+'|\n')
        else:
            my_file.write(td.text+'|')
        count += 1
    my_file.close()

def delete_tags(taglist):
    '''Takes a list of <a> tagged urls
   returns a non tagged list aka just the url
    '''
    no_taglist = []
    for urls in taglist:
        if urls['href'].find('files') != -1 or urls['href'].find('msreg') != -1:
            no_taglist.append(urls['href'])

    return no_taglist

def get_filename(url):
    '''Takes a url and extracts the filename'''
    split_list = url.split('/')
    a = split_list[-1]
    split_list = a.split('.')
    filename = split_list[0]
    return filename

if __name__ == "__main__":
    main()