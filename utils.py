from __future__ import print_function

def findPN(n):
    dicOut={}
    tryNum=2
    while n%tryNum == 0 or tryNum < round(n**0.5):
        if n%tryNum == 0:
            dicOut[tryNum] = dicOut[tryNum]+1 if tryNum in dicOut.keys() else 1
            n/=tryNum
        else:
            tryNum+=1
    dicOut[n] = dicOut[n]+1 if n in dicOut.keys() else 1
    dicOut.pop(1,None)
    return dicOut
            
        
if __name__ == "__main__":
    n=input("num:")
    r=findPN(n)
    flagFirst=True
    for k in sorted(r.keys()):
        print( (r'' if flagFirst else r'*' ) + r'{}^{}'.format(k,r[k]),end=r'')
        flagFirst = False
    print(r'')

