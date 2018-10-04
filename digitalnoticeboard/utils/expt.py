class Account:
    closed = False

    def deposit(self, amount):
        self.balance = self.balance + amount

    def withdraw(self, amount):
        self.balance = self.balance - amount

    def close(self):
        self.closed = True

    def transfer(self, account, amount):
        self.balance = self.balance - amount
        account.balance = account.balance + amount

    def display(self):
        print(self.balance)
        return self.balance

    def __init__(self):
        self.name = None
        self.acc_no = None
        self.phno = None
        self.bankname = None
        self.acc_type = None
        self.balance = None

    def __init__(self, **kwargs):
        self.name = kwargs['name']
        self.acc_no = kwargs['acc_no']
        self.phno = kwargs['phno']
        self.bankname = kwargs['bankname']
        self.acc_type = kwargs['acc_type']
        self.balance = kwargs['balance']


suraj = Account(name="Suraj", acc_no="420", phno="123", bankname="BOI", acc_type="Savings", balance=100)
k = Account(name="K", acc_no="421", phno="1234", bankname="SBI", acc_type="Savings", balance=10)
# suraj.withdraw(100000)
suraj.display()
suraj.transfer(k, 20)
suraj.display()
k.display()
