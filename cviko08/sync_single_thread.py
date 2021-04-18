import json
import queue
import urllib.request
import webbrowser
import time


def task_get_dog(dog_queue, tab_queue):
    while not dog_queue.empty():
        url = dog_queue.get()
        print(f'Getting new dog')
        time_start = time.perf_counter()
        with urllib.request.urlopen(url) as url:
            data = json.loads(url.read().decode())
            tab_queue.put(data.get('url'))
        elapsed = time.perf_counter() - time_start
        print(f'Getting dog elapsed time: {elapsed:.1f}')
        yield


def task_open_tab(work_queue, open_tab=False):
    while not work_queue.empty():
        url = work_queue.get()
        print(f'Opening tab, URL: {url}')
        time_start = time.perf_counter()
        urllib.request.urlopen(url)
        if open_tab:
            webbrowser.get('chrome').open(url)
        elapsed = time.perf_counter() - time_start
        print(f'Opening tab elapsed time: {elapsed:.1f}')
        yield


def main():
    default_url = 'https://random.dog/woof.json'
    # Create the queue of work
    dog_queue = queue.Queue()
    tab_queue = queue.Queue()

    for _ in range(20):
        dog_queue.put(default_url)
    tasks = [task_get_dog(dog_queue, tab_queue), task_open_tab(tab_queue, False)]

    # Run the tasks
    done = False
    start_time = time.perf_counter()
    while not done:
        for t in tasks:
            try:
                next(t)
            except StopIteration:
                tasks.remove(t)
            if len(tasks) == 0:
                done = True
    elapsed = time.perf_counter() - start_time
    print(f'\nTotal elapsed time: {elapsed:.1f}')


if __name__ == '__main__':
    # use Google Chrome as web browser
    webbrowser.register('chrome',
                        None,
                        webbrowser.BackgroundBrowser(
                            'C://Program Files (x86)//Google//Chrome//Application//chrome.exe'))
    main()
