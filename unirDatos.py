# -*- coding: utf-8 -*-
import pylab as plt
from scipy.stats import mode
import sys
import math
import csv  
import numpy as np
import pandas as pd


#---TORRE METEOROLOGICA

#---velocidad
year=[2012,2013,2014,2015,2016,2017,2018]

"""
dfTotal = pd.DataFrame({'A' : []})

for i in year:
    file_name =  'DatosTorreMeteorologica/velViento/'+str(i)+'.xlsx'
    print(i)
    df = pd.read_excel(io=file_name, names=['fecha','velAvg1','velAvg2','velStd1','velStd2'])
    dfTotal=dfTotal.append(df,ignore_index=True)

dfTotal['IT1']=dfTotal['velStd1']/dfTotal['velAvg1']
dfTotal['IT2']=dfTotal['velStd2']/dfTotal['velAvg2']

plt.figure(1)   
plt.plot(dfTotal['IT2'][0:(52705*2)],linestyle=' ',marker='o',linewidth=0.1,markersize=0.1)
plt.ylim(0, 1)
#plt.xlim(0, 10)
"""




#---temperatura
dfT = pd.DataFrame({'A' : []})

for i in year:
    file_name =  'DatosTorreMeteorologica/Temperatura/'+str(i)+'.xlsx'
    print(i)
    df = pd.read_excel(io=file_name, names=['fecha','ambient','T1','T2'])
    dfT=dfT.append(df,ignore_index=True)


dfT['grad']=(dfT['T2'] - dfT['T1'])/(79-3)
plt.figure(2)   
plt.plot(dfT['grad'][0:57000],'ob',linewidth=0.1,markersize=0.01)
plt.plot([0,50000],[0.01,0.01],'r')
plt.ylim(-0.04,0.01)
#plt.xlim(0, 10)

plt.figure(3)   
plt.plot(dfT['T1'][0:57000],'ob',linewidth=0.1,markersize=0.5)
#plt.ylim(0, 1)
#plt.xlim(0, 10)







"""
#---------------------------------------------------------------------
#------DATOS DE RAWSON CADA 10MIN-------------------------------------
#busca el viento para un cierto periodo
#---------------------------------------------------------------------
f = open("alturasHub.csv", 'rb') # opens the csv file
xyz=[]
reader = csv.reader(f)  # creates the reader object
for row in reader:   # iterates the rows of the file in orders
    xyz.append(row)    # prints each row
f.close()      # closing

alturas=[]
for i in range(len(xyz)):
    alturas.append(float(xyz[i][2]))


f = open("rawson10min.csv", 'rb') # opens the csv file
tabla=[]
reader = csv.reader(f)  # creates the reader object
for row in reader:   # iterates the rows of the file in orders
    tabla.append(row)    # prints each row
f.close()      # closing
    
#---recorto la tabla con el perido que quiero------------------------
#una semana
#tabla=tabla[74593:75589] #dato cada 10 min: 1/9/2013, hora:0, min: 10, hasta 7/9/2013, hora:22, min: 0 

#3 dias pronostico
#tabla=tabla[16272: 16705] #dato cada 10 min: 23/7/2012, hora:0, min: 0, hasta 26/7/2012, hora:0, min: 0 

#1 AÑO 2012-2013
#tabla=tabla[0: 52560] #dato cada 10 min: 1/4/2012, hora:0, min: 0, hasta 1/4/2013, hora:0, min: 0 
#MEDIO AÑO 
#tabla=tabla[0: 26280] #dato cada 10 min: 1/4/2012, hora:0, min: 0, hasta 1/4/2013, hora:0, min: 0 

#1 semana sep 2012
#tabla=tabla[24000: 25000] #dato cada 10 min: 14/9/2012, hora:16, min: 0, hasta 21/9/2012, hora:14, min: 30 
#2 dias 
#tabla=tabla[24500: 24790] #dato cada 10 min: 14/9/2012, hora:16, min: 0, hasta 21/9/2012, hora:14, min: 30 

print('dato cada 10 min: '+tabla[0][2]+'/'+tabla[0][1]+'/'+tabla[0][0]+', hora:'+tabla[0][3]+', min: '+tabla[0][4]+', hasta '+tabla[len(tabla)-1][2]+'/'+tabla[len(tabla)-1][1]+'/'+tabla[len(tabla)-1][0]+', hora:'+tabla[len(tabla)-1][3]+', min: '+tabla[len(tabla)-1][4]+' ')

dia=[]
horaInicial1=float(tabla[0][4])
diaActual=((horaInicial1/60)/24.00)

#---PARA PLOTEAR LOS DATOS-----------------------------------
intensidad=[]
direccion=[]
Ptotal=[]

#para la rosa de vientos y potencia total
intensidadOk=[]
direccionOk=[]
PtotalOk=[]
for i in range (len(tabla)):
    malo=False
    #---recolecto datos para la rosa de vientos (sin Nans)
    if (np.isnan(float(tabla[i][5])) or np.isnan(float(tabla[i][7])) or np.isnan(float(tabla[i][182])) ):
        malo=True
    if (malo==False):
        intensidadOk.append(float(tabla[i][5]))
        direccionOk.append(float(tabla[i][7]))
        PtotalOk.append(float(tabla[i][ 181])+float(tabla[i][ 182])) 
    intensidad.append(float(tabla[i][5]))
    direccion.append(float(tabla[i][7]))
    Ptotal.append(float(tabla[i][ 181])+float(tabla[i][ 182])) 

    dia.append(diaActual)
    diaActual=diaActual+(1/(6*24.00))

#---guardo las potencias de cada turbina
PturbinaOk=[]
for i in range (len(tabla)):
    malo=False
    #---recolecto datos para la rosa de vientos (sin Nans)
    for j in range (len(tabla[i])):
        if (np.isnan(float(tabla[i][j]))):
            malo=True
    if (malo==False):
        PturbinaOk.append(tabla[i][95:(95+43)]) 

Pturbina=[]
turbinas=43
for t in range (turbinas):
    Pturb=[]
    for j in range(len(PturbinaOk)):
        Pturb.append(float(PturbinaOk[j][t]))
    Pturbina.append(np.mean(Pturb))

intensidadMedia=round(np.mean(intensidadOk),1)
direccionMasFrec=int(mode(direccionOk)[0][0])
potenciaMedia=round(np.mean(PtotalOk),1)
print('intensidad media: '+str(intensidadMedia))
print('direcccion mas frecuente: '+str(direccionMasFrec))
print('potencia totoal media: '+str(potenciaMedia))
pl.figure(1)     
pl.plot(dia,intensidad,'r-',linewidth=0.1,label="Rawson IyII - intensidad cada 10 min") 
pl.plot([dia[0],dia[len(dia)-1]],[intensidadMedia,intensidadMedia],'k-',linewidth=1,label="Intensidad media: "+str(intensidadMedia))
pl.legend(loc='upper right', frameon=False)
pl.xlabel('dias')  
pl.ylabel('Intensidad')  
pl.ylim(0, 30)
pl.xlim(0, dia[len(dia)-1])
pl.grid()
pl.savefig("intensidadMedida.png", dpi = 300)     
pl.show() 
pl.clf()
 
pl.figure(2)    
pl.scatter(dia,direccion, s=0.1, c='r',label="Rawson IyII - direccion cada 10 min") 
pl.plot([dia[0],dia[len(dia)-1]],[direccionMasFrec,direccionMasFrec],'r-',linewidth=2,label="Direcion mas frecuente: "+str(direccionMasFrec))
pl.ylim(0, 450)
pl.xlim(0, dia[len(dia)-1])
pl.legend(loc='upper right', frameon=False)
pl.xlabel('dias')  
pl.ylabel('Direccion')  
pl.grid()
pl.savefig("direccionMedida.png", dpi = 300)    
pl.show() 
pl.clf()

pl.figure(3) 
pl.scatter(intensidad,Ptotal, s=0.1, c='k',label="Rawson IyII - potencia parque cada 10 min") 
pl.plot([0,25],[1800*43,1800*43],'r-',linewidth=1,label="max")
pl.legend(loc='upper right', frameon=False)
pl.xlabel('U')  
pl.ylabel('Potencia')  
pl.ylim(-4000, 100000)
pl.xlim(0, 25)
pl.grid()
pl.savefig("PotenciayU.png", dpi = 300)    
pl.show() 
pl.clf()

pl.figure(7) 
turb=[]
for i in range (turbinas):
    turb.append(i+1)
pl.scatter(turb,Pturbina, s=10, c='k') 
pl.plot([0,44],[np.mean(Pturbina),np.mean(Pturbina)],'r-',linewidth=1,label="potencia media")
pl.legend(loc='lower right', frameon=False)
pl.xlabel('N turbina')  
pl.ylabel('Potencia media')  
pl.ylim(600, 1000)
pl.xlim(0, 43)
pl.grid()
pl.savefig("PotenciaMedTurbinas.png", dpi = 300)    
pl.show() 
pl.clf()

pl.figure(10) 
pl.scatter(turb,alturas, s=10, c='k') 
pl.plot([0,44],[np.mean(alturas),np.mean(alturas)],'r-',linewidth=1,label="altura media")
pl.legend(loc='lower right', frameon=False)
pl.xlabel('N turbina')  
pl.ylabel('Altura')  
#pl.ylim(600, 1000)
pl.xlim(0, 43)
pl.grid()
pl.savefig("alturaHubTurbinas.png", dpi = 300)    
pl.show() 
pl.clf()
################################################################################    
#------ANALISIS DE DATOS

#---busco la intensidad y potencia media segun la direccion
UDirList=[]
PDirList=[]
UDir=[]
PDir=[]

Dir=[]
for i in range(361):
    Dir.append(i)
    UDirList.append([])
    PDirList.append([])
    
for i in range (len(intensidadOk)):
    UDirList[int(direccionOk[i])].append(intensidadOk[i])
    PDirList[int(direccionOk[i])].append(PtotalOk[i])
    
for i in range(len(Dir)):
    if len(UDirList) > 0:
        UDir.append(np.mean(UDirList[i]))
        Dirs=[]
        for j in range (len(UDirList[i])):
            Dirs.append(Dir[i])
        pl.figure(6)     
        pl.scatter(Dirs,UDirList[i],s=0.05, c='r') 
        
    if len(PDirList) > 0:
        PDir.append(np.mean(PDirList[i]))
        Dirs=[]
        for j in range (len(PDirList[i])):
            Dirs.append(Dir[i])
    else:
        UDir.append(np.nan)
        PDir.append(np.nan)
 
pl.figure(6)     
pl.plot(Dir,UDir,'r-',linewidth=2,label="Intensidad Media") 
pl.plot([dia[0],dia[len(dia)-1]],[intensidadMedia,intensidadMedia],'b-',linewidth=2,label="Intensidad media total: "+str(intensidadMedia))
pl.legend(loc='upper right', frameon=False)
pl.xlabel('Dir')  
pl.ylabel('Intensidad')  
pl.ylim(0, 30)
pl.xlim(0, 360)
pl.grid()
pl.savefig("IntensidadMed-Dir.png", dpi = 300)     
pl.show() 
pl.clf()
   
 
pl.figure(8)     
pl.plot(Dir,PDir,'r-',linewidth=2,label="Potencia Media") 
pl.plot([dia[0],dia[len(dia)-1]],[potenciaMedia,potenciaMedia],'b-',linewidth=2,label="Potencia media total: "+str(potenciaMedia))
pl.legend(loc='upper right', frameon=False)
pl.xlabel('Dir')  
pl.ylabel('Potencia')  
pl.ylim(0, potenciaMedia*2)
pl.xlim(0, 360)
pl.grid()
pl.savefig("PotenciaMed-Dir.png", dpi = 300)     
pl.show() 
pl.clf()    
#
#################################################################################    
##------ROSA DE VIENTOS
#
#from windrose import WindroseAxes
#
##A quick way to create new windrose axes...
#def new_axes():
#    fig = pl.figure(figsize=(8, 8), dpi=80, facecolor='w', edgecolor='w')
#    rect = [0.1, 0.1, 0.8, 0.8]
#    ax = WindroseAxes(fig, rect, axisbg='w')
#    fig.add_axes(ax)
#    return ax
#
##...and adjust the legend box
#def set_legend(ax):
#    l = ax.legend()
#    pl.setp(l.get_texts(), fontsize=10)
#
#
#pl.figure(4)  
#ax = new_axes()
#ax.bar(direccionOk, intensidadOk, normed=True, opening=0.8, edgecolor='white')
#set_legend(ax)
#pl.savefig('rosaVientosRawson', dpi = 300)     
#pl.show
#pl.clf
#
#pl.figure(5)  
#ax = new_axes()
#ax.bar(direccionOk, PtotalOk, normed=True, opening=0.8, edgecolor='white')
#set_legend(ax)
#pl.savefig('rosaPotenciaTotalRawson', dpi = 300)     
#pl.show
#pl.clf
#
#################################################################################  
##------IMPRIMO LA TABLA CON TIEMPO, VIENTO y POTENCIAS (TURBS Y TOTAL)
#
#salida=open('salidaVientoRawson10min.csv','w')
#
#cantidadTurbinas=43
##escribo encabezado
#salida.write('an~o, mes, dia, hora, minutos, U, Dir, ')
#for i in range(cantidadTurbinas):
#    salida.write('P'+str(i+1)+' ,')
#salida.write('Ptotal ')
#for i in range(cantidadTurbinas):
#    salida.write(',T'+str(i+1)+' ')
#salida.write('\n')
#
#
#for i in range(len(tabla)):
#    salida.write(str(tabla[i][0])+','+str(tabla[i][1])+','+str(tabla[i][2])+','+str(tabla[i][3])+','+str(tabla[i][4])+','+str(tabla[i][5])+','+str(tabla[i][7])+',')
#    for p in range (cantidadTurbinas): #escribo las potencias de cada turbina
#        salida.write(str(tabla[i][95+p])+' ,')
#    salida.write(str(float(tabla[i][181])+float(tabla[i][182]))) #escribo la potencia total
#    salida.write('\n')   
#    
#salida.close()
"""