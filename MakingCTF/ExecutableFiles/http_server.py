import http.server
import socketserver
from urllib.parse import urlparse, parse_qs
import os
import sys
import protocols as protocols

# Global variable to track the number of remaining requests after the stop condition is met
remaining_requests = None

class MyHandler(http.server.BaseHTTPRequestHandler):

    #a varibale that will tell us how many requests are left until the server is to die (as the client solved this stage), NONE signifies that the client did not yet solve this stage 

    def log_message(self, format, *args):
        """ Override to prevent logging to the terminal """
        return

    def get_file_data(self, filename):
        """ Get data from file """
        try:
            with open(filename, 'rb') as f: #open for reading bytes, supports text and images
                data = f.read()
                return data
        except FileNotFoundError: #file was not found
            return None
        
    def check_HOST(self):
        """check if the host is correct, ie, it matches our 'SERVER'"""
        return self.headers["Host"] == protocols.SERVER
    
    def do_GET(self):
        """handle standard get requests"""
        
        global remaining_requests
        
       
        try: #possible internal error
               
            # Parse the URL and query parameters
            parsed_url = urlparse(self.path)
            query_params = parse_qs(parsed_url.query)
            username = query_params.get('username', [None])[0] #get the username from the query parameters
            password = query_params.get('password', [None])[0] #get the password from the query parameters

            close_server=False #a flag to tell us if we need to close the server
            if isinstance(remaining_requests, int): # if we have a number, the client solved this stage
                remaining_requests -= 1 # decrement
                if remaining_requests == 0: # if we are done
                    close_server = True # time to shutdown the server
        

            #if the client tries to connect without properly specifying the host "student_finder.co.il"
            if not self.check_HOST(): #check if the host is correct 
                self.send_error(protocols.HTTP_MISDIRECTED_REQUEST)               

            #we will now  run through different cases of what the request is
            elif parsed_url.path.startswith("/hidden") and parsed_url.path != "/hidden": # we are dealing with an image, browser probably did this
                data = self.get_file_data(os.path.join(os.path.dirname(__file__), "webroot", "imgs", *(parsed_url.path.split("/")[2:])))
            
                if not data: #the file did not exist, must send the bad file searcher page
                    data = self.get_file_data(os.path.join(os.path.dirname(__file__), "webroot", "html_files", "bad_file_searcher.html"))
                    self.send_response(protocols.HTTP_NOT_FOUND)
                    self.send_header("Content-Type", "text/html")
                    self.send_header("Content-Length", str(len(data)))
                    self.send_header("Connection", "close")
                    self.end_headers()
                    self.wfile.write(data)

                else: #file was found, so it was a proper request      
                    self.send_response(protocols.HTTP_OK)
                    self.send_header("Content-Type", "image/jpeg") # we are dealing with an image
                    self.send_header("Content-Length", str(len(data)))
                    self.send_header("Connection", "close")
                    self.end_headers()
                    self.wfile.write(data)
        
            elif parsed_url.path == "/imgs/favicon.ico" or parsed_url.path == "/favicon.ico": # we are dealing with an the favicon, browser probably did this
                data = self.get_file_data(os.path.join(os.path.dirname(__file__), "webroot", "imgs", "favicon.ico"))
                self.send_response(protocols.HTTP_OK)
                self.send_header("Content-Type", "image/x-icon")
                self.send_header("Content-Length", str(len(data)))
                self.send_header("Connection", "close")
                self.end_headers()
                self.wfile.write(data)
            
        
            elif parsed_url.path == "/styles.css": # we are dealing with an the css file, browser probably did this
                data = self.get_file_data(os.path.join(os.path.dirname(__file__), "webroot", "html_files", "styles.css"))
                self.send_response(protocols.HTTP_OK)
                self.send_header("Content-Type", "text/css")
                self.send_header("Content-Length", str(len(data)))
                self.send_header("Connection", "close")
                self.end_headers()
                self.wfile.write(data)
          
            #now that we checked for browser automatic requests, we can check the requests the user made
            elif parsed_url.path != "/": # if the path is not the root, we will send a 404
                data = self.get_file_data(os.path.join(os.path.dirname(__file__), "webroot", "html_files", "requested_not_from_root.html"))
                self.send_response(protocols.HTTP_NOT_FOUND)
                self.send_header("Content-Type", "text/html")
                self.send_header("Content-Length", str(len(data)))
                self.send_header("Connection", "close")
                self.end_headers()
                self.wfile.write(data)

            #now we can check the query parameters to see if the player solved this stage

            #proper query parameters were used
            elif username == protocols.USERNAME and password == protocols.PASSWORD and parsed_url.path == "/":
                data = self.get_file_data(os.path.join(os.path.dirname(__file__), "webroot", "html_files", "goal.html"))
                self.send_response(protocols.HTTP_OK)
                self.send_header("Content-Type", "text/html")
                self.send_header("Content-Length", str(len(data)))
                self.send_header("Connection", "close")
                self.end_headers()
                self.wfile.write(data)

                #set the number of remaining requests to 2, as the player solved this stage, and needs only the image and the css file (we assume favicon was chached)
                remaining_requests = 2 
        
        
            # Check for missing parameters (both proper parameters are missing) 
            elif not username and not password and parsed_url.path == "/":
                data = self.get_file_data(os.path.join(os.path.dirname(__file__), "webroot", "html_files", "no_parameters.html"))
                self.send_response(protocols.HTTP_UNAUTHORIZED)
                self.send_header("Content-Type", "text/html")
                self.send_header("Content-Length", str(len(data)))
                self.send_header("Connection", "close")
                self.end_headers()
                self.wfile.write(data)

            # only username is missing
            elif not username and parsed_url.path == "/":
                data = self.get_file_data(os.path.join(os.path.dirname(__file__), "webroot", "html_files", "missing_username.html"))
                self.send_response(protocols.HTTP_UNAUTHORIZED)
                self.send_header("Content-Type", "text/html")
                self.send_header("Content-Length", str(len(data)))
                self.send_header("Connection", "close")
                self.end_headers()
                self.wfile.write(data)

            #only password is missing
            elif not password and parsed_url.path == "/":
                data = self.get_file_data(os.path.join(os.path.dirname(__file__), "webroot", "html_files", "missing_password.html"))
                self.send_response(protocols.HTTP_UNAUTHORIZED)
                self.send_header("Content-Type", "text/html")
                self.send_header("Content-Length", str(len(data)))
                self.send_header("Connection", "close")
                self.end_headers()
                self.wfile.write(data)

            # Check for incorrect values for the parameters
            elif username != protocols.USERNAME or password != protocols.PASSWORD and parsed_url.path == "/":
                data = self.get_file_data(os.path.join(os.path.dirname(__file__), "webroot", "html_files", "wrong_values.html"))
                self.send_response(protocols.HTTP_UNAUTHORIZED)
                self.send_header("Content-Type", "text/html")
                self.send_header("Content-Length", str(len(data)))
                self.send_header("Connection", "close")
                self.end_headers()
                self.wfile.write(data)
        

            else: # Default case for unknown paths, probably won't end up here
                data = self.get_file_data(os.path.join(os.path.dirname(__file__), "webroot", "html_files", "not_sure_how_this_was_sent.html"))
                self.send_response(protocols.HTTP_NOT_FOUND)
                self.send_header("Content-Type", "text/html")
                self.send_header("Content-Length", str(len(data)))
                self.send_header("Connection", "close")
                self.end_headers()
                self.wfile.write(data)

            if close_server:
                print("Nothing more to see here...")
                sys.exit()
    
        except Exception: #some sort of internal server error
            self.send_response(protocols.HTTP_INTERNAL_SERVER_ERROR)
            self.send_header("Connection", "close")
            self.end_headers()

def http_server_ctf():
    """set up the server"""
    with socketserver.TCPServer((protocols.HTTP_IP, protocols.HTTP_PORT), MyHandler) as httpd:
        httpd.serve_forever()

if __name__ == "__main__":
    http_server_ctf()

