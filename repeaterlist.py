

from Tix import *
import tkMessageBox
import Pmw

import devinfo
import constdef
import login
import net_train
import ado
import session
import user
import systemset
import dev_inner_params

##
#class PaneCareSubDev(Pmw.MegaToplevel):
#	def __init__(self,master):
#		Pmw.MegaToplevel.__init__(self,master)
#		self.master = master
#		f =Frame(self.component('hull'))
#		f.pack(fill='x',side='bottom',padx=4,pady=4)
#		Button(f,text=unicode('ȷ��'),command= self.onsave).grid(column=0,row=0)
#		Button(f,text=unicode('ȡ��'),command=lambda :self.destroy()).grid(column=1,row=0)
#		f = Frame(self.component('hull'))
#		f.pack(fill='both',padx=4,pady=4)
#		self.enArea = Pmw.EntryField(f,labelpos = 'w',label_text=unicode('�豸���:'),validate = {'validator' : 'integer',
#                        'min' : 0, 'max' : 6, 'minstrict' : 0})
#
#		
#		self.enArea.pack(fill='x',expand=1)
#		self.enSite = Pmw.EntryField(f,labelpos = 'w',label_text=unicode('���õص�:'),validate = {'max':50})		
#		self.enSite.pack(fill='x')
#		self.status =''
#		self.parentid =0	#���豸���
#		
#	def new(self,parentid):
#		self.parentid = parentid
#		self.status ='new'
#		self.component('hull').title(unicode('�����豸'))
#		pass 
#	def onsave(self):
#		if not self.enArea.valid():
#			tkMessageBox.showwarning(unicode('����!'),unicode('�豸�����Ч!'))			
#			return 
#		
#		equipmentid = int(self.enArea.getvalue())
#		#�豸��װ�ص�
#		site = self.enSite.getvalue()
#		#����豸���Ƿ����
#		sql ="select count(*) as cnt from repeaterinfo where parent_id=%s and equipment_id=%s"%(self.parentid,equipmentid)
#		rs = session.getdata(sql)
#		if rs[0]['CNT']!=0:
#			tkMessageBox.showwarning(unicode(''),unicode('�豸����Ѵ���!'))						
#			return 
#		####
#		
#		sql = "select * from repeaterinfo where id=%s"%self.parentid
#		rs = session.getdata(sql)
#		parentdev = rs[0]
#		
#		repeatertype=0
#		devcat = 0
#		if parentdev['DEVCAT']==1:
#			devat=2
#		if parentdev['DEVCAT']==5:
#			devcat=6
#		parentid = self.parentid
#		
#		query_interval = parentdev['QUERY_INTERVAL']
#		
#		sql = "select type_id from repeatertype where product_id=%s and  devcat=%s"%(parentdev['PRODUCT_ID'],devcat)
#		rs = session.getdata(sql)
#		repeatertype = int(rs[0]['TYPE_ID'])
#		id = session.getsequence()
#		
#		sql = "insert into repeaterinfo  (id,repeatertype,parent_id,equipment_id,devcat,query_interval,site) values(:id,:repeatertype,:parent_id,:equipment_id,:devcat,:query_interval,:site)"
#		
#		
#		data =[]
#		data.append(['id',id])
#		data.append(['repeatertype',repeatertype])
#		data.append(['parent_id',parentid])
#		data.append(['equipment_id',equipmentid])
#		data.append(['devcat',devcat])
#		data.append(['query_interval',query_interval])
#		data.append(['site',site])
#		
#		try:
#			session.dbcnn.Execute2(sql,data)
#			tkMessageBox.showwarning(unicode(''),unicode('�豸��ӳɹ�!'))						
#			session.user.load_repeaters()
#			str ="0,1,2,3,%s,4,5,6,7,8"%constdef.cmd_list["UPDATE_DEV_LIST"]		
#			if net_train.send2mss(str)==0:
#				tkMessageBox.showwarning(unicode('����'),unicode('֪ͨMSSʧ��!'))				
#
#		except:
#			tkMessageBox.showwarning(unicode('����!'),unicode('����ʧ�ܣ��޷�����豸!'))			
#		self.destroy()
#		

		


#���豸
class SingleDev(Button):
	def __init__(self,owner,data,master):
	
		Button.__init__(self,owner)
		
		#��ȡ�����豸
		self.master = master
		self.data = data
		
		#���ø澯��ɫ
		self.config(state='normal')
		self.config(fg='white')
		warningtype = session.get_warning_type(data['ID'])
		if warningtype==None:
			warningtype=0
		self.config(background=constdef.WCOLOR[str(warningtype)])
		self.pi = PhotoImage(file='./rc/alert_%s.gif'%warningtype)
		if self.data['PARENT_ID']==0:				
			self.config(image =self.pi)						
			pass
		else:
			self.config(font=('����',8))
			self.config(text=self.data['EQUIPMENT_ID'])							
			self.config(fg='black')							
			
		
		self.config(command=lambda: self.onlmouse(self))
		self.config(relief='raised')
		
		pass

	def onsel(self):
		tkMessageBox.showwarning('','error')		
		
	#�������
	def onlmouse(self,ev):
		
		self.menu_info =Menu(self,selectcolor='red',tearoff=0)	
		s = self.data['REPEATER_ID']
			
		if s==None:
			s=''
		else:
			s = str(s)
			self.menu_info.add_command(label=(unicode('ֱ��վ���:')+s))
			
		s = self.data['REPEATER_PHONE']
		if s==None:
			s=''
		else:
			s = s.strip()
			self.menu_info.add_command(label=(unicode('�豸�绰:')+s))		

		site = self.data['SITE']
		if site==None:
			site =""
		else:
			site = site.strip()
		self.menu_info.add_command(label=(unicode('���õص�:')+site))
		self.menu_info.add_separator()
		self.menu_info.add_command(label=unicode('ˢ��'),command=lambda:self.master.reload(self.data['ID']))
		self.menu_info.add_command(label=unicode('�豸��Ϣ'),command=self.onmodify)
		
		if session.user.has_rights(user.R_DEV_DEL):
			self.menu_info.add_command(label=unicode('ɾ��'),command= self.ondel)	
		
		self.menu_info.add_separator()
		if session.user.has_rights(user.R_DEV_STATUS_QUERY):
			self.menu_info.add_command(label=unicode('����״̬��ѯ'),command=lambda :session.query_it(self.data['ID']))		
		if session.user.has_rights(user.R_DEV_PARAM_QUERY):
			self.menu_info.add_command(label=unicode('����ϵͳ������ѯ'),command= lambda:session.query_netparam(self.data['ID']))		
		self.menu_info.add_separator()
		self.menu_info.add_command(label=unicode('״��̬'),command=self.onstatus)		
		self.menu_info.add_command(label=unicode('ϵͳ����'),command=self.onsysset)		


		self.menu_info.post(self.winfo_pointerx(),self.winfo_pointery())
		

	
		
	def onsysset(self):
		if session.form_sys_set==None:
			session.form_sys_set =dev_inner_params.PaneInnerParams(session.root)
#		session.form_warningflag.deiconify()
#		session.form_warningflag.transient(self)
		session.form_sys_set.lift()
		session.form_sys_set.show(int(self.data['ID']))
	
		
	#��ʾ״̬��Ϣ		
	def onstatus(self):
		if session.form_status==None:
			session.form_status =systemset.PaneStatus(session.root)
#		session.form_status.deiconify()
#		session.form_status.transient(self)
		session.form_status.lift()
		session.form_status.show_status(int(self.data['ID']))
	
		
	#ɾ���豸
	def ondel(self):
		masterdevid = 0
		sql =  ""
		if self.data['PARENT_ID']==0:
			if tkMessageBox.askyesno(unicode('����!'),unicode('ֱ��վ��������豸,���β�����ɾ���������豸,�Ƿ����ɾ��?')) ==0:
				return
			
			masterdevid = self.data['ID']
		else:
			masterdevid = self.data['PARENT_ID']		
		
		sql = "delete from repeaterinfo where id=%s or parent_id=%s"%(self.data['ID'],self.data['ID'])					
		try:
			session.dbcnn.Execute2(sql)				
			session.user.load_repeaters()	#���¼����û������豸�嵥
			
		except:
			tkMessageBox.showinfo(unicode('����!'),unicode('ɾ��ʧ��'))
			return
		#print "ondel()==",masterdevid
		self.master.reload(masterdevid)
	#�޸��豸��Ϣ

	def onmodify(self):
		pdi = devinfo.PaneDevInfo(session.root)
		pdi.show(self.data['ID'])
		pdi.activate()
		if pdi.save_to_close:
			self.master.reload(self.data['ID'])

class Repeater(Frame):
	def __init__(self,owner,devid,master):
		Frame.__init__(self,owner)
		self.master = master
		self.devid = devid
		self.name =''
		self.devs=[]	
		self.dev=None	#���豸	
		self.desc =None
		self.fslaves =None	
			
		self.reload(self.devid)
		
	def __del__(self):
		self.clear()
		self.destroy()		
			
		

	#��������豸��Ϣ
	def clear(self):
		for  w in self.devs:
			w.destroy()
			w=None
		if self.dev:
			self.dev.destroy()
			self.dev =None
		if self.desc:
			self.desc.destroy()
			self.desc =None
		
	#�����豸��Ϣ
	def reload(self,id):
		self.clear()	#ɾ�������Ӳ���

		data=None		

		for i in session.user.repeaters:	
			if i['ID']==id:
				data = i


				
		#���û��ֶ�ɾ��������ʱ��ˢ���豸�б�����
		if data==None:
			self.master.reflash()
			return
		
		
		self.name = data['NAME']
		self.name = self.name.strip()
		
		dev = SingleDev(self,data,self)
		self.devs.append(dev)
		dev.pack()		#�����豸
		
		
		self.desc = Label(self,text=self.name,font=(unicode('����'),9))
		self.desc.pack()


								

class RepeaterList(Frame):
	def __init__(self,master):		
		Frame.__init__(self,master)
		self.sb =Scrollbar(self)
		self.sb.pack(side='left',fill='y')
		self.tl = TList(self,orient='horizontal',padx=10,pady=10,yscrollcommand=self.sb.set )
		self.tl.pack(side='left',fill='both',expand=1)
		self.sb['command']=self.tl.yview
		self.devlist =[]
		self.area_id =0		#��ʾ����
		self.warningtype =0 #��ʾ�澯���
		
#		for i in range(100):
#			self.tl.insert('end',itemtype='window',window=Repeater(self.tl))
#			
	def show(self,area_id,warningtype,show_no_response=0):
		''' ��ʾ�豸��Ϣ  '''
		
		self.area_id = area_id
		self.warningtype = warningtype
		self.show_no_response = show_no_response
		#ɾ��������ʾ���豸
		dev_cnt = self.tl.tk.call(self.tl,'info','size')
		for i in range(int(dev_cnt)):
			w = self.tl.tk.call(self.tl,'entrycget',i,'-window')
			w = self.nametowidget(w)
			w.__del__()
			w.destroy()
			
		self.tl.delete(0,'end')
		self.devlist=[]
		
		list=[]
		for i in session.user.repeaters:			
			if i['AREA_ID']==area_id:				
				list.append(i)
		if warningtype ==-1:  #��ʾ���е��豸���������Ƿ�澯
			if show_no_response==0:	#ѡ������ʾ����İ�ť
				self.devlist = list
			else:	#��ʾ��Ӧ��ʱ�豸
				for i in session.user.repeaters:					
					if i['AREA_ID']==area_id:										
						if session.is_timeout(i['ID']): 
							self.devlist.append(i)
				
		else:
		#�ж��豸�澯����,ѡ����4�ָ澯����֮һ
			for i in list:
				wl=0
				for i2 in session.current_dev_statuses:
					if i['ID']==i2['REPEATER_ID']:
						if i2['WARNINGLEVEL']==None:
							wl =0	#����״̬��澯���ΪNUll
						else:
							wl = i2['WARNINGLEVEL']
				if wl==warningtype:
					self.devlist.append(i)
		#print "devs cnt %s by warningtype"%len(self.devlist)							
		
		for i in self.devlist:
			r = Repeater(self.tl,i['ID'],self)	#����豸		
			self.tl.insert('end',itemtype='window',window=r)
		
			
	def reflash(self):
		''' reflash all repeaters status '''
		
		self.show(self.area_id,self.warningtype,self.show_no_response)
		
		
		
		

 