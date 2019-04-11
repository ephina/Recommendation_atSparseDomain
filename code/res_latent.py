import re
from geopy.geocoders import Nominatim
import geocoder


fin1=open('/data/res_detail','r')
fout=open('/data/res_vector','w')
months=[]
for i in range(12):
	months.append(0)
rest=[]
for ln1 in fin1:
	rname=ln1.split('|')[0].strip()
	rloc=ln1.split('|')[1].strip().split('(')[0].strip()
	rest.append(rname+','+rloc)

uni_rest=list(set(rest))

uni_prop=[]
for i in range(len(uni_rest)):
	uni_prop.append('blank')
	
fin1.close()

fin1=open('/data/res_detail','r')
res_prop=[]
for ln1 in fin1:
	cur_rname=ln1.split('|')[0].strip()
	cur_rloc=ln1.split('|')[1].strip().split('(')[0].strip()
	cur_rest=cur_rname+','+cur_rloc
	cur_index=uni_rest.index(cur_rest)

	cur_pts=[]
	if uni_prop[cur_index] == 'blank':
		cur_rest_vec=ln1.split('|')[2].strip()+'|'+ ln1.split('|')[3].strip()+'|'+ln1.split('|')[4].strip()+'|'+ln1.split('|')[5].strip()
		uni_prop[cur_index]=cur_rest_vec
	else:
		cur_rest_vec=uni_prop[cur_index].split('|')
		cur_rest_rating=(float(cur_rest_vec[0])+float(ln1.split('|')[2].strip()))/2
		cur_rest_ranking=(float(cur_rest_vec[1])+float(ln1.split('|')[3].strip()))/2
		cur_rest_exvggap=ln1.split('|')[4].strip().split(',')
		prev_rest_exvggap=cur_rest_vec[2].split(',')
		for i in range(5):
			cur_pts.append((float(cur_rest_exvggap[i])+float(prev_rest_exvggap[i]))/2)

		cur_pts_str=''
		for i in range(len(cur_pts)):
			cur_pts_str=cur_pts_str+str(cur_pts[i])+','
		cur_res_prop=cur_rest_vec[3]+','+ln1.split('|')[5].strip()
		cur_res_prop_uni=list(set(cur_res_prop.split(',')))
		cur_rpu_uni_str=''
		for i in range(len(cur_res_prop_uni)):
			cur_rpu_uni_str=cur_rpu_uni_str+str(cur_res_prop_uni[i])+','
			res_prop.append(cur_res_prop_uni[i])

		uni_prop[cur_index]=str(cur_rest_rating)+'|'+str(cur_rest_ranking)+'|'+cur_pts_str+'|'+cur_rpu_uni_str

		
cuis_arr=[]

#selecting unique cuisine list
for i in range(len(uni_prop)):
	res_prop=uni_prop[i].split('|')
	cuisine=res_prop[3].split(',')
	for j in range(len(cuisine)):
		cuis_arr.append(cuisine[j])

cuis_uni=list(set(cuis_arr))
cuis_uni.remove('')

#writing to a file
for i in range(len(uni_rest)):
	
	ucuisines=[]
	for k in range(len(cuis_uni)):
		ucuisines.append(0)
	cur_prop=uni_prop[i].split('|')
	cur_cuis=cur_prop[3].split(',')
	for j in range(len(cur_cuis)):
		try:
			cur_index=cuis_uni.index(cur_cuis[j])
		except ValueError:
			pass
		ucuisines[cur_index]=1
	ucui_str=''
	for m in range(len(ucuisines)):
		ucui_str=str(ucuisines[m])+','+ucui_str

	rec=str(uni_rest[i])+'|'+str(cur_prop[0])+'|'+str(cur_prop[1])+'|'+str(cur_prop[2])+'|'+ucui_str
	print rec
	fout.write(rec)
	fout.write('\n')


