"""The following file contains the protocols I am defining for sending the certificate and the protocols for HTTP"""

import base64

#globals for both
SERVER = 'student_finder.co.il'
CERTIFICATE_PORT = 3000
USERNAME = "TeachersPet"
PASSWORD = "The_Best_Student"

#globals for the certificate to be created
CERTIFICATE_USERNAME = base64.b64encode("username".encode()).decode() + ": " + USERNAME
CERTIFICATE_PASSWORD = base64.b64encode("password".encode()).decode() + ": " + PASSWORD

#protocols for certificate
SIZE_OK = "OK: {}"
REQUEST_PERMISSION = "READY TO SEND FILE"
PERMISSION_TO_SEND = "BEGIN TRANSMISSION"

#protocols for HTTP_Server
HTTP_IP = '127.0.0.1'
HTTP_PORT = 80
HTTP_OK = 200
HTTP_NOT_FOUND = 404
HTTP_UNAUTHORIZED = 401
HTTP_MISDIRECTED_REQUEST = 421
HTTP_INTERNAL_SERVER_ERROR = 500






