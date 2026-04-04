from scripts import start_init
import asyncio

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(start_init())
