# -*- coding: cp1252 -*-
from datetime import datetime

def edad(fechanac):
    hoy = datetime.today().date()
    #fechanac = datetime.strptime(fechanac, "%Y-%m-%d")
    anios = int((hoy - fechanac).days/365.25)
    return anios

