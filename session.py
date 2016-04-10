

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

app_title=unicode("NMS1900直放站网管系统")

#####网络通信参数
mss_addr='202.109.13.151'
mss_listen_port=8000
#####系统参数
area_warningcount_interval =1000*20  #(秒)推荐间隔5分钟,区域显示的4种告警数量刷新时间间隔
send_cmd_fresh_interval=10	#命令列表状态查询刷新时间间隔
no_response_timeout = 10 #设备响应超时(秒)
browse_rowsets=100  #日志查询浏览记录总数
#
#ado数据连接字符串
dbcnnstr_template ='Provider=SQLOLEDB.1;Persist Security Info=False;User ID=sa;Initial Catalog=NMSDB_LINGTONG;Data Source=%s'	
dbcnnstr=""

dbcnn=None		#ado数据连接对象
user =None 	#当前登陆用户对象
log =None	#系统日志对象

#区域信息  [{'fieldname':fieldvalue}]
areas=[]
#用户信息
users=[]
#供应商列表  
providers=[]

#供应商的产品列表 {providerid:[ '产品的单条记录(见getdata())' ]}
products=[]

#设备型号详细
repeatertype=[]

#参数配置表
param_configs=[]

#设备信息
#repeaters=[]
#轮询时间
query_interval ={'L1':10,'L2':20,'L3':30,'L4':40,'L5':50}

#系统配置文件
sys_config_file = 'Dbini'
sys_run_config_file = 'syspt'	#系统运行参数 

_busy=None


#设备运行参数默认值
control_run_param_default=0

#runtime variable
login_ok=0
form_status = None	#状态窗体
form_warningflag = None	#状态窗体
form_send_status=None	#状态窗体
root=None	#system tk
form_sys_set =None	#系统参数设置

	
		
def getdata(sql):
	''' 取表数据'''
	ret =[]
	try:
		cnn = dbcnn
		rs = cnn.Select(sql)
		fields = cnn.getFields(rs)		
		while not rs.EOF:
			v ={}
			for i in fields:
				v[i]=rs.Fields.Item(i).Value				
			ret.append(v)	#添加一条记录			
			rs.MoveNext()
	except:
		ret =[]
	return ret


import log

#设备状态查询
def query_it(devid):
	data = grab_tcp_package(devid)
	data[4]="%s"%CMD_REMOTE_TEST
	data[8]= "%s"%getsequence()
	sendstr = "%s"%string.join(data,',')
	try:	
		if  net_train.send2mss(sendstr)!=1	:
			raise 1
		
		log.recLog(str(devid),log.LOG_STATUS,data[8])
		
		#tkMessageBox.showwarning(unicode(''),unicode('已发送状态查询!'))
	except:
		
		tkMessageBox.showwarning(unicode('警告!'),unicode('与MSS通信失败!'))
		
#区域网管查询		
def batch_query_status(areaid):
	for i in user.repeaters:
		if i['AREA_ID']==areaid:			
			query_it(i['ID'])
	
#网管参数查询
def query_netparam(devid):
	data = grab_tcp_package(devid)
	data[4]="%s"%CMD_REMOTE_SYS_QUERY
	data[8]= "%s"%getsequence()
	sendstr = "%s"%string.join(data,',')
	try:	
		if net_train.send2mss(sendstr)!=1	:
			raise 1
		log.recLog(str(devid),log.LOG_PARAM_QUERY,data[8])
		#tkMessageBox.showwarning(unicode(''),unicode('已发送网管查询!'))
	except:
		tkMessageBox.showwarning(unicode('警告!'),unicode('与MSS通信失败!'))
		
#区域网管参数查询		
def batch_query_netparam(areaid):
	for i in user.repeaters:
		if i['AREA_ID']==areaid:	
			query_netparam(i['ID']) 
	

#取设备放置地点
def getsite(row):
	title =''	
	
	title = row['SITE']
	if title==None:
		title=''
	return title


#取设备标题
def getdevtitle(row):
	title =''	
	title = row['NAME']
	return title


#匹配数据
#用于指定一个数据集和列表和字段名称
# rs ='select * from area'
# match(rs,'ID','INT',100,'NAME')
# 在记录集合rs中查找id =100的记录，并且返回此记录的NAME字段数据，返回类型是STRING

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
	

##获取命令
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
	

#取存储过程的序列号
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
	
	
			
			
#定义告警参数
#当前设备告警状态集合
#刷新告警个数的时候更新设备状态纪录
current_dev_statuses=[]

#检测设备是否响应超时
def is_timeout(devid):
	'''检测设备是否响应超时,如果设备没有状态纪录，返回超时'''
	
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
	'''取设备当前告警级别
		同时要检测当前设备是否存在子设备，取最高告警状态值
	'''	
	ret = 0
	for i in current_dev_statuses:
		if i["REPEATER_ID"]==devid:
			ret = i["WARNINGLEVEL"]
			if ret == None:
				ret =0
			return ret
	#如该设备无状态记录，返回正常 状态0
	return 	0  

#################################################			
#取可操作区域	
def get_areas():
	'''取可操作区域	
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
	'''  取告警使能标志信息  
		devtype -- 设备类型	
	'''
	pado = ado.PAdo(dbcnnstr,1)
	#pado.Select('')


if __name__=='__main__'	:
	print getsequence('getguid')


