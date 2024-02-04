from flet import *
import flet as ft
import mysql.connector
import streamlit as st 


#TESTE_2801

# CONECTION TO DB
mydb = mysql.connector.connect(
	host='localhost',
            user='root',
            password='Mari160571#',
            database='x_go'
	)

cursor = mydb.cursor()


def main(page:Page):
	nametxt = TextField(label="name")
	agetxt = TextField(label="age")
#  INPUT
	nametxt1 = TextField(label="name")
	agetxt1 = TextField(label="age")

	# CREATE EDIT 
	edit_nametxt = TextField(label="name")
	edit_agetxt = TextField(label="age")
	edit_id = Text()


#  INPUT
	edit_nametxt1 = TextField(label="name")
	edit_agetxt1 = TextField(label="age")
	edit_id1 = Text()

	mydt = DataTable(
		columns=[
			DataColumn(Text("id")),
			DataColumn(Text("name")),
			DataColumn(Text("age")),
			DataColumn(Text("actions")),
		],
		rows=[]

		)

#  INPUT
	mydt2 = DataTable(
		columns=[
			DataColumn(Text("id")),
			DataColumn(Text("name")),
			DataColumn(Text("age")),
			DataColumn(Text("actions")),
		],
		rows=[]

		)

	# DELETE FUNCTION
	def deletebtn(e):
		print("you selected id is = ",e.control.data['id'])
		try:
			sql = "DELETE FROM TESTE_2801a WHERE id = %s"
			val = (e.control.data['id'],)
			cursor.execute(sql,val)
			mydb.commit()
			print("you deleted !!!")
			mydt.rows.clear()
			load_data()

			# AND SHOW SNACBAR

			page.snack_bar = SnackBar(
				Text("Data success Deleted",size=30),
				bgcolor="red"

				)
			page.snack_bar.open = True
			page.update()
		except Exception as e:
			print(e)
			print("error you code for delete")


	def savedata(e):
		try:
			sql = "UPDATE TESTE_2801a SET age = %s , name = %s WHERE id = %s"
			val = (edit_agetxt.value,edit_nametxt.value,edit_id.value)
			cursor.execute(sql,val)
			mydb.commit()
			print("you succes edit data")
			dialog.open = False		
			page.update()

			# CLEAR EDIT TEXTFIELD
			edit_nametxt.value = ""
			edit_agetxt.value = ""
			edit_id.value = ""

			mydt.rows.clear()
			load_data()

			# AND SHOW SNACBAR

			page.snack_bar = SnackBar(
				Text("Data success EDIT",size=30),
				bgcolor="green"

				)
			page.snack_bar.open = True
			page.update()
		except Exception as e:
			print(e)
			print("ERROR SAVE EDIT !!!")

	# CREATE DIALOG SHOW WHEN YOU CLICK EDIT BUTTON
	dialog = AlertDialog(
		title=Text("Edit data"),
		content=Column([edit_nametxt,edit_agetxt	]),			actions=[			TextButton("Save",	on_click=savedata		)		]		)


	# EDIT FUNCTION
	def editbtn(e):
		edit_nametxt.value = e.control.data['name']
		edit_agetxt.value = e.control.data['age']
		edit_id.value = e.control.data['id']
		page.dialog = dialog
		dialog.open = True
		page.update()
		
		

	def load_data():
		# GET ALL DATA FROM DATABASE AND PUSH TO DATATABLE
		cursor.execute("SELECT * FROM TESTE_2801a")
		result = cursor.fetchall()

		# AND PUSH DATA TO DICT
		columns = [column[0] for column in cursor.description]
		rows = [dict(zip(columns,row)) for row in result]
		columns2=[columns]
		rows2=[rows]

		# LOOP AND PUSH
		for row in rows:
			mydt.rows.append(
				DataRow(
					cells=[
						DataCell(Text(row['id'])),
						DataCell(Text(row['name'])),
						DataCell(Text(row['age'])),
						DataCell(
							Row([
							IconButton("delete",icon_color="red",
								data=row,
								on_click=deletebtn
								),
							IconButton("create",icon_color="red",
								data=row,
								on_click=editbtn
								),
						


								])
							),

					]

					)

				)
		page.update()


	# AND CALL FUNCTION WHEN YOU APP IS FIRST OPEN
	load_data()







	def addtodb(e):
		try:
			
			sql = "INSERT INTO TESTE_2801a (name,age) VALUES(%s,%s)"
			val = (nametxt1.value,agetxt1.value)
			cursor.execute(sql,val)
			mydb.commit()
			print(cursor.rowcount,"YOU RECORD INSERT !!!")
			

			# AND CLEAR ROWS IN TABLE AND PUSH FROM DATABASE AGAIN
			mydt.rows.clear()
			load_data()

			# AND SHOW SNACBAR

			page.snack_bar = SnackBar(
				Text("Data success add",size=30),
				bgcolor="green"

				)
			page.snack_bar.open = True
			page.update()
		except Exception as e:
			print(e)
			print("error you CODE !!!!")

		# AND AFTER YOU SUCCESS INPUT TO DB THEN CLEAR TEXTINPUT
		nametxt1.value = ""
		agetxt1.value = ""
		page.update()
# CREATE DIALOG SHOW WHEN YOU CLICK INPUT BUTTON
	dialog2 = AlertDialog(
		title=Text("iMPUT data"),
		content=Column([edit_nametxt1,edit_agetxt1	]),		actions=[			TextButton("Save",	on_click=addtodb		)		]		)


	# EDIT FUNCTION
	def addtodb1(e):
		edit_nametxt1.value = e.control.data['name']
		edit_agetxt1.value = e.control.data['age']
		page.dialog = dialog2
		dialog.open = True
		page.update()
	

	page.add(mydt,
		  
	Column([
			Row([		
				IconButton("create",icon_color="blue",
				on_click=addtodb1	)]),
				edit_nametxt1,
				edit_agetxt1,
				ElevatedButton("add to db",	on_click=addtodb),	])		)
	


ft.app(target=main)