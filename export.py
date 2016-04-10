


#############################################
#
#	用户功能管理
#
#
import string
import session
import ado
from Tix import *
import Pmw
import tkMessageBox
import constdef
import copy
import re
import time
import webbrowser

def Make2Html(title,shl):
	''' export data to html file
		title -- report title
		shl --- scrolledhlist widgets that contain more records
	'''
	if shl==None:
		return 
	hlist = shl.hlist
	cols = int(hlist.cget('columns'))
	html="%s<br>%s<br>%s"
	table="<table width='100%' border=1 align='center' cellpadding=0 cellspacing=0>\n"
	
	table+="<TR bgcolor=#999999>"
	for i  in range(cols):
		text = hlist.header_cget(i,"-text")
		table+="\n\t<TD>%s</TD>"%text
	table+="\n<TR>\n"
	
	children = hlist.info_children()
	
	for child in children:
		table+="<TR>"
		for i  in range(cols):
			try:
				text = hlist.item_cget(child,i,"-text")
			except:
				text = ''
			table+="\n\t<TD>%s</TD>"%text
		table+="\n<TR>\n"
	table+="</TABLE>"
	timetag = time.strftime("%Y-%m-%d %H:%M:%S ",time.localtime())

	cache ='./cache'
	rtpfile ='./export/area_repeater.htm'
	html = html%(title,table,unicode('打印时间:')+timetag)

	tempreport = "%s/%s.htm"%(cache,str(time.clock()))
	fh = open(tempreport,'w')
	fh.write(html)
	fh.close()
	#显示报表输出
	webbrowser.open(tempreport)
	