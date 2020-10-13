text = 'standard wrench box end, 3/4'
toolname = text.split(',')
temp = toolname[0].split(' ')

text = ''
for t in temp:
    if text:
        text = text + '-' + t
    else:
        text = t
name = toolname[0]
size = toolname[1].strip()

