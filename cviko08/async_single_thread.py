import asyncio
import webbrowser

import aiohttp
import time


async def task_get_dog(work_queue, tab_queue):
    async with aiohttp.ClientSession() as session:
        while not work_queue.empty():
            url = await work_queue.get()
            print(f'Getting new dog')
            time_start = time.perf_counter()
            async with session.get(url) as response:
                data = await response.json()
                await tab_queue.put(data.get('url'))
            elapsed = time.perf_counter() - time_start
            print(f'Getting dog elapsed time: {elapsed:.1f}')


async def task_open_tab(work_queue, open_tab=False):
    async with aiohttp.ClientSession() as session:
        # wait for first url in queue
        while work_queue.qsize() == 0:
            await asyncio.sleep(0.1)
        while not work_queue.empty():
            url = await work_queue.get()
            print(f'Opening tab, URL: {url}')
            time_start = time.perf_counter()
            async with session.get(url) as response:
                await response.release()
            if open_tab:
                webbrowser.get('chrome').open(url)
            elapsed = time.perf_counter() - time_start
            print(f'Opening tab elapsed time: {elapsed:.1f}')


async def main():
    # Create the queue of work
    default_url = 'https://random.dog/woof.json'
    # Create the queue of work
    dog_queue = asyncio.Queue()
    tab_queue = asyncio.Queue()

    for _ in range(5):
        await dog_queue.put(default_url)

    # Run the tasks
    start_time = time.perf_counter()
    await asyncio.gather(
        task_get_dog(dog_queue, tab_queue),
        task_open_tab(tab_queue, False),
    )
    elapsed = time.perf_counter() - start_time
    print(f'\nTotal elapsed time: {elapsed:.1f}')


if __name__ == "__main__":
    # use Google Chrome as web browser
    webbrowser.register('chrome',
                        None,
                        webbrowser.BackgroundBrowser(
                            'C://Program Files (x86)//Google//Chrome//Application//chrome.exe'))
    asyncio.run(main())
