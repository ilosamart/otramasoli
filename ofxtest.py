import os
from ofxtools.Parser import OFXTree

file = open(file='/home/fabio/Downloads/Extrato_20180520.ofx', mode='r')

parser = OFXTree()

parser.parse('/home/fabio/Downloads/Extrato_20180520.ofx')

ofx = parser.convert()

for transaction in ofx.statements[0].transactions:
    print(transaction)
