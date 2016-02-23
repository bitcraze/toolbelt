import sys

__author__ = 'kristoffer'


class Ui:
    def user_input_yes_no(self, question):
        yes_no = input(question + " (y/n) ")
        if yes_no != "y":
            print("Aborted")
            sys.exit(-1)
