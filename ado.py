

############################################
# ����: ado���ݷ��ʰ�װ
# ���ڣ�2003-01-10
# ������runonce
# ��ʷ:	
#	2003-01-10  ����
#	20030419  ����Execute2����,Execute2֧��bcb���ݷ���ģʽ(name=:name),֧��sql���ݼ�����
##############################################

from win32com.client import *
import pythoncom 
import string
import tkMessageBox
import re
from adoconst import *
from Tix import *

#�����������
STRING = adVarChar
INT = adInteger
DOUBLE = adDouble


	
class PAdo:
	""" Ado���ݷ��ʰ�װ��
	"""
	def __init__(self,cnnstr='',bOpen=1):
		"cnnstr--ado ���������ַ���,bopen--�Ƿ��Զ���"
		self.cnnstr =cnnstr
		self.adoConn=None
		self.rs=None
		self.adoConn = Dispatch('ADODB.Connection')
		self.rs=Dispatch('ADODB.Recordset')
		if bOpen==1 :
			self.adoConn.Open(cnnstr)
			
	def Close(self):
		self.adoConn=None
		self.rs=None
		
	def	getTables(self):
		" ��ȡ���ݿ����б�����"
		
		adoRs = self.adoConn.OpenSchema(20)  #ȡ���ݿ����б�
		adoRs.MoveFirst()
		ar=[]
		while not adoRs.EOF:
		    ar.append(str(adoRs.Fields.Item('TABLE_NAME')))
		    adoRs.MoveNext()
		return ar
		
	def getFields(self,rs): #recordset
		"ȡ��¼���ֶ���Ϣ"
		fds=[]
		for i in range(0,rs.Fields.Count):
			fds.append(rs.Fields.Item(i).Name)
		return fds
	
	def Select(self,sql):
		"""ִ�в�ѯ�������������
			�����ò���ռλ����ʽ�������sqlֱ��ִ��	
		03.0109 
		"""
		sql = sql.upper()
		#print sql
		self.rs=Dispatch('ADODB.Recordset')
		self.rs.Open(sql,self.adoConn,-1,-1,-1)
		#
		#ar=[]
		#while not self.rs.EOF:
		#	print self.rs.Fields.Item('NAME').Value
		#	ar.append(self.rs.Fields.Item('NAME').Value)
		#	self.rs.MoveNext()
		
		return self.rs
		
		
	def Execute(self,sql,params=None):
		"""
			sql-- sqlִ����䣬����Ǵ���������ʽΪ insert into tablename (name) values(:name),ͬbcb
			params --params���б�����,�������ݵĲ�����ÿ��������һ��3Ԫ�飬��������ľ�����Ϣ ��(name,type,value) ,����size,��Ϊ3Ԫ���
					
			params=None,ָ��sqlΪ����sql(��������ռλ����)
		ʹ�÷���:
			ado.Execute('insert into basicinfo (name,type,dt,v2) values(?,?,?,?)',['name',STRING,'11'],
			['type',STRING,'����'],['dt',STRING,'2002-01-12 12:12:01'],['v2',DOUBLE,111111111.231])


		--δ���д��󱣻�
		
		"""
		
		sql = string.upper(sql)
		#print sql
		
		param = Dispatch('ADODB.Parameter')
		cmd = Dispatch('ADODB.Command')
		cmd.ActiveConnection = self.adoConn
		cmd.CommandText= sql
		
		if(params !=None):
			for ele in params:  #len(params) �������ֶδ���
				#print ele
				#print ele[0],ele[1],ele[2]
				if ele[1]==STRING:
					size = len(str(ele[2]))
					print size
				if ele[1]==INT:
					size = 4
				if ele[1]==DOUBLE:
					size =8
				cmd.Parameters.Append(cmd.CreateParameter(ele[0],ele[1],1,size,ele[2]))
		cmd.Execute()
		
	
	def Execute2(self,sql,params=None):
		""" 
			sql-- sqlִ����䣬����Ǵ���������ʽΪ insert into tablename (name) values(:name),ͬbcb
			params --params���б�����,�������ݵĲ�����ÿ��������һ��3Ԫ��[������,ֵ,����]					
			params=None,ָ��sqlΪ����sql(��������ռλ����)
		<<ʹ�÷���:>>			
			sql = 'insert userinfo (id,login_name) values(:id,:login_name)'
			data=[]
			data.append([' loGin_name ','test1'])
			data.append(['ID',101])
			rs = ado.Execute2(sql,data)

		--δ���д��󱣻�		
		"""
		
		_sql = string.upper(sql)
		#print _sql
		#step1: ���Ҳ���
		ps = re.findall(':(\w+)',_sql)
		#step1: ����ado sql ���  ,����: insert into a (a1,a2) values(?,?)
		_sql = re.sub(':(\w+)','?',_sql)
		#step3: У�Դ�������Ƿ���sql�еĲ���ƥ��
		if params:
			for i in params:
				p = i[0].upper().strip()
				try:					
					ps.index(p)
				except:
					tkMessageBox.showinfo('warning!',unicode('parameter error:')+p)
					return 						
		
		
		param = Dispatch('ADODB.Parameter')
		cmd = Dispatch('ADODB.Command')
		cmd.ActiveConnection = self.adoConn
		cmd.CommandText= _sql
		#print _sql
		
		if(params !=None):
			for p in ps:				
				for ele in params:  #len(params) �������ֶδ���
								
					if ele[0].upper().strip() == p:
						_type=0
						size =0
						#print type(ele[1]),type('string')
						if type(ele[1])==type(1): #integer
							size = 4
							_type = INT
							#print 'int '
						if type(ele[1])==type(1.1): #double
							size = 8
							_type = DOUBLE
							#print 'double'
						if type(ele[1])==type(unicode('string')) or type(ele[1])==type('string'): #string
							size = len(str(ele[1]))
							if size==0:
								size=1
								ele[1]=" "
							_type = STRING
							print 'string '
						#print p,_type,size,ele[1]
						cmd.Parameters.Append(cmd.CreateParameter(p,_type,1,size,ele[1]))
		(rs,ret) = cmd.Execute()
		#print "execute return value==>",ret
		return rs
		
	def GetRecordCount(self,adors):
		"ȡ��¼����¼����"
		adors.MoveFirst()
		cnt=0
		while not adors.EOF:
			cnt+=1
			adors.MoveNext()
		adors.MoveFirst()
		return cnt
		
#################################################################################################################

#if __name__=="__main__":
	
#	ado = PAdo('Provider=SQLOLEDB.1;Persist Security Info=False;User ID=sa;Initial Catalog=NMSDB_CM;Data Source=localhost')    
#	#ado =PAdo('''Provider=Microsoft.Jet.OLEDB.4.0;User ID=Admin;Data Source=E:\DevDoc\Database\�˿�ͳ��.mdb;
#		Mode=Share Deny None;Extended Properties="";Jet OLEDB:System database="";Jet OLEDB:Registry Path=;
#		Jet OLEDB:Database Password=;Jet OLEDB:Engine Type=4;Jet OLEDB:Database Locking Mode=0;Jet OLEDB:Global Partial Bulk Ops=2;Jet OLEDB:Global Bulk Transactions=1;Jet OLEDB:New Database Password="";Jet OLEDB:Create System Database=False;Jet OLEDB:Encrypt Database=False;Jet OLEDB:Don't Copy Locale on Compact=False;Jet OLEDB:Compact Without Replica Repair=False;Jet OLEDB:SFP=False''')
#	
#	rs = ado.Select('select * from area')
#	
#	print ado.getFields(rs)	
#	print rs.Fields.Count
##	sql = 'insert userinfo (id,login_name) values(:id,:login_name)'
#	data=[]
#	data.append([' loGin_name ','test1'])
#	data.append(['ID',101])
#	
#	
#	rs = ado.Execute2(sql,data)
		
	
	
	
	
