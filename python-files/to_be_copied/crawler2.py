import time
import os
from hook import Hook
from sender import Shoot
from datetime import datetime
import tset_module
from tset_module.config2 import constant_vars


def fetch_shares():
    url = constant_vars['main_url']
    length_to_select = constant_vars['selecting_length']
    url_fetcher_obj = tset_module.TsetCrawler()
    url_fetcher = url_fetcher_obj.fetch_urls(url, length_to_select)
    return url_fetcher


def fetch_data(urls):
    complete_url = []
    

    shoot = Shoot('qu1')
    hook=Hook('qu2')

    path = constant_vars["crawled_data_dir"]
    os.makedirs(path, exist_ok=True)
    data_fetcher_obj = tset_module.TsetCrawler()
    tmp = 0

    today_date = datetime.today().strftime('%Y-%m-%d')
    table_last_check_init(urls, db)

    for i in urls:
        make_table_i(i, db)
        tmp = tmp + 1
        if tmp > 50:
            return 0
        data_fetched = data_fetcher_obj.fetch_data(i)
        trimmer_no = data_fetched.split(';')

        last_update_query = f'request$$$SELECT last_update FROM last_check WHERE share_id={i};'

        shoot.send(last_update_query)
        var=hook.start_shit()

        last_update2 = curs.fetchall()[0]
        for last_update in last_update2:
            pass
        last_update = str(last_update)

        for jj in trimmer_no:
            row = jj.split('@')
            timestamp = ''.join(
                (row[0][0:4], '-', row[0][4:6], '-', row[0][6:8]))
            if timestamp < last_update:
                last_check_update_query = f'order$$$UPDATE last_check SET last_update="{today_date}" where share_id={i}; '
                curs.execute(last_check_update_query)
                break

            row[0] = timestamp
            if len(row) == 10:

                query = f'order$$$insert into `{i}` values("{row[0]}",{row[1]},{row[2]},{row[3]},{row[4]},{row[5]},{row[6]},{row[7]},{row[8]},{row[9]});'

                curs.execute(query)
        db.commit()


def table_last_check_init(urls, db):
    temp2 = 0
    curs = db.cursor()
    for ii in urls:
        temp2 = temp2+1
        column_for_table = f'response$$$INSERT IGNORE INTO last_check(share_id) values({ii});'
        curs.execute(column_for_table)
    db.commit()
    print('initiating done ', temp2)


def make_table_i(i, db):
    table_making_query = f'response$$$CREATE TABLE IF NOT EXISTS `{i}`(date DATE NOT NULL,max_price int unsigned,min_price int unsigned, total int unsigned,last_price int unsigned,first_price int unsigned, yesterday_price int unsigned, val bigint, volume bigint unsigned,number int unsigned);'
    curs = db.cursor()
    print(type(db), type(curs))
    curs.execute(table_making_query)
    db.commit()


def runner():
    start_time = time.time()
    fetched_shares = fetch_shares()
    print('collecting URLs took:', time.time() - start_time)
    start_time = time.time()
    fetch_data(fetched_shares)
    print('crawling data took:', time.time() - start_time)

def hooker_run():


    
if __name__ == '__main__':
    runner()