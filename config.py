from mysql import connector

class Connection():

    @classmethod
    def dev_connection(self):
        db = connector.connect(
            host = "localhost",
            user = "root",
            password = "1234",
            database = "blog"
        )
        return db

    @classmethod
    def prod_connection(self):
        db = connector.connect(
            host = "requiemdelespiritu.mysql.pythonanywhere-services.com",
            user = "requiemdelespiri",
            password = "Queen12344321",
            database = "requiemdelespiri$blog"
        )
        return db

#GRANT ALL PRIVILEGES ON * . * TO 'requiemdelespiri'@'requiemdelespiritu.mysql.pythonanywhere-services.com' by "Queen12344321" with grant option;