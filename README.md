Seller Sub-locality Visualisation

Aim: 
To visualise the orders placed by sellers in each sub-locality of selected cluster in d3.js. This visualisation is similar to Les Misérables Co-occurrence. (https://bost.ocks.org/mike/miserables/). 

Description:
Order count of all the sellers in past 1 month is displayed for each sub-locality in a colour coded manner. Database credentials is to be mentioned in dbConfig.py. A separate python script is executed first, which fetches the data from database. It fetches the list of cities, cluster name and cluster Ids for drop down menu. It also creates directories for every cluster, for example Cluster_id_1. In each directory, it stores the list of seller’s name in output_seller.csv, list of cluster’s name in output_subloc.csv, order count of a given seller in a particular sub-locality is mentioned in output_seller_subloc.csv. Output_seller_subloc.csv is modified in which seller’s name is replaced by the index at which they appeared in output_seller.csv and column is named as source. Similarly, sub-localities names are replaced by the index at which they appeared in output_subloc.csv and column is named as target. The third column is value in which order counts are bucketed and finally has a range of 1 to 10. This file is saved as Output_seller_subloc_list.csv. The list of buckets are stored in legend.csv. These files are then fetched in av4.html.
 
