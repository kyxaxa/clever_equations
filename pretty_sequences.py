# -*- coding: utf-8 -*-
import random
import itertools


def factorial(n):
    """
        returning factorial
    """
    if n == 0:
        return 1
    return n * factorial(n-1)


class Pretty_sequence():
    '''
        создаем красивые последовательности
    '''

    def __init__(
            self,
            size=10,  # размер последовательности
            ):
        self.size = size

    def create_sequence_cycle(self, size, template):
        '''
        create cycle sequence
        '''
        seq = []
        one_cycle = itertools.cycle(template)
        for i in range(size):
            #print ('    i%s/%s ' % (i, self.cnt_equations), end='')
            item = next(one_cycle)
            #print ('item %s' % item)
            seq.append(item)
        return seq

    def create_sequence(
            self,
            size=None,

            #mode='factorial',  # use factorial

            #mode='any',  # return None values

            mode='cycle',
            template=[1, 2, 3, 4, 5],

            reverse=0,
            ):
        '''
            main function for sequence creation
            it has high cyclomatic
        '''

        if size is None:
            size = self.size

        seq = []

        if mode == 'cycle':
            seq = self.create_sequence_cycle(size, template)

        elif mode == 'factorial':
            seq = [factorial(i) for i in range(size)]

        elif mode == 'any':
            seq = [None] * size

        # high Mccabe complexity? But it is really simple...
        #       https://stackoverflow.com/questions/52850003/avoid-multiple-if-to-ensure-mccabe-complexity
        elif mode == 1:
            pass

        elif mode == 2:
            pass

        else:
            #https://realpython.com/python-exceptions/
            raise Exception('unknown mode "%s"' % mode)

        if reverse:
            seq.reverse()

        return seq


###############################################main code
if __name__ == '__main__':
    print('__main__ pretty_sequences')
    t = 0
    t = 1
    if t:
        val = 4
        print('val %s, factorial %s' % (val, factorial(val)))

    t = 1
    t = 0
    if t:
        size = 20
        S = Pretty_sequence(20)

        mode = 'cycle'
        mode = 'unknown'
        template = [1, 2, 3, 4, 5]
        template = [1, 2]
        reverse = 1
        seq = S.create_sequence(
                mode=mode,
                reverse=reverse,
                template=template,
        )
        print('seq: %s' % seq)
