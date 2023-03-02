from sqlite_init import init_player_db
import get_sched_urls
from data_converter import chunks
import threading
from worker import worker
from colorama import Fore

try:
    print('Connecting to db')
    print('Started scraping data')
    sched_urls = get_sched_urls.get_sched_urls()
    split_sched_urls = chunks(get_sched_urls.get_sched_urls(), 3)
    for sched_urls in list(split_sched_urls):
        thread = threading.Thread(target=worker, args=[sched_urls])
        thread.start()
except KeyboardInterrupt:
    print(Fore.RED + f'\nABORTING!')