import os

import growtopia

server = growtopia.Server(("127.0.0.1", 10000))

growtopia.ErrorManager.set_callback(lambda error: print(error))

for ext in os.listdir("collections"):
    if ext.endswith(".py"):
        server.load_extension(ext, "collections")


server.start()
