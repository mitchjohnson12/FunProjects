from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import time
import pyodbc
import numpy

#my_url = 'https://www.fantasypros.com/nfl/auction-values/calculator.php'
#my_url = 'https://draftwizard.fantasypros.com/auction/fp_nfl.jsp?tab=tabP&C=0&1B=0&2B=0&SS=0&3B=0&OF=0&SP=0&RP=0&BN=6&Util=0&P=0&CI=0&MI=0&IF=0&LF=0&CF=0&RF=0&scoring=STD&teams=10&tb=200'
my_url = https://www.fantasypros.com/nfl/auction-values/calculator.php
uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()
page_soup = soup(page_html, "html.parser")

tableArray = page_soup.findAll("table",{"class","ValueTable"})

playerSqlList = []
print('client opened')
for table in tableArray:
	
	tableType = table['id']
	position = tableType[:tableType.find("Table")]
	
	if position == 'Overall':
		continue
	
	playerArray = table.findAll("tr")
	
	for player in playerArray:
		columns = player.findAll("td")
		name_container = columns[1].get_text()
		comma_index = name_container.rfind(",")
		player_name = name_container[:comma_index]
		if comma_index != -1:
			player_team = name_container[comma_index + 1:].strip()
			player_name = name_container[:comma_index]
		else: 
			player_team = 'N/A'
			player_name = name_container
		player_value_str = columns[2].get_text()
		player_value = player_value_str[1:]
		player_value_ndx = columns[3].get_text()
				
		newLine = (player_name, player_team, player_value, player_value_ndx, position)

		playerSqlList.append(newLine)

print('list created')

cnxn = pyodbc.connect(driver='{SQL Server}', server='EPIC42594\SQLEXPRESS', database='FantasyFootball', trusted_connection='yes')
cursor = cnxn.cursor()
'''
zsstatement = "INSERT INTO dbo.AuctionValues VALUES (?,?,?,?,?)"
print('connection made')
cursor.executemany(statement, playerSqlList)
'''
print("insert into AuctionValues VALUES (%s,%s,%s,%s,%s)" % (playerSqlList[0][0], playerSqlList[0][1], playerSqlList[0][2], playerSqlList[0][3], playerSqlList[0][4]))
cursor.executemany("insert into AuctionValues VALUES (?,?,?,?,?)", playerSqlList)
cnxn.commit()
cursor.close()
cnxn.close()
print('connection closed') 


'''
rows = [(1,7,3000), (1,8,3500), (1,9,3900)]
values = ', '.join(map(str, rows))
sql = "INSERT INTO ... VALUES {}".format(values)
'''




''' WRITE TO FILE
timestr = time.strftime("%Y%m%d-%H%M%S")
FileName = "FantasyProsAuctionValues_" + timestr + ".csv"
headers = "Player, value, int_value\n"
f = open(FileName, "w")


for table in tableArray:
	
	tableType = table['id']
	f.write("\n" + tableType + '\n')
	f.write(headers)
	
	playerArray = table.findAll("tr")
	
	for player in playerArray:
		columns = player.findAll("td")
		player_name = columns[1].get_text()
		player_value = columns[2].get_text()
		player_value_int = columns[3].get_text()
		
		f.write(player_name.replace(",", "|") + "," + player_value + "," + player_value_int + "\n")
f.close()
'''

''' PRINT TO SCREEN
for player in containers:
	columns = player.findAll("td")
	player_name = columns[1].get_text()
	player_value = columns[2].get_text()
	player_value_int = columns[3].get_text()
	
	print("player_name: " + player_name)
	print("player_value: " + player_value)
	print("player_value_int: " + player_value_int)
	
	f.write(player_name.replace(",", "|") + "," + player_value + "," + player_value_int + "\n")
	

len(containers)
<tr '="" class="PlayerQB" pid="16413" pts="338" v="26">
<td class="RankCell"></td>
<td>Patrick Mahomes (KC - QB)</td>
<td class="AlignRight DollarValue AuctionControls">$26</td>
<td class="RealValue">26</td></tr>


<tr '="" class="PlayerWR" pid="15629" pts="113" v="6">
<td class="RankCell"></td>
<td>Will Fuller, HOU</td>
<td class="AlignRight DollarValue AuctionControls">$6</td>
<td class="RealValue">6</td>
</tr>
'''
