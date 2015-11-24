import csv



f = open('country_city_location.txt', 'r')
record_list = []

for line in f:
	l = line.split(" ")
	l_new = []
	for w in l:
		if not w == "":
			w.replace("：", ".")
			l_new.append(w)
			# print(l_new)
	record_list.append(l_new)	
	# print(l_new)

for i in range(len(record_list) - 1):
	# print(record_list[i])
	if "-" in record_list[i][4]:
		record_list[i][2] = "-" + record_list[i][2]

	print(record_list[i])

f2 = open('country_city_location.csv', 'w')
previous_country = ""

for record in record_list:
	if len(record) >= 4:
		#original version - country AND city
		# f2.write(record[0] + "," + record[1] + "," + record[2] + "," + record[3] + "\n")

		if record[0] == previous_country:
			f2.write(record[1] + "," + record[2] + "," + record[3] + "\n")
		else:
			f2.write(record[0] + "," + record[2] + "," + record[3] + "\n")
			f2.write(record[1] + "," + record[2] + "," + record[3] + "\n")
		previous_country = record[0]

