

import time
import tkMessageBox
#log ϵͳ��־����
import ado
import session
import constdef
import net_train



#
LOG_ACCOUNT_ADD=1 #;       //����û��˺�
LOG_ACCOUNT_MODIFY=2 #;    //�޸��û��˺�
LOG_ACCOUNT_DEL=3 #;       //ɾ���û��˺�

LOG_PASSWORD_MODIFY=4 #;   //�û��˺������޸�

LOG_REPEATER_ADD=5 #;      //���ֱ��վ
LOG_REPEATER_MODIFY=6 # ; //�޸�ֱ��վ��Ϣ
LOG_REPEATER_DEL=7 #;     //ɾ��ֱ��վ

LOG_VIC_REPEATER_ADD=8 #;      //��ӽ��˻�
LOG_VIC_REPEATER_MODIFY=9 # ; //�޸Ľ��˻�
LOG_VIC_REPEATER_DEL=10 #;     //ɾ�����˻�
LOG_RMT_REPEATER_ADD=11 #;      //���Զ�˻�
LOG_RMT_REPEATER_MODIFY=12 # ; //�޸�Զ�˻�
LOG_RMT_REPEATER_DEL=13 #;     //ɾ��Զ�˻�

LOG_WARNINGLEVEL_MODIFY=14 #;//�޸ĸ澯����
LOG_CLIENT_LOGIN=15 #;     //�ͻ��˵�¼
LOG_CLIENT_LOGOFF=16 #;    //�ͻ����˳�
LOG_NETCENTRAL_MODIFY=17 #;//�޸�������Ϣ������������
LOG_CONTROL  =18 #;          //ֱ��վ����
LOG_STATUS  =19 #;          //ֱ��վ״̬��ѯ
LOG_PARAMSET  =20 #;          //ֱ��վ���ܲ�������
LOG_PARAM_QUERY  =21 #;          //ֱ��վ���ܲ�����ѯ
LOG_REPEATER_NO_SET  =22 #;          //ֱ��վ�������

LOG_RMT_WARNING=24 #;         //ֱ��վ�澯�������澯Ҫ��Mss��д�澯��¼
LOG_VIC_WARNING=25 #;         //ֱ��վ�澯�������澯Ҫ��Mss��д�澯��¼
LOG_MSS_STATISTICAL_QUERY=40 #;        // ��MSS��ͳ�Ʋ����Ĳ�ѯ
LOG_MSS_CONFIG_UPDATE=41 #;           // ��MSS���ò������޸�
LOG_CSS_STATISTICAL_QUERY_REQUEST= 42 #; // ��CSS��ͳ�Ʋ����Ĳ�ѯ
LOG_MODIFY_ALARMFLAG =51	#�澯ʹ�ܱ�־�޸�







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
		tkMessageBox.showwarning(unicode('����!'),unicode('�޷���¼������־'))
		print "error"
		return
		
	#�����ߴ��ݽ����� ����Ų�Ϊ0����ʾ��������״̬����
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
		#tkMessageBox.showwarning(unicode('����!'),unicode('�޷���¼������־'))
	

