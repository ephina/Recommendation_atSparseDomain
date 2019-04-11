#user records merge
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn import cluster


fin1=open('/data/user_restaurant','r')
fin2=open('/data/train1','r')
fin3=open('/data/user_vector','r')
fin4=open('/data/res_vector','r')
fin5=open('/data/attr_vector','r')

res_clus_no=4
resu_clus_no=5
attr_clus_no=4
attru_clus_no=4


#restaurant
res_usr_grp=[]
res_usr_dict=dict()
for ln in fin1:
	rec=ln.split('|')
	usr=rec[0].strip()
	key=rec[1].strip()+','+rec[2].strip()
	if key in res_usr_dict:
		prev_val=res_usr_dict[key]
		new_val=prev_val+'|'+usr
		res_usr_dict[key]=new_val
	else:
		res_usr_dict[key]=usr


user_mat=[]
for ln in fin3:
	usr_unit_vec=ln.split('\n')[0].split(',')
	usr_unit_vec.remove('')
	user_mat.append(usr_unit_vec)

res_key=[]
res_vec=[]
for ln in fin4:
	res_key.append(ln.split('|')[0].strip())
	res_vals=ln.split('|')
	res_str=''
	for i in range(len(res_vals)-1):
		res_str=res_str+res_vals[i+1]+','
	unit_res_vec=res_str.strip()[:-1].split(',')
	unit_res_vec.remove('')
	unit_res_vec.remove('\n')
	res_vec.append(unit_res_vec)

rest_con_mat=np.asarray(res_vec)

print "restaurant content matrix created"

X = StandardScaler().fit_transform(rest_con_mat)


spectral = cluster.SpectralClustering(n_clusters=res_clus_no,eigen_solver='arpack',affinity="nearest_neighbors")
spectral.fit(X)

labels_res=[]
for i in range(len(spectral.labels_)):
	labels_res.append(str(spectral.labels_[i].astype(np.int)))

res_dict=dict()
cnt=0
usr_lst=''
for i in range(len(labels_res)):
	str_label=str(labels_res[i])

	if str_label in res_dict:
		prev_val=res_dict[str_label]
		cur_res=res_key[i]
		try:
			usr_lst=res_usr_dict[cur_res]
		except KeyError:
			cnt=cnt+1
			pass
		cur_val=prev_val+'|'+usr_lst
		res_dict[str_label]=cur_val
	else:
		cur_res=res_key[i]
		try:
			usr_lst=res_usr_dict[cur_res]
		except KeyError:
			cnt=cnt+1
			pass
		res_dict[str_label]=usr_lst
for i in range(len(res_dict)):

	str_key=str(i)
	grp_usr_lst=list(set(res_dict[str_key].split('|')))
#	del grp_usr_lst[0]
	labels_usrs=[]
	grp_usr_prop_mat=[]
	for j in range(len(grp_usr_lst)):
		grp_usr_prop_vec=user_mat[int(grp_usr_lst[j])]
		grp_usr_prop_mat.append(grp_usr_prop_vec)

	ip_grp_usr_mat=np.asarray(grp_usr_prop_mat)

	print " restaurant  cluster -- " + str(i)

	X = StandardScaler().fit_transform(ip_grp_usr_mat)

	spectral = cluster.SpectralClustering(n_clusters=resu_clus_no,eigen_solver='arpack',affinity="nearest_neighbors")
	try:
		spectral.fit(X)
		for i in range(len(spectral.labels_)):
			labels_usrs.append(str(spectral.labels_[i].astype(np.int)))
	except ValueError:
		for i in range(len(grp_usr_lst)):
			labels_usrs.append('0')
		pass
	

	usr_dict=dict()
	cnt=0
	for j in range(len(labels_usrs)):
		str_ind = str(labels_usrs[j])
		if str_ind in usr_dict:
			prev_val=usr_dict[str_ind]
			cur_usr=grp_usr_lst[j]
			cur_val=prev_val+'|'+cur_usr
			usr_dict[str_ind]=cur_val
		else:
			cur_usr=grp_usr_lst[j]
			usr_dict[str_ind]=cur_usr
	
	for k in range(len(usr_dict)):
		ind=str(k)
		usrs=usr_dict[ind]
		res_usr_grp.append(usrs)
	del ip_grp_usr_mat

#######
res_usr_aff=[]
for i in range(len(user_mat)):
	res_usr_vec=[]
	for j in range(len(user_mat)):
		if i==j:
			res_usr_vec.append(1.0)
		else:
			res_usr_vec.append(0.0)
	res_usr_aff.append(res_usr_vec)

rusr_grps_mat=[]
for p in range(len(res_usr_grp)):
	rusr_grps_mat.append((res_usr_grp[p]).split('|'))

total_rgrps=1/float(len(rusr_grps_mat))

for i in range(len(res_usr_aff)):
	for p in range(len(rusr_grps_mat)):
		if str(i) in rusr_grps_mat[p]:
			for j in range(len(rusr_grps_mat[p])):
				if str(i) != rusr_grps_mat[p][j]:
					x=i
					y=int(rusr_grps_mat[p][j])
					res_usr_aff[x][y]=res_usr_aff[x][y] + total_rgrps

#************************** restaurant domain completed ***************************************

#attraction
attr_usr_grp=[]
attr_usr_dict=dict()
for ln in fin2:
	rec=ln.split('|')
	usr=rec[0].strip()
	key=rec[1].strip()+','+rec[2].strip()
	if key in attr_usr_dict:
		prev_val=attr_usr_dict[key]
		new_val=prev_val+'|'+usr
		attr_usr_dict[key]=new_val
	else:
		attr_usr_dict[key]=usr

attr_key=[]
attr_vec=[]
for ln in fin5:
	attr_key.append(ln.split('|')[0].strip())
	attr_vals=ln.split('|')
	attr_str=''
	for i in range(len(attr_vals)-1):
		attr_str=attr_str+attr_vals[i+1]+','
	unit_attr_vec=attr_str.strip()[:-1].split(',')
	unit_attr_vec.remove('')
	unit_attr_vec.remove('\n')
	attr_vec.append(unit_attr_vec)

attr_con_mat=np.asarray(attr_vec)

print "attraction content matrix created"


X = StandardScaler().fit_transform(attr_con_mat)

spectral = cluster.SpectralClustering(n_clusters=attr_clus_no,eigen_solver='arpack',affinity="nearest_neighbors")
spectral.fit(X)

labels_attr=[]
for i in range(len(spectral.labels_)):
	labels_attr.append(str(spectral.labels_[i].astype(np.int)))

attr_dict=dict()
cnt=0
usr_lst=''
for i in range(len(labels_attr)):
	str_label=str(labels_attr[i])
	if str_label in attr_dict:
		prev_val=attr_dict[str_label]
		cur_attr=attr_key[i]
		try:
			usr_lst=attr_usr_dict[cur_attr]
		except KeyError:
			cnt=cnt+1
			pass
		cur_val=prev_val+'|'+usr_lst
		attr_dict[str_label]=cur_val
	else:
		cur_attr=attr_key[i]
		try:
			usr_lst=attr_usr_dict[cur_attr]
		except KeyError:
			cnt=cnt+1
			pass
		attr_dict[str_label]=usr_lst

for i in range(len(attr_dict)):
	str_key=str(i)

	grp_usr_lsta=list(set(attr_dict[str_key].split('|')))
	del grp_usr_lsta[0]
	grp_usr_prop_mat=[]
	labels_usrs=[]
	for j in range(len(grp_usr_lsta)):
		grp_usr_prop_vec=user_mat[int(grp_usr_lsta[j])]
		grp_usr_prop_mat.append(grp_usr_prop_vec)

	ip_grp_usr_mat=np.asarray(grp_usr_prop_mat)

	print " attraction  cluster -- " + str(i)

	X = StandardScaler().fit_transform(ip_grp_usr_mat)

	spectral = cluster.SpectralClustering(n_clusters=attru_clus_no,eigen_solver='arpack',affinity="nearest_neighbors")
	try:
		spectral.fit(X)
		for i in range(len(spectral.labels_)):
			labels_usrs.append(str(spectral.labels_[i].astype(np.int)))
	except ValueError:
		for i in range(len(grp_usr_lsta)):
			labels_usrs.append('0')
		pass
	
	usr_dict=dict()
	cnt=0
	for j in range(len(labels_usrs)):
		str_ind = str(labels_usrs[j])
		if str_ind in usr_dict:
			prev_val=usr_dict[str_ind]
			cur_usr=grp_usr_lsta[j]
			cur_val=prev_val+'|'+cur_usr
			usr_dict[str_ind]=cur_val
		else:
			cur_usr=grp_usr_lsta[j]
			usr_dict[str_ind]=cur_usr
		
	for k in range(len(usr_dict)):
		ind=str(k)
		usrs=usr_dict[ind]
		attr_usr_grp.append(usrs)
	del ip_grp_usr_mat

attr_usr_aff=[]
for i in range(len(user_mat)):
	attr_usr_vec=[]
	for j in range(len(user_mat)):
		if i==j:
			attr_usr_vec.append(1.0)
		else:
			attr_usr_vec.append(0.0)
	attr_usr_aff.append(attr_usr_vec)

ausr_grps_mat=[]
for p in range(len(attr_usr_grp)):
	ausr_grps_mat.append((res_usr_grp[p]).split('|'))

total_agrps=1/float(len(ausr_grps_mat))

for i in range(len(attr_usr_aff)):
	for p in range(len(ausr_grps_mat)):
		if str(i) in ausr_grps_mat[p]:
			for j in range(len(ausr_grps_mat[p])):
				if str(i) != ausr_grps_mat[p][j]:
					x=i
					y=int(ausr_grps_mat[p][j])
					attr_usr_aff[x][y]=attr_usr_aff[x][y] + total_agrps


usr_attr_rmat=[]
for i in range(len(user_mat)):
	usr_attr_rvec=[]
	for j in range(len(attr_key)):
		usr_attr_rvec.append(0)
	usr_attr_rmat.append(usr_attr_rvec)



fin8=open('/data/train1','r')
for ln in fin8:
	rec=ln.split('|')
	usr=int(rec[0])
	place=rec[1].strip()+','+rec[2].strip()
	rate=rec[4]
	try:
		place_ind=int(attr_key.index(place)) 
		usr_attr_rmat[usr][place_ind]=int(rate)
	except ValueError:
		continue

# Recommendation Generation
d_sim=0.833
sim_i_k=1

usr_sim_mat=[]
for i in range(len(usr_attr_rmat)):
	usr_sim_vec=[]
	for k in range(len(usr_attr_rmat)):
		if i != k:
			sim_i_k=float(attr_usr_aff[i][k])+float(d_sim*res_usr_aff[i][k])
		else:
			sim_i_k=1
		
		usr_sim_vec.append(sim_i_k)
	usr_sim_mat.append(usr_sim_vec)

attr_fnl_mat=[]
for k in range(len(usr_attr_rmat)):		
	attr_fnl_vec=[]
	for i in range(len(attr_key)):
		tot_rate=0.0
		for j in range(len(usr_attr_rmat)):
			tot_rate=tot_rate+float(usr_sim_mat[k][j]*usr_attr_rmat[j][i])
		attr_fnl_vec.append(tot_rate)
	attr_fnl_mat.append(attr_fnl_vec)

for i in range(len(attr_fnl_mat)):
	print 'Recommendation for -->'+str(i)
	cnt=0
	for j in range(len(attr_key)):
		if attr_fnl_mat[i][j] != 0.0:
			cnt=cnt+1
	print cnt

##below code for testing purpose

ftest=open('/data/test1','r')
tcnt=0
fcnt=0
cnt=0

for ln in ftest:
	trec=ln.split('|')
	lst_loc= attr_fnl_mat[int(trec[0].strip())]

	loc=trec[1].strip()+','+trec[2].strip()
	cur_usr_pref=[]
	for j in range(len(lst_loc)):
		if lst_loc[j] != 0.0:
			cur_usr_pref.append(attr_key[j])
	try:
		print attr_key.index(loc)
		print lst_loc[int(attr_key.index(loc))]
	except ValueError:
		print loc

		
	

print tcnt
print fcnt
print cnt


'''
#diversity

print attr_key.index(loc)

	for j in range(len(lst_loc)):
		if lst_loc[j] != 0.0:
			cur_usr_pref.append(attr_key[j])

	if loc in cur_usr_pref:
		print "true"+ trec[0].strip()
		print loc
		tcnt=tcnt+1
	else:
		print "false"+ trec[0].strip()
		print loc
		fcnt=fcnt+1
	cnt=cnt+1
'''
