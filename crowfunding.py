import datetime
from flask import Flask, render_template,request,session,redirect
from DBConnection import Db
from web3 import HTTPProvider,Web3



app = Flask(__name__)
app.secret_key="987654"

compiled_contract_path=r"C:\smartcontracts\build\contracts\Crowdfunding.json"
deployed_contract_address="0x46e89b2d1EE12882502255d18cFb32Bc11142DfF"
import json
web3 = Web3(HTTPProvider("HTTP://127.0.0.1:7545"))

# @app.route('/ab')
# def hello_world():
#     return 'Hello World!'


@app.route('/')
def publichome():
    session["name"] = 'All'
    return render_template("public/homeindex.html")

@app.route('/login')
def login():
    return render_template("index.html")

@app.route('/logout')
def logout():
    session['lid']=''
    return render_template("index.html")

@app.route('/admin_home')
def admin_home():
    if session['lid']=='':
        return redirect('/')
    qry1="SELECT COUNT(*) as cnt FROM `donation_request` "
    db=Db()
    res=db.selectOne(qry1)
    session['cnt']=res['cnt']
    qry2="SELECT COUNT(*) as cnt FROM `donation_request` WHERE STATUS='pending'"
    db = Db()
    res = db.selectOne(qry2)
    session['cntp'] = res['cnt']
    qry3="SELECT COUNT(*) as cnt FROM `donation_request` WHERE STATUS='approved' "
    db = Db()
    res = db.selectOne(qry3)
    session['cntap'] = res['cnt']
    return render_template("admin/aindex.html")

@app.route('/public_home')
def public_home():
    qry1="SELECT COUNT(*) as cnt FROM `donation_request` "
    db=Db()
    res=db.selectOne(qry1)
    cnt=res
    qry2="SELECT COUNT(*) as cnt FROM `donation_request` WHERE STATUS='pending'"
    db = Db()
    res = db.selectOne(qry2)
    cntp= res
    qry3="SELECT COUNT(*) as cnt FROM `donation_request` WHERE STATUS='approved' "
    db = Db()
    res = db.selectOne(qry3)
    cntap = res
    return render_template("public/homeindex.html")

@app.route('/org_home')
def org_home():
    if session['lid']=='':
        return redirect('/')
    return render_template("organization/orgindex.html")

@app.route('/user_home')
def userhome():
    if session['lid']=='':
        return redirect('/')
    return render_template("user/userindex.html")

@app.route('/loginpost',methods=['post'])
def loginpost():
    username=request.form['textfield']
    password=request.form['textfield2']

    db=Db()
    qry="SELECT * FROM `login` WHERE `username`='"+username+"' AND  `password`='"+password+"'"
    res=db.selectOne(qry)
    if res is None:
        return "<script>alert('Invalid username or password');window.location='/login'</script>"

    if res['type']=="admin":
        session['lid']=res['login_id']
        session["name"] = 'Admin'
        return redirect('/admin_home')
    elif res['type']=="organization":
        qry = "SELECT * FROM `organization` WHERE `org_lid`='" + str(res['login_id']) + "'"
        dd = db.selectOne(qry)
        if dd is not None and dd['status'] =='accepted':
            session['lid']=res['login_id']
            session["name"] = str(dd["name"]).upper()
            return redirect('/org_home')
        else:
            return "<script>alert('Organization is not approved by admin');window.location='/login'</script>"

    elif res['type']=="user":
        qry="SELECT * FROM `users` WHERE `lid`='"+str(res['login_id'])+"'"
        dd=db.selectOne(qry)
        if dd is not None:
            session['lid'] = res['login_id']
            session["name"]=str(dd["name"]).upper()
            return redirect('/user_home')
        else:
            return "<script>alert('Invalid username or password');window.location='/login'</script>"


    else:
        return "<script>alert('Invalid username or password');window.location='/login'</script>"




    return render_template("login.html")

@app.route('/changepassword')
def changepassword():
    if session['lid']=='':
        return redirect('/')
    return render_template("admin/changepassword.html")

@app.route('/changepasswordpost',methods=['post'])
def changepasswordpost():
    if session['lid']=='':
        return redirect('/')
    current_pwd=request.form['textfield']
    new_pwd = request.form['textfield2']
    confirm_pwd = request.form['textfield3']
    lid="1"
    db=Db()
    qry="SELECT * FROM `login` WHERE `password`='"+current_pwd+"' AND `login_id`='"+lid+"'"
    res=db.selectOne(qry)
    if res is not None:
        if new_pwd==confirm_pwd:
            qry="UPDATE `login` SET `password`='"+new_pwd+"' WHERE `login_id`='"+lid+"'"
            res=db.update(qry)
            return "<script>alert('password updated');window.location='/'</script>"
        else:
            return "<script>alert('password does not match');window.location='/'</script>"
    else:
        return "<script>alert('invalid password');window.location='/'</script>"

@app.route('/adddonationrequest')
def adddonationrequest():
    if session['lid']=='':
        return redirect('/')
    return render_template("admin/adddonationrequest.html")

@app.route('/adddonationrequestpost',methods=['post'])
def adddonationrequestpost():
    if session['lid']=='':
        return redirect('/')
    # Date_entry = request.form['textfield2']
    Amount = request.form['textfield3']
    Need_beforedate = request.form['textfield4']
    Purpose = request.form['textfield5']
    description = request.form['textfield6']
    db = Db()
    qry="INSERT INTO `donation_request` (`date_entry`,`amount`,`needed_beforedate`,`purpose`,`orglid`,`description`,`status`) VALUES (curdate(),'"+Amount+"','"+Need_beforedate+"','"+Purpose+"','1','"+description+"','approved')"
    res=db.insert(qry)
    return "<script>alert('added donation');window.location='/adddonationrequest'</script>"


@app.route('/viewdonationrequest')
def viewdonationrequest():
    db = Db()
    if session['lid']=='':
        return redirect('/')
    qry="SELECT * FROM `donation_request` WHERE orglid='1'"
    res=db.select(qry)
    return render_template("admin/viewdonationrequest.html",data=res)

@app.route('/orgviewdonationrequest')
def orgviewdonationrequest():
    db = Db()
    if session['lid']=='':
        return redirect('/')
    qry="SELECT * FROM `donation_request` JOIN `organization` ON `donation_request`.`orglid`=`organization`.`org_lid` WHERE `donation_request`.`status` ='pending' "
    res=db.select(qry)
    return render_template("admin/orgviewdonationrequest.html",data=res)


@app.route('/approve_org_donation_req/<id>')
def approve_org_donation_req(id):
    db=Db()
    if session['lid']=='':
        return redirect('/')
    qry="UPDATE `donation_request` SET `status`='approved'WHERE `did`='"+id+"'"
    res=db.update(qry)
    return "<script>alert('approved');window.location='/orgviewdonationrequest'</script>"
@app.route('/rejected_org_donation_req/<id>')
def rejected_org_donation_req(id):
    db=Db()
    if session['lid']=='':
        return redirect('/')
    qry="UPDATE `donation_request` SET `status`='rejected'WHERE `did`='"+id+"'"
    res=db.update(qry)
    return "<script>alert('rejected');window.location='/orgviewdonationrequest'</script>"

@app.route('/view_org_approved_donationrequest')
def view_org_approved_donationrequest():
    db=Db()
    if session['lid']=='':
        return redirect('/')
    qry = "SELECT * FROM `donation_request` JOIN `organization` ON `donation_request`.`orglid`=`organization`.`org_lid` WHERE `donation_request`.`status` ='approved' AND `orglid`!=1"
    res = db.select(qry)
    return render_template("admin/viewapprovedorgdonationrequest.html", data=res)
@app.route('/sendreply/<id>')
def sendreply(id):
    if session['lid']=='':
        return redirect('/')
    return render_template("admin/sendreply.html",id=id)

@app.route('/sendreplypost',methods=['post'])
def sendreplypost():
    if session['lid']=='':
        return redirect('/')
    id=request.form['id']
    reply=request.form['textfield']
    db=Db()
    qry="UPDATE `complaint` SET `reply`='"+reply+"',`status`='replied' WHERE `comp_id`='"+id+"'"
    res=db.update(qry)
    return '''<script>alert('Replied');window.location='/view_complaint_reply'</script>'''

@app.route('/view_complaint_reply')
def view_complaint_reply():
    db = Db()
    if session['lid']=='':
        return redirect('/')
    qry="SELECT * FROM `complaint` JOIN `users` ON`complaint`.`userid`=`users`.`lid`"
    res=db.select(qry)
    return render_template("admin/view_complaint_reply.html",data=res)

@app.route('/viewandapprove')
def viewandapprove():
    if session['lid']=='':
        return redirect('/')
    db = Db()
    qry="SELECT * FROM `organization` where status='pending'"
    res=db.select(qry)
    return render_template("admin/viewandapprove.html",data=res)

@app.route('/viewuser')
def viewuser():
    if session['lid']=='':
        return redirect('/')
    db = Db()
    qry="SELECT * FROM `users`"
    res=db.select(qry)
    return render_template("admin/viewuser.html",data=res)

@app.route('/view_charitynews')
def view_charitynews():
    if session['lid']=='':
        return redirect('/')
    db = Db()
    qry="SELECT * FROM `charity`"
    res=db.select(qry)
    return render_template("admin/view_charitynews.html",data=res)

@app.route('/viewandapprove_accept')
def viewandapprove_accept():
    db = Db()
    if session['lid']=='':
        return redirect('/')
    qry="SELECT * FROM `organization` where status='accepted'"
    res=db.select(qry)
    return render_template("admin/viewandapprove_accept.html",data=res)

@app.route('/viewandapprove_reject')
def viewandapprove_reject():
    if session['lid']=='':
        return redirect('/')
    db = Db()
    qry="SELECT * FROM `organization` where status='rejected'"
    res=db.select(qry)
    return render_template("admin/viewandapprove_reject.html",data=res)

############################# organization


@app.route('/addcharity')
def addcharity():
    if session['lid']=='':
        return redirect('/')
    return render_template("ORGANIZATION/addcharity.html")

@app.route('/addcharitypost',methods=['post'])
def addcharitypost():
    if session['lid']=='':
        return redirect('/')
    db=Db()
    # date_entry=request.form['textfield']
    amount = request.form['textfield2']
    need_beforedate = request.form['textfield3']
    purpose = request.form['textfield4']
    description = request.form['textfield5']
    # org_id = request.form['textfield5']
    #status = request.form['textfield6']
    qry="INSERT INTO `donation_request`(`date_entry`,`amount`,`needed_beforedate`,`purpose`,`description`,`orglid`,`status`) VALUES (curdate(),'"+amount+"','"+need_beforedate+"','"+purpose+"','"+description+"','"+str(session['lid'])+"','pending')"
    res=db.insert(qry)
    return "<script>alert('Donation request sent');window.location='/org_home'</script>"

@app.route('/changepassword_org')
def changepassword_org():
    if session['lid']=='':
        return redirect('/')
    return render_template("ORGANIZATION/changepassword_org.html")

@app.route('/changepassword_orgpost',methods=['post'])
def changepassword_orgpost():
    if session['lid']=='':
        return redirect('/')
    current_pwd = request.form['textfield']
    new_pwd = request.form['textfield2']
    confirm_pwd = request.form['textfield3']
    db = Db()
    qry = "SELECT * FROM `login` WHERE `password`='" + current_pwd + "' AND `login_id`='" + str(session['lid']) + "'"
    res = db.selectOne(qry)
    print(qry)
    if res is not None:
        if new_pwd == confirm_pwd:
            qry = "UPDATE `login` SET `password`='" + new_pwd + "' WHERE `login_id`='" + str(session['lid']) + "'"
            res = db.update(qry)
            return "<script>alert('password updated');window.location='/'</script>"
        else:
            return "<script>alert('password does not match');window.location='/'</script>"
    else:
        return "<script>alert('invalid password');window.location='/'</script>"


@app.route('/neworganization')
def neworganization():
    return render_template("ORGANIZATION/rindex.html")

@app.route('/adminapprove_org/<orgid>')
def adminapprove_org(orgid):
    if session['lid']=='':
        return redirect('/')
    db=Db()
    qry="UPDATE `organization` SET `status`='accepted' WHERE `organization_id`='"+orgid+"'"
    db.update(qry)
    return "<script>alert('Approved');window.location='/viewandapprove'</script>"

@app.route('/adminreject_org/<orgid>')
def adminreject_org(orgid):
    if session['lid']=='':
        return redirect('/')
    db=Db()
    qry="UPDATE `organization` SET `status`='rejected' WHERE `organization_id`='"+orgid+"'"
    db.update(qry)
    return "<script>alert('Rejected');window.location='/viewandapprove'</script>"


@app.route('/neworganizationpost',methods=['post'])
def neworganizationpost():
    db=Db()
    username=request.form['textfield']
    name=request.form['textfield2']
    place = request.form['textfield3']
    city = request.form['textfield4']
    state = request.form['textfield5']
    email = request.form['textfield6']
    aboutus = request.form['textarea']
    estd = request.form['textfield7']
    password = request.form['textfield8']
    confirm_password = request.form['textfield9']

    qry="INSERT INTO `login` (`username`,`password`,`type`)  VALUES ('"+username+"','"+password+"','organization')"
    res=db.insert(qry)

    qry1="INSERT INTO `organization` (`name`,`place`,`city`,`state`,`email`,`aboutus`,`estd`,`status`,org_lid) VALUES ('"+name+"','"+place+"','"+city+"','"+state+"','"+email+"','"+aboutus+"','"+estd+"','pending','"+str(res)+"')"
    res1=db.insert(qry1)

    return "<script>alert('Registered successfully');window.location='/'</script>"

@app.route('/viewprofile_org')
def viewprofile_org():
    if session['lid']=='':
        return redirect('/')
    # lid="1"
    db =Db()
    qry="SELECT * FROM `organization` WHERE org_lid ='"+str(session['lid'])+"'"
    res = db.selectOne(qry)
    return render_template("ORGANIZATION/viewprofile_org.html",data=res)

@app.route('/view_mycharity')
def view_mycharity():
    if session['lid']=='':
        return redirect('/')
    # lid="1"
    db =Db()
    qry="SELECT * FROM `donation_request` WHERE orglid ='"+str(session['lid'])+"'"
    res = db.select(qry)
    return render_template("ORGANIZATION/view_mycharity.html",data=res)

@app.route('/editprofileorg')
def editprofileorg():
    if session['lid']=='':
        return redirect('/')
    qry = "SELECT * FROM `organization` WHERE org_lid ='"+str(session['lid'])+"'"
    db = Db()
    res = db.selectOne(qry)
    return render_template("ORGANIZATION/editprofileorg.html",data=res)

@app.route('/edit_charity/<did>')
def edit_charity(did):
    if session['lid']=='':
        return redirect('/')
    session['did']=did
    qry = "SELECT * FROM `donation_request` WHERE did ='"+did+"'"
    db = Db()
    res = db.selectOne(qry)
    return render_template("ORGANIZATION/edit_charity.html",data=res)

@app.route('/delete_charity/<did>')
def delete_charity(did):
    if session['lid']=='':
        return redirect('/')
    qry = "DELETE FROM `donation_request` WHERE did='"+did+"'"
    db = Db()
    res = db.delete(qry)
    return "<script>alert('Charity Deleted');window.location='/view_mycharity'</script>"

@app.route('/edit_charitypost',methods=['post'])
def edit_charitypost():
    if session['lid']=='':
        return redirect('/')
    date_entry = request.form['textfield2']
    amount  = request.form['textfield3']
    needed_beforedate = request.form['textfield4']
    purpose = request.form['textfield5']
    description = request.form['textfield6']

    db = Db()
    qry = "UPDATE `donation_request` SET `date_entry`='"+date_entry+"', `amount`='"+amount+"', `needed_beforedate`='"+needed_beforedate+"',`purpose`='"+purpose+"',`description`='"+description+"' WHERE `did`='" + str(session['did']) + "'"
    res = db.update(qry)

    return "<script>alert('Charity Updated');window.location='/view_mycharity'</script>"



@app.route('/editprofileorgpost',methods=['post'])
def editprofileorgpost():
    if session['lid']=='':
        return redirect('/')
    name = request.form['textfield2']
    place = request.form['textfield3']
    city = request.form['textfield4']
    state = request.form['textfield5']
    email = request.form['textfield6']
    aboutus = request.form['textarea']
    estd = request.form['textfield7']

    db = Db()
    qry = "UPDATE `organization` SET `name`='"+name+"', `place`='"+place+"', `city`='"+city+"',`state`='"+state+"',`email`='"+email+"',`aboutus`='"+aboutus+"',`estd`='"+estd+"' WHERE `org_lid`='" + str(
            session['lid']) + "'"
    res = db.update(qry)

    return "<script>alert('Profile Updated');window.location='/viewprofile_org'</script>"
#############################

@app.route('/changepassword_user')
def changepassword_user():
    if session['lid']=='':
        return redirect('/')
    return render_template("USER/changepassword_user.html")

@app.route('/changepassword_userpost',methods=['post'])
def changepassword_userpost():
    if session['lid']=='':
        return redirect('/')
    current_pwd = request.form['textfield']
    new_pwd = request.form['textfield2']
    confirm_pwd = request.form['textfield3']
    db=Db()
    qry = "SELECT * FROM `login` WHERE `password`='"+current_pwd+"' AND `login_id`='"+str(session['lid'])+"'"
    res = db.selectOne(qry)
    print(qry)
    if res is not None:
        if new_pwd==confirm_pwd:
            qry="UPDATE `login` SET `password`='"+new_pwd+"' WHERE `login_id`='"+str(session['lid'])+"'"
            res=db.update(qry)
            return "<script>alert('password updated');window.location='/'</script>"
        else:
            return "<script>alert('password does not match');window.location='/'</script>"
    else:
        return "<script>alert('invalid password');window.location='/'</script>"



@app.route('/signup_user')
def signup_user():
    return render_template("USER/uindex.html")

@app.route('/signup_userpost',methods=['post'])
def signup_userpost():
    db = Db()
    username=request.form['textfield']
    name = request.form['textfield0']
    email=request.form['textfield2']
    phone = request.form['textfield3']
    photo = request.files['fileField']
    place = request.form['place']
    city = request.form['city']
    state = request.form['state']
    pincode = request.form['pincode']
    password = request.form['password']
    confirm_password = request.form['confirm_password']

    from datetime import datetime
    s= datetime.now().strftime("%Y%m%d%H%M%S")+".jpg"



    p="C:\\Users\\fhm70\\PycharmProjects\\crowfunding\\static\\userphoto\\"

    photo.save(p+s)

    pth="/static/userphoto/"+s


    qry="INSERT INTO `login` (`username`,`password`,`type`)  VALUES ('"+username+"','"+password+"','user')"
    lid=db.insert(qry)
    qry2="INSERT INTO  `users`(`name`,`email`,`phone`,`photo`,`lid`,`place`,`state`,`city`,`pincode`) VALUES ('"+name+"','"+email+"','"+phone+"','"+pth+"','"+str(lid)+"','"+place+"','"+city+"','"+state+"','"+pincode+"')"
    res1=db.insert(qry2)
    return "<script>alert('Registered successfully');window.location='/'</script>"
@app.route('/sendcomplaint')
def sendcomplaint():


    return render_template("USER/sendcomplaint.html")

@app.route('/sendcomplaintpost',methods=['post'])
def sendcomplaintpost():
    if session['lid']=='':
        return redirect('/')
    complaint=request.form['textarea']
    qry="INSERT	INTO `complaint` (`complaint`,`userid`,`reply`,`date`,`status`) VALUES ('"+complaint+"','"+str(session['lid'])+"','pending',curdate(),'pending')"
    db = Db()
    res=db.insert(qry)
    return render_template("USER/sendcomplaint.html")



@app.route('/viewreply')
def viewreply():
    if session['lid']=='':
        return redirect('/')
    qry = "SELECT * FROM `complaint` JOIN `users` ON`complaint`.`userid`=`users`.`lid`"
    db=Db()
    res = db.select(qry)
    return render_template("USER/viewreply.html",data=res)



@app.route('/viewprofile_user')
def viewprofile_user():
    if session['lid']=='':
        return redirect('/')

    #lid="1"
    qry="SELECT * FROM `users` WHERE lid ='"+str(session['lid'])+"'"
    db=Db()
    res=db.selectOne(qry)
    return render_template("USER/viewprofile_user.html",data=res)


@app.route('/editprofile')
def editprofile():
    if session['lid']=='':
        return redirect('/')
    qry = "SELECT * FROM `users` WHERE lid ='" + str(session['lid']) + "'"
    db = Db()
    res = db.selectOne(qry)
    return render_template("USER/editprofile.html",data=res)

@app.route('/editprofilepost',methods=['post'])
def editprofilepost():
    if session['lid']=='':
        return redirect('/')
    name = request.form['textfield0']
    email = request.form['textfield2']
    phone = request.form['textfield3']
    photo = request.files['fileField']
    db = Db()
    if photo.filename!='':
        from datetime import datetime
        s= datetime.now().strftime("%Y%m%d%H%M%S")+".jpg"



        p="C:\\Users\\fhm70\\PycharmProjects\\crowfunding\\static\\userphoto\\"

        photo.save(p+s)
        pth="/static/userphoto/"+s
        qry = "UPDATE `users` SET `name`='"+name+"',`email`='"+email+"',`phone`='"+phone+"', `photo`='"+pth+"' WHERE `lid`='"+str(session['lid'])+"'"
        res = db.update(qry)

        return "<script>alert('Profile Updated');window.location='/viewprofile_user'</script>"
    else:
        qry = "UPDATE `users` SET `name`='" + name + "',`email`='" + email + "',`phone`='" + phone + "'  WHERE `lid`='" + str(
            session['lid']) + "'"
        res = db.update(qry)

        return "<script>alert('Profile Updated');window.location='/viewprofile_user'</script>"


##################### public

@app.route('/charity_news')
def charity_news():
    return render_template("public/charity_news")

@app.route('/charity_newspost' ,methods=['post'])
def charity_newspost():
    db=Db()
    name=request.form['textfield2']
    email=request.form['textfield3']
    subject=request.form['textfield4']
    description=request.form['textfield6']
    qry="INSERT INTO `charity` (`Name`,`email`,`subject`,`description`) VALUES ('"+name+"','"+email+"','"+subject+"','"+description+"')"
    res = db.insert(qry)
    return "<script>alert('Charity news sent');window.location='/charity_news'</script>"

@app.route('/viewdonationstatus')
def viewdonationstatus():
    # if session['lid']=='':
    #     return redirect('/')
    db=Db()
    qry = "SELECT * FROM `donation_request` JOIN `organization` ON `donation_request`.`orglid`=`organization`.`org_lid` WHERE `donation_request`.`status` ='approved' "
    res = db.select(qry)

    result = []
    ramt = 0.0
    for i in res:
        ramt = getdonations(i['did'])
        print(i['did'], "did")
        print(ramt, "ramt")
        print(i['amount'], "amt")
        balance = i['amount'] - ramt
        print(balance)
        result.append({'did': i['did'], 'date_entry': i['date_entry'], 'amount': i['amount'],'name':i['name'],'orglid':i['orglid'],
                       'needed_beforedate': i['needed_beforedate'], 'purpose': i['purpose'], 'orglid': i['orglid'],'description':i['description'],'status':i['description'], 'ramt': ramt,
                       'balance': balance})
    return render_template("public/viewdonationstatus.html",data=result)

#######################




#==========================================================BlockChain===================================================



def checkbalance(amount,accountnumber,privatekey):
    from web3 import Web3, HTTPProvider
    blockchain_address = "http://127.0.0.1:7545"
    web3 = Web3(HTTPProvider(blockchain_address))
    if web3.isConnected():
        acc1 = accountnumber
        # acc2 = "0x51880fF461918bCfb06A40468ad49223193530BD"
        acc2=deployed_contract_address

        prvkey = privatekey
        nonce = web3.eth.getTransactionCount(acc1)

        abcd = web3.eth.get_balance(acc1)
        abcd = web3.fromWei(abcd, 'ether')
        print(abcd)

        tx = {
            'nonce': nonce,
            'to': acc2,
            'value': web3.toWei(int(amount), 'ether'),
            'gas': 200000,
            'gasPrice': web3.toWei('50', 'gwei')
        }
        signedtx = web3.eth.account.sign_transaction(tx, prvkey)
        hashx = web3.eth.send_raw_transaction(signedtx.rawTransaction)
        print(web3.toHex(hashx))


def checkdonation(donationrequest):
    from web3 import Web3, HTTPProvider
    blockchain_address = "http://127.0.0.1:7545"
    web3 = Web3(HTTPProvider(blockchain_address))
    if web3.isConnected():
        with open(compiled_contract_path) as file:
            contract_json = json.load(file)  # load contract info as JSON
            contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions

        contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)

        blocknumber = web3.eth.get_block_number()
        print(blocknumber)
        lq = []
        for i in range(blocknumber, 5, -1):
            a = web3.eth.get_transaction_by_block(i, 0)
            try:
                decoded_input = contract.decode_function_input(a['input'])
                print(decoded_input)
                print("ku")
                print(decoded_input)
                lq.append(decoded_input[1])
            except Exception as a:
                pass

        print(lq)
        tot = 0
        ls = []
        for i in lq:

            if str(i["startupida"]) == str(donationrequest):
                qry = "SELECT * FROM `startup` WHERE `startup_id`='"+str(i["startupida"])+"'"
                db = Db()
                res = db.selectOne(qry)
                if res is not None:
                    a = {'amounta': i['amounta'],'amount':res['amount']}
                    ls.append(a)
                tot += i["amounta"]
                ls.append({'total':tot})
                print(tot,"++++++++++++++++++++++++++Total amount+++++++++++++++++++++++++++++++++")
        print(ls,"--------------------------------------------------------------------Raising Amount-------------------------------------------------------------------------")



def checkdonationss(donationrequest):
    from web3 import Web3, HTTPProvider
    blockchain_address = "http://127.0.0.1:7545"
    web3 = Web3(HTTPProvider(blockchain_address))
    if web3.isConnected():
        with open(compiled_contract_path) as file:
            contract_json = json.load(file)  # load contract info as JSON
            contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
        contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
        blocknumber = web3.eth.get_block_number()
        print(blocknumber)
        lq = []
        for i in range(blocknumber, 5, -1):
            a = web3.eth.get_transaction_by_block(i, 0)
            try:
                decoded_input = contract.decode_function_input(a['input'])
                print(decoded_input)
                print("ku")
                print(decoded_input)
                lq.append(decoded_input[1])
            except Exception as a:
                pass
        tot = 0
        ls = []
        for i in lq:
            if str(i["startupida"]) == str(donationrequest):
                qry = "SELECT * FROM `startup` WHERE `startup_id`='" + str(i["startupida"]) + "'"
                db = Db()
                res = db.selectOne(qry)
                if res is not None:
                    a = {'amounta': i['amounta'], 'amount': res['amount']}
                    ls.append(a)
                tot += i["amounta"]
    return tot

def getdonations(startupid):
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
    blocknumber = web3.eth.get_block_number()
    print(blocknumber)
    lq = []
    for i in range(blocknumber, 5, -1):
        a = web3.eth.get_transaction_by_block(i, 0)
        try:
            decoded_input = contract.decode_function_input(a['input'])
            print(decoded_input[1])
            # print("ku")
            # print(decoded_input)
            lq.append(decoded_input[1])
        except Exception as a:
            pass

    tot = 0
    ls = []
    for i in lq:

        if str(i["policyida"]) == str(startupid):
            # ls.append(i)

            tot += i["amounta"]
    return tot



@app.route('/viewdonation_req')
def viewdonation_req():
    if session['lid']=='':
        return redirect('/')
    db=Db()
    qry = "SELECT * FROM `donation_request` JOIN `organization` ON `donation_request`.`orglid`=`organization`.`org_lid` WHERE `donation_request`.`status` ='approved' "
    res = db.select(qry)

    result = []
    ramt = 0.0
    for i in res:
        ramt = getdonations(i['did'])
        print(i['did'], "did")
        print(ramt, "ramt")
        print(i['amount'], "amt")
        balance = i['amount'] - ramt
        print(balance)
        result.append({'did': i['did'], 'date_entry': i['date_entry'], 'amount': i['amount'],'name':i['name'],'orglid':i['orglid'],
                       'needed_beforedate': i['needed_beforedate'], 'purpose': i['purpose'], 'orglid': i['orglid'],'description':i['description'],'status':i['description'], 'ramt': ramt,
                       'balance': balance})
    return render_template("USER/viewdonation_req.html",data=result)

@app.route('/view_charityadmin')
def view_charityadmin():

    db=Db()
    qry = "SELECT * FROM `donation_request` WHERE `orglid`=1"
    res = db.select(qry)

    result = []
    ramt = 0.0
    for i in res:
        ramt = getdonations(i['did'])
        print(i['did'], "did")
        print(ramt, "ramt")
        print(i['amount'], "amt")
        balance = i['amount'] - ramt
        print(balance)
        result.append({'did': i['did'], 'date_entry': i['date_entry'], 'amount': i['amount'],'orglid':i['orglid'],
                       'needed_beforedate': i['needed_beforedate'], 'purpose': i['purpose'], 'orglid': i['orglid'],'description':i['description'],'status':i['description'], 'ramt': ramt,
                       'balance': balance})

    return render_template("USER/view_charityadmin.html",data=result)


@app.route('/userpayment/<oid>/<did>/<amount>/<balance>')
def userpayment(oid,did,amount,balance):
    if session['lid']=='':
        return redirect('/')
    session['oid']=oid
    session['did']=did
    session['amount']=amount
    return render_template("USER/userpayment.html",oid=oid,did=did,amount=amount,balance=balance)


@app.route('/addamountpost',methods=["post"])
def addamountpost():

    accountnumber=request.form["textfield4"]
    privatekey=request.form["textfield"]
    amount = int(request.form["textfield3"])
    checkbalance(amount,accountnumber,privatekey)
    rid = request.form["did"]
    print(rid)
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
        print(contract_abi)
    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
    blocknumber = web3.eth.get_block_number()
    print(blocknumber)

    policyid = int(rid)
    print(policyid)
    userid = int(session["lid"])


    from datetime import datetime
    date = datetime.now().strftime("%Y/%m/%d-%H:%M:%S")
    print(policyid)

    # message2 = contract.functions.addTransaction(blocknumber + 1, policyid, userid, int(amount), date).transact()
    message2 = contract.functions.addTransaction(policyid, policyid, userid, amount, date).transact({'from': web3.eth.accounts[0], 'gasPrice': web3.eth.gasPrice, 'gas': web3.eth.getBlock('latest').gasLimit})

    print(message2)


    return "<script>alert('Success');window.location='/viewdonation_req'</script>"





@app.route("/mytrans")
def mytrans():
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions

    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)

    blocknumber = web3.eth.get_block_number()
    print(blocknumber)
    lq=[]
    for i in range(blocknumber,5, -1):
        a = web3.eth.get_transaction_by_block(i, 0)
        try:
            decoded_input = contract.decode_function_input(a['input'])
            print(decoded_input)
            print("ku")
            print(decoded_input)
            lq.append(decoded_input[1])
        except Exception as a:
            pass
    print(lq)
    tot=0
    ls=[]
    for i in lq:
        print(i["policyida"])
        if int(i["userida"])==int(session['lid']):
            # ls.append(i)
            print(i['userida'],"aaaaaaaaaaaaaaaaa")

            qry="SELECT * FROM `donation_request` JOIN `organization` ON `donation_request`.`orglid`=`organization`.`org_lid` WHERE donation_request.did='"+str(i['policyida'])+"'"
            db=Db()
            res=db.selectOne(qry)
            if res is not None:
                a={'amounta':i['amounta'],'userida':i['userida'],'policyida':i['policyida'],'datea':i['datea'], 'amount': res['amount'],'name':res['name'],'orglid':res['orglid'],
                       'needed_beforedate': res['needed_beforedate'], 'purpose': res['purpose'],'description':res['description'],'status':res['description']}
                ls.append(a)
            tot+=i["amounta"]
    return render_template("USER/view_my_donations.html",ls=ls,tot=tot)


@app.route("/org_view_donations/<did>")
def org_view_donations(did):

    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions

    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
    blocknumber = web3.eth.get_block_number()

    print(blocknumber)
    lq=[]
    for i in range(blocknumber,5, -1):
        a = web3.eth.get_transaction_by_block(i, 0)
        try:
            decoded_input = contract.decode_function_input(a['input'])
            lq.append(decoded_input[1])
        except Exception as a:
            pass

    print(lq)
    tot=0
    ls=[]
    for i in lq:
        print(i["policyida"])
        if int(i["policyida"])==int(did):
            db=Db()
            qry="SELECT * FROM `users` WHERE `lid`='"+str(i['userida'])+"' "
            res=db.selectOne(qry)
            a={'amounta':i['amounta'],'userida':i['userida'],'policyida':i['policyida'],'datea':i['datea'],'uname':res['name'],'uemail':res['email'],'uphone':res['phone']}
            ls.append(a)
            tot+=i["amounta"]
    return render_template("ORGANIZATION/org_view_donations.html",ls=ls,tot=tot)


@app.route("/admin_view_donations/<did>")
def admin_view_donations(did):

    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
    blocknumber = web3.eth.get_block_number()

    print(blocknumber)
    lq=[]
    for i in range(blocknumber,5, -1):
        a = web3.eth.get_transaction_by_block(i, 0)
        try:
            decoded_input = contract.decode_function_input(a['input'])
            lq.append(decoded_input[1])
        except Exception as a:
            pass
    print(lq)
    tot=0
    ls=[]
    for i in lq:
        print(i["policyida"])
        if int(i["policyida"])==int(did):
            a={'amounta':i['amounta'],'userida':i['userida'],'policyida':i['policyida'],'datea':i['datea']}
            ls.append(a)
            tot+=i["amounta"]

    return render_template("admin/admin_view_donations.html",ls=ls,tot=tot)




@app.route("/admin_donationrefund/<did>/<amtt>")
def admin_donationrefund(did,amtt):
    if session['lid']=='':
        return redirect('/')
    session["rid"]=did
    session["amt"]=amtt

    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
    blocknumber = web3.eth.get_block_number()

    print(blocknumber)
    lq=[]
    for i in range(blocknumber,5, -1):
        a = web3.eth.get_transaction_by_block(i, 0)
        try:
            decoded_input = contract.decode_function_input(a['input'])
            lq.append(decoded_input[1])
        except Exception as a:
            pass
    print(lq)
    tot=0
    ls=[]
    for i in lq:
        print(i["policyida"])
        if int(i["policyida"]) == int(did):
            a={'amounta':i['amounta'],'userida':i['userida'],'policyida':i['policyida'],'datea':i['datea']}
            ls.append(a)
            tot+=i["amounta"]
    print(ls,"haiiiiiiiiiiiiiiiiiiiiiiiii")
    return render_template("admin/admin_refunddonations.html",ls=ls,tot=tot)

@app.route('/admin_donationrefundpost',methods=["post"])
def admin_donationrefundpost():
    if session['lid']=='':
        return redirect('/')
    refund_amt = request.form['textfield2']
    did=session["rid"]
    totamt=float(session["amt"])
    print(refund_amt)
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
    blocknumber = web3.eth.get_block_number()

    print(blocknumber)
    lq=[]
    for i in range(blocknumber,5, -1):
        a = web3.eth.get_transaction_by_block(i, 0)
        try:
            decoded_input = contract.decode_function_input(a['input'])
            lq.append(decoded_input[1])
        except Exception as a:
            pass
    print(lq)
    tot=0
    ls=[]
    for i in lq:
        print(i["policyida"])
        if int(i["policyida"])==int(did):
            a={'amounta':i['amounta'],'userida':i['userida'],'policyida':i['policyida'],'datea':i['datea']}
            ls.append(a)
            tot+=i["amounta"]
    k=len(ls)
    if k==1:
        qry="select * from user_account where uid='"+str(ls[0]["userida"])+"'"
        print(qry)
        db=Db()
        res=db.selectOne(qry)
        print(res)
        if res is not None:
            if web3.isConnected():
                acc1 = deployed_contract_address
                acc2 = res['account_no']

                prvkey = "0x68d1bbc7b73723093fc8ee9d85db9d717341cedd6a6d40fc53ee280224c4bde5"
                nonce = web3.eth.getTransactionCount(acc1)

                abcd = web3.eth.get_balance(acc1)
                abcd = web3.fromWei(abcd, 'ether')
                print(abcd)

                tx = {
                    'nonce': nonce,
                    'to': acc2,
                    'value': web3.toWei(refund_amt, 'ether'),
                    'gas': 200000,
                    'gasPrice': web3.toWei('50', 'gwei')
                }
                signedtx = web3.eth.account.sign_transaction(tx, prvkey)
                hashx = web3.eth.send_raw_transaction(signedtx.rawTransaction)
                print(web3.toHex(hashx))

                qry="INSERT INTO `refund_status` (`user_id`,`request_id`,`amount`)VALUES('"+str(ls[0]["userida"])+"','"+str(ls[0]["policyida"])+"','"+refund_amt+"')"
                db.insert(qry)

                qry = "update `donation_request` SET `status`='refunddone' WHERE `did`='" + str(
                    ls[0]["policyida"]) + "'"
                db.update(qry)



    elif k>1:

        for i in range(k):
            userid=ls[i]["userida"]
            amountu=ls[i]["amounta"]
            ratio=amountu/totamt
            # give=float(refund_amt)/ratio
            give=float(refund_amt)*ratio
            qry = "select * from user_account where uid='" + str(userid) + "'"
            print(qry)
            db = Db()
            res = db.selectOne(qry)
            print(res)
            if res is not None:
                if web3.isConnected():
                    acc1 = deployed_contract_address
                    acc2 = res['account_no']


                    print( 'give', give, '----------------------------------')
                    print( 'tot', tot, '----------------------------------')
                    print( 'totamt', totamt, '----------------------------------')

                    prvkey = "0x68d1bbc7b73723093fc8ee9d85db9d717341cedd6a6d40fc53ee280224c4bde5"
                    nonce = web3.eth.getTransactionCount(acc1)

                    abcd = web3.eth.get_balance(acc1)
                    abcd = web3.fromWei(abcd, 'ether')
                    print(abcd)

                    tx = {
                        'nonce': nonce,
                        'to': acc2,
                        'value': web3.toWei(give, 'ether'),
                        'gas': 200000,
                        'gasPrice': web3.toWei('50', 'gwei')
                    }
                    signedtx = web3.eth.account.sign_transaction(tx, prvkey)
                    hashx = web3.eth.send_raw_transaction(signedtx.rawTransaction)
                    print(web3.toHex(hashx))

                    qry = "INSERT INTO `refund_status` (`user_id`,`request_id`,`amount`)VALUES('" + str(ls[i]["userida"]) + "','" + str(ls[i]["policyida"]) + "','" + str(give) + "')"
                    db.insert(qry)

        qry = "update `donation_request` SET `status`='refunddone' WHERE `did`='" + str(ls[0]["policyida"]) + "'"
        db.update(qry)

    else:
        pass
    return redirect("/viewdonationrequest")


@app.route('/transaction_hist')
def transaction_hist():
    return render_template("admin/transaction_hist.html")


@app.route('/refund_history')
def refund_history():
    db =Db()
    if session['lid']=='':
        return redirect('/')
    qry="SELECT * FROM `refund_status` WHERE `user_id`='"+str(session['lid'])+"'"
    res = db.select(qry)
    print(res)
    return render_template("user/refund_history.html",data=res)




#orgrefund


@app.route("/org_donationrefund/<did>/<amtt>")
def org_donationrefund(did,amtt):
    session["rid"]=did
    session["amt"]=amtt

    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
    blocknumber = web3.eth.get_block_number()

    print(blocknumber)
    lq=[]
    for i in range(blocknumber,5, -1):
        a = web3.eth.get_transaction_by_block(i, 0)
        try:
            decoded_input = contract.decode_function_input(a['input'])
            lq.append(decoded_input[1])
        except Exception as a:
            pass
    print(lq)
    tot=0
    ls=[]
    for i in lq:
        db=Db()
        qry="SELECT * FROM `users` WHERE `lid`='"+str(i['userida'])+"'"
        res=db.selectOne(qry)

        qry2="SELECT * FROM `user_account` WHERE `uid`='"+str(i['userida'])+"'"
        res2=db.selectOne(qry2)
        print(i["policyida"])
        if int(i["policyida"]) == int(did):
            a={'amounta':i['amounta'],'userida':i['userida'],'policyida':i['policyida'],'datea':i['datea'],"uname":res['name'],"uemail":res['email'],"uphone":res['phone'],"account":res2['account_no']}
            ls.append(a)
            tot+=i["amounta"]
    print(ls,"haiiiiiiiiiiiiiiiiiiiiiiiii")
    return render_template("ORGANIZATION/org_refunddonations.html",ls=ls,tot=tot)

@app.route('/org_donationrefundpost',methods=["post"])
def org_donationrefundpost():
    refund_amt = request.form['textfield2']
    did=session["rid"]
    totamt=float(session["amt"])
    print(refund_amt)

    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
    blocknumber = web3.eth.get_block_number()

    print(blocknumber)
    lq=[]
    for i in range(blocknumber,5, -1):
        a = web3.eth.get_transaction_by_block(i, 0)
        try:
            decoded_input = contract.decode_function_input(a['input'])
            lq.append(decoded_input[1])
        except Exception as a:
            pass
    print(lq)
    tot=0
    ls=[]
    for i in lq:
        print(i["policyida"])
        if int(i["policyida"])==int(did):
            a={'amounta':i['amounta'],'userida':i['userida'],'policyida':i['policyida'],'datea':i['datea']}
            ls.append(a)
            tot+=i["amounta"]
    k=len(ls)
    if k==1:
        qry="select * from user_account where uid='"+str(ls[0]["userida"])+"'"
        print(qry)
        db=Db()
        res=db.selectOne(qry)
        print(res)
        if res is not None:
            if web3.isConnected():
                acc1 = deployed_contract_address
                acc2 = res['account_no']

                prvkey = "0x68d1bbc7b73723093fc8ee9d85db9d717341cedd6a6d40fc53ee280224c4bde5"
                nonce = web3.eth.getTransactionCount(acc1)

                abcd = web3.eth.get_balance(acc1)
                abcd = web3.fromWei(abcd, 'ether')
                # print(abcd)

                tx = {
                    'nonce': nonce,
                    'to': acc2,
                    'value': web3.toWei(refund_amt, 'ether'),
                    'gas': 200000,
                    'gasPrice': web3.toWei('50', 'gwei')
                }
                signedtx = web3.eth.account.sign_transaction(tx, prvkey)
                hashx = web3.eth.send_raw_transaction(signedtx.rawTransaction)
                print(web3.toHex(hashx))

                qry="INSERT INTO `refund_status` (`user_id`,`request_id`,`amount`)VALUES('"+str(ls[0]["userida"])+"','"+str(ls[0]["policyida"])+"','"+refund_amt+"')"
                db.insert(qry)


                qry="update `donation_request` SET `status`='refunddone' WHERE `did`='"+str(ls[0]["policyida"])+"'"
                db.update(qry)

    elif k>1:

        for i in range(k):
            userid=ls[i]["userida"]
            amountu=ls[i]["amounta"]

            print(totamt,"totamt")

            # print(amountu,"amounttttttttt")

            ratio=amountu/totamt

            # print(ratio,"rattttttttttttttt")


            give=float(refund_amt)*ratio

            # print(give,"ggggggggggggggggg")

            qry = "select * from user_account where uid='" + str(userid) + "'"
            print(qry)
            db = Db()
            res = db.selectOne(qry)
            print(res)
            if res is not None:
                if web3.isConnected():
                    acc1 = deployed_contract_address

                    # print(acc1,"account nooooooo")
                    acc2 = res['account_no']

                    # print(acc2,"acccccount22")

                    prvkey = "0x68d1bbc7b73723093fc8ee9d85db9d717341cedd6a6d40fc53ee280224c4bde5"


                    # print(prvkey,"pkkkkkkkkkkkkkkkkkkkk")
                    nonce = web3.eth.getTransactionCount(acc1)

                    # print(nonce,"hlooooooooooo")

                    abcd = web3.eth.get_balance(acc1)
                    abcd = web3.fromWei(abcd, 'ether')
                    print(abcd)

                    print("give","==============================", give, acc2)

                    tx = {
                        'nonce': nonce,
                        'to': acc2,
                        'value': web3.toWei(give, 'ether'),
                        'gas': 200000,
                        'gasPrice': web3.toWei('50', 'gwei')
                    }
                    signedtx = web3.eth.account.sign_transaction(tx, prvkey)
                    hashx = web3.eth.send_raw_transaction(signedtx.rawTransaction)
                    print(web3.toHex(hashx))

                    qry = "INSERT INTO `refund_status` (`user_id`,`request_id`,`amount`)VALUES('" + str(ls[i]["userida"]) + "','" + str(ls[i]["policyida"]) + "','" + str(give) + "')"
                    db.insert(qry)

        qry = "update `donation_request` SET `status`='refunddone' WHERE `did`='" + str(ls[0]["policyida"]) + "'"
        db.update(qry)


    else:
        pass
    return redirect('/view_mycharity')








if __name__ == '__main__':
    app.run(debug=True)


