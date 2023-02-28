from pyrogram.types import ReplyKeyboardMarkup

import config
from bot.const import profiles

home_buttons = ReplyKeyboardMarkup(

    [
        ["Menu"],
        ["Settings"],
        # ['About']
    ],
    resize_keyboard=True

)
"""Home"""

menu_buttons = ReplyKeyboardMarkup(
    [
        ['Home'],
        ['Notices'],
        # ['Online Examination Updates'],
        ['Online Admission'],
        ['About']
    ],
    resize_keyboard=True
)
"""Menu"""

notice_buttons = ReplyKeyboardMarkup(
    [
        ['Back'],
        ['Search'],
        ['Today'],
        ['Latest'],
        ['Yesterday'],
        ['Last 7 Days'],
        ['This Month'],
        ['By Date']
    ],
    resize_keyboard=True
)
"""Notices"""


def setting_button(subscribed: bool | None = None):
    """Settings"""
    menu = [['Home']]
    if config.PROFILE == profiles.DEVELOPMENT:
        menu = [['Home'], ['Clear History']]

    if subscribed is None:
        return ReplyKeyboardMarkup(menu, resize_keyboard=True)

    menu = [['Home'], ['Subscribe'] if not subscribed else ['Unsubscribe']]
    if config.PROFILE == profiles.DEVELOPMENT:
        menu = [
            ['Home'],
            ['Subscribe'] if not subscribed else ['Unsubscribe'],
            ['Clear History']
        ]
    return ReplyKeyboardMarkup(menu, resize_keyboard=True)


next_button = ReplyKeyboardMarkup(
    [
        ['Next'],
        ['𝖡𝖺𝖼𝗄']
    ],
    resize_keyboard=True
)
"""Next"""

about_button = ReplyKeyboardMarkup(
    [
        ['Back'],
        ['About Bot'],
        ['About Burdwan Raj College']
    ],
    resize_keyboard=True
)
"""About"""

"""
   // Home  //  |         // Menu / Back //          |    // Notices/𝖡𝖺𝖼𝗄 //   |  // Next //
----------------|------------------------------------|--------------------------|------------------
1.[    Menu   ] |  [  Home                 ]         |   [ Back       ]         |  [ Next ]
                |  [  Notices              ]         |   [ Search     ]         |  [ 𝖡𝖺𝖼𝗄 ]
                | #[  Headlines            ]         |   [ Today      ]         |
                | _[  Online Admission     ]         |   [ Latest     ]         |
                |  [  About                ]         |   [ Yesterday  ]         |
--            --|____________________________________|   [ Last 7 Days]         |
2. [  Settings  ] |         // Settings //           |   [ This Month ]         |
                | --                              -- |   *[ By Date    ]        |
                |            [  Home   ]             |------------------------- +
                |   [  Subscribe ] / [Unsubscribe]   | 
                |          [ Clear History]          |
                |                                    |
--           -- |------------------------------------|
3. #[  About  ] |  // About //
                |  [ Back ]
                |  *[ About Bot ] 
                |  [ About Burdwan Raj College ]
________________|
"""
