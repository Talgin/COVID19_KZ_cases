from bs4 import BeautifulSoup
import requests
import pandas as pd
import schedule
import time
from datetime import datetime
import os
from git import Repo

def parse():    
    path = ""
    cities = [
        "Kazakhstan", #18
        "Nur-Sultan",#1
        "Almaty",#2
        "Shymkent",#8
        "Aqmola oblysy",#5
        "Aqtöbe oblysy",#12
        "Almaty oblysy",#6
        "Atyraū oblysy",#4
        "Shyghys Qazaqstan oblysy",#9
        "Zhambyl oblysy",#7
        "Batys Qazaqstan oblysy",#11
        "Qaraghandy oblysy",#3
        "Qostanay oblysy", #17
        "Qyzylorda oblysy",#10
        "Mangghystaū oblysy",#15
        "Pavlodar oblysy",#14
        "Soltüstik Qazaqstan oblysy",#13
        "Türkistan oblysy",#16
    ]
    city_codes = [
        "KAZ",
        "AST",#1
        "ALA",#2
        "SHY",#8
        "AKM",#5
        "AKT",#12
        "ALM",#6
        "ATY",#4
        "VOS",#9
        "ZHA",#7
        "ZAP",#11
        "KAR",#3
        "KUS", #17
        "KZY",#10
        "MAN",#15
        "PAV",#14
        "SEV",#13
        "YUS",#16
        ]
    soup = BeautifulSoup(requests.get("https://www.coronavirus2020.kz/").content, "html.parser")
    city_cov = soup.findAll(class_ = "city_cov")

    inf = soup.findAll(class_ =  "number_cov marg_med")
    kz_inf = inf[0].text.replace(" ","")

    kz_rec = soup.findAll(class_ = "recov_bl")
    kz_reco = kz_rec[0].text.replace(" ","").replace("Выздоровевших:","")

    kz_dea = soup.findAll(class_ = "deaths_bl")
    kz_death = kz_dea[0]('div')[0].text.replace("Летальных случаев:","").replace(" ","")#=kz_rec[0].text.replace(" ","").replace("Выздоровевших:","")

    f_city_l = []
    f_zar_l = []
    zar_list = city_cov[0]('div')#[i].text
    for i in range(len(zar_list)):
        zar = zar_list[i].text.split('–')[1].replace(" ","")
        city = zar_list[i].text.split('–')[0].replace("ã.","").replace("\t","").replace(" ","").replace(" ","")
        f_zar_l.append(zar)
        f_city_l.append(city)
    infection_list = []
    infection_list.append(kz_inf)
    infection_list.append(f_zar_l[0])   #1 almaty
    infection_list.append(f_zar_l[1])   #2 nursultan
    infection_list.append(f_zar_l[2])   #8 shymkent
    infection_list.append(f_zar_l[3])   #5 akmola
    infection_list.append(f_zar_l[4])   #12 aktobe
    infection_list.append(f_zar_l[5])   #6 almaty obl
    infection_list.append(f_zar_l[6])   #4 atyrau
    infection_list.append(f_zar_l[7])   #9 east kaz
    infection_list.append(f_zar_l[8])   #7 zhambyl
    infection_list.append(f_zar_l[9])   #11 west kaz
    infection_list.append(f_zar_l[10])  #3 karagandy
    infection_list.append(f_zar_l[11])  #17 qostanay
    infection_list.append(f_zar_l[12])  #10 kyzylorda
    infection_list.append(f_zar_l[13])  #15 mangistau
    infection_list.append(f_zar_l[14])  #14 pavlodar
    infection_list.append(f_zar_l[15])  #13 north kaz
    infection_list.append(f_zar_l[16])  #16 turkestan
    
    r_city_l = []
    r_zar_l = []
    recov_list = []
    zar_list = city_cov[1]('div')#[i].text
    for i in range(len(zar_list)):
        zar = zar_list[i].text.split('–')[1].replace(" ","")
        city = zar_list[i].text.split('–')[0].replace("ã.","").replace("\t","").replace(" ","").replace(" ","")
        r_zar_l.append(zar)
        r_city_l.append(city)
    for i in range(len(f_city_l)):
        recov_list.append(0)
    for i in range(len(r_city_l)):
        try:
            recov_list[f_city_l.index(r_city_l[i])] = r_zar_l[i]
        except ValueError:
            pass
    recovered_list = []
    recovered_list.append(kz_reco)
    recovered_list.append(recov_list[0])    #1 almaty
    recovered_list.append(recov_list[1])    #2 nursultan
    recovered_list.append(recov_list[2])    #8 shymkent
    recovered_list.append(recov_list[3])    #5 akmola
    recovered_list.append(recov_list[4])    #12 aktobe
    recovered_list.append(recov_list[5])    #6 almaty obl
    recovered_list.append(recov_list[6])    #4 atyrau
    recovered_list.append(recov_list[7])    #9 east kaz
    recovered_list.append(recov_list[8])    #7 zhambyl
    recovered_list.append(recov_list[9])    #11 West zapad kz
    recovered_list.append(recov_list[10])   #3 karagandy
    recovered_list.append(recov_list[11])   #17 qostanay
    recovered_list.append(recov_list[12])   #10 kyzylorda
    recovered_list.append(recov_list[13])   #15 mangistau
    recovered_list.append(recov_list[14])   #14 pavlodar
    recovered_list.append(recov_list[15])   #13 north kaz
    recovered_list.append(recov_list[16])   #16 turkestan

    d_city_l = []
    d_zar_l = []
    dead_list = []
    zar_list = city_cov[2]('div')#[i].text
    for i in range(len(zar_list)):
        zar = zar_list[i].text.split('–')[1].replace(" ","")
        city = zar_list[i].text.split('–')[0].replace("ã.","").replace("\t","").replace(" ","").replace(" ","")
        d_zar_l.append(zar)
        d_city_l.append(city)
    for i in range(len(f_city_l)):
        dead_list.append(0)
    for i in range(len(d_city_l)):
        try:
            dead_list[f_city_l.index(d_city_l[i])] = d_zar_l[i]
        except ValueError:
            pass
    death_list = []
    death_list.append(kz_death)
    death_list.append(dead_list[0])     #1 almaty
    death_list.append(dead_list[1])     #2 nursultan
    death_list.append(dead_list[2])     #8 shymkent
    death_list.append(dead_list[3])     #5 akmola
    death_list.append(dead_list[4])     #12 aktobe
    death_list.append(dead_list[5])     #6 almaty region
    death_list.append(dead_list[6])     #4 atyrau
    death_list.append(dead_list[7])     #9 east kaz
    death_list.append(dead_list[8])     #7 zhambyl
    death_list.append(dead_list[9])     #11 west kaz
    death_list.append(dead_list[10])    #3 karagandy
    death_list.append(dead_list[11])    #17 qostanay
    death_list.append(dead_list[12])    #10 kyzylorda
    death_list.append(dead_list[13])    #15 mangistau
    death_list.append(dead_list[14])    #14 pavlodar
    death_list.append(dead_list[15])    #13 north kaz
    death_list.append(dead_list[16])    #16 turkestan
    # for i in range(len(cities)):
    #     print(cities[i] + " :\n" + infection_list[i] + ": " + recovered_list[i] + " : " + death_list[i])
    
    cur_date = datetime.now().strftime("%Y-%m-%d")
    todate = [cur_date] * 18
    infections = {'date': todate, 'codes': city_codes, 'names': cities, 'infected': infection_list}
    path_inf = './data/infected.csv'
    infect_df = pd.read_csv(path_inf, sep=',')
    # read_csv and compare dates
    # if last date is current date, just replace this column with new values :)
    if infect_df.iloc[[-1][0]][0] == cur_date:
        sub_df = pd.DataFrame(infections, index=list(range(len(infect_df)-18,len(infect_df))))
        infect_df.update(sub_df)
    else:
        sub_df = pd.DataFrame(infections)
        infect_df = infect_df.append(sub_df, ignore_index=True)
    infect_df.to_csv(path_inf, index=False, sep=',')
    '''
    inf_df = pd.DataFrame({cur_date: infection_list})
    if infect_df.columns[-1] == cur_date:
        infect_df.update(inf_df)
    else:
        infect_df[cur_date] = infection_list
    infect_df.to_csv(path_inf, index=False, sep=';')

    # infections = {'CityCode': city_codes, 'CityName': cities, 'infected': infection_list}
    # infected_df = pd.DataFrame(infections)
    # infected_df.to_csv(path, index=False, sep=';')
    
    path_rec = './test_data/recovered.csv' # 
    recov_df = pd.read_csv(path_rec, sep=';')
    rec_df = pd.DataFrame({cur_date: recovered_list})
    if recov_df.columns[-1] == cur_date:
        recov_df.update(rec_df)
    else:
        recov_df[cur_date] = recovered_list
    recov_df.to_csv(path_rec, index=False, sep=';')

    # recovered = {'CityCode': city_codes, 'CityName': cities, 'recovered': recovered_list}
    # recovered_df = pd.DataFrame(recovered)
    # recovered_df.to_csv(path, index=False, sep=';')
    path_dead = './test_data/deaths.csv' 
    death_df = pd.read_csv(path_dead, sep=';')
    dead_df = pd.DataFrame({cur_date: death_list})
    if death_df.columns[-1] == cur_date:
        death_df.update(dead_df)
    else:
        death_df[cur_date] = death_list
    death_df.to_csv(path_dead, index=False, sep=';')

    # dead = {'CityCode': city_codes, 'CityName': cities, 'death': death_list}
    # deaths_df = pd.DataFrame(dead)
    # deaths_df.to_csv(path, index=False, sep=';')
    '''    
    try:
        repo = Repo(os.getcwd())
        repo.git.add(update=True)
        repo.index.commit('test of automated commit')
        origin = repo.remote(name='origin')
        origin.push()
    except:
        print('error happened')

    #repo.git.commit('-m', 'test of automated commit', author='talgat90.07@gmail.com')

# schedule.every(3).hour.do(parse)
schedule.every().day.at("06:03").do(parse)

while True:
    schedule.run_pending()
    time.sleep(10)
    print('Done at: ', datetime.now())