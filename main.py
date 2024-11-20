import pymysql
dbstr = 'http://localhost:3006'


def main():
    print("Hello World!")
    mydb = pymysql.connect(dbstr, True, 60)


main()