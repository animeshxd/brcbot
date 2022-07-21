import asyncio

if __name__ == '__main__':
    from bot import client, notice
    import bot.events.home
    import bot.events.menu
    import bot.events.settings
    import bot.events.notices
    import bot.events.next
    import bot.events.about
    try:
        client.run(notice.init())
        client.run()
    finally:
        asyncio.new_event_loop().run_until_complete(notice.close())
