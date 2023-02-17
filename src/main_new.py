from ithor import IthorManager
from slurk import SlurkBot
from argparsing import get_args

token, user, level, variant = get_args()

ithor_manager = IthorManager(level, variant)

slurk_bot = SlurkBot(token, user, 'localhost', 5000, ithor_manager)
slurk_bot.run() 

