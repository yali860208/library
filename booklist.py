#coding=utf-8

import csv
import sys



x2_read = csv.DictReader(open('booklist2.csv','r',encoding='utf-8'))
#header = x2_read.fieldnames



with open('booklist1.csv','a',encoding='utf-8') as f:
	my_read = csv.DictWriter(f, fieldnames=['條碼書目','書名'])
	my_read.writeheader()
	my_read.writerows(x2_read)
	#my_read.writerows(x2_read)


		#x1_read = csv.reader(x1)
		#members1 = [(row[0], row[1], row[2], row[3])for row in x1_read]
		#members1 = x1_read.fieldnames





