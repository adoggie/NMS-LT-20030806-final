

import time
import tkMessageBox
#log 系统日志处理
import ado
import session
import constdef
import net_train



#
LOG_ACCOUNT_ADD=1 #;       //添加用户账号
LOG_ACCOUNT_MODIFY=2 #;    //修改用户账号
LOG_ACCOUNT_DEL=3 #;       //删除用户账号

LOG_PASSWORD_MODIFY=4 #;   //用户账号密码修改

LOG_REPEATER_ADD=5 #;      //添加直放站
LOG_REPEATER_MODIFY=6 # ; //修改直放站信息
LOG_REPEATER_DEL=7 #;     //删除直放站

LOG_VIC_REPEATER_ADD=8 #;      //添加近端机
LOG_VIC_REPEATER_MODIFY=9 # ; //修改近端机
LOG_VIC_REPEATER_DEL=10 #;     //删除近端机
LOG_RMT_REPEATER_ADD=11 #;      //添加远端机
LOG_RMT_REPEATER_MODIFY=12 # ; //修改远端机
LOG_RMT_REPEATER_DEL=13 #;     //删除远端机

LOG_WARNINGLEVEL_MODIFY=14 #;//修改告警级别
LOG_CLIENT_LOGIN=15 #;     //客户端登录
LOG_CLIENT_LOGOFF=16 #;    //客户端退出
LOG_NETCENTRAL_MODIFY=17 #;//修改网管信息　　　　　　
LOG_CONTROL  =18 #;          //直放站控制
LOG_STATUS  =19 #;          //直放站状态查询
LOG_PARAMSET  =20 #;          //直放站网管参数设置
LOG_PARAM_QUERY  =21 #;          //直放站网管参数查询
LOG_REPEATER_NO_SET  =22 #;          //直放站编号设置

LOG_RMT_WARNING=24 #;         //直放站告警，主动告警要求Mss填写告警记录
LOG_VIC_WARNING=25 #;         //直放站告警，主动告警要求Mss填写告警记录
LOG_MSS_STATISTICAL_QUERY=40 #;        // 对MSS的统计参数的查询
LOG_MSS_CONFIG_UPDATE=41 #;           // 对MSS配置参数的修改
LOG_CSS_STATISTICAL_QUERY_REQUEST= 42 #; // 对CSS的统计参数的查询
LOG_MODIFY_ALARMFLAG =51	#告警使能标志修改







def recLog(target,action_id,trans_no='0'):
		
		
		
	sql ="insert into operateinfo (id,target,actionid,TRANSACTIONNO,OPERATOR,OPTTIME) values(:id,:target,:actionid,:TRANSACTIONNO,:OPERATOR,:OPTTIME)"
	
	
	
	data=[]
	data.append(['id',session.getsequence()])
	data.append(['target',target])
	data.append(['actionid',action_id])
	t_no = trans_no
	if trans_no=='0':
		trans_no = session.getsequence()
	data.append(['TRANSACTIONNO',int(trans_no)])
	data.append(['OPERATOR',session.user.login_name])
	t = time.strftime("%Y-%m-%d %H:%M:%S ", time.localtime())
	data.append(['OPTTIME',str(t)])
	try:
		session.dbcnn.Execute2(sql,data)
		sql = "insert into transactionstatus (TRANSACTIONNO,TRANSACTIONSTATUS) values(:TRANSACTIONNO,:TRANSACTIONSTATUS)"
		data=[]
		data.append(['TRANSACTIONNO',int(trans_no)])
		data.append(['TRANSACTIONSTATUS',1])
		session.dbcnn.Execute2(sql,data)
	except:
		tkMessageBox.showwarning(unicode('警告!'),unicode('无法记录事务日志'))
		print "error"
		return
		
	#调度者传递进来的 事务号不为0则显示发送命令状态窗口
	if int(t_no):
		if session.form_send_status==None:
			session.form_send_status = net_train.net_send_status(None)
		session.form_send_status.add_item(int(trans_no))

#	
def recLogin():
	sql ="insert into logininfo (id,username,password,logintime,loginip) values(:id,:username,:password,:logintime,:loginip)"
	data =[]
	
	data.append(['id',session.getsequence()])
	
	data.append(['username',session.user.login_name])
	data.append(['password',session.user.psw])
	t = time.strftime("%Y-%m-%d %H:%M:%S ", time.localtime())
	data.append(['logintime',t])
	
	localip = net_train.getlocalip()
	data.append(['loginip',localip])
	
	try:
		session.dbcnn.Execute2(sql,data)
	except:
		return
		#tkMessageBox.showwarning(unicode('警告!'),unicode('无法记录事务日志'))
	

