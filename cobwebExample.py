from retratodefases import *
import matplotlib.pyplot as plt


def LogisticToIterate(x, r):
    return r*x*(1-x)

def LogisticIterated(x, *, r=1.3):
    return LogisticToIterate(LogisticToIterate(LogisticToIterate(LogisticToIterate(LogisticToIterate(LogisticToIterate(LogisticToIterate(LogisticToIterate(LogisticToIterate(LogisticToIterate(LogisticToIterate(LogisticToIterate(LogisticToIterate(LogisticToIterate(LogisticToIterate(LogisticToIterate(LogisticToIterate(LogisticToIterate(LogisticToIterate(LogisticToIterate(x, r), r), r),r),r),r),r),r),r),r),r),r),r),r),r),r),r),r),r),r)

lolgistic = Cobweb(LogisticIterated, 0.69, [0,1], dF_args={'r':1.3}, yrange=[0,1], max_steps=10, Title='Lol-gistic map cobweb plot')
lolgistic.add_slider('r', valinit=1.3, valinterval=[0,4])
lolgistic.initial_position_slider()
lolgistic.plot()
plt.show()