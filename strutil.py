class strUtil:
    @staticmethod
    def removeSpace(strIn):
        strIn = strIn.strip()
        strIn = strIn.replace(' ','')
        return strIn
    @staticmethod
    def removeAttrInCss(style,attr):
        idx = style.find(attr)
        if(idx >=0):
            style1 = style[:idx]
            print 'left:',style1
            style2 = style[idx:]
            print 'right:',style2
            idx2  = style2.find(';')
            if(idx2 >=0):
                style2 = style2[idx2+1:]
            else:
                style2 = ''
            style = style1 + style2
        return style


if __name__ == '__main__':
    print strUtil.removeSpace(' a b c')
    print strUtil.removeSpace(' aa bb cc  ')
    print strUtil.removeAttrInCss('opacity: 0','opacity')
    print strUtil.removeAttrInCss('opacity: 0;','opacity')
    print strUtil.removeAttrInCss('test:1;opacity: 0;','opacity')
