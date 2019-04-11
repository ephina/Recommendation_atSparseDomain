from sklearn.cross_validation import train_test_split
#attraction
fin1=open('/data/user_attraction','r')
ftrain=open('/data/train1','w')
ftest=open('/data/test1','w')
data_arr=[]
label_arr=[]
Dtrain=[]
Ltrain=[]
Dtest=[]
Ltest=[]
for ln in fin1:
	values=ln.split('|')
	data=values[0]+'|'+values[1]+'|'+values[2]+'|'+values[3]
	label=values[4]
	data_arr.append(data)
	label_arr.append(label)
print len(data_arr)
Dtrain,Dtest,Ltrain,Ltest= train_test_split( data_arr, label_arr, test_size=0.20, random_state=1 )
print len(Dtrain)
print len(Dtest)
for i in range(len(Dtrain)):
	record=Dtrain[i]+'|'+Ltrain[i]
	ftrain.write(record)

for i in range(len(Dtest)):
	record=Dtest[i]+'|'+Ltest[i]
	ftest.write(record)

ftest.close()
ftrain.close()
fin1.close()

