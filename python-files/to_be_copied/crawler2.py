import time
import os

from hook import Hook
from sender import Shoot

from datetime import datetime
import tset_module
from config2 import constant_vars

from threading import Thread

def fetch_shares():

    url = constant_vars['main_url']
    length_to_select = constant_vars['selecting_length']
    url_fetcher_obj = tset_module.TsetCrawler()
    url_fetcher = url_fetcher_obj.fetch_urls(url, length_to_select)

    return url_fetcher


def fetch_data(urls):
    complete_url = []
    th=Thread(target=database_hook_init)
    th.start()

    shoot = Shoot(constant_vars['qeue_to_db'])
    hook = Hook('qu2')

    data_fetcher_obj = tset_module.TsetCrawler()
    tmp = 0

    today_date = datetime.today().strftime('%Y-%m-%d')

    table_last_check_init(urls)

    for i in urls:
        hook = Hook(constant_vars['qeue_to_crawler'])
        
        make_table_i(i)

        data_fetched = data_fetcher_obj.fetch_data(i)
        trimmer_no = data_fetched.split(';')
        last_update_query = f'request$$$SELECT last_update FROM last_check WHERE share_id={i};'
        shoot.send(last_update_query)

        hook.start_shit()
        last_update = hook.body
        hook.terminate()

        for iterator in trimmer_no:

            row = iterator.split('@')
            timestamp = ''.join(
                (row[0][0:4], '-', row[0][4:6], '-', row[0][6:8]))

            if timestamp < last_update:
                last_check_update_query = f'order$$$UPDATE last_check SET last_update="{today_date}" where share_id={i}; '
                shoot.send(last_check_update_query)
                shoot.send('commit$$$')

                break

            row[0] = timestamp
            if len(row) == 10:
                query = f'order$$$insert into `{i}` values("{row[0]}",{row[1]},{row[2]},{row[3]},{row[4]},{row[5]},{row[6]},{row[7]},{row[8]},{row[9]});'
                shoot.send(query)


def table_last_check_init(urls):
    temp2 = 0

    shoot2 = Shoot(constant_vars['qeue_to_db'])

    for iterator in urls:
        temp2 = temp2 + 1
        column_for_table = f'order$$$INSERT IGNORE INTO last_check(share_id) values({iterator});'
        shoot2.send(column_for_table)

    shoot2.terminate()
    print('initiating done ', temp2)


def make_table_i(i):
    shoot2 = Shoot(constant_vars['qeue_to_db'])
    table_making_query = f'order$$$CREATE TABLE IF NOT EXISTS `{i}`(date DATE NOT NULL,max_price int unsigned,min_price int unsigned, total int unsigned,last_price int unsigned,first_price int unsigned, yesterday_price int unsigned, val bigint, volume bigint unsigned,number int unsigned);'

    shoot2.send(table_making_query)
    shoot2.terminate()

def database_hook_init():

    hook_db=Hook(constant_vars['qeue_to_db'])
    hook_db.start_shit()


def runner():
    start_time = time.time()

    fetched_shares = fetch_shares()
    print('collecting URLs took:', time.time() - start_time)

    start_time = time.time()

    fetch_data(fetched_shares)
    print('crawling data took:', time.time() - start_time)


if __name__ == '__main__':
    runner()
