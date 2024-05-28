from tkinter import *
import pymysql
from tkinter import messagebox,filedialog
from tkinter import ttk
from datetime import *

taj=Tk()
width= taj.winfo_screenwidth()
print(width)
height = taj.winfo_screenheight()
print(height)

########## database connection
tazTV=ttk.Treeview(height=10,columns=('Item Name''Rate','Type'))
tazTV1=ttk.Treeview(height=10,columns=('Date''Name','Type','Rate','Total'))


########for char input
def only_char_input(P):
    if P.isalpha() or P=='':
        return True
    return False
callback=taj.register(only_char_input)
####### for digit
def only_numeric_input(P):
    if P.isdigit() or P=='':
        return True
    return False
callback2=taj.register(only_numeric_input)

def dbconfig():
    global conn,mycursor
    conn=pymysql.connect(host="localhost",user="root",db="myhotel")
    mycursor=conn.cursor()

####### clear screen
def clear_screen():
    global taj
    for widgets in taj.winfo_children():
        widgets.grid_remove()

########Logout######

def Logout():
    clear_screen()
    mainheading()
    loginwindow()

def mainheading():
    label = Label(taj, text="Hotel Taj Management System", fg="red", bg="yellow",
                  font=("comic sans Ms", 40, "bold"), padx=400, pady=0)
    label.grid(row=0, columnspan=4)

usernamevar=StringVar()
passwordvar=StringVar()


def loginwindow():
    usernamevar.set("")
    passwordvar.set("")
    labellogin=Label(taj, text="Admin Login",
                  font=("ariel", 25, "bold"))
    labellogin.grid(row=1,column=1,columnspan=2,padx=50,pady=10)

    usernameLabel=Label(taj,text="User Name",font=("ariel", 12, "bold"))
    usernameLabel.grid(row=2,column=1,padx=20,pady=5)

    passwordLabel = Label(taj, text="User Password",font=("ariel", 12, "bold"))
    passwordLabel.grid(row=3, column=1, padx=20, pady=5)

    usernameEntry=Entry(taj,textvariable=usernamevar)
    usernameEntry.grid(row=2,column=2,padx=20,pady=5)

    passwordEntry = Entry(taj,show="*" ,textvariable=passwordvar)
    passwordEntry.grid(row=3, column=2, padx=20, pady=5)

    loginButton=Button(taj,text="Login",width=20,height=2,fg="green",bd=10,command=adminLogin)
    loginButton.grid(row=4, column=1,columnspan=2, padx=20, pady=5)

def welcomewindow():
    clear_screen()
    mainheading()
    welcome = Label(taj, text="Welcome Admin",
                       font=("ariel", 25, "bold"))
    welcome.grid(row=1, column=1, columnspan=2, padx=50, pady=10)
    logoutButton = Button(taj, text="Logout", width=20, height=2, fg="green", bd=10, command=Logout)
    logoutButton.grid(row=4, column=1, columnspan=2, padx=20, pady=5)

    manageRest=Button(taj,text="Manage Hotel",width=20,height=2,fg="green",bd=10,command=addItemWindow)
    manageRest.grid(row=5,column=1, columnspan=2, padx=20, pady=5)

    billGen = Button(taj, text="Bill Generation", width=20, height=2, fg="red", bd=10, command=billWindow)
    billGen.grid(row=6, column=1, columnspan=2, padx=20, pady=5)

##### back button ######
def back():
    clear_screen()
    mainheading()
    welcomewindow()
############
def getItemInTreeview():
    # to delete already inserted data
    records=tazTV.get_children()
    for x in records:
        tazTV.delete(x)


    conn=pymysql.connect(host="localhost",user="root",db="myhotel")
    mycursor=conn.cursor(pymysql.cursors.DictCursor)
    query1="select * from itemlist"
    mycursor.execute(query1)
    data = mycursor.fetchall()
    #print(data)
    for row in data:
        tazTV.insert('','end',text=row['item_name'],values=(row["item_rate"],row["item_type"]))
    conn.close()

    tazTV.bind("<Double-1>",onDoubleClick)

###### Double click##############
def onDoubleClick(event):
    item=tazTV.selection()
    itemnameVar1=tazTV.item(item,"text")
    item_detail = tazTV.item(item, "values")
    itemnameVar.set(itemnameVar1)
    itemrateVar.set(item_detail[0])
    itemtypeVar.set(item_detail[1])

###########
######## update item#####
def updateitem():
    name=itemnameVar.get()
    rate=itemrateVar.get()
    type=itemtypeVar.get()
    dbconfig()
    que= "update itemlist set item_rate=%s,item_type=%s where item_name=%s"
    val=(rate,type,name)
    mycursor.execute(que,val)
    conn.commit()
    messagebox.showinfo("Updation confirmation","item updated successfully")
    itemnameVar.set("")
    itemrateVar.set("")
    itemtypeVar.set("")
    getItemInTreeview()

####### delete item###
def deleteitem():
    name=itemnameVar.get()
    rate=itemrateVar.get()
    type=itemtypeVar.get()
    dbconfig()
    que1= "delete from itemlist where item_name=%s"
    val=(name)
    mycursor.execute(que1,val)
    conn.commit()
    messagebox.showinfo("Delete confirmation","item deleted successfully")
    itemnameVar.set("")
    itemrateVar.set("")
    itemtypeVar.set("")
    getItemInTreeview()

##########
itemnameVar=StringVar()
itemrateVar=StringVar()
itemtypeVar=StringVar()
customerNameVar=StringVar()
mobileVar=StringVar()
combovariable=StringVar()
baserate=StringVar()
cost=StringVar()
qtyvariable=StringVar()
######## combo data######
def combo_input():
    dbconfig()
    mycursor.execute('Select item_name from itemlist')
    data=[]

    for row in mycursor.fetchall():
        data.append(row[0])
        #print(row[0])
    return data

##############optionCallBack

def optionCallBack(*args):
    global itemname
    itemname=combovariable.get()
    #print(itemname)
    aa=ratelist()
    print(aa)
    baserate.set(aa)
    global v
    for i in aa:
        for j in i:
            v=j
########### optionCallBack2

def optionCallBack2(*args):
    global qty
    qty=qtyvariable.get()
    final=int(v)*int(qty)
    cost.set(final)


####### ratelist
def ratelist():
    dbconfig()
    que2="select item_rate from itemlist where item_name=%s"
    val=(itemname)
    mycursor.execute(que2,val)
    data= mycursor.fetchall()
    #print(data)
    return data

############ bill Window#########
global x
x= datetime.now()
datetimeVar=StringVar()
datetimeVar.set(x)
def billWindow():
    clear_screen()
    mainheading()
    billitem = Label(taj, text="Generate Bill",
                    font=("ariel", 25, "bold"))
    billitem.grid(row=1, column=1, columnspan=2, padx=50, pady=10)

    logoutButton = Button(taj, text="Logout", width=20, height=2, fg="green", bd=10, command=Logout)
    logoutButton.grid(row=3, column=0, columnspan=1)

    backButton = Button(taj, text="Back", width=20, height=2, fg="green", bd=10, command=back)
    backButton.grid(row=4, column=0, columnspan=1)

    printButton = Button(taj, text="Print Bill", width=20, height=2, fg="green", bd=10, command=printBill)
    printButton.grid(row=5, column=0, columnspan=1)

    dateTimeLabel=Label(taj,text="Date & Time", font=("ariel", 15, "bold"))
    dateTimeLabel.grid(row=2,column=1,padx=20,pady=5)

    dateTimeEntry=Entry(taj,textvariable=datetimeVar, font=("ariel", 15, "bold"))
    dateTimeEntry.grid(row=2,column=2,padx=20,pady=5)

    customerNameLabel = Label(taj, text="Customer Name", font=("Customer Name", 15, "bold"))
    customerNameLabel.grid(row=3, column=1, padx=20, pady=5)


    customerNameEntry = Entry(taj, textvariable=customerNameVar, font=("ariel", 15, "bold"))
    customerNameEntry.grid(row=3, column=2, padx=20, pady=5)
    customerNameEntry.configure(validate="key", validatecommand=(callback, "%P"))


    mobileLabel = Label(taj, text="Contact no", font=("ariel", 15, "bold"))
    mobileLabel.grid(row=4, column=1, padx=20, pady=5)


    mobileEntry = Entry(taj, textvariable=mobileVar, font=("ariel", 15, "bold"))
    mobileEntry.grid(row=4, column=2, padx=20, pady=5)
    mobileEntry.configure(validate="key", validatecommand=(callback2, "%P"))

    selectLabel = Label(taj, text="Select Item", font=("ariel", 15, "bold"))
    selectLabel.grid(row=5, column=1, padx=20, pady=5)

    l=combo_input()
    c=ttk.Combobox(taj,values= l,textvariable=combovariable, font=("ariel", 15, "bold"))
    c.set("select Item")
    combovariable.trace('w',optionCallBack)
    c.grid(row=5, column=2, padx=20, pady=5)

    rateLabel = Label(taj, text="Item Rate", font=("ariel", 15, "bold"))
    rateLabel.grid(row=6, column=1, padx=20, pady=5)

    rateEntry = Entry(taj, textvariable=baserate, font=("ariel", 15, "bold"))
    rateEntry.grid(row=6, column=2, padx=20, pady=5)

    qtyLabel = Label(taj, text="Select Quantity", font=("ariel", 15, "bold"))
    qtyLabel.grid(row=7, column=1, padx=20, pady=5)

    global qtyvariable
    l2 = [1,2,3,4,5]
    qty = ttk.Combobox(taj, values=l2, textvariable=qtyvariable, font=("ariel", 15, "bold"))
    qty.set("select Quantity")
    qtyvariable.trace('w', optionCallBack2)
    qty.grid(row=7, column=2, padx=20, pady=5)

    costLabel = Label(taj, text="Cost", font=("ariel", 15, "bold"))
    costLabel.grid(row=8, column=1, padx=20, pady=5)

    costEntry = Entry(taj, textvariable=cost, font=("ariel", 15, "bold"))
    costEntry.grid(row=8, column=2, padx=20, pady=5)

    billButton=Button(taj,text='Save Bill',width=20,height=2,bd=10,fg='red',bg='yellow',command=saveBill)
    billButton.grid(row=9, column=2, padx=20, pady=5)

######### Save bill#######
def saveBill():
    dt=datetimeVar.get()
    custname=customerNameVar.get()
    mobile=mobileVar.get()
    item_name=combovariable.get()     # point to be noted
    #print(item_name)
    itemrate=v
    itemqty=qtyvariable.get()
    total=cost.get()
    print(dt,custname)
    dbconfig()
    insque="insert into bill (datetime,customer_name,contact_no,item_name,item_rate,item_qty,cost)values(%s,%s,%s,%s,%s,%s,%s)"
    val=(dt,custname,mobile,item_name,itemrate,itemqty,total)
    mycursor.execute(insque,val)
    conn.commit()
    messagebox.showinfo("Save data","Bill Saved successfully")
    customerNameVar.set("")
    mobileVar.set("")
    itemnameVar.set("")
    cost.set("")

#######printBill
def printBill():
    clear_screen()
    mainheading()
    printitem = Label(taj, text="Bill Details",
                    font=("ariel", 25, "bold"))
    printitem.grid(row=1, column=1, columnspan=2, padx=50, pady=10)

    logoutButton = Button(taj, text="Logout", width=20, height=2, fg="green", bd=10, command=Logout)
    logoutButton.grid(row=1, column=0, columnspan=1)

    backButton = Button(taj, text="Back", width=20, height=2, fg="green", bd=10, command=back)
    backButton.grid(row=1, column=3, columnspan=1)

    clickbutton = Button(taj, text="Duoble click to TreeView to print bill",
                      font=("ariel", 25, "bold"))
    clickbutton.grid(row=2, column=1, columnspan=3, padx=50, pady=10)

    #### treeview

    tazTV1.grid(row=5, column=0, columnspan=4)
    style = ttk.Style(taj)
    style.theme_use('clam')
    style.configure("Treeview", fieldbackground="green")
    scrollBar = Scrollbar(taj, orient="vertical", command=tazTV1.yview)
    scrollBar.grid(row=5, column=5, sticky="NSE")

    tazTV1.configure(yscrollcommand=scrollBar.set)
    tazTV1.heading('#0', text="Date/Time")
    tazTV1.heading('#1', text="Name")
    tazTV1.heading('#2', text="Mobile")
    tazTV1.heading('#3', text="Selected food")
    tazTV1.heading('#4', text="Total cast")

    displaybill()
###### displaybill

def displaybill():
    # to delete already inserted data
    records = tazTV1.get_children()
    for x in records:
        tazTV.delete(x)

    conn = pymysql.connect(host="localhost", user="root", db="myhotel")
    mycursor = conn.cursor(pymysql.cursors.DictCursor)
    query1 = "select * from bill"
    mycursor.execute(query1)
    data = mycursor.fetchall()
    #print(data)
    for row in data:
        tazTV1.insert('', 'end', text=row['datetime'], values=(row["customer_name"], row["contact_no"], row["item_name"], row["cost"]))
    conn.close()

    tazTV1.bind("<Double-1>", onDoubleClick2)

#########onDoubleClick2
def onDoubleClick2(event):
    item = tazTV1.selection()
    global itemnameVar11
    itemnameVar11 = tazTV1.item(item, "text")
    item_detail1 = tazTV1.item(item, "values")
    receipt()

#####receipt()
def receipt():
    billstring=""
    billstring+="==================My Hotel Bill================\n\n"
    billstring += "=================Customer Detail================\n\n"
    dbconfig()
    query="select * from bill where datetime='{}';".format(itemnameVar11)
    mycursor.execute(query)
    data=mycursor.fetchall()
    print(data)
    for row in data:
        print(row)
        billstring+="{}{:<20}{:10}\n".format("Date/Time","",row[1])
        billstring += "{}{:<20}{:10}\n".format("Customer Name", "", row[2])
        billstring += "{}{:<20}{:10}\n".format("Contact No", "", row[3])
        billstring += "\n================== Item Detail==================\n"
        billstring+= "{:<10}{:<10}{:<15}{:<15}".format("Item Name","Rate","Quantity","Total Cost\n  ")
        billstring+="\n{:<10}{:<10}{:<15}{:<15}".format(row[4],row[5],row[6], row[7])

        billstring+= "\n=============================================\n"
        billstring+= "{}{:<10}{:<15}{:<10}\n".format("Total Cost","  ","  ",row[7])
        billstring+="\n\n========Thanks Please Visit Again========\n"

    billFile=filedialog.asksaveasfile(mode="w",defaultextension=".txt")
    if billFile is None:
        messagebox.showerror("File Name Error","Invalid File Name")
    else:
        billFile.write(billstring)
        billFile.close()


###########
def addItemWindow():
    clear_screen()
    mainheading()
    additem = Label(taj, text="Insert Item",
                    font=("ariel", 25, "bold"))
    additem.grid(row=1, column=1, columnspan=2, padx=50, pady=10)

    itemnameLabel=Label(taj,text="Item Name",font=("ariel", 20, "bold"))
    itemnameLabel.grid(row=2,column=1,padx=20,pady=5)

    itemrateLabel = Label(taj, text="Item Rate(INR)", font=("ariel", 20, "bold"))
    itemrateLabel.grid(row=3, column=1, padx=20, pady=5)

    itemtypeLabel = Label(taj, text="Item Type", font=("ariel", 20, "bold"))
    itemtypeLabel.grid(row=4, column=1, padx=20, pady=5)

    itemnameEntry=Entry(taj,textvariable=itemnameVar)
    itemnameEntry.grid(row=2,column=2,padx=20,pady=5)
    # for validation
    itemnameEntry.configure(validate="key",validatecommand=(callback,"%P"))

    itemrateEntry = Entry(taj, textvariable=itemrateVar)
    itemrateEntry.grid(row=3, column=2, padx=20, pady=5)
    itemrateEntry.configure(validate="key", validatecommand=(callback2, "%P"))

    itemtypeEntry = Entry(taj, textvariable=itemtypeVar)
    itemtypeEntry.grid(row=4, column=2, padx=20, pady=5)
    itemtypeEntry.configure(validate="key", validatecommand=(callback, "%P"))

    additemButton=Button(taj,text="Add Item",width=20,height=2,fg="green",bd=10,command=additemprocess)
    additemButton.grid(row=3,column=3,columnspan=1)

    updateButton = Button(taj, text="UPDATE Item", width=20, height=2, fg="green", bd=10, command=updateitem)
    updateButton.grid(row=4, column=3, columnspan=1)

    deleteButton = Button(taj, text="DELETE Item", width=20, height=2, fg="green", bd=10, command=deleteitem)
    deleteButton.grid(row=5, column=3, columnspan=1)

    logoutButton = Button(taj, text="Logout", width=20, height=2, fg="green", bd=10, command=Logout)
    logoutButton.grid(row=3, column=0, columnspan=1)

    backButton = Button(taj, text="Back", width=20, height=2, fg="green", bd=10, command=back)
    backButton.grid(row=4, column=0, columnspan=1)

    #### treeview

    tazTV.grid(row=8,column=0,columnspan=3)
    style=ttk.Style(taj)
    style.theme_use('clam')
    style.configure("Treeview",fieldbackground="green")
    scrollBar= Scrollbar(taj,orient="vertical",command=tazTV.yview)
    scrollBar.grid(row=8,column=2,sticky="NSE")

    tazTV.configure(yscrollcommand=scrollBar.set)
    tazTV.heading('#0',text="Item Name")
    tazTV.heading('#1', text="Rate")
    tazTV.heading('#2', text="Type")

    getItemInTreeview()

def additemprocess():
    name=itemnameVar.get()
    rate=itemrateVar.get()
    type=itemtypeVar.get()
    dbconfig()
    que="insert into itemlist(item_name,item_rate,item_type)values(%s,%s,%s)"
    val=(name,rate,type)
    mycursor.execute(que,val)
    conn.commit()
    messagebox.showinfo("Save Item","Item Saved Successfully")
    itemnameVar.set("")
    itemrateVar.set("")
    itemtypeVar.set("")
    getItemInTreeview()

def adminLogin():
    dbconfig()
    username=usernamevar.get()
    password=passwordvar.get()
    que= "select * from user_info where user_id=%s and user_pass=%s"
    val=(username,password)
    mycursor.execute(que,val)
    data=mycursor.fetchall()
    flag=False
    for row in data:
        flag=True
    conn.close()

    if flag==True:
        welcomewindow()
    else:
       messagebox.showerror("Invalid user Credential","Either Username or Password is incorrect")
       usernamevar.set("")
       passwordvar.set("")

mainheading()
loginwindow()
taj.title("Hotel Taj Management System")
taj.geometry("%dx%d+0+0"%(width,height))
taj.mainloop()