


#����������



appspecs = {'window_font':('����',10)}

#-------------------------------------------------------------------------------------
#�澯������
warninglevel={'0':unicode('����'),
				'1':unicode('һ��'),
				'2':unicode('��Ҫ'),
				'3':unicode('����')
			}

WGREEN=0
WYELLO=1
WBLUE=2
WRED =3
WCOLOR = {'0':'green','1':'yellow','2':'blue','3':'red'}
#-------------------------------------------------------------------------------------
#   �澯ʹ�ܱ�־  ���� 0-15 λ
#-------------------------------------------------------------------------------------
#	'HPA','����','�Լ��澯','�Ž�澯','��Դ����','���е���Ź���
#	','���е���Ź���','���շ�ģ�����','��Դģ�����','���й��Ź�����','���й��Ź�
#	����','���й��Ź���','���й��Ź���','���й���פ�����޸澯','���й���פ�����޸澯
#	','�շ��źŸ澯',

alarmflags=['HPAWARN','NULL','SELFEXWARN','DOORWARN','POWOFF',
			'UPLNAWRONG','DOWNLNAWRONG','RAYRSWRONG','POWERMODULEWRONG','UPAMPOVERPOWER',
			'DOWNAMPOVERPOWER','UPAMPOVERTEMP','DOWNAMPOVERTEMP','UPAMPWAVEWARN',
			'DOWNAMPWAVEWARN','SIGNALWARN']

#-------------------------------------------------------------------------------------
#ͨ�Ų���
COMM_MODE_BY_ID ={'0':unicode('CDMA����Ϣ'),'1':unicode('����Modem'),'2':unicode('����Modem'),'4':unicode('���������ݴ���')}
COMM_MODE_BY_TITLE = {unicode('CDMA����Ϣ'):0,unicode('����Modem'):1,unicode('����Modem'):2,unicode('���������ݴ���'):4}			

#-------------------------------------------------------------------------------------

#Transfer status
transfer_status={'0':"->MSS",
					'1':'->CSS',
					'2':'->Repeater',
					'100':'NMC<-'
				}
#-------------------------------------------------------------------------------------
#    �豸����
#-------------------------------------------------------------------------------------
dev_cat={	'1':unicode('��Ƶֱ��վ���˻�'),
			'2':unicode('��Ƶֱ��վԶ�˻�'),
			'3':unicode('ѡƵֱ��վ'),
			'4':unicode('���ֱ��վ'),
			'5':unicode('����ֱ��վ���˻�'),
			'6':unicode('����ֱ��վԶ�˻�'),
			'7':unicode('�ɷ�ֱ��վ���˻�'),
			'8':unicode('���豸����')	#������ͨЭ��
		}
dev_cat2={	unicode('��Ƶֱ��վ���˻�'):1,
			unicode('��Ƶֱ��վԶ�˻�'):2,
			unicode('ѡƵֱ��վ'):3,
			unicode('���ֱ��վ'):4,
			unicode('����ֱ��վ���˻�'):5,
			unicode('����ֱ��վԶ�˻�'):6,
			unicode('�ɷ�ֱ��վ���˻�'):7,
			unicode('���豸����'):8
		}


switch={'0':unicode('��'),'5':unicode('��')}	
switch2 ={unicode('��'):0,unicode('��'):5}




cmd_list ={"UPOUTPUTPOWERWARN":73,"DOWNOUTPUTPOWERWARN":73,#��������ֵ֮
				"UPAMPSWITCH":74,"DOWNAMPSWITCH":74,	#���ù�������
				"REPEATERID":70,"EQUIPMENTID":70,		#ֱ��վϵͳ���
				"NMS_PHONE":71,"ALARM_PHONE":71,"RCOMMODE":71 , #Զ��ͨ�Ų���
				"UPATTEN":75,"DOWNATTEN":75,		#����˥����
				"WORKCHANNEL":76,"FSCHANNEL":76,    ##�����ŵ���	
				"SETALCSWITCH":77,		 #77����ALC���ܿ���
						
				"CSS_QUERY":10 ,		#10 ��CSS��ͳ�Ʋ����Ĳ�ѯ			
				"MSS_QUERY":12,			# ��MSS��ͳ�Ʋ����Ĳ�ѯ
				"MSS_CONFIG":13, 		#��MSS���ò������޸�
				"UPDATE_DEV_LIST":14, 	#ֱ��վ�б���Ҫ����
				"NMS_PARAM_QUERY":60, 	#��ʾ���ܲ�����ѯ
				"DEV_STATUS":61, 		#��ʾֱ��վ������ѯ
				"SET_REPEATER_ID":70 ,	#��ʾ����ֱ��վ���
				"SET_REMOTE_COMM":71 ,	# ��ʾ����Զ��ͨ�Ų���
				"SET_AUTO_ALARM_FLAG":72	# ��ʾ���������澯ʹ�ܱ�־
				
				
			}
single_cmd ={'73':["UPOUTPUTPOWERWARN","DOWNOUTPUTPOWERWARN"],
			 '74':["UPAMPSWITCH","DOWNAMPSWITCH"],	#���ù�������
			 '70':["REPEATERID","EQUIPMENTID"],		#ֱ��վϵͳ���
			 '71':["NMS_PHONE","ALARM_PHONE","RCOMMODE"],  #Զ��ͨ�Ų���
			 '75':["UPATTEN","DOWNATTEN"],		#����˥����
			 '76':["WORKCHANNEL","FSCHANNEL"],  ##�����ŵ���				
			 '77':["SETALCSWITCH"]  ##77����ALC���ܿ���
			}			

errors={'0':unicode('�ɹ�'),
				'1':unicode('�����Ŵ�'),
				'2':unicode('ֱ��վ��Ŵ�'),
				'3':unicode('�豸��Ŵ�'),
				'4':unicode('����Ŵ�'),
				'5':unicode('У���'),
				'6':unicode('���е绰��')				
			}


#��ͨ�豸��������
#���ݰ�����
CMD_REMOTE_CTRL=72 			#ң��
CMD_REMOTE_TEST = 61 		#ң�� 
CMD_REMOTE_SYS_QUERY =73 	# ϵͳ���ò�ѯ
CMD_REMOTE_SYS_SET = 71		#ϵͳ����


#ADC����
# struct define ==> hash{ repeatertype=>[ADC0..ADC13]}
#WYG04GSM��׼
wyg04gsmstd=[	unicode('���ŵ�Դ���'),		#ADC0
				unicode('ǰ�õ�Դ���'),		#ADC1
				unicode('����ͨ��1�������'),	#ADC2	
				unicode('���й����¶ȼ��'),	#ADC3
				unicode('����ͨ��2�������'),	#ADC4
				unicode('���й����¶ȼ��'),	#ADC5
				unicode('����ͨ��2�������'),	#ADC6
				unicode('����ͨ��1�������'),	#ADC7
				unicode('����ͨ��1���ż��'),	#ADC8
				unicode('����ͨ��2���ż��'),	#ADC9
				unicode('����ͨ��1���ż��'),	#ADC10
				unicode('����ͨ��2���ż��'),	#ADC11		
				unicode('����'),				#ADC12
				unicode('����'),					#ADC13				
				'',
				'',
				''
			]
			
wyg04II=[		unicode('���ŵ�Դ���'), #ADC0
				unicode('ǰ�õ�Դ���'),
				unicode('���й����������'),
				unicode('���й����¶ȼ��'),
				unicode('���й��ſ��Ƶ�ѹ���'),
				unicode('���й����¶ȼ��'),
				unicode('���й��ſ��Ƶ�ѹ���'),
				unicode('���й����������'),
				unicode(''),
				unicode(''),				
				unicode(''),
				unicode(''),				
				unicode('����'),
				unicode('����'),
				'',
				'',
				''				
			]

wyg04V=[		unicode('���ŵ�Դ���'),		#ADC0
				unicode('ǰ�õ�Դ���'),		#ADC1
				unicode('���й����������'),	#ADC2	
				unicode('���й����¶ȼ��'),	#ADC3
				unicode('���й��ſ��Ƶ�ѹ���'),	#ADC4
				unicode('���й����������'),	#ADC5
				unicode('���й����¶ȼ��'),	#ADC6
				unicode('���й��ſ��Ƶ�ѹ���'),	#ADC7
				unicode(''),	#ADC8
				unicode(''),	#ADC9
				unicode(''),	#ADC10
				unicode(''),	#ADC11		
				unicode('����'),				#ADC12
				unicode('����'),				#ADC13				
				'',
				'',
				''
			]

wyg04VI=[	unicode('���ŵ�Դ���'),		#ADC0
				unicode('ǰ�õ�Դ���'),		#ADC1
				unicode('���й����������'),	#ADC2	
				unicode('���й����¶ȼ��'),	#ADC3
				unicode('���й��ſ��Ƶ�ѹ���'),	#ADC4
				unicode('���й����¶ȼ��'),	#ADC5
				unicode('���й��ſ��Ƶ�ѹ���'),	#ADC6
				unicode('���й����������'),	#ADC7
				unicode(''),	#ADC8
				unicode(''),	#ADC9
				unicode(''),	#ADC10
				unicode(''),	#ADC11		
				unicode('����'),				#ADC12
				unicode('����'),					#ADC13				
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
		
#���ֵ�ƽ��ⶨ��
# D0..D15
dp_wyg04gsmstd=[	unicode('������Ƶ1����'),					#D0				
					unicode('������Ƶ2����'),					#D1				
					unicode('������Ƶ1����'),					#D2				
					unicode('������Ƶ2����'),					#D3				
					unicode('���й���״ָ̬ʾ'),					#D4				
					unicode('���й������ָʾ'),					#D5				
					unicode('���й���פ��ָʾ'),					#D6				
					unicode('���й��ŵ���ָʾ'),					#D7				
					unicode('���й���״ָ̬ʾ'),					#D8				
					unicode('���й������ָʾ'),					#D9				
					unicode('���й���פ��ָʾ'),					#D10				
					unicode('���й��ŵ���ָʾ'),					#D11				
					unicode('���й���״ָ̬ʾ'),					#D12				
					unicode(''),					#D13				
					unicode(''),					#D14			
					unicode('�Ž�ָʾ')		#D15				
				]

dp_wyg04II=[		unicode(''),					#D0				
					unicode(''),					#D1				
					unicode('����ѡƵ����ָʾ'),					#D2				
					unicode('����ѡƵ����ָʾ'),					#D3				
					unicode('���й���״ָ̬ʾ'),					#D4				
					unicode('���й������ָʾ'),					#D5				
					unicode('���й���פ��ָʾ'),					#D6				
					unicode('���й��ŵ���ָʾ'),					#D7				
					unicode('���й���״ָ̬ʾ'),					#D8				
					unicode('���й������ָʾ'),					#D9				
					unicode('���й���פ��ָʾ'),					#D10				
					unicode('���й��ŵ���ָʾ'),					#D11				
					unicode('���й���״ָ̬ʾ'),					#D12				
					unicode(''),					#D13				
					unicode(''),					#D14			
					unicode('�Ž�ָʾ')		#D15				
				]
dp_wyg04V=[			unicode(''),					#D0				
					unicode(''),					#D1				
					unicode('����ѡƵ����ָʾ'),					#D2				
					unicode('����ѡƵ����ָʾ'),					#D3				
					unicode('���й���״ָ̬ʾ'),					#D4				
					unicode('���й������ָʾ'),					#D5				
					unicode('���й���פ��ָʾ'),					#D6				
					unicode('���й��ŵ���ָʾ'),					#D7				
					unicode('���й���״ָ̬ʾ'),					#D8				
					unicode('���й������ָʾ'),					#D9				
					unicode('���й���פ��ָʾ'),					#D10				
					unicode('���й��ŵ���ָʾ'),					#D11				
					unicode('���й���״ָ̬ʾ'),					#D12				
					unicode(''),					#D13				
					unicode(''),					#D14			
					unicode('�Ž�ָʾ')		#D15				
				]
				
dp_wyg04VI=[		unicode('��Ƶ1����ָʾ'),					#D0				
					unicode('��Ƶ1����ָʾ'),					#D1				
					unicode('��Ƶ1����ָʾ'),					#D2				
					unicode('��Ƶ1����ָʾ'),					#D3				
					unicode('���й���״ָ̬ʾ'),					#D4				
					unicode('���й������ָʾ'),					#D5				
					unicode('���й���פ��ָʾ'),					#D6				
					unicode('���й��ŵ���ָʾ'),					#D7				
					unicode('���й���״ָ̬ʾ'),					#D8				
					unicode('���й������ָʾ'),					#D9				
					unicode('���й���פ��ָʾ'),					#D10				
					unicode('���й��ŵ���ָʾ'),					#D11				
					unicode('���й���״ָ̬ʾ'),					#D12				
					unicode(''),					#D13				
					unicode(''),					#D14			
					unicode('�Ž�ָʾ')		#D15				
				]
				
dp_hash={
			'1':dp_wyg04gsmstd,
			'2':dp_wyg04II,
			'3':dp_wyg04V,
			'4':dp_wyg04VI
		}
		
LT_ALARM_SWITCH={unicode('�澯'):0,unicode('���澯'):1}
LT_ALARM_SWITCH2={'0':unicode('�澯'),'1':unicode('���澯')}





