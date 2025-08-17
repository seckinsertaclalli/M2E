# -*- coding: utf-8 -*-
"""
Created on Tue Dec 29 17:27:00 2020

@author: Seçkin Sertaç LALLI
"""
  
import numpy
import struct

class structtype():
    pass

def readMALA(file_name,fidlog):
    try:  
        info = readGPRhdr(file_name+'.rad')
        fidlog.write('%s.rad dosyası başarıyla okunmuştur.\n' % file_name)
    except:
        fidlog.write('%s.rad dosaysı okunamamıştır. Dosya olmayabilir veya içeriği bozuk olabilir. \n' % file_name)
    try:   
        filename = file_name + '.rd3'
        data = numpy.fromfile(filename, dtype=numpy.int16) 
        nrows=int(len(data)/int(info['SAMPLES']))
        data = (numpy.asmatrix(data.reshape(nrows,int(info['SAMPLES'])))).transpose()  
        fidlog.write('%s.rd3 dosyası başarıyla okunmuştur.\n' % file_name)
        return data, list(info.items())
    except:
        fidlog.write('%s.rd3 dosaysı okunamamıştır. Dosya olmayabilir veya içeriği bozuk olabilir. \n' % file_name)
        
    
def readGPRhdr(filename):
    info = {}
    with open(filename) as f:
        for line in f:
            strsp = line.split(':')
            info[strsp[0]] = strsp[1].rstrip()
    return info

def creatHD(file_name,rad_hd):
    antenna=numpy.double(rad_hd[14][1].split(' MHz')[0])
    fid3 = open(file_name+'.HD','w+')
    fid3.write('%d\n\n' % 1)
    fid3.write('%s\n\n\n\n' % rad_hd[17][1])
    fid3.write('NUMBER OF TRACES   =    %d\n\n' % int(rad_hd[22][1]))
    fid3.write('NUMBER OF PTS/TRC  =  %d\n\n' % int(rad_hd[0][1]))
    fid3.write('TIMEZERO AT POINT  =    0\n\n')
    fid3.write('TOTAL TIME WINDOW  =   %.4f\n\n' % numpy.double(rad_hd[18][1]))
    fid3.write('STARTING POSITION  =     %.4f\n\n' % numpy.double(rad_hd[25][1]))
    fid3.write('FINAL POSITION     =    %.4f\n\n' % numpy.double((numpy.double(rad_hd[22][1])-1)*numpy.double(rad_hd[10][1])))
    fid3.write('STEP SIZE USED     =     %.4f\n\n' % numpy.double(rad_hd[10][1]))
    fid3.write('POSITION UNITS     = METER\n\n')
    fid3.write('NOMINAL FREQUENCY  =   %.4f\n\n' % antenna)
    fid3.write('ANTENNA SEPARATION =     %.4f\n\n' % numpy.double(rad_hd[16][1]))
    fid3.write('PULSER VOLTAGE (V) = 0\n\n')
    fid3.write('NUMBER OF STACKS   = %d\n\n' % int(rad_hd[19][1]))
    fid3.write('SURVEY MODE        = Reflection \n\n')
    fid3.close()
    return

def rad2head(rad_hd):
    head_con = [structtype() for i in range(int(rad_hd[22][1]))]
    for i in range(int(rad_hd[22][1])):
        head_con[i].traces=i+1
        head_con[i].position=(i)*numpy.double(rad_hd[10][1])
        head_con[i].samples=numpy.double(rad_hd[0][1])
        head_con[i].topo=0
        head_con[i].x1=0
        head_con[i].bytes=2
        head_con[i].trac_num=numpy.double(rad_hd[18][1])
        head_con[i].stack=numpy.double(rad_hd[19][1])
        head_con[i].windows=0
        head_con[i].x2=0
        head_con[i].x3=0
        head_con[i].x4=0
        head_con[i].x5=0
        head_con[i].x6=0
        head_con[i].x_rec=0
        head_con[i].y_rec=0
        head_con[i].z_rec=0
        head_con[i].x_tra=0
        head_con[i].y_tra=0
        head_con[i].z_tra=0
        head_con[i].time_zero=0
        head_con[i].zero=0
        head_con[i].x7=0
        head_con[i].time=0
        head_con[i].x8=0
        head_con[i].com0=1.356315642694011e-19
        head_con[i].com1=1.356315642694011e-19
        head_con[i].com2=1.356315642694011e-19
        head_con[i].com3=1.356315642694011e-19
        head_con[i].com4=1.356315642694011e-19
        head_con[i].com5=1.356315642694011e-19
        head_con[i].com6=1.356315642694011e-19
    return head_con
        
def write_dt1(file_name,head,data):
    fid1 = open(file_name+".DT1","wb")
    for i in range(len(head)):  
        fid1.write(struct.pack('@f',head[i].traces))
        fid1.write(struct.pack('@f',head[i].position))
        fid1.write(struct.pack('@f',head[i].samples))
        fid1.write(struct.pack('@f',head[i].topo))
        fid1.write(struct.pack('@f',head[i].x1))
        fid1.write(struct.pack('@f',head[i].bytes))
        fid1.write(struct.pack('@f',head[i].trac_num))
        fid1.write(struct.pack('@f',head[i].stack))
        fid1.write(struct.pack('@f',head[i].windows))
        fid1.write(struct.pack('@f',head[i].x2))
        fid1.write(struct.pack('@f',head[i].x3))
        fid1.write(struct.pack('@f',head[i].x4))
        fid1.write(struct.pack('@f',head[i].x5))
        fid1.write(struct.pack('@f',head[i].x6))
        fid1.write(struct.pack('@f',head[i].x_rec))
        fid1.write(struct.pack('@f',head[i].y_rec))
        fid1.write(struct.pack('@f',head[i].z_rec))
        fid1.write(struct.pack('@f',head[i].x_tra))
        fid1.write(struct.pack('@f',head[i].y_tra))
        fid1.write(struct.pack('@f',head[i].z_tra))
        fid1.write(struct.pack('@f',head[i].time_zero))
        fid1.write(struct.pack('@f',head[i].zero))
        fid1.write(struct.pack('@f',head[i].x7))
        fid1.write(struct.pack('@f',head[i].time))
        fid1.write(struct.pack('@f',head[i].x8))
        fid1.write(struct.pack('@f',head[i].com0))
        fid1.write(struct.pack('@f',head[i].com1))
        fid1.write(struct.pack('@f',head[i].com2))
        fid1.write(struct.pack('@f',head[i].com3))
        fid1.write(struct.pack('@f',head[i].com4))
        fid1.write(struct.pack('@f',head[i].com5))
        fid1.write(struct.pack('@f',head[i].com6))
        for j in range(len(data[:,i])):
            fid1.write(struct.pack('@h',data[j,i]))
    fid1.close()
    return

def cor2gps(filename1,filename2,flog):

    D=read_cor(filename1)
    LAT=numpy.array([])
    LON=numpy.array([])
    try: 
        if len(D)==0:
            flog.write('%s.cor dosyası boştur. GPS dosyası oluşturulamamıştır. \n' % filename1)
            return
        for i in range(len(D)):
            LAT=numpy.append(LAT,D[i].North)
            LON=numpy.append(LON,D[i].East)
        integ = numpy.fix(LAT); fract = numpy.abs(LAT-integ); xi = integ*100+fract*60;
        integ = numpy.fix(LON); fract = numpy.abs(LON-integ); yi = integ*100+fract*60;
        flog.write('%s.cor dosyası başarıyla okunmuştur. \n' % filename1)
    except:
        flog.write('%s.cor dosyası okunamamıştır.' % filename1)
        flog.write('%s.GPS dosyası oluşturulamamıştır. \n' % filename2)
        return
    try:
        fid = open(filename2 +'.GPS','w+')
        for i in range(len(D)):
            fid.write('Trace # %d at position 0\n' % D[i].TrcN)
            fid.write('$GPGGA,185721.00,%9.4f,N,%9.4f,E,2,09,1.2,%.3f,M,-35.1,M,,138*68\n'%(xi[i],yi[i],D[i].Height))
        fid.close()
        flog.write('%s.GPS dosyası başarıyla oluşturulmuştur. \n' % filename2)
        return
    except:
        flog.write('%s.GPS dosyası oluşturulamamıştır. \n' % filename2)
        return
        
def read_cor(filename):
    fid=open(filename+'.cor','r')
    lns=[]
    for line in fid:
        lns.append(line)
    fid.close
    cor_dat = [structtype() for i in range(len(lns))]
    for i in range(len(lns)):
        text=lns[i].split('\t')
        cor_dat[i].TrcN=numpy.double(text[0])
        cor_dat[i].DateTime=numpy.datetime64(text[1]+' '+text[2])
        cor_dat[i].North=numpy.double(text[3])
        cor_dat[i].East=numpy.double(text[5])
        cor_dat[i].Height=numpy.double(text[7])
        cor_dat[i].Q=numpy.double(text[9].split('\n')[0])

    return cor_dat

