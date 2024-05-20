import pymysql.cursors   

# create a connection.
def getConnection(): 
    """
    The getConnection() function creates a connection to mysql database server by using library PyMySQL.

    Parameters:
    This function doesn't have any parameters.

    Returns:
    This function returns a connection to your database
    
    """

    # create connection to database with host, username, password, database
    connection = pymysql.connect(host='sinno.soict.ai',
                                 user='nguyenquanghung',
                                 password='20183760',
                                 db='vnindex',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection