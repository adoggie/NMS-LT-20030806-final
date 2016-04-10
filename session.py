

from Tix import *
from tktable import *
import time
import SimpleDialog
import tkMessageBox

from win32com.client import *
import pythoncom 

import ado
from constdef import *

import net_train

_DEBUG=1


data ={'user':None,'psw':None,
'loginip':None,'logintime':None
}

app_title=unicode("NMS1900ֱ��վ����ϵͳ")

#####����ͨ�Ų���
mss_addr='202.109.13.151'
mss_listen_port=8000
#####ϵͳ����
area_warningcount_interval =1000*20  #(��)�Ƽ����5����,������ʾ��4�ָ澯����ˢ��ʱ����
send_cmd_fresh_interval=10	#�����б�״̬��ѯˢ��ʱ����
no_response_timeout = 10 #�豸��Ӧ��ʱ(��)
browse_rowsets=100  #��־��ѯ�����¼����
#
#ado���������ַ���
dbcnnstr_template ='Provider=SQLOLEDB.1;Persist Security Info=False;User ID=sa;Initial Catalog=NMSDB_LINGTONG;Data Source=%s'	
dbcnnstr=""

dbcnn=None		#ado�������Ӷ���
user =None 	#��ǰ��½�û�����
log =None	#ϵͳ��־����

#������Ϣ  [{'fieldname':fieldvalue}]
areas=[]
#�û���Ϣ
users=[]
#��Ӧ���б�  
providers=[]

#��Ӧ�̵Ĳ�Ʒ�б� {providerid:[ '��Ʒ�ĵ�����¼(��getdata())' ]}
products=[]

#�豸�ͺ���ϸ
repeatertype=[]

#�������ñ�
param_configs=[]

#�豸��Ϣ
#repeaters=[]
#��ѯʱ��
query_interval ={'L1':10,'L2':20,'L3':30,'L4':40,'L5':50}

#ϵͳ�����ļ�
sys_config_file = 'Dbini'
sys_run_config_file = 'syspt'	#ϵͳ���в��� 

_busy=None


#�豸���в���Ĭ��ֵ
control_run_param_default=0

#runtime variable
login_ok=0
form_status = None	#״̬����
form_warningflag = None	#״̬����
form_send_status=None	#״̬����
root=None	#system tk
form_sys_set =None	#ϵͳ��������

	
		
def getdata(sql):
	''' ȡ������'''
	ret =[]
	try:
		cnn = dbcnn
		rs = cnn.Select(sql)
		fields = cnn.getFields(rs)		
		while not rs.EOF:
			v ={}
			for i in fields:
				v[i]=rs.Fields.Item(i).Value				
			ret.append(v)	#���һ����¼			
			rs.MoveNext()
	except:
		ret =[]
	return ret


import log

#�豸״̬��ѯ
def query_it(devid):
	data = grab_tcp_package(devid)
	data[4]="%s"%CMD_REMOTE_TEST
	data[8]= "%s"%getsequence()
	sendstr = "%s"%string.join(data,',')
	try:	
		if  net_train.send2mss(sendstr)!=1	:
			raise 1
		
		log.recLog(str(devid),log.LOG_STATUS,data[8])
		
		#tkMessageBox.showwarning(unicode(''),unicode('�ѷ���״̬��ѯ!'))
	except:
		
		tkMessageBox.showwarning(unicode('����!'),unicode('��MSSͨ��ʧ��!'))
		
#�������ܲ�ѯ		
def batch_query_status(areaid):
	for i in user.repeaters:
		if i['AREA_ID']==areaid:			
			query_it(i['ID'])
	
#���ܲ�����ѯ
def query_netparam(devid):
	data = grab_tcp_package(devid)
	data[4]="%s"%CMD_REMOTE_SYS_QUERY
	data[8]= "%s"%getsequence()
	sendstr = "%s"%string.join(data,',')
	try:	
		if net_train.send2mss(sendstr)!=1	:
			raise 1
		log.recLog(str(devid),log.LOG_PARAM_QUERY,data[8])
		#tkMessageBox.showwarning(unicode(''),unicode('�ѷ������ܲ�ѯ!'))
	except:
		tkMessageBox.showwarning(unicode('����!'),unicode('��MSSͨ��ʧ��!'))
		
#�������ܲ�����ѯ		
def batch_query_netparam(areaid):
	for i in user.repeaters:
		if i['AREA_ID']==areaid:	
			query_netparam(i['ID']) 
	

#ȡ�豸���õص�
def getsite(row):
	title =''	
	
	title = row['SITE']
	if title==None:
		title=''
	return title


#ȡ�豸����
def getdevtitle(row):
	title =''	
	title = row['NAME']
	return title


#ƥ������
#����ָ��һ�����ݼ����б���ֶ�����
# rs ='select * from area'
# match(rs,'ID','INT',100,'NAME')
# �ڼ�¼����rs�в���id =100�ļ�¼�����ҷ��ش˼�¼��NAME�ֶ����ݣ�����������STRING

def match(target_rs,target_field,datatype,value,result_field):
	
	
	for row in target_rs:
		if row[target_field]==None:
			continue
		if datatype=='INT':					
			if int(row[target_field])==value:
				return row[result_field]
		if datatype=='STRING':
			
			if row[target_field].strip()==value:
				return row[result_field]
	return None
	

##��ȡ����
def grab_tcp_package(devid):
	sql = "select * from repeaterinfo where id=%s"%str(devid)
	rs = getdata(sql)
	rs = rs[0]
	rs2 =None
		
	set=[]
	set.append("%04d"%rs['REPEATERTYPE']+"%05d"%rs['REPEATER_ID']+"%05d"%rs['EQUIPMENT_ID']+rs['REPEATER_PHONE'].strip())
	set.append(str(rs['REPEATERTYPE']))
	set.append(str(rs['REPEATER_ID']))
	set.append(str(rs['COMM_MODE']))
	set.append('cmd_type')
	set.append(str(rs['EQUIPMENT_ID']))
	set.append(str(rs['REPEATER_PHONE']).strip())
	query_phone=rs['QUERY_PHONE']
	if query_phone==None:	 
		query_phone =" "
	else :
		if query_phone.strip()=="":
			query_phone=" "
		else:
			query_phone = query_phone.strip()
		
	set.append(query_phone)
	set.append('trans_no')
	return set
	

#ȡ�洢���̵����к�
def getsequence(spname='GetGuid',key=None):	
	try:		
		comm = Dispatch('ADODB.Command')
		comm.ActiveConnection = dbcnn.adoConn			
		comm.CommandText= spname
		comm.CommandType = 4
	
		comm.Parameters.Refresh()
		#p1 =comm.CreateParameter('sequence',131,2)
		#comm.Parameters.Append(p1)
		comm.Execute()
		return int(comm.Parameters.Item(1).Value)	
	except:
		if _DEBUG:
			print 'get sequence number error!'			
		return 0
	
	
			
			
#����澯����
#��ǰ�豸�澯״̬����
#ˢ�¸澯������ʱ������豸״̬��¼
current_dev_statuses=[]

#����豸�Ƿ���Ӧ��ʱ
def is_timeout(devid):
	'''����豸�Ƿ���Ӧ��ʱ,����豸û��״̬��¼�����س�ʱ'''
	
	current_time = time.time()
	
	for i in current_dev_statuses:
		if devid == i['REPEATER_ID']:
			status_time = i['OPTTIME']		;
			
			#print current_time
			#print int(status_time)
			#print time.localtime(int(status_time))
			#print current_time - float(status_time)

			if current_time-int(status_time) > no_response_timeout:
				return 1
			
	return 0
			
def get_warning_type(devid):
	'''ȡ�豸��ǰ�澯����
		ͬʱҪ��⵱ǰ�豸�Ƿ�������豸��ȡ��߸澯״ֵ̬
	'''	
	ret = 0
	for i in current_dev_statuses:
		if i["REPEATER_ID"]==devid:
			ret = i["WARNINGLEVEL"]
			if ret == None:
				ret =0
			return ret
	#����豸��״̬��¼���������� ״̬0
	return 	0  

#################################################			
#ȡ�ɲ�������	
def get_areas():
	'''ȡ�ɲ�������	
	'''
	id=2
	sql = 	"select a.area_id as id,b.name from userarea a,area b,userinfo c \
			where a.user_id=%s  and a.user_id=c.id and a.area_id = b.id "%id
	#print sql
	sql = sql.upper()
	
	areas = getdata(sql)
	#print self.areas	
#	sql ="select a.rights_id,b.name from userrights a, rights b,userinfo c \
#			where a.user_id=2  and a.user_id=c.id and a.rights_id = b.id "%self.id		
#	
#	self.rights = session.getdata(sql)
#	print sql

	return areas
	
def get_rights():
	return self.rights


def get_warning_enableflag(devtype):
	'''  ȡ�澯ʹ�ܱ�־��Ϣ  
		devtype -- �豸����	
	'''
	pado = ado.PAdo(dbcnnstr,1)
	#pado.Select('')


if __name__=='__main__'	:
	print getsequence('getguid')


