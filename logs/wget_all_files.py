import os

URL = "playtak.com/games/{}.ptn"
CMD = "wget -P wgot/ {}"

def get(i):
    run = CMD.format(URL).format(i)
    print("Executing", CMD.format(URL.format(i)))
    os.system(run)

for i in range(1, 240789):
    get(i)
