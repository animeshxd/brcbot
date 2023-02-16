from bot.services.mongodb import MongoSession
from bot.services.notice.brc import CollegeNoticeClient
from config import MONGO_SRV


async def test():

    async with CollegeNoticeClient() as notices:

        mongo = MongoSession(MONGO_SRV)
        # await mongo.notice_upload_file_info(date='2022-07-21')
        # last = await mongo.notice_get_last_file_info()
        # print(last)
        # subscribers = mongo.user_iter()
        # send_to = []
        notices_ = ""
        try:
            async for index, i in notices.iter_from('2022-07-14', 'Notice_14072022_88.pdf'):
                # text, button = parse(i)
                # await client.send_message()
                date = i.get('dop', '')
                subject = i.get('subject', ' ')
                file = i.get('filename', '')
                if file:
                    file = f'https://burdwanrajcollege.ac.in/docs/notices/{file}'
                notices_ = (
                               f"{index}.\n"
                               f"Date: {date}\n"
                               f"**{subject}**\n"
                               f"[[Download PDF]({file})]\n"
                               f"________________________________\n"
                           ) + notices_
                # await mongo.notice_upload_file_info(date=i['don'], file_id=i['filename'])
            print(notices_)
        except Exception as _:
            # if send_to:
            #     await mongo.users.update({'_id': {'$in': send_to}}, {'$set': {'notified': True}}, multi=True)
            raise _

if __name__ == '__main__':
    import asyncio
    asyncio.new_event_loop().run_until_complete(test())