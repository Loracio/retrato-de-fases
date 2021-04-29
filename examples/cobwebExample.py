from retratodefases import *
import matplotlib.pyplot as plt


def Logistic(x, *, r):
    return r*x*(1-x)

logistic = Cobweb(Logistic, 0.2, [0,1], dF_args={'r':0.12}, yrange=[0,1])
logistic.add_slider('r', valinit=0.12, valinterval=[0,4])
logistic.plot()

def LogisticToIterate(x, r):
    return r*x*(1-x)

def LogisticIterated(x, *, r=3.8):
    return LogisticToIterate(LogisticToIterate(LogisticToIterate(LogisticToIterate(LogisticToIterate(LogisticToIterate(LogisticToIterate(LogisticToIterate(LogisticToIterate(LogisticToIterate(LogisticToIterate(LogisticToIterate(LogisticToIterate(LogisticToIterate(LogisticToIterate(LogisticToIterate(LogisticToIterate(LogisticToIterate(LogisticToIterate(LogisticToIterate(x, r), r), r),r),r),r),r),r),r),r),r),r),r),r),r),r),r),r),r),r)

lolgistic = Cobweb(LogisticIterated, 0.69, [0,1], dF_args={'r':0.1}, yrange=[0,1], max_steps=5)
lolgistic.add_slider('r', valinit=0.1, valinterval=[0,4])
lolgistic.plot()

plt.show()