import numpy as np
from scipy.optimize import brute
from scipy.optimize import leastsq
from scipy.interpolate import interp1d

def get_sumofgaussians(x,p):
    global prefs
    A_1, A_2, sigma, offset=p
    if sigma>0:
        sumofgaussians= A_1*np.exp(-((x-prefs[0])/sigma)**2)+\
                        A_1*np.exp(-((x-prefs[1])/sigma)**2)+\
                        A_2*np.exp(-((x-prefs[2])/sigma)**2)+\
                        A_2*np.exp(-((x-prefs[3])/sigma)**2)+\
                        offset
    else:
        sumofgaussians=np.ones(x.shape)*offset

    return sumofgaussians

def get_residuals_brute(p,y_meas_stretch,x_stretch):
    err = y_meas_stretch-get_sumofgaussians(x_stretch,p)
    err=sum(err**2)
    return err

def curve_fit_brute(y_meas_stretch,x_fit):
    ranges=((0,1),(0,1),(15,60),((0,.01)))
    p_fit,residual,grid,Jout=brute(get_residuals_brute, ranges, args=(y_meas_stretch,x_fit),Ns=5,full_output=True,finish=None)
    return p_fit

def within_bounds(p):
    A_1, A_2, sigma, offset=p
    if A_1<0 or A_2<0:
        return False
    elif sigma>90 or sigma<15: # sigma>15 constraint in Chen et. al. 2013, about GCaMP6
        return False
    elif offset<0:
        return False
    else:
        return True

def get_residuals_leastsq(p,y,x):
    if not within_bounds(p):
        return 1e12
    err = y-get_sumofgaussians(x,p)
    return err

def stretch(x,y):
    x=np.append(x,360)
    y=np.append(y,y[0])
    f=interp1d(x,y)
    x_new=np.arange(0,360,1)
    return x_new, f(x_new)

def curve_fit_leastsq(p,y_meas_stretch,x_fit):
    leastsq_ans=leastsq(get_residuals_leastsq,p,args=(y_meas_stretch,x_fit), ftol=.001, maxfev=100, full_output=True, diag=(1,1,100,1) )
    p_fit=leastsq_ans[0]
    return p_fit

def get_preferred_orientation(x,y):
    # Niell and Stryker 2008
    x_rad=np.deg2rad(x)
    numerator=sum(y*np.exp(2j*x_rad))
    denomenator=sum(y)
    oPref=np.angle(numerator/denomenator,deg=True)
    if oPref<0:
        oPref+=360
    oPref=oPref/2
    return oPref

def fit(x, y_meas):
    global prefs
    x=np.array(x)
    y_meas=np.array(y_meas)
    oPref=get_preferred_orientation(x,y_meas) # it will always fall between 0 and 180
    oOppos=oPref+180
    oPref2=oPref+360
    oOppos2=oPref-180
    prefs=[oPref,oPref2,oOppos,oOppos2]
    x_fit, y_meas_stretch=stretch(x,y_meas)#DXFV - change to np.absolute(stretch(x,y_meas)) when trace flipped sign

    p_fit = curve_fit_brute(y_meas_stretch,x_fit)
    p_fit = curve_fit_leastsq(p_fit,y_meas_stretch,x_fit)

    if p_fit[0]>p_fit[1]:
        o1=oPref
        o2=oOppos
    else:
        o2=oPref
        o1=oOppos
    oPref=o1
    oOppos=o2

    y_fit=get_sumofgaussians(x_fit,p_fit)
    residuals=get_residuals_leastsq(p_fit,y_meas_stretch,x_fit)
    residual=sum(residuals**2)
    return (p_fit, residual, [x_fit, y_fit],[oPref, oOppos], y_meas_stretch)
