import json
from urllib.parse import urlparse
from data.extra import *


def is_valid_url(url):
    parsed_url = urlparse(url)
    return all([parsed_url.scheme, parsed_url.netloc])


def settings():
    settings_json = {}
    print("\n")
    logo.logo()

    while True:
        try:
            run(f"\n{bold}{yellow}[{cyan}●{yellow}] {sky_blue2}CHECK THREADS {yellow}({medium_spring_green}minimum {bold}= {medium_spring_green}500 {cyan}- {red}maximum {bold}= {red}5000{yellow}){bold}: ")
            check_threads = int(input())
            if check_threads < 500 or check_threads > 5000:
                error_input()
            else:
                settings_json.update({"threads": check_threads})
                break
        except(ValueError, ):
            continue
    while True:
        run(f"\n{bold}{yellow}[{cyan}●{yellow}] {sky_blue2}CHECK URL {bold}: ")
        check_url = input()
        if is_valid_url(check_url) is False:
            error_input()
        else:
            settings_json.update({"urls": check_url})
            break
    while True:
        run(
            f"\n{bold}{yellow}[{cyan}●{yellow}] {sky_blue2}CHECK TIMEOUT {yellow}({red}maximum {bold}= {red}10{yellow}){bold}: "
            )
        check_timeout = int(input())
        if check_timeout < 0 or check_timeout > 10:
            error_input()
        else:
            settings_json.update({"timeout": check_timeout})
            break
    while True:
        run(f"\n{bold}{yellow}[{cyan}●{yellow}] {sky_blue2}CHECK RETRIES {yellow}({red}maximum {bold}= {red}4{yellow}){bold}: ")
        check_retries = int(input())
        if check_retries < 0 or check_retries > 4:
            error_input()
        else:
            settings_json.update({"retries": check_retries})
            break

    run(f"\n{bold}{yellow}[{cyan}●{yellow}] {sky_blue2}CHECK KEYWORDS {yellow}({green}Y{bold}/{red}n{yellow}) {bold}: ")
    check_keywords = input()

    if check_keywords == "Y" or check_keywords == "y":
        run(f"\n{bold}{yellow}[{cyan}●{yellow}] {sky_blue2}KEYWORDS {yellow}({medium_spring_green}example = name|title{yellow}) {bold}: ")
        keywords_urls = input()
        list_keywords = keywords_urls.split("|")
        list_keywords = [keyword for keyword in list_keywords if keyword]
        settings_json.update({"keywords": list_keywords})

    with open('data/settings.json', 'w', encoding="UTF-8") as json_file:
        json.dump(settings_json, json_file, indent=4, ensure_ascii=False)

    print(f"\n{yellow}[{red}!{yellow}] {medium_spring_green}SETTINGS SAVED SUCCESSFULLY{bold}")
    sleep(5)
