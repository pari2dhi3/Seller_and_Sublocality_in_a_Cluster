#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import csv
import re
import json
import mysql.connector as sqlcon
import dbConfig
import pandas
import os
import sys
import math

reload(sys)
sys.setdefaultencoding('utf-8')

# Open database connection
cnx = sqlcon.connect(user=dbConfig.USER, password=dbConfig.PWD,
                     host=dbConfig.HOST, database=dbConfig.DATABASE)

# prepare a cursor object using cursor() method
cursor = cnx.cursor()

# sql0 --> returns a list of Cluster Id's  
sql0 = "Query to select cluster id from database"
cursor.execute(sql0)
cluster_id = cursor.fetchall()

#loop is running for each cluster
for k in cluster_id:
	#curr_direc = os.getcwd()
	#os.mkdir("Cluster_id_"+str(k[0]))
	os.system('mkdir -p Cluster_id_' + str(k[0]))
	os.chdir("Cluster_id_"+str(k[0]))
	# Prepare SQL query to INSERT a record into the database.
	# sql1 --> order count sublocality wise in all the sellers. 
	# sql2 --> list of sublocality and their order count
	# sql3 --> list of seller and their order count
	sql1 = "Order count by sellers within a sublocality for kth cluster"

	sql2 = "List of sublocalities and their order count for kth cluster"

	sql3 = "List of sellers and their order count for kth cluster"

	# Execute the sql1 command
	cursor.execute(sql1)

	# Fetch all the rows in a list of lists.
	results1 = cursor.fetchall()

	#Write output of sql1 in a CSV file. 
	with open("output_seller_subloc.csv", "wb") as f:
	    writer = csv.writer(f)
	    writer.writerow(["seller_id","seller_name","sublocality_id","sublocality_name","order_count"])
	    writer.writerows(results1)

	# Execute the sql2 command
	cursor.execute(sql2)
	
	# Fetch all the rows in a list of lists.
	results2 = cursor.fetchall()

	#Write output of sql2 in a CSV file. 
	with open("output_subloc.csv", "wb") as f:
	    writer = csv.writer(f)
	    writer.writerow(["sublocality_id","subloclaity_name","order_count"])
	    writer.writerows(results2)

	# Execute the SQL3 command
	cursor.execute(sql3)

	# Fetch all the rows in a list of lists.
	results3 = cursor.fetchall()

	#Write output of sql3 in a CSV file. 
	with open("output_seller.csv", "wb") as f:
	    writer = csv.writer(f)
	    writer.writerow(["seller_id","seller_name","order_count"])
	    writer.writerows(results3)

	with open("output_subloc_list.csv", "wb") as f:
	    writer = csv.writer(f)
	    writer.writerow(["name"])
	    for i in range(len(results2)):
	    	writer.writerow([(results2[i][1])])    

	with open("output_seller_list.csv", "wb") as f:
	    writer = csv.writer(f)
	    writer.writerow(["name"])
	    for i in range(len(results3)):
	    	writer.writerow([(results3[i][1])]) 

	results4=[[0] * 3 for i in range(len(results1))]
	results5=[[0] * 1 for i in range(10)]
	max_value=0
	min_value=0

	#write CSV file of Seller and Subloc matrix that will be converted to JSON
	with open("output_seller_subloc_list.csv", "wb") as f:
		for i in range(len(results3)):    #results3			|Seller_id|Seller Name|Order Count|
			for j in range(len(results1)):		#results1		|seller_id|seller_name|sublocality_id|sublocality_name|order_count|
				results4[j][2]=results1[j][4]		#results4		|			|		|order_count|		|
				max_value = max(results4[j][2],max_value)
				min_value = min(results4[j][2],min_value)
				if(results3[i][0]==results1[j][0]):
					results4[j][0]=int(i)

		for i in range(len(results2)):
			for j in range(len(results1)):
				if(results2[i][0]==results1[j][2]):
					results4[j][1]=int(i)

		#bucketing the order count and setting its range from 1 to 10.
		bucket_size=math.ceil((max_value-min_value)*1.0/10)

		for i in range(len(results4)):
			results4[i][2]=math.ceil(results4[i][2]*1.0/bucket_size)

		prev = min_value
		for i in range(10):
			results5[i][0]=(''+str(prev+1)+'-'+str(prev+bucket_size))
			prev += bucket_size 

		writer = csv.writer(f)
		writer.writerow(["source","target","value"])
		writer.writerows(results4)

	#saving the buckets as legend in a CSV file
	with open("legend.csv", "wb") as g:
		writer = csv.writer(g)
		writer.writerow(["legend"])
		writer.writerows(results5)

	#go to previous directory
	os.chdir("..")

# sql4 --> prepare city list for drop down menu 
sql4 = "Prepare city list drop down menu"

# sql5 --> prepare cluster list for drop down menu
sql5 = "Prepare cluster list drop down menu"

# Execute the sql4 command
cursor.execute(sql4)

# Fetch all the rows in a list of lists.
city_list = cursor.fetchall()

#Write output of sql4 in a CSV file. 
with open("city_list.csv", "wb") as f:
    writer = csv.writer(f)
    writer.writerow(["City"])
    writer.writerows(city_list)

# Execute the sql5 command
cursor.execute(sql5)

# Fetch all the rows in a list of lists.
cluster_list = cursor.fetchall()

#Write output of sql5 in a CSV file. 
with open("cluster_list.csv", "wb") as f:
    writer = csv.writer(f)
    writer.writerow(["Cluster_id", "Cluster_name", "City"])
    writer.writerows(cluster_list)

# disconnect from server
cnx.close()