from my_test import classes

print("Load m3")
@classes.register("A")
class A:
    c = 3
    d = 3


from my_test.modules import test
print("successful import of", test, test.A)
from my_test.modules.test import A
