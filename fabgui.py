# -*- coding: utf-8 -*-

from Tkinter import *
import tkMessageBox
import tkFileDialog
from subprocess import check_output
from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap, CommentedSeq
import sys

root = Tk()
root.geometry("960x600")
root.title("Certificate Authority")
root.resizable(False, False)

cmd = check_output("cd $CAPATH;pwd", shell=True).rstrip()
addr = ""
dir = ""

def fab():


    def createfile():
        """Creates a client config file at desired location"""

        loc = tkFileDialog.askdirectory()
        with open(loc + "/fabric-ca-client-config.yaml", "w") as fp:
            fp.write(doc)


    def error(e):
        tkMessageBox.showinfo("Error", str(e))

    def slogin():
        """Function to start server"""

        try:
            un = t1.get()
            ps = t3.get()
            yaml = YAML()
            with open(cmd + "/docker-compose.yml") as fp:
                data = yaml.load(fp)
            data['fabric-ca-server']['command'] = "sh -c 'fabric-ca-server start -b " + \
                un + ":" + ps + "'"
            fp = open(cmd + "/docker-compose.yml", "w")
            yaml.dump(data, fp)
            res = check_output(
                "cd " + cmd + "; docker-compose up -d;", shell=True)
            print(res)
        except Exception as e:
            error(str(e))

        tkMessageBox.showinfo(message="Server Started")
        #raisef2(f1)


    def logout():
        """Function to stop server"""

        try:
            res = check_output(
                "cd " + cmd + "; docker rm -f $(docker ps -aq)", shell=True)
            tkMessageBox.showinfo("Logout", "Successful")
        except Exception as e:
            error(str(e))
        #raisef1(f2)


    def clogin():
        """Client Login"""

        global addr
        addr = t2.get()
        raisef3(f1)


    def cselect():
        """Client Select Radiobutton"""

        l1.place_forget()
        l2.place_forget()
        t1.place_forget()
        t3.place_forget()
        b1.place_forget()
        l3.place(x=355, y=130, width=250, height=30)
        t2.place(x=355, y=170, width=250, height=30)
        b10.place(x=430, y=220, width=100, height=30)


    def sselect():
        """Server Select Radiobutton"""

        l3.place_forget()
        t2.place_forget()
        b10.place_forget()
        l1.place(x=370, y=120, width=100, height=25)
        t1.place(x=460, y=120, width=100, height=25)
        l2.place(x=370, y=170, width=100, height=25)
        t3.place(x=460, y=170, width=100, height=25)
        b1.place(x=430, y=230, width=100, height=25)


    def donothing():
        pass


    def raisef1(f):
        """Raise First Frame"""

        f.place_forget()
        f1.place(x=0, y=0, width=960, height=600)
        f1.tkraise()


    def raisef2(f):
        """Raise Second Frame"""

        f.place_forget()
        f2.place(x=0, y=0, width=960, height=600)
        f2.tkraise()


    def raisef3(f):
        """Raise Third Frame"""

        f.place_forget()
        f3.place(x=0, y=0, width=960, height=600)
        f3.tkraise()


    def enrollshow():
        """Enroll Selection Button"""

        f3.place_forget()
        f4.place(x=0, y=0, width=960, height=600)
        f4.tkraise()


    def saveenroll():
        """Save and Enroll"""

        global dir

        try:
            yaml = YAML()
            with open(cmd + "/client-config.yaml") as fp:
                data = yaml.load(fp)

            data['url'] = "http://" + addr
            data['mspdir'] = dir + "/msp"
            data['csr']['cn'] = t5.get()

            f = CommentedSeq([CommentedMap([('C', t6.get()), ('ST', t7.get(
            )), ('L', t8.get()), ('O', t9.get()), ('OU', t10.get())])])
            data['csr']['names'] = f

            fp = open(cmd + "/client-config.yaml", "w")
            yaml.dump(data, fp)
            res = check_output("cd " + cmd + "; export FABRIC_CA_CLIENT_HOME=" + dir +
                               "; fabric-ca-client enroll -c client-config.yaml -u http://" + t11.get() + ":" + t12.get() + "@" + addr, shell=True)
        except Exception as e:
            error(str(e))
        print(res)
        tkMessageBox.showinfo(message="Successfully Enrolled")


    def seldir(t):
        """Select Directory"""

        global dir
        dir = tkFileDialog.askdirectory()
        t.delete(0, END)
        t.insert(0, dir)


    def registershow():
        """Show Register Page"""

        f3.place_forget()
        f6.place(x=0, y=0, width=960, height=600)
        f6.tkraise()


    def register():
        """Register Selection Button"""

        global dir
        global addr
        arg = ""

        if t16.get().rstrip() != "":
            arg += " --id.name " + t16.get()
        if t19.get().rstrip() != "":
            arg += " --id.type " + t19.get()
        if t18.get().rstrip() != "":
            arg += " --id.affiliation " + t18.get()
        if t17.get().rstrip() != "":
            arg += " --id.secret " + t17.get()
        if t21.get().rstrip() != "":
            arg += " --id.attrs " + t21.get()
        if t20.get().rstrip() != "":
            arg += " --id.maxenrollments " + t20.get()

        arg+=" -u http://"+addr
        #
        print(arg)
        try:
            res = check_output("export FABRIC_CA_CLIENT_HOME=" + dir +"; fabric-ca-client register " + arg,shell=True)
            print(res)
        except Exception as e:
            error(str(e))

        print(res)
        tkMessageBox.showinfo(message="Successfully Registered")


    def revokeshow():
        """Show Revoke Frame"""

        f3.place_forget()
        f5.place(x=0, y=0, width=960, height=600)
        f5.tkraise()


    def revoke():
        """Revokes Submitted Identity"""

        try:
            res = check_output("export FABRIC_CA_CLIENT_HOME=" +
                               dir + "; fabric-ca-client revoke -e " + t13.get() + ";",shell=True)
            print(res)
        except Exception as e:
            error(str(e))
        tkMessageBox("Info", "Successfully Revoked")

    def gencrl():
        """Generates CRL in MSP folder"""

        loc = tkFileDialog.askdirectory()
        try:
            res = check_output("cd " + loc + "; fabric-ca-client gencrl -M ~/msp",shell=True)
        except Exception as e:
            error(str(e))

    def modifyshow():
        """Show Modify Frame"""

        f3.place_forget()
        f7.place(x=0, y=0, width=960, height=600)
        f7.tkraise()

    def modify():
        """Modify Selection Button"""

        global dir
        arg = ""

        if t26.get().rstrip() != "":
            arg += " --type " + t26.get()
        if t25.get().rstrip() != "":
            arg += " --affliation " + t25.get()
        if t24.get().rstrip() != "":
            arg += " --secret " + t24.get()
        if t28.get().rstrip() != "":
            arg += " --attrs " + t28.get()
        if t27.get().rstrip() != "":
            arg += " --maxenrollments " + t27.get()

        try:
            res = check_output("export FABRIC_CA_CLIENT_HOME=" + dir + "; fabric-ca-client identity modify "+ t23.get() +" "+ arg,shell=True)
        except Exception as e:
            error(str(e))

        print(res)
        tkMessageBox.showinfo(message="Successfully Modified")


    def removeshow():
        """Show Remove Frame"""

        f3.place_forget()
        f8.place(x=0, y=0, width=960, height=600)
        f8.tkraise()


    def remove():
        """Remove Selection Button"""

        global dir

        try:
            res = check_output("export FABRIC_CA_CLIENT_HOME=" + dir + "; fabric-ca-client identity remove "+ t30.get(),shell=True)
        except Exception as e:
            error(str(e))

        print(res)
        tkMessageBox.showinfo(message="Successfully Modified")

    # MenuBAR Declaration


    m = Menu(root)

    opmenu = Menu(m, tearoff=0)
    #opmenu.add_command(label="Create New CA", command=donothing)
    opmenu.add_command(label="Create Client Config File", command=createfile)
    opmenu.add_separator()
    opmenu.add_command(label="Exit", command=root.quit)
    m.add_cascade(label="Options", menu=opmenu)

    # Frame Declaration

    f1 = Frame(root)
    f1.grid_rowconfigure(0, weight=1)
    f1.grid_columnconfigure(0, weight=1)

    f2 = Frame(root)
    f2.grid_rowconfigure(0, weight=1)
    f2.grid_columnconfigure(0, weight=1)

    f3 = Frame(root)
    f3.grid_rowconfigure(0, weight=1)
    f3.grid_columnconfigure(0, weight=1)

    f4 = Frame(root)
    f4.grid_rowconfigure(0, weight=1)
    f4.grid_columnconfigure(0, weight=1)

    f5 = Frame(root)
    f5.grid_rowconfigure(0, weight=1)
    f5.grid_columnconfigure(0, weight=1)

    f6 = Frame(root)
    f6.grid_rowconfigure(0, weight=1)
    f6.grid_columnconfigure(0, weight=1)

    f7 = Frame(root)
    f7.grid_rowconfigure(0, weight=1)
    f7.grid_columnconfigure(0, weight=1)

    f8 = Frame(root)
    f8.grid_rowconfigure(0, weight=1)
    f8.grid_columnconfigure(0, weight=1)



    # Frame F1
    rbvar = IntVar()
    l1 = Label(f1, text="Username")
    l2 = Label(f1, text="Password")
    l3 = Label(f1, text="Enter Server Address")
    t1 = Entry(f1)
    t2 = Entry(f1)
    t3 = Entry(f1, show="•")
    b1 = Button(f1, text="Login", command=slogin)
    b10 = Button(f1, text="Next", command=clogin)
    rb1 = Radiobutton(f1, text="Server", variable=rbvar, value=1, command=sselect)
    rb2 = Radiobutton(f1, text="Client", variable=rbvar, value=2, command=cselect)

    l1.place(x=370, y=120, width=100, height=25)
    t1.place(x=460, y=120, width=100, height=25)
    l2.place(x=370, y=170, width=100, height=25)
    t3.place(x=460, y=170, width=100, height=25)
    b1.place(x=430, y=230, width=100, height=25)
    rb1.place(x=370, y=90, width=100, height=25)
    rb2.place(x=460, y=90, width=100, height=25)

    b2 = Button(f1, text="End Server", command=logout)
    b2.place(x=430, y=500, width=100, height=25)

    # Frame F2

    # Frame F3
    b3 = Button(f3, text="Enroll", command=enrollshow)
    b4 = Button(f3, text="Register", command=registershow)
    b5 = Button(f3, text="Revoke Certificates", command=revokeshow)
    b6 = Button(f3, text="Generate CRL", command=gencrl)
    b7 = Button(f3, text="Modify", command=modifyshow)
    b8 = Button(f3, text="Remove", command=removeshow)
    b9 = Button(f3, text="Go Back", command=lambda: raisef1(f3))

    b3.place(x=320, y=200, width=140, height=30)
    b4.place(x=320, y=240, width=140, height=30)
    b5.place(x=320, y=280, width=140, height=30)
    b6.place(x=500, y=200, width=140, height=30)
    b7.place(x=500, y=240, width=140, height=30)
    b8.place(x=500, y=280, width=140, height=30)
    b9.place(x=410, y=320, width=140, height=30)


    # Frame F4

    t4 = Entry(f4)
    l4 = Label(f4, text="Select Directory")
    t5 = Entry(f4)
    l5 = Label(f4, text="Enrollment ID")
    t6 = Entry(f4)
    l6 = Label(f4, text="Country(C)")
    t7 = Entry(f4)
    l7 = Label(f4, text="State(ST)")
    t8 = Entry(f4)
    l8 = Label(f4, text="Location(L)")
    t9 = Entry(f4)
    l9 = Label(f4, text="Organisation(O)")
    t10 = Entry(f4)
    l10 = Label(f4, text="Organisational Unit(OU)")
    t11 = Entry(f4)
    l11 = Label(f4, text="ID")
    t12 = Entry(f4, show="•")
    l12 = Label(f4, text="Password")
    b11 = Button(f4, text="Back", command=lambda: raisef3(f4))
    b12 = Button(f4, text="Select", command=lambda: seldir(t4))
    b13 = Button(f4, text="Enroll", command=saveenroll)

    l4.place(x=20, y=20, width=150, height=25)
    t4.place(x=180, y=20, width=450, height=25)
    l5.place(x=20, y=120, width=180, height=25)
    t5.place(x=220, y=120, width=180, height=25)
    l6.place(x=20, y=160, width=180, height=25)
    t6.place(x=220, y=160, width=180, height=25)
    l7.place(x=20, y=200, width=180, height=25)
    t7.place(x=220, y=200, width=180, height=25)
    l11.place(x=20, y=240, width=180, height=25)
    t11.place(x=220, y=240, width=180, height=25)
    l8.place(x=390, y=120, width=180, height=25)
    t8.place(x=590, y=120, width=180, height=25)
    l9.place(x=390, y=160, width=180, height=25)
    t9.place(x=590, y=160, width=180, height=25)
    l10.place(x=390, y=200, width=180, height=25)
    t10.place(x=590, y=200, width=180, height=25)
    l12.place(x=390, y=240, width=180, height=25)
    t12.place(x=590, y=240, width=180, height=25)
    b12.place(x=640, y=20, width=150, height=25)
    b11.place(x=430, y=550, width=100, height=25)
    b13.place(x=430, y=500, width=100, height=25)

    # Frame f5

    sel = StringVar()
    l13 = Label(f5, text="Enrollment ID")
    t13 = Entry(f5)
    l14 = Label(f5, text="Reason")
    om1 = OptionMenu(f5, sel, "unspecified", "keycompromise", "cacompromise", "affiliationchange", "superseded",
                     "cessationofoperation", "certificatehold", "removefromcrl", "privilegewithdrawn", "aacompromise")
    t15 = Entry(f5)
    l15 = Label(f5, text="Select Revoker Directory")
    b14 = Button(f5, text="Revoke", command=revoke)
    b15 = Button(f5, text="Back", command=lambda: raisef3(f5))
    b16 = Button(f5, text="Select", command=lambda: seldir(t15))

    l13.place(x=320, y=200, width=150, height=25)
    t13.place(x=490, y=200, width=150, height=25)
    l14.place(x=320, y=240, width=150, height=25)
    om1.place(x=490, y=240, width=150, height=25)
    l15.place(x=20, y=20, width=200, height=25)
    t15.place(x=230, y=20, width=450, height=25)
    b14.place(x=430, y=280, width=100, height=25)
    b15.place(x=430, y=320, width=100, height=25)
    b16.place(x=700, y=20, width=150, height=25)

    # Frame 6

    t16 = Entry(f6)
    l16 = Label(f6, text="Name")
    t17 = Entry(f6)
    l17 = Label(f6, text="Secret")
    t18 = Entry(f6)
    l18 = Label(f6, text="Affliation")
    t19 = Entry(f6)
    l19 = Label(f6, text="Type")
    t20 = Entry(f6)
    l20 = Label(f6, text="Max Enrollments")
    t21 = Entry(f6)
    l21 = Label(f6, text="Attributes")
    t22 = Entry(f6)
    l22 = Label(f6, text="Select User Directory")
    b17 = Button(f6, text="Register", command=register)
    b18 = Button(f6, text="Back", command=lambda: raisef3(f6))
    b19 = Button(f6, text="Select", command=lambda: seldir(t22))

    l17.place(x=320, y=120, width=150, height=25)
    t17.place(x=490, y=120, width=150, height=25)
    l16.place(x=320, y=80, width=150, height=25)
    t16.place(x=490, y=80, width=150, height=25)
    l18.place(x=320, y=160, width=150, height=25)
    t18.place(x=490, y=160, width=150, height=25)
    l19.place(x=320, y=200, width=150, height=25)
    t19.place(x=490, y=200, width=150, height=25)
    l20.place(x=320, y=240, width=150, height=25)
    t20.place(x=490, y=240, width=150, height=25)
    l21.place(x=320, y=280, width=150, height=25)
    t21.place(x=490, y=280, width=150, height=25)
    l22.place(x=20, y=20, width=200, height=25)
    t22.place(x=230, y=20, width=450, height=25)
    b17.place(x=430, y=340, width=100, height=25)
    b18.place(x=430, y=380, width=100, height=25)
    b19.place(x=700, y=20, width=150, height=25)

    #Frame 7
    t23 = Entry(f7)
    l23 = Label(f7, text="Name")
    t24 = Entry(f7)
    l24 = Label(f7, text="Secret")
    t25 = Entry(f7)
    l25 = Label(f7, text="Affliation")
    t26 = Entry(f7)
    l26 = Label(f7, text="Type")
    t27 = Entry(f7)
    l27 = Label(f7, text="Max Enrollments")
    t28 = Entry(f7)
    l28 = Label(f7, text="Attributes")
    t29 = Entry(f7)
    l29 = Label(f7, text="Select User Directory")
    b20 = Button(f7, text="Modify", command=modify)
    b21 = Button(f7, text="Back", command=lambda: raisef3(f7))
    b22 = Button(f7, text="Select", command=lambda: seldir(t28))

    l23.place(x=320, y=80, width=150, height=25)
    t23.place(x=490, y=80, width=150, height=25)
    l24.place(x=320, y=120, width=150, height=25)
    t24.place(x=490, y=120, width=150, height=25)
    l25.place(x=320, y=160, width=150, height=25)
    t25.place(x=490, y=160, width=150, height=25)
    l26.place(x=320, y=200, width=150, height=25)
    t26.place(x=490, y=200, width=150, height=25)
    l27.place(x=320, y=240, width=150, height=25)
    t27.place(x=490, y=240, width=150, height=25)
    l28.place(x=320, y=280, width=150, height=25)
    t28.place(x=490, y=280, width=150, height=25)
    l29.place(x=20, y=20, width=200, height=25)
    t29.place(x=230, y=20, width=450, height=25)
    b20.place(x=430, y=340, width=100, height=25)
    b21.place(x=430, y=380, width=100, height=25)
    b22.place(x=700, y=20, width=150, height=25)


    #Frame 8

    t30 = Entry(f8)
    l30 = Label(f8, text="Name")
    t31 = Entry(f8)
    l31 = Label(f8, text="Select User Directory")
    b23 = Button(f8, text="Remove", command=modify)
    b24 = Button(f8, text="Back", command=lambda: raisef3(f8))
    b25 = Button(f8, text="Select", command=lambda: seldir(t31))

    l30.place(x=320, y=200, width=150, height=25)
    t30.place(x=490, y=200, width=150, height=25)
    l31.place(x=20, y=20, width=200, height=25)
    t31.place(x=230, y=20, width=450, height=25)
    b23.place(x=430, y=340, width=100, height=25)
    b24.place(x=430, y=380, width=100, height=25)
    b25.place(x=700, y=20, width=150, height=25)


    # Start Initial Window with Frame 1

    f1.place(x=0, y=0, width=960, height=600)
    f1.tkraise()

    root.config(menu=m)

    #Client Config Document Template

    doc = """
    # Start Display

    #############################################################################
    #   This is a configuration file for the fabric-ca-client command.
    #
    #   COMMAND LINE ARGUMENTS AND ENVIRONMENT VARIABLES
    #   ------------------------------------------------
    #   Each configuration element can be overridden via command line
    #   arguments or environment variables.  The precedence for determining
    #   the value of each element is as follows:
    #   1) command line argument
    #      Examples:
    #      a) --url https://localhost:7054
    #         To set the fabric-ca server url
    #      b) --tls.client.certfile certfile.pem
    #         To set the client certificate for TLS
    #   2) environment variable
    #      Examples:
    #      a) FABRIC_CA_CLIENT_URL=https://localhost:7054
    #         To set the fabric-ca server url
    #      b) FABRIC_CA_CLIENT_TLS_CLIENT_CERTFILE=certfile.pem
    #         To set the client certificate for TLS
    #   3) configuration file
    #   4) default value (if there is one)
    #      All default values are shown beside each element below.
    #
    #   FILE NAME ELEMENTS
    #   ------------------
    #   The value of all fields whose name ends with "file" or "files" are
    #   name or names of other files.
    #   For example, see "tls.certfiles" and "tls.client.certfile".
    #   The value of each of these fields can be a simple filename, a
    #   relative path, or an absolute path.  If the value is not an
    #   absolute path, it is interpretted as being relative to the location
    #   of this configuration file.
    #
    #############################################################################

    #############################################################################
    # Client Configuration
    #############################################################################

    # URL of the Fabric-ca-server (default: http://localhost:7054)
    url: <<<URL>>>

    # Membership Service Provider (MSP) directory
    # This is useful when the client is used to enroll a peer or orderer, so
    # that the enrollment artifacts are stored in the format expected by MSP.
    mspdir: msp

    #############################################################################
    #    TLS section for secure socket connection
    #
    #  certfiles - PEM-encoded list of trusted root certificate files
    #  client:
    #    certfile - PEM-encoded certificate file for when client authentication
    #    is enabled on server
    #    keyfile - PEM-encoded key file for when client authentication
    #    is enabled on server
    #############################################################################
    tls:
      # TLS section for secure socket connection
      certfiles:
      client:
        certfile:
        keyfile:

    #############################################################################
    #  Certificate Signing Request section for generating the CSR for an
    #  enrollment certificate (ECert)
    #
    #  cn - Used by CAs to determine which domain the certificate is to be generated for
    #
    #  serialnumber - The serialnumber field, if specified, becomes part of the issued
    #     certificate's DN (Distinguished Name).  For example, one use case for this is
    #     a company with its own CA (Certificate Authority) which issues certificates
    #     to its employees and wants to include the employee's serial number in the DN
    #     of its issued certificates.
    #     WARNING: The serialnumber field should not be confused with the certificate's
    #     serial number which is set by the CA but is not a component of the
    #     certificate's DN.
    #
    #  names -  A list of name objects. Each name object should contain at least one
    #    "C", "L", "O", or "ST" value (or any combination of these) where these
    #    are abbreviations for the following:
    #        "C": country
    #        "L": locality or municipality (such as city or town name)
    #        "O": organization
    #        "OU": organizational unit, such as the department responsible for owning the key;
    #         it can also be used for a "Doing Business As" (DBS) name
    #        "ST": the state or province
    #
    #    Note that the "OU" or organizational units of an ECert are always set according
    #    to the values of the identities type and affiliation. OUs are calculated for an enroll
    #    as OU=<type>, OU=<affiliationRoot>, ..., OU=<affiliationLeaf>. For example, an identity
    #    of type "client" with an affiliation of "org1.dept2.team3" would have the following
    #    organizational units: OU=client, OU=org1, OU=dept2, OU=team3
    #
    #  hosts - A list of host names for which the certificate should be valid
    #
    #############################################################################
    csr:
      cn: <<<ENROLLMENT_ID>>>
      serialnumber:
      names:
        - C: US
          ST: North Carolina
          L:
          O: Hyperledger
          OU: Fabric
      hosts:
        - <<<MYHOST>>>

    #############################################################################
    #  Registration section used to register a new identity with fabric-ca server
    #
    #  name - Unique name of the identity
    #  type - Type of identity being registered (e.g. 'peer, app, user')
    #  affiliation - The identity's affiliation
    #  maxenrollments - The maximum number of times the secret can be reused to enroll.
    #                   Specially, -1 means unlimited; 0 means to use CA's max enrollment
    #                   value.
    #  attributes - List of name/value pairs of attribute for identity
    #############################################################################
    id:
      name:
      type:
      affiliation:
      maxenrollments: 0
      attributes:
       # - name:
       #   value:

    #############################################################################
    #  Enrollment section used to enroll an identity with fabric-ca server
    #
    #  profile - Name of the signing profile to use in issuing the certificate
    #  label - Label to use in HSM operations
    #############################################################################
    enrollment:
      profile:
      label:

    #############################################################################
    # Name of the CA to connect to within the fabric-ca server
    #############################################################################
    caname:

    #############################################################################
    # BCCSP (BlockChain Crypto Service Provider) section allows to select which
    # crypto implementation library to use
    #############################################################################
    bccsp:
        default: SW
        sw:
            hash: SHA2
            security: 256
            filekeystore:
                # The directory used for the software file-based keystore
                keystore: msp/keystore
    """
    root.mainloop()


if __name__=="__main__":
    fab()
