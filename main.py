from pyswip import Prolog, call

class MyClass:
    def __init__(self):
        self.prolog = Prolog()
        self.fileName ='test.pl'

    def consult(self):
        self.prolog.consult(self.fileName)
        print(self.fileName + " loaded successfully!")

    def handlingReceived(self):
        print("Handling received...")
        self.prolog.query("handling_received.")

    def received(self):
        print("Received:")
        received = list(self.prolog.query("received(X)"))
        print(received)

    def listAll(self):
        listing = self.prolog.query("listAll.")
        print("Listing:")
        print(list(listing))

def main():
    myClass = MyClass()
    myClass.consult()
    myClass.handlingReceived()
    myClass.received()


if __name__ == "__main__":
    main()