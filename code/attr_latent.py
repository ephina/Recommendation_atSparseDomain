import re
from geopy.geocoders import Nominatim
import geocoder

fin1=open('/data/attraction_detail','r')
fout=open('/data/attr_vector','w')

months=[]
for i in range(12):
	months.append(0)
attr=[]
for ln1 in fin1:
	aname=ln1.split('|')[0].strip()
	aloc=ln1.split('|')[1].strip().split('(')[0].strip()
	attr.append(aname+','+aloc)

uni_attr=list(set(attr))

uni_prop=[]
for i in range(len(uni_attr)):
	uni_prop.append('blank')
	
fin1.close()

fin1=open('/data/attraction_detail','r')
attr_prop=[]
for ln1 in fin1:
	cur_aname=ln1.split('|')[0].strip()
	cur_aloc=ln1.split('|')[1].strip().split('(')[0].strip()
	cur_attr=cur_aname+','+cur_aloc
	cur_index=uni_attr.index(cur_attr)

	cur_pts=[]
	if uni_prop[cur_index] == 'blank':
		cur_attr_vec=ln1.split('|')[2].strip()+'|'+ ln1.split('|')[3].strip()+'|'+ln1.split('|')[4].strip()
		uni_prop[cur_index]=cur_attr_vec
	else:
		cur_attr_vec=uni_prop[cur_index].split('|')
		cur_attr_ranking=(float(cur_attr_vec[0])+float(ln1.split('|')[2].strip()))/2
		
		cur_attr_exvggap=ln1.split('|')[3].strip().split(',')
		prev_attr_exvggap=cur_attr_vec[1].split(',')
		for i in range(5):
			cur_pts.append((float(cur_attr_exvggap[i])+float(prev_attr_exvggap[i]))/2)

		cur_pts_str=''
		for i in range(len(cur_pts)):
			cur_pts_str=str(cur_pts[i])+','+cur_pts_str

		cur_attr_prop=cur_attr_vec[2]+','+ln1.split('|')[4].strip()
		cur_attr_prop_uni=list(set(cur_attr_prop.split(',')))
		cur_rpu_uni_str=''
		for i in range(len(cur_attr_prop_uni)):
			cur_rpu_uni_str=str(cur_attr_prop_uni[i])+','+cur_rpu_uni_str
			attr_prop.append(cur_attr_prop_uni[i])

		uni_prop[cur_index]=str(cur_attr_ranking)+'|'+cur_pts_str+'|'+cur_rpu_uni_str
		
attr_arr=[]

#selecting unique attraction property list
for i in range(len(uni_prop)):
	attr_prop=uni_prop[i].split('|')
	props=attr_prop[2].split(',')
	for j in range(len(props)):
		attr_arr.append(props[j])

attr_uni=list(set(attr_arr))
attr_uni.remove('')

#writing to a file
for i in range(len(uni_attr)):
	
	uprops=[]
	for k in range(len(attr_uni)):
		uprops.append(0)
	cur_prop=uni_prop[i].split('|')
	cur_ap=cur_prop[2].split(',')
	for j in range(len(cur_ap)):
		try:
			cur_index=attr_uni.index(cur_ap[j])
		except ValueError:
			pass
		uprops[cur_index]=1
	uap_str=''
	for m in range(len(uprops)):
		uap_str=str(uprops[m])+','+uap_str

	rec=str(uni_attr[i])+'|'+str(cur_prop[0])+'|'+str(cur_prop[1])+'|'+uap_str
	print rec
	fout.write(rec)
	fout.write('\n')


