from bot.services.notice.brc import CollegeNoticeClient


async def test():
    async with CollegeNoticeClient() as notices:
        # async for i in notices.iter_until('2022-07-12', ):
        #     print(i)
            
        async for i, d in notices.iter_from(file_id='Notice_06022023_157.pdf'):
            print(i, d)


if __name__ == '__main__':
    import asyncio

    asyncio.new_event_loop().run_until_complete(test())
