# Importing libraries
import random
import time
import requests
import telegram
import difflib
# from difflib_data import *

# test bot api_key: 5321651396:AAEV8S4X98piXMA4SjHHQ3lYxFr1HEiIvmI
# semester bot api_key: 5481119860:AAHj84BYPzx69ulinMLIkFmWp6p1ButNQTg

def get_http(url_array):
    html_list = []
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:39.0)'}
    for website_url in url_array:
        site_html = requests.get(website_url, headers=headers)
        print(site_html)
        html_list.append(site_html.text)
        if site_html.status_code != requests.codes.ok:
            site_html.raise_for_status()
        return html_list  # .content returns the actual website html needed to render it on telegram

def save_html(responseObj):
    with open('site_content.html', 'wb') as f:
        f.write(responseObj)

def ckeckList(lst1, lst2):
    # Comparing each element with first item
    for i in range(len(lst1)):
        if lst1[i] != lst2[i]:
            return i
    return -1

def main():
    # telegram bot parameters
    #sem proj bot api_key = '5481119860:AAHj84BYPzx69ulinMLIkFmWp6p1ButNQTg'
    #using test bot api_key = '5321651396:AAEV8S4X98piXMA4SjHHQ3lYxFr1HEiIvmI' for debug
    api_key = '5321651396:AAEV8S4X98piXMA4SjHHQ3lYxFr1HEiIvmI'
    user_id = '936628732'
    bot = telegram.Bot(token=api_key)

    # import url list:
    with open('url_list_try.txt', 'r') as f:
        url_array = f.read().split('\n')

    old_htmls = get_http(url_array)
    while True:
        try:
            # wait for some seconds
            min_count = random.randint(1, 10)
            #time.sleep(min_count * 60)
            time.sleep(2)
            # perform the get request
            new_htmls = get_http(url_array)
            # check if new hash is same as the previous hash
            chk = ckeckList(old_htmls,new_htmls)
            print(chk)
            if chk == -1:
                old_htmls = new_htmls
                print('Nothing changes, continuing\n')
                continue
            # if something changed in the hashes
            else:
                # notify
                string = "INFO: Something changed in ", url_array[chk], "website"
                print(string)
                text_old_lines = old_htmls[chk].splitlines()
                text_new_lines = new_htmls[chk].splitlines()
                d = difflib.HtmlDiff()
                html_diff = d.make_file(text_new_lines, text_old_lines)
                #print(html_diff)

                bot.send_message(chat_id=user_id, text=string)
                bot.send_message(chat_id=user_id, text=html_diff, parse_mode='html')

        # To handle exceptions
        except Exception as e:
            raise e

if __name__ == "__main__":
    main()