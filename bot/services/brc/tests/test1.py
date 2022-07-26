from bot.services.brc import Notices


async def test():
    async with Notices() as notices:
        # async for i in notices.iter_until('2022-07-12', ):
        #     print(i)
            
        async for i, d in notices.iter_from(file_id='Notice_12072022_87.pdf'):
            print(i, d)


if __name__ == '__main__':
    import asyncio

    asyncio.new_event_loop().run_until_complete(test())
