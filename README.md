# FabGUI Workflow

## Initial Setup

1.	Install the fabric-ca files from github
2.	Add an environment variable to PATH, CAPATH which points to the location of the docker-compose.yaml file. It’ll be in /go/src/github.com/hyperledger/fabric-ca/docker/server
3.	After this the python script will run. The only dependency the python script will require is ruamel.yaml package. Install that using pip. This package is used for the editing of YAML files.

## Working

1.	Run two instances of the python script from shell. One will act as server. Another will act as the client.
2.	Log in to the admin with username and password. This is a bootstrap identity. Check fabric-ca documentation for more details: https://hyperledger-fabric-ca.readthedocs.io/en/latest/users-guide.html#initializing-the-server
3.	On the client choose client option and enter the address of the server. In this case it is localhost:7054. The server location details are stored in the docker-compose.yaml file.
4.	Now choose enroll option to enroll the server admin. Enter the details and location to save the certificates which will be generated. Use username and password as the same used in step 2. More details can be found at https://hyperledger-fabric-ca.readthedocs.io/en/latest/users-guide.html#enrolling-the-bootstrap-identity. Now we can use the admin identity to register and enroll other entities. Once we register other identities, we can use those identities to register other entities as well. The capabilities of each entity is described by the attributes given during registration. For a full overview of attributes check https://hyperledger-fabric-ca.readthedocs.io/en/latest/users-guide.html#registering-a-new-identity and https://hyperledger-fabric-ca.readthedocs.io/en/latest/users-guide.html#enrolling-a-peer-identity
5.	Similarly the other functions are self descriptive. Modify, delete, revoke, remove and generate revoked list. All of them requires the fabric-ca-client-config.yaml file for checking the details of the identity which executes these operations. So the select directory option in each of these options are used for selecting the location of the fabric-ca-client-config.yaml file of identity running these commands.
6.	Custom attributes can be entered into the certificates while registering. For a more detailed discussion see https://hyperledger-fabric-ca.readthedocs.io/en/latest/users-guide.html#attribute-based-access-control
