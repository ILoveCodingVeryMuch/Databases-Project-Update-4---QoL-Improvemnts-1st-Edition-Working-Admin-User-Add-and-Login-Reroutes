from flask import Flask, render_template, redirect, url_for, request
import pymysql
import pymysql.cursors

conn= pymysql.connect(host='localhost', user='root', password='Rainbow.86', db='Project')
app = Flask(__name__)


@app.route('/AdminHome')
def AdminHome():
    return render_template('adminhome.html')

@app.route('/AdminAdd', methods = ['GET', 'POST'])
def AdminAdd():
    a = conn.cursor()
    error = None
    if request.method =='POST':
        Name = request.form['Username']
        Password = request.form['Pass']
        Role = request.form['UserRole']
        FName = request.form['FName']
        LName = request.form['LName']
        Email = request.form['Email']
        Address = request.form['Address']
        ContactDetail = request.form['ContactDetail']
        Gender = request.form['Gender']
        addsql = 'INSERT INTO UserTable VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
        a.execute(addsql, (Name, Password, Role, FName, LName, Email, Address, ContactDetail, Gender))
        conn.commit()
        return redirect(url_for('AdminHome'))
    return render_template('adminadd.html', error = error)

####################################################
@app.route('/ManagerHome')
def ManagerHome():
    return render_template('managerhome.html')

####################################################
@app.route('/ShopHome')
def ShopHome():
    return render_template('shophome.html')


@app.route('/search', methods =['GET', 'POST'])
def ShopSearch():
    a = conn.cursor()
    error = None
    if request.method == 'POST':
        item = request.form['search']
        sql = 'SELECT * FROM ItemTable WHERE ItemName = %s'
        a.execute(sql, (item))
        results = a.fetchone()
        N1 = results[0]
        N2 = results[1]
        N3 = results[2]
        sql2 = 'INSERT INTO MatIndentTable VALUES (%s, %s, %s)'
        a.execute(sql2, (str(N1), str(N2), N3))
        conn.commit()
        print(results)
        #return(str(results))
        return redirect(url_for('PurchaseOrderCreate'))
    return render_template('search.html', error = error)

@app.route('/orderconfirm')
def PurchaseOrderCreate():
    a = conn.cursor()
    sql = 'INSERT INTO PurchaseOrder SELECT * FROM MatIndentTable'
    a.execute(sql)
    conn.commit()
    return redirect(url_for('CreateGoodsReceipt'))

@app.route('/goodsreceiptinfo')
def CreateGoodsReceipt():
    a = conn.cursor()
    #create purchase order table?
    #create table with counter for intervals to allow placement of data from sql, increase incrementally
    sql = 'SELECT * FROM PurchaseOrder'
    #save this data and print it?
    a.execute(sql)
    results = a.fetchall()
    print(results)
    sqldelete = 'DELETE PurchaseOrder'
    a.execute(sqldelete)
    conn.commit()
    return redirect(url_for('ManagerHome'))
######################################
@app.route('/VendorHome')
def VendorHome():
    return render_template('vendorhome.html')

#######################################
@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        usern = request.form['username']
        passw = request.form['password']
        a = conn.cursor()
        sql = 'SELECT * FROM UserTable WHERE UserName = %s AND Pass = %s'
        data = a.execute(sql, (usern, passw))
        data2 = a.fetchone()
        if data2[2] == "Admin":
            return redirect(url_for('AdminHome'))
        elif data2[2] == "Shop":
            return redirect(url_for('ShopHome'))
        elif data2[2] == 'Manager':
            return redirect(url_for('ManagerHome'))
        elif data2[2] == "Vendor":
            return redirect(url_for('VendorHome'))
        #....
        else:
            error = 'Invalid Credentials. Please try again.'
    return render_template('fancylogin.html', error=error)


if __name__ == '__main__':
    app.run(debug=True)


