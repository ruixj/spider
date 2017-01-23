class strUtil:
    @staticmethod
    def removeSpace(strIn):
        strIn = strIn.strip()
        strIn = strIn.replace(' ','')
        return strIn

if __name__ == '__main__':
    print strUtil.removeSpace(' a b c')
    print strUtil.removeSpace(' aa bb cc  ')
