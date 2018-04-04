strxx = "◎译　　名　茉莉牌局 / 茉莉的牌局 / 决胜女王(台) / 莫莉游戏(港)"
# print(strxx.index(' '))
# print(strxx[0:strxx.index(' ')])
print(strxx)
strxx = strxx.replace(' ', '')
strxx = strxx.replace('　', '')
print(strxx)
if '◎译名' in strxx:
    print(strxx[strxx.index('◎译名') + 3:strxx.index('/')])
# print(strxx.replace(' ' | '　', ''))
# print(strxx.replace('  ', ''))
# print(strxx.replace('　　', ''))
# print(strxx.replace('　', ''))
