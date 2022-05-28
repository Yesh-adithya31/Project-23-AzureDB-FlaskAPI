from flask import jsonify,make_response
from flask import Blueprint, request
import json
import pyodbc

conn = pyodbc.connect('Driver={SQL Server};Server=tcp:finalresearchdbserver.database.windows.net,1433;Database=SuperMarket;Uid=imesha;Pwd=Mitb@1018;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
    # with conn.cursor() as cursor:
    #     cursor.execute("SELECT @@Version")
    #     row = cursor.fetchall()
    #     print("This is connection String: ",row)


api = Blueprint('api',__name__)

#cursor.execute('SELECT * FROM users WHERE usertype = % s', (searchParent, ))

@api.route('/registration', methods=['POST'])
def customerRegistration():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
        NIC = json['NIC']
        customerName = json['customerName']
        DOB = json['DOB']
        email = json['email']
        pwd = json['pwd']
        
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM [dbo].[customer] WHERE (email = ?)',(email))
        rows = [x for x in cursor]

        if not rows:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO customer (NIC, customerName, DOB, email, pwd) VALUES (?, ?, ?, ?, ?)", (NIC, customerName, DOB, email, pwd))
            if cursor.rowcount == 1:
                return  make_response(jsonify({"data" : "Registartion Done Successfully.", "status" : "Success"}), 200)
            else:
                return  make_response(jsonify({"data" : "Error... Something went wrong", "status" : "Error"}), 500)
        else:
            return  make_response(jsonify({"data" : "User already exists.", "status" : "Success"}), 501)

    else:
        return make_response(jsonify({"data" : "Content Not Supported!.", "status" : "Error"}), 500)
    
@api.route('/login', methods=['POST'])
def customerLogin():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
        email = json['email']
        pwd = json['pwd']

        try: 
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM [dbo].[customer] WHERE (email = ?) AND (pwd = ?)',(email, pwd))
            rows = [x for x in cursor]
            cols = [x[0] for x in cursor.description]
            customers = []
            cusID = 0
            
            for row in rows:
                customer = {}
                for prop, val in zip(cols, row):
                    customer[prop] = val
                customers.append(customer)
            for i, cus in enumerate(customers): 
                cusID = cus['customerID'] 
                   
            print(cusID)
            if not rows:
                return  make_response(jsonify({"data" : "Invalid Credintial.", "status" : "Error"}), 500)
            else:
                return  make_response(jsonify({"userData" : cusID , "data" : "Login Successfully.", "status" : "Success"}), 200)
                
        except Exception as e:
            return  make_response(jsonify({"data" : 'Server Error.', "status" : "Error"}), 500)    
    else:
        return make_response(jsonify({"data" : "Content Not Supported!.", "status" : "Error"}), 500)    

@api.route('/viewBill', methods=['POST'])
def billsView():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
        customerID = json['customerID']

        try:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM bill  INNER JOIN customer ON bill.customerID = customer.customerID INNER JOIN product ON bill.productID = product.productID WHERE customer.customerID = ?',(customerID))
            print("row: ", cursor.rowcount , " row/s Effected")
            rows = [x for x in cursor]
            cols = [x[0] for x in cursor.description]
            bills = []
            
            for row in rows:
                bill = {}
                for prop, val in zip(cols, row):
                    bill[prop] = val
                bills.append(bill)
            # Create a string representation of your array of bills.
            return  make_response(jsonify({"data" : bills, "status" : "Success"}), 200)
        except Exception as e:
            # return f"An Error Occured: {e}"
            return  make_response(jsonify({"data" : 'Server Error.', "status" : "Error"}), 500)
    else:
        return make_response(jsonify({"data" : "Content Not Supported!.", "status" : "Error"}), 500)    

@api.route('/deletebill', methods=['DELETE'])
def deleteBill():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
        customerID = json['customerID']
        orderID = json['orderID']
        try:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM bill WHERE (orderID = ?) AND (customerID = ?)',(customerID,orderID))
            print("row: ", cursor.rowcount , " row/s Effected")
            
            if cursor.rowcount == 0:
                # Create a string representation of your array of bills.
                return  make_response(jsonify({"data" : "Bill Detail Deleted Successfully", "status" : "Success"}), 200)
            else:
                return  make_response(jsonify({"data" : 'This bill details Already Deleted.', "status" : "Error"}), 500)
        except Exception as e:
            # return f"An Error Occured: {e}"
            return  make_response(jsonify({"data" : 'Server Error.', "status" : "Error"}), 500)
    else:
        return make_response(jsonify({"data" : "Content Not Supported!.", "status" : "Error"}), 500)   

@api.route('/viewExample', methods=['GET'])
def createExample():
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM product')
        # cursor.execute('SELECT * FROM bill')
        # product = cursor.fetchall() 
        # mylist = {str(product)}
        # conn.close()
        # return json.dumps( [dict(ix) for ix in product] ) #CREATE JSON
        rows = [x for x in cursor]
        cols = [x[0] for x in cursor.description]
        songs = []
        for row in rows:
            song = {}
            for prop, val in zip(cols, row):
                song[prop] = val
            songs.append(song)
        # Create a string representation of your array of songs.
        songsJSON = json.dumps(songs)
        return songsJSON
    except Exception as e:
        return f"An Error Occured: {e}"
