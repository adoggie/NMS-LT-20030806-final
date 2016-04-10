


#　常数定义



appspecs = {'window_font':('宋体',10)}

#-------------------------------------------------------------------------------------
#告警级别定义
warninglevel={'0':unicode('正常'),
				'1':unicode('一般'),
				'2':unicode('重要'),
				'3':unicode('严重')
			}

WGREEN=0
WYELLO=1
WBLUE=2
WRED =3
WCOLOR = {'0':'green','1':'yellow','2':'blue','3':'red'}
#-------------------------------------------------------------------------------------
#   告警使能标志  排列 0-15 位
#-------------------------------------------------------------------------------------
#	'HPA','保留','自激告警','门襟告警','电源调电','上行低噪放故障
#	','下行低噪放故障','光收发模块故障','电源模块故障','上行功放过功率','下行功放过
#	功率','上行功放过温','下行功放过温','上行功放驻波门限告警','下行功放驻波门限告警
#	','收发信号告警',

alarmflags=['HPAWARN','NULL','SELFEXWARN','DOORWARN','POWOFF',
			'UPLNAWRONG','DOWNLNAWRONG','RAYRSWRONG','POWERMODULEWRONG','UPAMPOVERPOWER',
			'DOWNAMPOVERPOWER','UPAMPOVERTEMP','DOWNAMPOVERTEMP','UPAMPWAVEWARN',
			'DOWNAMPWAVEWARN','SIGNALWARN']

#-------------------------------------------------------------------------------------
#通信参数
COMM_MODE_BY_ID ={'0':unicode('CDMA短消息'),'1':unicode('有线Modem'),'2':unicode('无线Modem'),'4':unicode('分组型数据传递')}
COMM_MODE_BY_TITLE = {unicode('CDMA短消息'):0,unicode('有线Modem'):1,unicode('无线Modem'):2,unicode('分组型数据传递'):4}			

#-------------------------------------------------------------------------------------

#Transfer status
transfer_status={'0':"->MSS",
					'1':'->CSS',
					'2':'->Repeater',
					'100':'NMC<-'
				}
#-------------------------------------------------------------------------------------
#    设备类型
#-------------------------------------------------------------------------------------
dev_cat={	'1':unicode('移频直放站近端机'),
			'2':unicode('移频直放站远端机'),
			'3':unicode('选频直放站'),
			'4':unicode('宽带直放站'),
			'5':unicode('光纤直放站近端机'),
			'6':unicode('光纤直放站远端机'),
			'7':unicode('干放直放站近端机'),
			'8':unicode('单设备主机')	#用于灵通协议
		}
dev_cat2={	unicode('移频直放站近端机'):1,
			unicode('移频直放站远端机'):2,
			unicode('选频直放站'):3,
			unicode('宽带直放站'):4,
			unicode('光纤直放站近端机'):5,
			unicode('光纤直放站远端机'):6,
			unicode('干放直放站近端机'):7,
			unicode('单设备主机'):8
		}


switch={'0':unicode('开'),'5':unicode('关')}	
switch2 ={unicode('开'):0,unicode('关'):5}




cmd_list ={"UPOUTPUTPOWERWARN":73,"DOWNOUTPUTPOWERWARN":73,#设置门限之值
				"UPAMPSWITCH":74,"DOWNAMPSWITCH":74,	#设置供方开关
				"REPEATERID":70,"EQUIPMENTID":70,		#直放站系统编号
				"NMS_PHONE":71,"ALARM_PHONE":71,"RCOMMODE":71 , #远程通信参数
				"UPATTEN":75,"DOWNATTEN":75,		#设置衰减量
				"WORKCHANNEL":76,"FSCHANNEL":76,    ##设置信道号	
				"SETALCSWITCH":77,		 #77设置ALC功能开关
						
				"CSS_QUERY":10 ,		#10 对CSS的统计参数的查询			
				"MSS_QUERY":12,			# 对MSS的统计参数的查询
				"MSS_CONFIG":13, 		#对MSS配置参数的修改
				"UPDATE_DEV_LIST":14, 	#直放站列表需要更新
				"NMS_PARAM_QUERY":60, 	#表示网管参数查询
				"DEV_STATUS":61, 		#表示直放站参数查询
				"SET_REPEATER_ID":70 ,	#表示设置直放站编号
				"SET_REMOTE_COMM":71 ,	# 表示设置远程通信参数
				"SET_AUTO_ALARM_FLAG":72	# 表示设置主动告警使能标志
				
				
			}
single_cmd ={'73':["UPOUTPUTPOWERWARN","DOWNOUTPUTPOWERWARN"],
			 '74':["UPAMPSWITCH","DOWNAMPSWITCH"],	#设置供方开关
			 '70':["REPEATERID","EQUIPMENTID"],		#直放站系统编号
			 '71':["NMS_PHONE","ALARM_PHONE","RCOMMODE"],  #远程通信参数
			 '75':["UPATTEN","DOWNATTEN"],		#设置衰减量
			 '76':["WORKCHANNEL","FSCHANNEL"],  ##设置信道号				
			 '77':["SETALCSWITCH"]  ##77设置ALC功能开关
			}			

errors={'0':unicode('成功'),
				'1':unicode('命令编号错'),
				'2':unicode('直放站编号错'),
				'3':unicode('设备编号错'),
				'4':unicode('包序号错'),
				'5':unicode('校验错'),
				'6':unicode('主叫电话错')				
			}


#灵通设备参数定义
#数据包定义
CMD_REMOTE_CTRL=72 			#遥控
CMD_REMOTE_TEST = 61 		#遥测 
CMD_REMOTE_SYS_QUERY =73 	# 系统设置查询
CMD_REMOTE_SYS_SET = 71		#系统设置


#ADC数据
# struct define ==> hash{ repeatertype=>[ADC0..ADC13]}
#WYG04GSM标准
wyg04gsmstd=[	unicode('功放电源检测'),		#ADC0
				unicode('前置电源检测'),		#ADC1
				unicode('上行通道1输出功率'),	#ADC2	
				unicode('上行功放温度检测'),	#ADC3
				unicode('上行通道2输出功率'),	#ADC4
				unicode('下行功放温度检测'),	#ADC5
				unicode('下行通道2输出功率'),	#ADC6
				unicode('下行通道1输出功率'),	#ADC7
				unicode('上行通道1功放检测'),	#ADC8
				unicode('上行通道2功放检测'),	#ADC9
				unicode('下行通道1功放检测'),	#ADC10
				unicode('下行通道2功放检测'),	#ADC11		
				unicode('备用'),				#ADC12
				unicode('备用'),					#ADC13				
				'',
				'',
				''
			]
			
wyg04II=[		unicode('功放电源检测'), #ADC0
				unicode('前置电源检测'),
				unicode('上行功放输出功率'),
				unicode('上行功放温度检测'),
				unicode('上行功放控制电压检测'),
				unicode('下行功放温度检测'),
				unicode('下行功放控制电压检测'),
				unicode('下行功放输出功率'),
				unicode(''),
				unicode(''),				
				unicode(''),
				unicode(''),				
				unicode('备用'),
				unicode('备用'),
				'',
				'',
				''				
			]

wyg04V=[		unicode('功放电源检测'),		#ADC0
				unicode('前置电源检测'),		#ADC1
				unicode('上行功放输出功率'),	#ADC2	
				unicode('上行功放温度检测'),	#ADC3
				unicode('上行功放控制电压检测'),	#ADC4
				unicode('下行功放输出功率'),	#ADC5
				unicode('下行功放温度检测'),	#ADC6
				unicode('下行功放控制电压检测'),	#ADC7
				unicode(''),	#ADC8
				unicode(''),	#ADC9
				unicode(''),	#ADC10
				unicode(''),	#ADC11		
				unicode('备用'),				#ADC12
				unicode('备用'),				#ADC13				
				'',
				'',
				''
			]

wyg04VI=[	unicode('功放电源检测'),		#ADC0
				unicode('前置电源检测'),		#ADC1
				unicode('上行功放输出功率'),	#ADC2	
				unicode('上行功放温度检测'),	#ADC3
				unicode('上行功放控制电压检测'),	#ADC4
				unicode('下行功放温度检测'),	#ADC5
				unicode('下行功放控制电压检测'),	#ADC6
				unicode('下行功放输出功率'),	#ADC7
				unicode(''),	#ADC8
				unicode(''),	#ADC9
				unicode(''),	#ADC10
				unicode(''),	#ADC11		
				unicode('备用'),				#ADC12
				unicode('备用'),					#ADC13				
				'',
				'',
				''
			]

adc_hash={
			'1':wyg04gsmstd,
			'2':wyg04II,
			'3':wyg04V,
			'4':wyg04VI
		}	
		
#数字电平检测定义
# D0..D15
dp_wyg04gsmstd=[	unicode('下行载频1锁定'),					#D0				
					unicode('下行载频2锁定'),					#D1				
					unicode('上行载频1锁定'),					#D2				
					unicode('上行载频2锁定'),					#D3				
					unicode('上行功放状态指示'),					#D4				
					unicode('上行功放起控指示'),					#D5				
					unicode('上行功放驻波指示'),					#D6				
					unicode('上行功放低噪指示'),					#D7				
					unicode('上行功放状态指示'),					#D8				
					unicode('下行功放起控指示'),					#D9				
					unicode('上行功放驻波指示'),					#D10				
					unicode('上行功放低噪指示'),					#D11				
					unicode('下行功放状态指示'),					#D12				
					unicode(''),					#D13				
					unicode(''),					#D14			
					unicode('门禁指示')		#D15				
				]

dp_wyg04II=[		unicode(''),					#D0				
					unicode(''),					#D1				
					unicode('上行选频锁定指示'),					#D2				
					unicode('下行选频锁定指示'),					#D3				
					unicode('上行功放状态指示'),					#D4				
					unicode('上行功放起控指示'),					#D5				
					unicode('上行功放驻波指示'),					#D6				
					unicode('上行功放低噪指示'),					#D7				
					unicode('上行功放状态指示'),					#D8				
					unicode('下行功放起控指示'),					#D9				
					unicode('上行功放驻波指示'),					#D10				
					unicode('上行功放低噪指示'),					#D11				
					unicode('下行功放状态指示'),					#D12				
					unicode(''),					#D13				
					unicode(''),					#D14			
					unicode('门禁指示')		#D15				
				]
dp_wyg04V=[			unicode(''),					#D0				
					unicode(''),					#D1				
					unicode('上行选频锁定指示'),					#D2				
					unicode('下行选频锁定指示'),					#D3				
					unicode('上行功放状态指示'),					#D4				
					unicode('上行功放起控指示'),					#D5				
					unicode('上行功放驻波指示'),					#D6				
					unicode('上行功放低噪指示'),					#D7				
					unicode('上行功放状态指示'),					#D8				
					unicode('下行功放起控指示'),					#D9				
					unicode('上行功放驻波指示'),					#D10				
					unicode('上行功放低噪指示'),					#D11				
					unicode('下行功放状态指示'),					#D12				
					unicode(''),					#D13				
					unicode(''),					#D14			
					unicode('门禁指示')		#D15				
				]
				
dp_wyg04VI=[		unicode('载频1锁定指示'),					#D0				
					unicode('载频1锁定指示'),					#D1				
					unicode('载频1锁定指示'),					#D2				
					unicode('载频1锁定指示'),					#D3				
					unicode('上行功放状态指示'),					#D4				
					unicode('上行功放起控指示'),					#D5				
					unicode('上行功放驻波指示'),					#D6				
					unicode('上行功放低噪指示'),					#D7				
					unicode('上行功放状态指示'),					#D8				
					unicode('下行功放起控指示'),					#D9				
					unicode('上行功放驻波指示'),					#D10				
					unicode('上行功放低噪指示'),					#D11				
					unicode('下行功放状态指示'),					#D12				
					unicode(''),					#D13				
					unicode(''),					#D14			
					unicode('门禁指示')		#D15				
				]
				
dp_hash={
			'1':dp_wyg04gsmstd,
			'2':dp_wyg04II,
			'3':dp_wyg04V,
			'4':dp_wyg04VI
		}
		
LT_ALARM_SWITCH={unicode('告警'):0,unicode('不告警'):1}
LT_ALARM_SWITCH2={'0':unicode('告警'),'1':unicode('不告警')}





