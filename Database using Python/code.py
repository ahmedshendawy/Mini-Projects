import psycopg2

con = psycopg2.connect(database='DBname', user='username', password='YourPassword',
                       host='127.0.0.1', port='5432')
print('Database opened successfully')
cur = con.cursor()

cur.execute('''create table if not exists Employee(
             Id int primary key not null,
             fname text not null,
             lname text not null,
             age int not null,
             dep char(250),
             salary numeric        
             );''')
con.commit()

class Employee :
    List=[]
    employee_id=0
    def __init__(self,fname,Lname,Age,Dep,Salary):
        self.Fname=fname
        self.Lname = Lname
        self.Age = Age
        self.Dep = Dep
        self.Salary = Salary
        Employee.List.append(self.Fname+ ' '+self.Lname)
        Employee.employee_id += 1
        cur.execute(f"Insert into Employee(Id, fname,lname, age, dep, salary) values(%s,%s,%s,%s,%s,%s) ON CONFLICT do nothing",(self.employee_id, self.Fname, self.Lname, self.Age, self.Dep, self.Salary))
        print('Record inserted successfully')
        con.commit()

    def transfer(self,Dep):
        self.Dep=Dep
        update_db = f"UPDATE Employee SET dep = %s WHERE Id =%s"
        cur.execute(update_db,(self.Dep,Employee.employee_id))
        con.commit()
        print('transfered')

    def fire(self):
        del Employee.List[Employee.employee_id -1]
        cur.execute(f"delete from Employee where Id= {Employee.employee_id}")
        con.commit()
        print('fired')

    def show(self):
        cur.execute(f"select * from Employee where Id= {Employee.employee_id}")
        print(cur.fetchall())
        con.commit()


    def List_employees():
        cur.execute('select * from Employee')
        rows = cur.fetchall()
        for row in rows:
            print(row)
        con.commit()




class manager(Employee):
	def __init__(self,fname,Lname,Age,Dep,Salary,mgd_dep):
                Employee. __init__(self,fname,Lname,Age,Dep,Salary)
                self.mgd_dep=mgd_dep


	def show(self):
                cur.execute(f"select Id,fname,lname,age,dep from Employee where Id= {Employee.employee_id}")
                print(cur.fetchall(),'confidential')
                con.commit()


def Get_data():
        add_emp=input('For adding new employee data, Please type the word “add”')
        if (add_emp == 'add'):
                Emp_Mang=input('''If you're a manager type “m” / if you're employee type ‘e’''')
                print('Please insert data')
                FName=input('FName: ')
                LName=input('LName: ')
                Age=int( input('Age: '))
                Dep=input('Deparment: ')
                Salary=int(input('Salary: '))
                if Emp_Mang=="m":
                        mgd_dep=input('Managed_Depatment')
                        new_obj=manager(FName,LName,Age,Dep,Salary,mgd_dep)
                elif Emp_Mang=='e':
                        new_obj=Employee(FName,LName,Age,Dep,Salary)
                new_obj.show()
                quit = input('Do you wanna quit? if so type "q"')
                if (quit=='q'):
                        Employee.List_employees()
                else:
                        Get_data()


x=Employee("Adam",'Issac',23,"Development",2000)
x.show()
x.transfer("creation")
x.show()
Employee.List_employees()
x.fire()
x.show()
y=manager("Mark",'Riley',40,"hr",5000,'human resource')
y.show()
Employee.List_employees()
x.show()
Get_data()
con.close()


