"""This code mimics a server and sends sorted data back to the user.

Author: Andrew Vinci
Class: CSI-275-01
Assignment: Lab/HW 5 -- Sorting Server

Certification of Authenticity:
I certify that this is entirely my own work, except where I have given
fully-documented references to the work of others. I understand the definition
and consequences of plagiarism and acknowledge that the assessor of this
assignment may, for the purpose of assessing this assignment:
- Reproduce this assignment and provide a copy to another member of academic
- staff; and/or Communicate a copy of this assignment to a plagiarism checking
- service (which may then retain a copy of this assignment on its database for
- the purpose of future plagiarism checking)
"""

import socket

HOST = "localhost"
PORT = 20000


class SortServer:
    """This class is a server sorting class that sorts data."""

    def __init__(self, host, port):
        """This is the constructor to the sort server class."""

        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.address_tuple = (host, port)
        self.sock.bind(self.address_tuple)

    def run_server(self):
        """This function runs the server and parses data."""

        # listen to socket

        self.sock.listen(20)

        # while true, accept incoming data from socket

        while True:
            client_sock, addr = self.sock.accept()

            # while true, receive data from socket, if there is
            # no data then break loop

            while True:
                data = client_sock.recv(4096)
                if not data:
                    client_sock.close()
                    break

                # decode data from ascii

                string_data = data.decode('ascii')

                # if beginning of list doesn't begin with LIST
                # then return error message decoded in ascii

                string_data = string_data.split()
                if string_data[0] != "LIST":
                    error_string = "ERROR"
                    client_sock.sendall(error_string.encode('ascii'))
                    continue

                # new string is equal to all the information after first word

                new_string = string_data[1:]

                str1 = " "
                join_string = str1.join(new_string)

                # remove all characters that will cause problems in string

                remove_spaces = join_string.replace(" ", "")
                remove_decimal = remove_spaces.replace(".", "")
                remove_decimal_spaces = remove_decimal.replace(" ", "")
                remove_line = remove_decimal_spaces.replace("|", "")
                final_check = remove_line.replace("-", "")

                # check if list ends with specified character

                a = "a"
                d = "d"
                s = "s"
                char_tuple = (a, d, s)
                if final_check.endswith(char_tuple):
                    final_check = final_check[:-1]

                check_numbers = final_check.isdigit()

                if not check_numbers:
                    error_string = "ERROR"
                    client_sock.sendall(error_string.encode('ascii'))
                    continue

                # remove the last digit in the string for special character

                remove_last_digit = join_string.replace(a, "")
                remove_last_digit_2 = remove_last_digit.replace(d, "")
                remove_last_digit_3 = remove_last_digit_2.replace(s, "")
                remove_last_digit_4 = remove_last_digit_3.replace("|", "")

                new_string_2 = remove_last_digit_4.split()

                temp_var = new_string[-1]
                temp_var_2 = list(temp_var)

                # if list ends with special character send keyword back
                # do this for every keyword
                # if keyword doesn't exist, then proceed without

                if temp_var_2[-1] == a:
                    new_string_2.sort(key=float)
                    sorted_keyword = "SORTED"
                    new_string_2.insert(0, sorted_keyword)

                    str3 = " "
                    sorted_list = str3.join(new_string_2)
                    return_data = sorted_list.encode('ascii')
                    client_sock.sendall(return_data)
                    continue
                elif temp_var_2[-1] == d:
                    new_string_2.sort(key=float, reverse=True)
                    sorted_keyword = "SORTED"
                    new_string_2.insert(0, sorted_keyword)

                    str4 = " "
                    sorted_list = str4.join(new_string_2)
                    return_data = sorted_list.encode('ascii')
                    client_sock.sendall(return_data)
                    continue
                elif temp_var_2[-1] == s:
                    new_string_2.sort()
                    sorted_keyword = "SORTED"
                    new_string_2.insert(0, sorted_keyword)

                    str5 = " "
                    sorted_list = str5.join(new_string_2)
                    return_data = sorted_list.encode('ascii')
                    client_sock.sendall(return_data)
                    continue
                else:
                    new_string_2.sort(key=float)
                    sorted_keyword = "SORTED"
                    new_string_2.insert(0, sorted_keyword)

                    str2 = " "
                    sorted_list = str2.join(new_string_2)
                    return_data = sorted_list.encode('ascii')

                # send data back to server and close the socket.

                client_sock.sendall(return_data)
            client_sock.close()


if __name__ == "__main__":

    server = SortServer(HOST, PORT)
    server.run_server()
