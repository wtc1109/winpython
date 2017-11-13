import os,sys,time,math
"""
LTx = 20.0
LTy = 90.0
RTx = 40.0
RTy = 80.0
LBx = 5.0
LBy = 10.0
RBx = 25.0
RBy = 6.0
"""
""""""
LTx = 40.0
LTy = 80.0
RTx = 60.0
RTy = 82.0
LBx = 26.0
LBy = 8.0
RBx = 70.0
RBy = 15.0
_lty = max(LTy, RTy)
xx = [-1,-1,-1,-1,-1]
yy = [-1,-1,-1,-1,-1]

spaces = []
while True:
    print _lty
    k1 = (LTy-LBy)/(LTx-LBx)
    b1 = LBy - k1*LBx
    xx[1] = (_lty - b1)/k1
    yy[1] = _lty

    k2 = (RTy-LTy)/(RTx-LTx)
    b2 = RTy - k2*RTx
    xx[2] = (_lty - b2)/k2
    if xx[2] >max(RTx, LTx) or xx[2] < min(RTx, LTx):
        xx[2] = -1
        yy[2] = -1
    else:
        yy[2] = k2*xx[2]+b2
        if yy[2] > max(LTy, RTy) or yy[2] < min(LTy, RTy):
            yy[2] = -1

    k3 = (RTy-RBy)/(RTx-RBx)
    b3 = RTy - k3*RTx
    xx[3] = (_lty - b3)/k3
    if xx[3] > max(RTx, RBx) or xx[3] <min(RTx, RBx):
        xx[3] = -1
        yy[3] = -1
    else:
        yy[3] = k3*xx[3] + b3

    k4 = (RBy-LBy)/(RBx-LBx)
    b4 = RBy - k4*RBx
    xx[4] = (_lty - b4)/k4
    if xx[4] > max(LBx, RBx) or xx[4] <min(LBx, RBx):
        xx[4] = -1
        yy[4] = -1
    else:
        yy[4] = k4*xx[4] + b4

    space = [-1, -1, -1, -1, -1]
    for i in range(2,5):
        if xx[i] < 0:
            continue
        if 2 == i:
            yt1 = k3*xx[i] + b3
            """"""
            if yt1 > max(RTy, RBy) or yt1 < min(RTy, RBy):
                yt1 = 0
            yt2 = k4*xx[i] + b4
            if yt2 > max(LBy, RBy) or yt2 < min(LBy, RBy):
                yt2 == 0
        elif 3 == i:
            yt1 = k2 * xx[i] + b2
            if yt1 > max(RTy, LTy) or yt1 < min(RTy, LTy):
                yt1 = 0
            yt2 = k4 * xx[i] + b4
            if yt2 > max(LBy, RBy) or yt2 < min(LBy, RBy):
                yt2 == 0
        elif 4 == i:
            yt1 = k2 * xx[i] + b2
            if yt1 > max(RTy, LTy) or yt1 < min(RTy, LTy):
                yt1 = 0
            yt2 = k4 * xx[i] + b4
            if yt2 > max(LBy, RBy) or yt2 < min(LBy, RBy):
                yt2 == 0
        if 0 == max(yt2, yt1):
            space[i] = 0.0
            continue
        space[i] = abs(xx[i]-xx[1])*abs(max(yt1,yt2)-yy[1])
    spaces.append(space)
    _lty -= 1.0
    if _lty < min(LBy, RBy):
        print "over"
        break
print "end"

