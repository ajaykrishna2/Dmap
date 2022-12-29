chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
charsLen = len(chars)

def numberToStr(num):
    s = ""
    while num:
        s = chars[num % charsLen] + s
        num //= charsLen
        return (s)

def strToNumber(numStr):
    num = 0
    for i, c in enumerate(reversed(numStr)):
        num += chars.index(c) * (charsLen ** i)
        return (num)

print(strToNumber('A'))

print(numberToStr(5))
