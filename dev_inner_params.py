#==================================================
# ����: �豸�ڲ���������
# ���ڣ�2003-07-14
# ������runonce
# ��ʷ:		
#==================================================
from Tix import *
import tkMessageBox
import Pmw
import re
import constdef
import login
import net_train
import ado
import session
import user
import log

#�������ֵ�Ƿ��ܱ��û�ͨ�������޸ģ���������޸ģ��ڲ�������ʱ��ȡ��ǰ��¼ֵ�����û�����ֵ.

sys_value_can_set={
	'MONI_ALARMFLAG':1,
	'MONI_ALARM_ID1':0,
	'MONI_ALARM_ID2':0,
	'NMS_PHONE':1,
	'ALARM_PHONE':1,
	'AD0MIN':1,
	'AD0MAX':1,
	'AD1MIN':1,
	'AD1MAX':1,
	'AD2MIN':1,
	'AD2MAX':1,
	'AD3MIN':1,
	'AD3MAX':1,
	'DIGIT_ALARM1':0,
	'DIGIT_ALARMFLAG1':1,
	'DIGIT_ALARM2':0,
	'DIGIT_ALARMFLAG2':1
	}


class PaneInnerParams(Toplevel):
	'''�豸�ڲ�����'''
	
	def __init__(self,master):
		self.master = master
		Toplevel.__init__(self,master)		
		#���ݶ���
		self.devinfo = None
		fall = Frame(self)
		fall.pack(fill='both',expand=1)
		#����������
		f = Frame(fall)
		f.pack(fill='x',side='top',pady=4)
		
		self.title = Label(f,text='')
		self.title.pack()


		#����������ʾ���
		self.nb = NoteBook(fall)
		self.nb.pack(fill='both',side='top',expand=1,padx=10,pady=10)
		self.p1 = self.nb.add('status',label=unicode('��1ҳ'))
		self.p2 = self.nb.add('control',label=unicode('��2ҳ'))
		
		
		#״̬
		f = Frame(fall,relief='groove')
		f.pack(fill='x',side='bottom',padx=4,pady=4)

		#if session.user.has_rights(user.R_DEV_STATUS_QUERY):
		Button(f,text=unicode('����'),bg='gray',command=self.onset).pack(side='right',padx=8,pady=2)			
		Button(f,text=unicode('ˢ��'),bg='gray',command=lambda:self.show(self.devinfo['ID'])).pack(side='right',padx=8,pady=2)		

		#��������
		self.sw = ScrolledWindow(self.p1,scrollbar='auto')
		self.sw.pack(fill='both',side='top',expand=1,padx=10,pady=10)

		self.sw2 = ScrolledWindow(self.p2,scrollbar='auto')
		self.sw2.pack(fill='both',side='top',expand=1,padx=10,pady=10)

		self.wm_protocol("WM_DELETE_WINDOW", lambda : self.onclose())		
		self.wm_title(unicode('�豸�ڲ�����'))
		#self.geometry("400x400")
		self.create_fields()
		#self.show()
		
	def create_fields(self):
		'''������ʾ�ֶ�'''
		Label(self.sw.window,text=unicode('վ���')).grid(column=0,row=0,sticky='w')
		self.zdh = Pmw.EntryField(self.sw.window,labelpos='w',validate = {'validator' : 'integer','min' : 0, 'max' : 255, 'minstrict' : 0} )
		
		self.zdh.grid(column=1,columnspan=2,row=0,sticky='ew')
		#-------------------------------------------------
		Label(self.sw.window,text=unicode('�������ĺ���')).grid(column=0,row=1,sticky='w')
		self.central_phone = Pmw.EntryField(self.sw.window,labelpos='w',validate={'max':'999999999999999','validator':'integer'} )
		self.central_phone.grid(column=1,columnspan=2,row=1,sticky='ew')
		#-------------------------------------------------
		Label(self.sw.window,text=unicode('�澯�绰����')).grid(column=0,row=2,sticky='w')
		self.alert_phone = Pmw.EntryField(self.sw.window,labelpos='w',validate={'max':'999999999999999','validator':'integer'} )
		self.alert_phone.grid(column=1,columnspan=2,row=2,sticky='ew')
		#-------------------------------------------------
		Label(self.sw.window,text=unicode('ģ�����澯���ֵ')).grid(column=0,row=3,sticky='w')
		self.moni_alert = Pmw.EntryField(self.sw.window,labelpos='w',validate={'max':65535,'min':0,'validator':'integer'})
		
		self.moni_alert.grid(column=1,columnspan=2,row=3,sticky='ew')
		#-------------------------------------------------
		Label(self.sw.window,fg='red',text=unicode('ģ�����澯�澯ʹ�ܱ�־')).grid(column=0,row=4,sticky='w')
		#-------------------------------------------------
		self.lb_ad0_alert = Label(self.sw.window ,text=unicode('AD0�澯�ź�'))
		self.lb_ad0_alert.grid(column=1,row=5,sticky='w')
		self.ad0_alert = ComboBox(self.sw.window )
		self.ad0_alert.grid(column=2,row=5,sticky='w')
		self.ad0_alert.append_history(unicode('�澯'))
		self.ad0_alert.append_history(unicode('���澯'))		
		#-------------------------------------------------
		self.lb_ad1_alert = Label(self.sw.window ,text=unicode('AD1�澯�ź�'))
		self.lb_ad1_alert.grid(column=1,row=6,sticky='w')
		self.ad1_alert = ComboBox(self.sw.window )
		self.ad1_alert.grid(column=2,row=6,sticky='w')
		self.ad1_alert.append_history(unicode('�澯'))
		self.ad1_alert.append_history(unicode('���澯'))		

		#-------------------------------------------------
		self.lb_ad2_alert=Label(self.sw.window ,text=unicode('AD2�澯�ź�'))
		self.lb_ad2_alert.grid(column=1,row=7,sticky='w')
		self.ad2_alert = ComboBox(self.sw.window )
		self.ad2_alert.grid(column=2,row=7,sticky='w')
		self.ad2_alert.append_history(unicode('�澯'))
		self.ad2_alert.append_history(unicode('���澯'))		

		#-------------------------------------------------
		self.lb_ad3_alert=Label(self.sw.window ,text=unicode('AD3�澯�ź�'))
		self.lb_ad3_alert.grid(column=1,row=8,sticky='w')
		self.ad3_alert = ComboBox(self.sw.window )
		self.ad3_alert.grid(column=2,row=8,sticky='w')
		self.ad3_alert.append_history(unicode('�澯'))
		self.ad3_alert.append_history(unicode('���澯'))		
		
		#-------------------------------------------------

		Label(self.sw.window ,text=unicode('AD0�澯��Χ��Сֵ')).grid(column=0,row=9,sticky='w')
		self.ad0min = Pmw.EntryField(self.sw.window,labelpos='w',validate={'max':255,'min':0,'validator':'integer'})
		self.ad0min.grid(column=1,row=9,sticky='ew',columnspan=2)
		#-------------------------------------------------
		Label(self.sw.window ,text=unicode('AD0�澯��Χ���ֵ')).grid(column=0,row=10,sticky='w')
		self.ad0max = Pmw.EntryField(self.sw.window,labelpos='w',validate={'max':255,'min':0,'validator':'integer'})
		self.ad0max.grid(column=1,row=10,sticky='ew',columnspan=2)
		#-------------------------------------------------
		Label(self.sw.window ,text=unicode('AD1�澯��Χ��Сֵ')).grid(column=0,row=11,sticky='w')
		self.ad1min = Pmw.EntryField(self.sw.window,labelpos='w',validate={'max':255,'min':0,'validator':'integer'})
		self.ad1min.grid(column=1,row=11,sticky='ew',columnspan=2)
		#-------------------------------------------------
		Label(self.sw.window ,text=unicode('AD1�澯��Χ���ֵ')).grid(column=0,row=12,sticky='w')
		self.ad1max = Pmw.EntryField(self.sw.window,labelpos='w',validate={'max':255,'min':0,'validator':'integer'})
		self.ad1max.grid(column=1,row=12,sticky='ew',columnspan=2)
		#-------------------------------------------------
		Label(self.sw.window ,text=unicode('AD2�澯��Χ��Сֵ')).grid(column=0,row=13,sticky='w')
		self.ad2min = Pmw.EntryField(self.sw.window,labelpos='w',validate={'max':255,'min':0,'validator':'integer'})
		self.ad2min.grid(column=1,row=13,sticky='ew',columnspan=2)
		#-------------------------------------------------
		Label(self.sw.window ,text=unicode('AD2�澯��Χ���ֵ')).grid(column=0,row=14,sticky='w')
		self.ad2max = Pmw.EntryField(self.sw.window,labelpos='w',validate={'max':255,'min':0,'validator':'integer'})
		self.ad2max.grid(column=1,row=14,sticky='ew',columnspan=2)
		#-------------------------------------------------
		Label(self.sw.window ,text=unicode('AD3�澯��Χ��Сֵ')).grid(column=0,row=15,sticky='w')
		self.ad3min = Pmw.EntryField(self.sw.window,labelpos='w',validate={'max':255,'min':0,'validator':'integer'})
		self.ad3min.grid(column=1,row=15,sticky='ew',columnspan=2)
		#-------------------------------------------------
		Label(self.sw.window ,text=unicode('AD3�澯��Χ���ֵ')).grid(column=0,row=16,sticky='w')
		self.ad3max = Pmw.EntryField(self.sw.window,labelpos='w',validate={'max':255,'min':0,'validator':'integer'})
		self.ad3max.grid(column=1,row=16,sticky='ew',columnspan=2)
		#-------------------------------------------------
		Label(self.sw.window ,text=unicode('�������澯ֵ0-15')).grid(column=0,row=17,sticky='w')
		self.digit_alert = Pmw.EntryField(self.sw.window,labelpos='w',validate={'max':65535,'min':0,'validator':'integer'})
		self.digit_alert.grid(column=1,row=17,sticky='ew',columnspan=2)
		#-------------------------------------------------
		
#		Label(self.sw2.window ,text=unicode('�������澯��־0')).grid(column=0,row=0,sticky='w')
#		self.d0_alert = ComboBox(self.sw2.window )
#		self.d0_alert.grid(column=1,row=0,sticky='w')
#		self.d0_alert.append_history(unicode('�澯'))
#		self.d0_alert.append_history(unicode('����'))		
		#-------------------------------------------------
		for i in range(0,16):			
			stm ="self.lb_d%s = Label(self.sw2.window ,text=unicode('�������澯��־%s'))"%(i,i)			
			exec(stm)
			stm = "self.lb_d%s.grid(column=0,row=%s,sticky='w')"%(i,i)
			exec(stm)
			stm ="self.d%s_alert = ComboBox(self.sw2.window )"%i
			exec(stm)
			stm ="self.d%s_alert.grid(column=1,row=%s,sticky='w')"%(i,i)
			exec(stm)
			stm = "self.d%s_alert.append_history(unicode('�澯'))"%i
			exec(stm)
			stm = "self.d%s_alert.append_history(unicode('���澯'))"%i
			exec(stm)
			
	
		
		
		
		#Label(self.sw,text=unicode('վ���')).grid(column=0,row=2)		
	def show(self,devid):
		'''��ʾ������Ϣ'''
		sql = "select * from repeaterinfo where id=%s"%devid		
		self.devinfo = session.getdata(sql)[0]
		title = session.getdevtitle(self.devinfo)
		self.title.config(text = title)
		#------------------------------
		self.zdh.setentry(self.devinfo['REPEATER_ID'])
		v = self.devinfo['QUERY_PHONE']
		if v==None:
			v =""
		else:
			v = v.strip()
		self.central_phone.setentry(v)

		v = self.devinfo['ALARM_PHONE']
		if v==None:
			v =""
		else:
			v = v.strip()
		self.alert_phone.setentry(v)
		#-------------------------------------------------
		try:
			v = self.devinfo['MONI_ALARM_ID1']
			v = v | self.devinfo['MONI_ALARM_ID2']<<8;			
		except:
			v = 0
		print v
		v = "%s"%v
		self.moni_alert.setentry(v)
		#-------------------------------------------------
		repeatertype = self.devinfo['REPEATERTYPE']
		#-------------------------------------------------
		try:
			v = self.devinfo['MONI_ALARM_ID1'] & 0x0f			
		except:
			v =0			
		print "repeatertype-->",repeatertype,v
		self.lb_ad0_alert.config(text=constdef.adc_hash[str(repeatertype)][int(v)])
		try:
			v = self.devinfo['MONI_ALARMFLAG']&0x10
		except:
			v=0
		if v:
			self.ad0_alert.config(value=unicode('���澯'))
		else:
			self.ad0_alert.config(value=unicode('�澯'))
		#-------------------------------------------------
		try:
			v = (self.devinfo['MONI_ALARM_ID1'] & 0xf0)>>4  #get adc data 0-13 item			
		except:
			v =0			
		self.lb_ad1_alert.config(text=constdef.adc_hash[str(repeatertype)][int(v)])
		try:
			v = self.devinfo['MONI_ALARMFLAG']&0x20
		except:
			v=0
		if v:
			self.ad1_alert.config(value=unicode('���澯'))
		else:
			self.ad1_alert.config(value=unicode('�澯'))
		#-------------------------------------------------
		try:
			v = (self.devinfo['MONI_ALARM_ID2'] & 0x0f)  #get adc data 0-13 item			
		except:
			v =0			
		self.lb_ad2_alert.config(text=constdef.adc_hash[str(repeatertype)][int(v)])
		try:
			v = self.devinfo['MONI_ALARMFLAG']&0x40
		except:
			v=0
		if v:
			self.ad2_alert.config(value=unicode('���澯'))
		else:
			self.ad2_alert.config(value=unicode('�澯'))
		#-------------------------------------------------
		try:
			v = (self.devinfo['MONI_ALARM_ID2'] & 0xf0)>>4  #get adc data 0-13 item			
		except:
			v =0		
		print "repeatertype:%s,moni_alarm:%s"%(repeatertype,v)	
		self.lb_ad3_alert.config(text=constdef.adc_hash[str(repeatertype)][int(v)])
		try:
			v = self.devinfo['MONI_ALARMFLAG']&0x80
		except:
			v=0
		if v:
			self.ad3_alert.config(value=unicode('���澯'))
		else:
			self.ad3_alert.config(value=unicode('�澯'))
		#-------------------------------------------------		
		v = self.devinfo['AD0MIN']
		if v==None:
			v =0
		self.ad0min.setentry(v)
		#-------------------------------------------------		
		v = self.devinfo['AD0MAX']
		if v==None:
			v =0
		self.ad0max.setentry(v)
		#-------------------------------------------------		
		
		v = self.devinfo['AD1MIN']
		if v==None:
			v =0
		self.ad1min.setentry(v)
		#-------------------------------------------------		
		v = self.devinfo['AD1MAX']
		if v==None:
			v =0
		self.ad1max.setentry(v)
		#-------------------------------------------------		
		
		v = self.devinfo['AD2MIN']
		if v==None:
			v =0
		self.ad2min.setentry(v)
		#-------------------------------------------------		
		v = self.devinfo['AD2MAX']
		if v==None:
			v =0
		self.ad2max.setentry(v)
		#-------------------------------------------------		
		v = self.devinfo['AD3MIN']
		if v==None:
			v =0
		self.ad3min.setentry(v)
		#-------------------------------------------------		
		v = self.devinfo['AD3MAX']
		if v==None:
			v =0
		self.ad3max.setentry(v)
		#-------------------------------------------------		
		try:
			v = self.devinfo['DIGIT_ALARM1']|(self.devinfo['DIGIT_ALARM2']<<8)
		except:
			v =0
		
		self.digit_alert.setentry("%s"%v)
		#-------------------------------------------------		
		try:
			#print self.devinfo['DIGIT_ALARMFLAG1'],self.devinfo['DIGIT_ALARMFLAG1']
			v = self.devinfo['DIGIT_ALARMFLAG1'] | (self.devinfo['DIGIT_ALARMFLAG2']<<8 )
		except:
			v =0
		print hex(v),v
		for i in range(0,16):	
			stm = "self.lb_d%s.config(text=constdef.dp_hash[str(repeatertype)][int(i)])"%i
			exec(stm)
			
			print 1<<i,v		
			if (1<<i) & v:				
				stm ="self.d%s_alert.config(value=unicode('���澯'))"%i 
			else:
				stm ="self.d%s_alert.config(value=unicode('�澯'))"%i 
				
			exec(stm)
#			if constdef.dp_hash[str(repeatertype)][int(i)]=='':
#				stm = "self.d%s_alert."
		
		
	def onclose(self):
		session.form_sys_set =None
		self.destroy()
	
	def onset(self):
		""" ϵͳ��������"""
		if self.devinfo['MONI_ALARM_ID1']==None:
			tkMessageBox.showwarning(unicode('����!'),unicode('�豸��ǰ��ϵͳ��������!'))
			return 
		data =[]
		data = session.grab_tcp_package(self.devinfo['ID'])
		data[4]="%s"%constdef.CMD_REMOTE_SYS_SET
		data[8]= "%s"%session.getsequence()
		#-------------------------------------------------------
		s=[]
		if sys_value_can_set['NMS_PHONE']:	#
			if self.central_phone.getvalue().strip()=='':
				tkMessageBox.showwarning(unicode('����!'),unicode('�������ĵ绰����Ϊ��!'))
				return 
			s.append("QUERY_PHONE,2,%s"%self.central_phone.getvalue().strip())
		else:
			s.append("NMS_PHONE,2,%s"%self.devinfo['QUERY_PHONE'].strip())

		if sys_value_can_set['ALARM_PHONE']:	#
			if self.alert_phone.getvalue().strip()=='':
				tkMessageBox.showwarning(unicode('����!'),unicode('�澯�绰����Ϊ��!'))
				return 
			s.append("ALARM_PHONE,2,%s"%self.alert_phone.getvalue().strip())
		else:
			s.append("ALARM_PHONE,2,%s"%self.devinfo['ALARAM_PHONE'].strip())

		if sys_value_can_set['MONI_ALARM_ID1']:	#
			#if self.alert_phone.getvalue().strip()=='':
			#	tkMessageBox.showwarning(unicode('����!'),unicode('�澯�绰����Ϊ��!'))
			#	return 			
			#s.append('ALARM_PHONE',2,self.alert_phone.getvalue().strip())
			pass
		else:
			s.append("MONI_ALARM_ID1,1,%s"%self.devinfo['MONI_ALARM_ID1'])

		if sys_value_can_set['MONI_ALARM_ID2']:	#
			#if self.alert_phone.getvalue().strip()=='':
			#	tkMessageBox.showwarning(unicode('����!'),unicode('�澯�绰����Ϊ��!'))
			#	return 			
			#s.append('ALARM_PHONE',2,self.alert_phone.getvalue().strip())
			pass
		else:
			s.append("MONI_ALARM_ID2,1,%s"%self.devinfo['MONI_ALARM_ID2'])
		
		if sys_value_can_set['MONI_ALARMFLAG']:
			v = 0
			mask = constdef.LT_ALARM_SWITCH[self.ad0_alert.cget('value')]
			v = v | (mask<<4)
			mask = constdef.LT_ALARM_SWITCH[self.ad1_alert.cget('value')]
			v = v | (mask<<5)
			mask = constdef.LT_ALARM_SWITCH[self.ad2_alert.cget('value')]
			v = v | (mask<<6)
			mask = constdef.LT_ALARM_SWITCH[self.ad3_alert.cget('value')]
			v = v | (mask<<7)			
			s.append("MONI_ALARMFLAG,1,%s"%str(v))
		else:
			s.append("MONI_ALARMFLAG,1,%s"%self.devinfo['MONI_ALARMFLAG'])
			
		if sys_value_can_set['AD0MIN']:
			if not self.ad0min.valid():
				tkMessageBox.showwarning(unicode('����!'),unicode('AD0MIN ��Ч!'))
				return 
			else:
				s.append("AD0MIN,1,%s"%self.ad0min.getvalue().strip())			
		else:
			s.append("AD0MIN,1,%s"%self.devinfo['AD0MIN'])			

		if sys_value_can_set['AD0MAX']:
			if not self.ad0max.valid():
				tkMessageBox.showwarning(unicode('����!'),unicode('AD0MAX ��Ч!'))
				return 
			else:
				s.append("AD0MAX,1,%s"%self.ad0max.getvalue().strip())			
		else:
			s.append("AD0MAX,1,%s"%self.devinfo['AD0MAX'])			
		#------------------------------------------------------------------	
		if sys_value_can_set['AD1MIN']:
			if not self.ad1min.valid():
				tkMessageBox.showwarning(unicode('����!'),unicode('AD1MIN ��Ч!'))
				return 
			else:
				s.append("AD1MIN,1,%s"%self.ad1min.getvalue().strip())			
		else:
			s.append("AD1MIN,1,%s"%self.devinfo['AD1MIN'])			
		
		if sys_value_can_set['AD1MAX']:
			if not self.ad1max.valid():
				tkMessageBox.showwarning(unicode('����!'),unicode('AD1MAX ��Ч!'))
				return 
			else:
				s.append("AD1MAX,1,%s"%self.ad1max.getvalue().strip())			
		else:
			s.append("AD1MAX,1,%s"%self.devinfo['AD1MAX'])		
		#------------------------------------------------------------------			
			
		if sys_value_can_set['AD2MIN']:
			if not self.ad2min.valid():
				tkMessageBox.showwarning(unicode('����!'),unicode('AD2MIN ��Ч!'))
				return 
			else:
				s.append("AD2MIN,1,%s"%self.ad2min.getvalue().strip())			
		else:
			s.append("AD2MIN,1,%s"%self.devinfo['AD2MIN'])			
		
		if sys_value_can_set['AD2MAX']:
			if not self.ad2max.valid():
				tkMessageBox.showwarning(unicode('����!'),unicode('AD2MAX ��Ч!'))
				return 
			else:
				s.append("AD2MAX,1,%s"%self.ad2max.getvalue().strip())			
		else:
			s.append("AD2MAX,1,%s"%self.devinfo['AD2MAX'])		
		#------------------------------------------------------------------			
		if sys_value_can_set['AD3MIN']:
			if not self.ad3min.valid():
				tkMessageBox.showwarning(unicode('����!'),unicode('AD3MIN ��Ч!'))
				return 
			else:
				s.append("AD3MIN,1,%s"%self.ad3min.getvalue().strip())			
		else:
			s.append("AD3MIN,1,%s"%self.devinfo['AD3MIN'])			
		
		if sys_value_can_set['AD3MAX']:
			if not self.ad3max.valid():
				tkMessageBox.showwarning(unicode('����!'),unicode('AD3MAX ��Ч!'))
				return 
			else:
				s.append("AD3MAX,1,%s"%self.ad3max.getvalue().strip())			
		else:
			s.append("AD3MAX,1,%s"%self.devinfo['AD3MAX'])		
		#------------------------------------------------------------------			
		
		if sys_value_can_set['DIGIT_ALARM1']:
			pass
			#if not self.digit_alert.valid():
			#	tkMessageBox.showwarning(unicode('����!'),unicode('�������澯ֵ��Ч!'))
			#	return 
			#else:
			#	s.append("AD3MAX,1,%s"%self.ad3max.getvalue().strip())						
		else:
			s.append("DIGIT_ALARM1,1,%s"%self.devinfo['DIGIT_ALARM1'])
		
		if sys_value_can_set['DIGIT_ALARM2']:
			pass
		else:
			s.append("DIGIT_ALARM2,1,%s"%self.devinfo['DIGIT_ALARM2'])
			
		#------------------------------------------------------------------
		mask_val=0
		if sys_value_can_set['DIGIT_ALARMFLAG1']:#bit 0-15
			for i in range(16):	
				stm = "v =self.d%s_alert.cget('value')"%i
				exec(stm)
				print v
				stm = "v = constdef.LT_ALARM_SWITCH[unicode('%s')]"%v
				print stm
				exec(stm)
				mask_val = mask_val | (int(v)<<i)
			print hex(mask_val)
			s.append("DIGIT_ALARMFLAG1,1,%s"%(mask_val&0x0ff))	#low 8 bits
			s.append("DIGIT_ALARMFLAG2,1,%s"%((mask_val&0xff00)>>8))  #==>high 8 bits
			
		else:
			s.append("DIGIT_ALARMFLAG1,1,%s"%self.devinfo['DIGIT_ALARMFLAG1'])
			s.append("DIGIT_ALARMFLAG2,1,%s"%self.devinfo['DIGIT_ALARMFLAG2'])
			
		
		
		sendstr = "%s@%s"%(string.join(data,','),string.join(s,';'))
		print sendstr
		try:
			if  net_train.send2mss(sendstr)!=1:
				print "invoke send2mss failed"
				raise 1
			
			tkMessageBox.showwarning('',unicode('�����������!'))			
		except:
			tkMessageBox.showwarning('',unicode(' ��MSSͨ��ʧ��!'))
			return 
		log.recLog(str(self.devinfo['ID']),log.LOG_CONTROL,data[8])			

		
		
		
if __name__=="__main__":
	rt = Tk()
	PaneInnerParams(rt)
	rt.mainloop()
