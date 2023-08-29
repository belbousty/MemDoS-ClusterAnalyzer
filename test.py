import re

def check(pod):
    if re.search(r"-m$", pod):
        print('LOL')
    else:
        print('PSS')

if __name__ == '__main__':
    check("victim-02")
    check("victim-02-m")