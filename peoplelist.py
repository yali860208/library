#coding=utf-8

import csv
import sys


x2_read = csv.DictReader(open('peoplelist2.csv','r',encoding='utf-8'))
header = x2_read.fieldnames

with open('peoplelist1.csv','a',encoding='utf-8') as f:
	x1_read = csv.DictWriter(f, fieldnames=header)
	x1_read.writerows(x2_read)


		#x1_read = csv.reader(x1)
		#members1 = [(row[0], row[1], row[2], row[3])for row in x1_read]
		#members1 = x1_read.fieldnames





