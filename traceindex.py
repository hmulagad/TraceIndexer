########################################################################################################
## Author: Harikishan Mulagada
## Role  : Staff Engineer SteelCentral
## Date  : Jun 20th 2018
##
## The script will create folder structure in AS based on the raw trace file name and then kick off
## reindex command.
########################################################################################################

import os
import subprocess

##Function to get list of all trace file names
def _trace_list(path):
	traces = []
	basepath = '/mnt/data/silo/data/traces/app/'
	username = 'appinternals'

	try:
		for tname in os.listdir(path):
			if tname.endswith('.apptrace'):
				traces.append(tname)
		
		for name in traces:
			##print(name)
			##print(name[name.index('@'):])
			##print(name.split('@'))
			##print(name.split('@')[1])
			##print('DSA-'+name.split('@')[2])
			##print(name.split('@')[1].split('-'))
			##print(name.split('@')[1].split('-')[2].split('_')[0])
			dirname = basepath+'DSA-'+name.split('@')[2]+'/'+name.split('@')[1].split('-')[0]+'/'+name.split('@')[1].split('-')[1]+'/'+name.split('@')[1].split('-')[2].split('_')[0]+'/'+name.split('@')[1].split('-')[2].split('_')[1].split('.')[0]
			filename = os.path.abspath(path+'/'+name)
			##print(basepath+'DSA-'+name.split('@')[2]+'/'+name.split('@')[1].split('-')[0]+'/'+name.split('@')[1].split('-')[1]+'/'+name.split('@')[1].split('-')[2].split('_')[0]+'/'+name.split('@')[1].split('-')[2].split('_')[1].split('.')[0])
			
			print('Creating folder...',dirname)
			subprocess.call(['mkdir','-p',dirname])
			
			print('Copying '+filename+' to '+dirname)
			subprocess.call(['cp',filename,dirname])

			print('Changing permissions.... ')
			subprocess.call(['chown','-R',username,os.path.abspath(basepath+'DSA-'+name.split('@')[2])])

		_reindex()

	except Exception as e:
		print(e)

##Function to call reindex on Analysis server
def _reindex():
	try:
		print('Do you want to reindex? (Y/N)')
		reindex_flag = raw_input()

		if (reindex_flag == 'Y' or reindex_flag == 'y'):
			try:
				subprocess.call(['curl','http://localhost:29102/reindex'])
			except Exception as e:
				print(e)
		else:
			return
	except Exception as e:
		print(e)

##Main function
def main():
	print('Enter the full path to trace files :')
	path = raw_input()

	_trace_list(path)


main()
