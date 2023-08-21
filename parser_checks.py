# -*- coding: utf-8 -*-
"""
Created on Thu Jan 27 16:45:13 2022

@author: Likhith Chilukurthi
"""

import os
import zipcodes
import re
import json
import base_parser
import sys
import csv
from uszipcode import SearchEngine
import pyap
from commonregex import CommonRegex

sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')

class Check:

    def __init__(self):
        self.date = None
        self.bankname = []
        self.photo_id = None
        self.victim = None
        self.amount = []
        self.zipcode = []
        self.city=[]
        self.state = []

    def get_date_and_id_from_title(self, title):
        re1 = title.split("@")
        photo_id = re1[0].split("_")[1]
        date = re1[1].split("_")[0]
        return photo_id, date

    '''def check_zipcode(self,content):
        # return all the information related to zipcode too
        # libpostal to get address
        # find zipcode 5-digit and extract other into
        # get the city info
        result = set()
        for i in re.finditer(r'(?!\A)\b\d{5}(?:-\d{4})?\b', content):
            if zipcodes.is_real(i.group()):
                state  = zipcodes.matching(i.group())[0]['state']
                if state in content:
                    result.add((i.group(),state))
        return result'''

    def check_bankname(self, content):
        # return bank name if finds a match from the given names
        # print(Banks)
        bank_list = ["bank of america", "suntrust", "j.p.morgan", "bankozk", "hhsb", "first convenience bank", 
        "chase", "regions", "navy fed", "citibank", "usb financial services", "us bank", "pnc bank", "capital one", 
        "td bank", "wells fargo", "Citizen Bank", "fifth third bank", "first fidelity bank", "commerce bank", "us bank", 
        "first citizens bank", "capital one", "first republic bank", "u.s. century bank","active duty", "american express",
        "aspirations bank", "b&t Bank", "banco felabella", "bb&t", "barrera farms", "bmo harris bank", "burning bank",
        "chime", "choice financial group", "citi", "commerce", "cryptocurrency", "discover", "DUPACO community credit union",
        "fair financial", "Go2Bank", "green dot bank", "hancock whitney", "huntington", "IPC bank", "Indi",
        "Kabbage", "key bank", "M&T bank", "Marcus", "Navy Fedral credit union", "New York Community Bank",
        "RCB bank", "Reve", "RF bank finance", "Robin Financial", "T Mobile Money", "usaa", "varo bank", "WAFD",
        "woodforest", "5 star bank", "allegiance bank", "ally bank", "alpine bank", "amerant bank", "ann arbour",
        "ArrowPointe", "ArrowPointe federal credit union", "bancorp south", "atlantic union bank", "bank of madison",
        "bank of texas", "bank of the james", "bank of tokyo", "bank united", "bank york", "bbva", "bragg mutual",
        "c&F bank", "carotrans", "cashier's check", "cathay bank", "CBC bank", "centerstate", "charlotte metro",
        "cnb","comerica", "community bank","community credit union","county educators","county national bank",
        "crown bank", "customers bank", "Dexterous mold and tool","eagle bank", "east west bank",
        "edfed", "erie insurance group","evolution risk advisors","executive banking","federal","federal credit union",
        "federal incentive check","federal tax return","fidelity bank","financial credit union","first national bank",
        "first south bank","first state bank","floridian community bank","founders","freedom bank","frost",
        "gamebreaker","german american bank","grove bank and trust", "guilford savings bank","harford bank",
        "havensavings bank","hudson valley credit union","huntington","IBM southeast employees","ibmsecu",
        "invesco","investors bank","jeff bank","key bank","key bank national association","lncb national bank",
        "lgfcu","lindell bank","marine","merril","merrimac valley credit union","metabank","midflorida",
        "morgan stanley","motion federal credit union","NC dept of revenue","ncua","new brunswick credit union",
        "northeast family", "northern trust","northview bank","nycb","ocean bank","pacific premier bank",
        "pacific western bank","patriot bank","peoples bank","peoples bank and trust","people's united bank",
        "planters bank","popa federal credit union","popular bank","prosperity bank","professional bank",
        "roselle bank","ruth smith","santandar bank","seacoast bank","select bank and trust", "signature bank",
        "simmons bank","south atlantic bank","south state bank","sovereign bank","space coast credit union",
        "spencer savings bank","state employees credit union","state of florida","stifel bank","sun east",
        "sunshine bank","sunstate bank","td bank","texena bank","the bank of new york mellon","the family bank",
        "the merchants national bank","towne bank","treasury of illinois","tri counties bank","u.s capital advisors",
        "u.s central bank","u.s century bank","ubs","umb bank","union county savings bank","united southern bank",
        "united states treasury","valley bank","vanguard municipal money market fund","valley neational bank",
        "voya institutional trust", "walmart moneycard","webster bank", "chime",'1st source bank','allegiance bank','american national bank','american national bank of texas',
        'amplify credit union','anb bank','associated bank',
        'atlantic union bank','bank of america','bank of the west','banner bank','bb&t','bbva','bbva usa','bmo harris bank','c1 bank','cadence bank','capital bank',
        'capital one','capital one 360','catholic federal credit union','chase','chase bank','citigroup','citi','citizencredit union','citizens bank','citizens first bank',
        'citizens national bank','cnb bank','columbia bank','comerica bank','community bank','community banks of colorado','community first bank','community state bank',
        'compeer financial','cornerstone bank','cornerstone community financial','country bank','crossfirst bank','crystal lake bank & trust','crystal valley credit union',
        'csb bank','dakota community bank','dakota heritage bank','dakota state bank','dakota valley bank','davies county bank','ddn credit union','diamond bank',
        'dime community bank','discover bank','east west bank','edward jones credit union','empower credit union','esl federal credit union','farm bureau bank','fifth third bank',
        'first citizens bank','first community bank','first citizens national bank','first community credit union','first community financial bank','first farmers bank & trust',
        'first financial bank','first financial credit union','first financial bank, na','first financial northwest bank','first midwest bank','first national bank',
        'first national bank and trust','first national bank of omaha','first national bank texas','first national community bank','first national of nebraska','first state bank',
        'first state bank and trust','first western bank','firstbank','fluvanna bank','fnb bank','fnb community bank','frost bank','ge capital','ge capital retail bank','gemb',
        'genisys credit union','george weston limited','goldman sachs','goldman sachs bank usa','green dot bank','hancock bank','hancock whitney bank','harborstone credit union',
        'hawaii national bank','hillcrest bank','hilltop national bank','houston texans credit union','huntington bank','icici bank','inland bank','integrity bank','interbank',
        'investors bank','investors community bank','jpmorgan chase','keybank','klein bank','kleinbank','lake city bank','lakeside bank','landmark bank','latitude financial services',
        'legacytexas bank','liberty bank','libertyville bank & trust','lincoln savings bank','little river bank','logix credit union','m&t bank','madison county state bank',
        'maine savings federal credit union','manchester credit union','maspeth federal savings and loan association','mecu credit union','merchants bank','merchants and farmers bank',
        'midfirst bank','midland states bank','milwaukee credit union','minnwest bank','mizzou credit union','mounthaven bank','mt. morris bank','mt. sterling national bank',
        'mt. vernon bank & trust','mutual of omaha bank','navy federal credit union','nebraska state bank','nebraska state bank and trust','nebraska state bank of commerce',
        'nicolet national bank','north community bank','north central bank','north shore bank','northwest bank','northwest bank and trust','northwest community credit union',
        'northwest savings bank','northwestfederal credit union','norwegian american credit union','norwegian american hospital employees credit union','norwegian credit union',
        'ocean first bank','omega federal credit union','oneamerica bank','oneaz credit union','oneunited bank','orchard bank','pinnacle bank','pinnacle bank nebraska','pnb bank',
        'pnc bank','pnc financial services','premier bank','premier bank inc','premier credit union','premier members credit union','premier valley bank','provident bank',
        'provident credit union','ps bank','pscu','puget sound cooperative credit union','pulse federal credit union','quest credit union','quorum federal credit union','reliant bank',
        'republic bank','republic bank of chicago','republic bank of nebraska','republic bank of texas','republic first bank','republic state mortgage','republican valley bank',
        'richmond state bank','rock valley credit union','rockland trust','roundbank','rural heritage bank','rural heritage bank and trust','rural state bank','s&t bank','s&t bank, na',
        'safra national bank of new york','sandy spring bank','santander bank','saratoga national bank','saratoga national bank and trust','sbt bank','scotia bank','scotiabank','sdccu',
        'seaboard federal credit union','seacoast bank','seaway bank and trust','seaway community bank','security bank','security bank of kansas city','security credit union',
        'security first bank','security state bank','security state bank of marine','sefcu','selco community credit union','service credit union','servicefirst bank','serviceone credit union',
        'shawmut bank','shore bank','shore community bank','signature bank','skagit state bank','skokie bank','skokie valley community federal credit union','smartbank','smith county national bank',
        'sns bank','south jersey federal credit union','southern trust bank','southwest missouri bank','southwest national bank','sparks state bank','sparks state bank and trust','spencer savings bank',
        'spire credit union','standard bank and trust','standard bank and trust company','standard chartered','standard chartered bank','star financial bank','star one credit union','state bank',
        'state bank and trust','state bank and trust company','state bank financial','state bank of india','state bank of liang','state bank of long island','state bank of the lakes',
        'state department federal credit union','state employees credit union','state farm bank','statewide federal credit union','stonebridge bank','stonegate bank','suntrust bank','svb',
        'svb financial group','synergy bank','texas capital bank','texas first bank','texas bank and trust','texas trust credit union','the bank','the bank of clarendon','the bank of edwardsville',
        'the bank of greene county','the bank of hancock county','the bank of harrison county','the bank of herrin','the bank of henderson','the bank of hickman','the bank of hinsdale',
        'the bank of jamestown','the bank of kentucky','the bank of lancaster county','the bank of madison','the bank of marin','the bank of middletown','the bank of missouri',
        'the bank of new glarus and sugar river','the bank of new york mellon','the bank of nova scotia','the bank of oak ridge','the bank of perryville','the bank of south carolina',
        'the bank of southside virginia','the bank of tampa','the bank of the commonwealth','the bank of the james','the bank of the ozarks','the bank of tennessee','the bank of tony',
        'the bank of washington','the bank of wayne county','the bank of western massachusetts','the bank of white county','the bank of winchester','the bank of york','the banks company',
        'the banks of the san juans','the banks of the san juans, n.a.','the banks of the san juans, na','the benjamin bank','the california bank','the capital bank',
        'the cedar valley bank and trust company',"the citizen's national bank",'the city national bank of florida','the commercial and savings bank','the community bank',
        'the community bank of raymore','the community bank of the chesapeake','the cooperative bank','the credit union of colorado','the fairfield national bank',
        'the farmers and merchants state bank of argonia','the farmers bank','the farmers bank and trust','the farmers bank and trust company','the farmers bank of china',
        'the farmers state bank','the farmers state bank of la porte city','the fauquier bank','the fauquier bank, na','the fayette county bank','the fidelis group',
        'the flint hills bank','the focus bank','the frederick county bank','the freeport state bank','the fremont bank','the fremont company','the fremont national bank',
        'the fremont national bank and trust','the fremont national bank and trust company','the fremont national bank of joliet','u.s. bank','u.s. bank national association',
        'u.s. bank, na','u.s. bancorp','u.s. bankcorp','ucbi','ucb&t','ucb&t co','ucb&t company','ucb&t, co','ucb&t, company','ucb&t, national association','ucb&t, na',
        'valley national bank','xceed financial credit union','yadkin bank','yadkin valley bank and trust','yadkin valley bank and trust company','yadkin valley financial corporation',
        'zb','zions bancorporation','zions bank']
        
        re = set()
        
        ##### check bank name in text #####
        content_lower = content.lower()
        # print()
        for i in bank_list:
            if i in content_lower:
                re.add(i)
        return re

    def check_amount(self, content):
        # return the amounts present in the content
        result = set() 
        # find with digit and decimal
        for i in re.finditer(r"\d{1,3}(?:,\d{3})*(?:\.\d+)", content):
            # print(i)
            result.add(i.group())
        #find with S digit and deciaml
        # for i in re.finditer(r"(\b[S][0-9]*\.[0-9]*)|\b[S][0-9]+", content):
        #     print(i.group())
        #     result.add(i.group()[1:])
        for i in re.finditer(r"\b[S]\d{1,3}(?:,\d{3})*(?:\.\d+)|\b[S]\d{1,3}(?:,\d{3})*", content):
            # print(i.group())
            result.add(i.group()[1:])
        # find with $ digit and decimal
        # for i in re.finditer(r"\$\d+(?:\.\d+)?", content):
        #     print(i.group())
        #     result.add(i.group()[1:])
        for i in re.finditer(r"\$\d{1,3}(?:,\d{3})*(?:\.\d+)|\$\d{1,3}(?:,\d{3})*", content):
            # print(i.group())
            result.add(i.group()[1:])
            print(result)
        # print(result)
        return result
    
    ###Method to Parse City
    '''def check_city(self,content):
        result = set()
        index_of_state=0
        search = SearchEngine()
        for i in re.finditer(r'(?!\A)\b\d{5}(?:-\d{4})?\b', content):
            if zipcodes.is_real(i.group()):
                state  = zipcodes.matching(i.group())[0]['state']
                if("-" in i.group()):
                   zipcode = search.by_zipcode(i.group().split("-")[0])
                else:
                    zipcode = search.by_zipcode(i.group())
                    
                #'uszipcode.model.SimpleZipcode'
                if(zipcode and (state in content)):
                    if(zipcode.post_office_city and (zipcode.post_office_city.split(',')[0].lower() in content.lower())):
                        print("The city is", zipcode.post_office_city.split(',')[0])
                        result.add(zipcode.post_office_city.split(',')[0])
                    else:
                        for i in zipcode.common_city_list:
                            if i.lower() in content.lower():
                                print("The city is", i)
                                result.add(i)
                                break
                            
                                
                
                if state in content:
                    index_of_state=content.index(state)
                    #regexp = "[0-9]{1,3} .+, .+, [A-Z]{2} [0-9]{5}"
                    #address = re.findall(regexp, content)
                    for j in range(index_of_state-2,0,-1):
                        if(content[j]==" "):
                            #print('City is',content[j+1:index_of_state-2])
                            if(content[index_of_state-2]==","):
                                result.add(content[j+1:index_of_state-2])
                                print(content[j+1:index_of_state-2])
                            else:
                                result.add(content[j+1:index_of_state-1])
                                print(content[j+1:index_of_state-1])
                            break
        print("SSSSSSSSSSSSSSSSSSSSSSSSSSSS",result)           
        return result'''
    ###Method to Parse street
    def check_street(self,content):
        address_list=[]
        zipcodes_list=[]
        search = SearchEngine()
        check_signed_dates = re.findall("\d{1,2}/\d{1,2}/\d{4}|\d{1,2}-\d{1,2}-\d{4}", content)
        door_number_search = re.findall("\d+-+\d+/+\d*.\s[a-z]*", content)
        po_box_search=re.findall("[pP.]+[oO.]+.?[BboOxX]*.\d*",content)
        adresses=pyap.parse(content, country='US')
        print("door Numbers",door_number_search)
        print("Addresses are",adresses)
        for i in re.finditer(r'(?!\A)\b\d{5}(?:-\d{4})?\b', content):
                if zipcodes.is_real(i.group()):
                    zipcodes_list.append(i.group())
                   
        print(adresses)
        print(zipcodes_list)
        print(content)
        for adress in adresses:
            print(adress)
            pincode=''
            state=""
            city=""
            street=""
            for i in re.finditer(r'(?!\A)\b\d{5}(?:-\d{4})?\b', str(adress)):
                pincode=i.group()
            if("-" in pincode):
                zipcode = search.by_zipcode(pincode.split("-")[0])
            else:
                zipcode = search.by_zipcode(pincode)
            if(zipcode):
                state=zipcode.state
                if(zipcode.common_city_list):
                    for i in zipcode.common_city_list:
                            if i.lower() in str(adress).lower():
                                city=i
                                street=str(adress).lower().split(city.lower())[0]
                                for o in po_box_search:
                                    if(o in street):
                                        po_box_search.remove(o)
                               
                                for k in door_number_search:
                                    if(k in street):
                                        door_number_search.remove(k)
                                    if(street!="" and street in content.lower() and (k in content.lower()) and  content.lower().index(k)>=0 and (content.lower().index(street)-50>=0) and (k in content[content.lower().index(street)-50:content.lower().index(street)])):
                                        street=content[content.lower().index(k):content.lower().index(street)].lower()+street
                                        door_number_search.remove(k)
            if(pincode!=""):
                address_list.append([street,city,state,pincode])
                print("zipcode being removed is",pincode)
                if(pincode in zipcodes_list):
                    zipcodes_list.remove(pincode)
        
            
        for i in zipcodes_list:
            city_find=""
            address_find=""
            if zipcodes.is_real(i):
                state_find  = zipcodes.matching(i)[0]['state']
                print("state is",state_find)
                if("-" in i):
                    zipcode = search.by_zipcode(i.split("-")[0])
                else:
                    zipcode = search.by_zipcode(i)
                if(zipcode and zipcode.common_city_list):
                    for j in zipcode.common_city_list:
                        if j.lower() in content.lower():
                            city_find=j
                            break
                
                if state_find in content:
                    address_find=''
                    #myregex = "(?:p\.?\s*o\.?|post\s+office)(\s+)?(?:box|[0-9]*)?"
                    parsed_text = CommonRegex(content).street_addresses
                    for k in parsed_text:
                        print("****************",k)
                        if(k in content[content.index(i)-100:content.index(i)]):
                            print("Addresses are: ",content[content.index(k):content.index(state_find)].replace(city_find, ''))
                            address_find=content[content.index(k):content.index(state_find)].title().replace(city_find.title(), '')
                            address_list.append([address_find,city_find,state_find,i])
                    for o in po_box_search:
                        if(o in address_find):
                            po_box_search.remove(o)
                    for k in door_number_search:
                        if(k in address_find):
                            door_number_search.remove(k)   
                
                for nn in door_number_search:
                    if(content.index(i)-100>=0 and nn in content[content.index(i)-100:content.index(i)]): 
                        address_Drnum_find=content[content.index(nn):content.index(i)].title().replace(state_find.title(), '').replace(city_find.title(), '').replace(',', '')
                        door_number_search.remove(nn) 
                        address_list.append([address_Drnum_find,city_find,state_find,i])
                for pp in  po_box_search:
                    if(content.index(i)-100>=0 and pp in content[content.index(i)-100:content.index(i)]): 
                        address_pb_find=content[content.index(pp):content.index(i)].title().replace(state_find.title(), '').replace(city_find.title(), '').replace(',', '')
                        po_box_search.remove(pp) 
                        address_list.append([address_pb_find,city_find,state_find,i])
                        print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
                        
                zipcodes_list.remove(i)
                    
                    
                        
    
        print("Searched post boxes",po_box_search)
        print("Searched door numbers",door_number_search)            
        return address_list
                                
                                
                
                
          
            
            
            
    
        

    def data_assign_rowby(self, photo_id, date, bank, whole_address_list, amount, writer):
        list_to_set=[tuple(lst) for lst in whole_address_list]
        whole_address_list=list(set(list_to_set))
        whole_address_list=[list(lst) for lst in whole_address_list]
        num_banks = len(bank)
        num_address_whole=len(whole_address_list)
        num_amount = len(amount)
        # amount = [float(i) for i in amount]
        amount.sort()

        if num_banks == 0 and num_address_whole == 0:
            writer.writerow([photo_id, date, "", "", "", "",""])

        if len(bank) == 1:
            for i in range(0,max(num_banks,num_address_whole)):
                bank_name = bank[0]
                if num_address_whole > 0:
                    this_address=whole_address_list.pop(0)
                    zipcode = this_address[3]
                    state = this_address[2]
                    city=this_address[1]
                    address=this_address[0]
                    num_address_whole -=1
                else:
                    zipcode = ""
                    state = ""
                    city=""
                    address=""
                    
                if num_amount > 0:
                    amt = amount.pop()
                    num_amount -= 1
                else:
                    amt = ""
                writer.writerow([photo_id, date, bank_name, zipcode,address,city, state, amt])
        else:
            for i in range(0,max(num_banks,num_address_whole)):
                if num_banks > 0:
                    bank_name = bank.pop(0)
                    num_banks -= 1
                else:
                    bank_name = ""
                if num_address_whole > 0:
                    this_address=whole_address_list.pop(0)
                    zipcode = this_address[3]
                    state = this_address[2]
                    city=this_address[1]
                    address=this_address[0]
                    num_address_whole -=1
                else:
                    zipcode = ""
                    state = ""
                    city=""
                    address=""
                    
                if num_amount > 0:
                    amt = amount.pop()
                    num_amount -= 1
                else:
                    amt = ""
                writer.writerow([photo_id, date, bank_name, zipcode,address,city, state, amt])

if __name__ == '__main__':
    folder_textdoc_path = sys.argv[1]
    textdoc_paths = base_parser.get_textdoc_paths(folder_textdoc_path)
    headerList = ['Pic ID', 'Date', 'Bank Name', 'Zipcode','Address','City', 'State', 'Amount']
    with open('june_checks'+'.csv','w', newline='', encoding='utf-8') as f1:
        dw = csv.DictWriter(f1, delimiter=',', fieldnames=headerList)
        dw.writeheader()
        writer=csv.writer(f1, delimiter=',')#lineterminator='\n',
    # for i in np.arange(0,9):
    #     row = data[i]
    #     writer.writerow(row)
  
        for text_doc in textdoc_paths:
            whole_address_list=[]
            writer=csv.writer(f1, delimiter=',')
            check = Check()
            file_name = os.path.basename(text_doc)

            #### parse photo id and date
            photo_id, date = check.get_date_and_id_from_title(file_name)
            if photo_id:
                check.photo_id = photo_id
                print("Photo id is:",photo_id)
            if date:
                check.date = date

            ### parse zipcode and state
            with open(text_doc, encoding = "utf-8") as f:
                content = f.readlines()
            if content:
                text_des = content[-1]
            else:
                writer.writerow([check.photo_id, check.date, "", "", "","", "",""])
                continue
            #print((text_des).encode('utf-8'))
            
            
            ### Parse Street
            if content:
                whole_address_list=check.check_street(text_des)
                
             
 
            
            
 
            #### parse bankname
                info_bank = check.check_bankname(text_des)
                check.bankname.extend([i for i in info_bank])
                for i in check.bankname:
                    print("bank:",i)
                info_amount = check.check_amount(text_des)
                check.amount.extend(i for i in info_amount)

            # for i,code in enumerate(check.zipcode):
            #     writer.writerow()

            #print(check.photo_id, check.date, check.bankname, check.zipcode, check.state, check.amount)
            # writer.writerow([check.photo_id, check.date, check.bankname, check.zipcode, check.state, check.amount])
            check.data_assign_rowby(check.photo_id, check.date, check.bankname,whole_address_list , check.amount, writer)

        # exit()
        