


#############################################
#
#	功能: 系统参数配置
#
#
from  Tix import *
import ado
import session
import shelve
import Pmw
import re
import user



wm =None	
items={}
def onsave(items,toplevel):
	global wm
	try:
		cf = shelve.open('./syspt')
		for (k,v) in items.items():
			item = items[k]
			v = item[0].getvalue()		
			if k=='mss_addr':
				#####网络通信参数
				session.mss_addr=str(v)	
			if k=='mss_listen_port':
				session.mss_listen_port=int(v)	
			if k=='area_warningcount_interval':
				#区域显示的4种告警数量刷新时间间隔
				session.area_warningcount_interval =int(str(v))*1000 
			if k=='send_cmd_fresh_interval':
				#命令列表状态查询刷新时间间隔
				session.send_cmd_fresh_interval=int(str(v))	
			if k=='browse_rowsets':
				#日志查询浏览记录总数	
				session.browse_rowsets=int(str(v))  
			if k=='no_response_timeout':		#设备响应超时(分钟)
				session.no_response_timeout = int(str(v))*60
			cf[k]= v+'&'+item[1] #取界面上entry值		
		cf.close()
	except:
		tkMessageBox.showwarning(unicode('警告!'),unicode('参数值无效:'))
	
	
#	print session.mss_addr
#	print session.mss_listen_port
#	print session.area_warningcount_interval 
#	print session.send_cmd_fresh_interval
#	print session.browse_rowsets
	
	wm.destroy()
	

def config(master):
	global wm,items
	items={}
	wm = Toplevel()	#创建窗体
	wm.title(unicode('系统运行参数配置'))
	rt = Frame(wm)
	rt.pack(fill='both',expand=1,pady=10,padx=10)
	
	rt.bind_all('<Escape>',lambda ev=None : rt.destroy())  #销毁窗体	
	#rt.option_add('*Button*relief','groove')
	#rt.option_add('*Button*background','gray')
	
	
	
	cf = shelve.open('./syspt')
	
	algin=[]
	for i in cf.keys():
		label = cf[i]
		label = re.split('&',label)		
		item = Pmw.EntryField(rt,labelpos='w',label_text=label[1],labelmargin=10 )
		
		item.pack(side='top',fill='x',padx=10,pady=2)
		item.setentry(label[0])   #解析格式参见配置程序 
		items[i]=[item,label[1]]
		algin.append(item)
	cf.close()
	Pmw.alignlabels(algin)

	f = Frame(rt)
	f.pack(side='bottom',fill='x',padx=10,pady=4)
	
	Button(f,text=unicode('关闭'),command=lambda:wm.destroy()).pack(side='right')
	if session.user.has_rights(user.R_SYS_RUN_PARAM_SET):
		Button(f,text=unicode('存储'),command=lambda items=items,top=rt: onsave(items,rt)).pack(side='right')
	wm.wm_protocol("WM_DELETE_WINDOW", lambda : wm.destroy())
	
def load_run_param():
	cf = shelve.open('./syspt')
	for k in cf.keys():
		label = cf[k]
		label = re.split('&',label)		
		v = label[0]
		
		if k=='mss_addr':
			#####网络通信参数
			session.mss_addr=str(v)	
			
		if k=='mss_listen_port':
			session.mss_listen_port=int(v)	
			
		if k=='area_warningcount_interval':
			#区域显示的4种告警数量刷新时间间隔
			session.area_warningcount_interval =int(str(v))*1000  
			
		if k=='send_cmd_fresh_interval':
			#命令列表状态查询刷新时间间隔
			session.send_cmd_fresh_interval=int(str(v))	
			
		if k=='browse_rowsets':
			#日志查询浏览记录总数	
			session.browse_rowsets=int(str(v))  
		if k=='no_response_timeout':
			session.no_response_timeout = int(str(v))*60
			
		
	cf.close()

