import random

h = {''}
def availible_positions(name_of_block, field):
    print(name_of_block)
    print(*field, sep='\n')

if __name__ == '__main__':
    h = [[0] * 10] * 20
    availible_positions('kara', h)