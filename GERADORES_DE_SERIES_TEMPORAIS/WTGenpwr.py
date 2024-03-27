#  Get WTG power
#  WTG system model - Hadayeghparast, S., SoltaniNejad Farsangi,
#  A., & Shayanfar, H. (2019). Day-ahead stochastic multi-objective 
#  economic/emission operational scheduling of a large scale virtual 
#  power plant. Energy (Oxford, England), 172, 630–646. 
#  https://doi.org/10.1016/j.energy.2019.01.143

def WTGenPwr(speed, cut_in_speed, cut_out_speed, nom_speed, nom_pwr, Nwtg):

    if speed < cut_in_speed:
        Pwtg = 0
    elif cut_in_speed <= speed < nom_speed:
        Pwtg = nom_pwr * ((speed - cut_in_speed) / (nom_speed - cut_in_speed))**3
    elif nom_speed <= speed < cut_out_speed:
        Pwtg = nom_pwr
    elif cut_out_speed <= speed:
        Pwtg = 0    

    return Nwtg * Pwtg