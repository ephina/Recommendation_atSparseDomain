import re
from geopy.geocoders import Nominatim
import geocoder


fin1=open('/data/user_detail','r')
fout=open('/data/user_vector','w')
months=[]
styles=[]
ustyles=[]
for i in range(12):
	months.append(0)
for ln1 in fin1:
	istyle=ln1.split('|')[3].strip().split(',')
	for i in range(len(istyle)):
		styles.append(istyle[i])
fin1.close()

styles_uni=set(styles)
sty_uni_lst=list(styles_uni)

sty_uni_lst.remove('')
sty_uni_lst.remove('Not Known')

for i in range(len(sty_uni_lst)):
	ustyles.append(0)

fin1=open('/data/user_detail','r')


for ln1 in fin1:
	uid=ln1.split('|')[0].strip()
	loc=ln1.split('|')[1].strip().split(',')[0]
	if(loc != 'Not Known'):
		geolocator=Nominatim()
		location=geolocator.geocode(loc)
		g=geocoder.elevation([location.latitude,location.longitude])
	
		if(g.meters<=30):
			nos=10
		elif(g.meters>30 and g.meters<1000):
			nos=100
		else:
			nos=1000
	else:
		nos=0


	vmonths=ln1.split('|')[2].strip().split(',')
	for i in range(len(vmonths)):
		if vmonths[i]=='Jan':
			months[0]=months[0]+1
		elif vmonths[i]=='Feb':
			months[1]=months[1]+1
		elif vmonths[i]=='Mar':
			months[2]=months[2]+1
		elif vmonths[i]=='Apr':
			months[3]=months[3]+1
		elif vmonths[i]=='May':
			months[4]=months[4]+1
		elif vmonths[i]=='Jun':
			months[5]=months[5]+1
		elif vmonths[i]=='Jul':
			months[6]=months[6]+1
		elif vmonths[i]=='Aug':
			months[7]=months[7]+1
		elif vmonths[i]=='Sep':
			months[8]=months[8]+1
		elif vmonths[i]=='Oct':
			months[9]=months[9]+1
		elif vmonths[i]=='Nov':
			months[10]=months[10]+1
		elif vmonths[i]=='Dec':
			months[11]=months[11]+1
	u_tour=[]
	for i in range(len(months)):
		u_tour.append(months[i])

	vsty=ln1.split('|')[3].strip().split(',')
	for i in range(len(vsty)):
		try:
			sty_index=sty_uni_lst.index(vsty[i])  
			
		except ValueError:
			pass
		ustyles[sty_index]=1
		
	
	u_points=re.sub("[^0123456789]","",ln1.split('|')[4].strip())

	u_bdgs=re.sub("[^0123456789]","",ln1.split('|')[5].strip())
	user_vec=[]
	user_vec.append(nos)
	for i in range(len(u_tour)):
		user_vec.append(u_tour[i])
	for i in range(len(ustyles)):
		user_vec.append(ustyles[i])
	user_vec.append(int(u_points))
	user_vec.append(int(u_bdgs))
	
	ustyles=[]
	for i in range(len(sty_uni_lst)):
		ustyles.append(0)
	
	for i in range(12):
		months[i]=0
	record=''
	for i in range(len(user_vec)):
		record=record+str(user_vec[i])+','
	print record
	fout.write(record)
	fout.write('\n')
fout.close()
	
