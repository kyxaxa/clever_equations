# -*- coding: utf-8 -*-
import random
import itertools
from pretty_sequences import *


class Create_Equations:
    def __init__(
                self,
                student='dasha',
                cnt_equations=20,
                numbers_template=[2, 3],

                number_low=0,
                number_high=10,

                answers_mode='cycle',
                answers_template=[0, 1, 2, 3, 4, 5],

                numbers_must_be=None,
                ):

        cnt_equations = int(cnt_equations)
        numbers_template = [int(_) for _ in numbers_template]

        self.cnt_equations = cnt_equations  # how many ecamples do I need?
        self.student = student
        #numbers_template = [2, 3, 4, 5, 6]
        #numbers_template = [2]
        #numbers_template = [2, 3]

        self.numbers_template = numbers_template

        self.answers_mode = answers_mode
        self.answers_template = answers_template

        if self.student == 'dasha':
            number_low = 0
            number_high = 10

        elif self.student == 'dasha+-':
            number_low = -10
            number_high = 10

        else:
            m = 'unknown student "%s"' % student
            print(m)
            #os._exit(m)

        number_low = int(number_low)
        number_high = int(number_high)

        self.number_low = number_low
        self.number_high = number_high

        self.numbers_must_be = numbers_must_be

    def create_one_equation(
            self,
            cnt_numbers=5,
            number_low=None,    # дефолтный
            number_high=None,
            answer_exact=None,  # точный ответ неважен
            option_no_answer_exact='return_last',       # если нет ответа - что делаем?
            limit_answer_search=1000,   # сколько раз пытаемся искать ответ?
            numbers_must_be=None,
            ):
        '''создаем пример из cnt_nubers чисел
        причем answer_exact если установлен, то ответ должен совпасть
        '''
        if number_low is None:
            number_low = self.number_low

        if number_high is None:
            number_high = self.number_high

        if numbers_must_be is None:
            numbers_must_be = self.numbers_must_be

        #пробуем пока не получим уравнение с нужным ответом
        equation = None
        hashes = set()  # we want only unique equations
        for i in range(limit_answer_search):
            numbers = []
            for i in range(cnt_numbers):
                number = random.randint(number_low, number_high)
                numbers.append(number)

            ##### check if exists at least one number in numbers from numbers_must_be
            if numbers_must_be is not None:
                number_exists = any(i in numbers_must_be for i in numbers)
                #print(numbers, number_exists)
                if not number_exists:
                    continue

            ##### check if we have already such equation
            hash = str(numbers)
            if hash in hashes:
                continue
            hashes.add(hash)

            ##### calculate answer and add it
            answer = sum(numbers)

            equation_last = {
                    'numbers': numbers,
                    'answer': answer,
                    'cnt_numbers': cnt_numbers,
                    'is_answer_exact': 0,       # точный ответ?
                    'hash': hash,
                }

            #есть совпадение по ответу, или ответ неважен
            if answer_exact is None or answer_exact == answer:
                equation = equation_last
                equation['is_answer_exact'] = 1
                break

            else:
                continue

        if equation is None:
            if option_no_answer_exact == 'return_last':
                equation = equation_last
            else:
                print('bad answer')
                os._exit(0)

                #wait_for_ok()
        return equation

    def convert_numbers_to_str(self, numbers=[]):
        #strings = map(str, numbers)
        strings = []
        i = 0
        for number in numbers:
            i += 1
            if number == 0:
                clas = 'plus'
                znak = '+'
            elif number > 0:
                clas = 'plus'
                znak = '+'
            else:
                clas = 'minus'
                znak = r''

            if i == 1 and znak == '+':
                znak = ''
            number_znak = '%s%s' % (znak, number)
            s = "<span class='number %s'>%s</span>" % (clas, number_znak)
            strings.append(s)
        s = " ".join(strings)
        return s

    def convert_equations_to_html_table(self, equations=[]):
        tpl = '''<tr class="{class_pair}">
        <td><span  class="position">{num}</span></td>
        <td class='image_{cnt_numbers}'><span>&nbsp;&nbsp;&nbsp;&nbsp;</span></td>
        <td>{equation_str} = </td>
        <td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</td>
        <td class="answer">{answer}</td></tr>
        '''

        lines = []
        num_equation = 0
        for eq in equations:
            num_equation += 1
            if num_equation % 2 == 0:
                class_pair = 'row_pair'
            else:
                class_pair = 'row_unpair'
            eq['class_pair'] = class_pair
            eq['num'] = num_equation
            equation_str = self.convert_numbers_to_str(eq['numbers'])
            eq['equation_str'] = equation_str
            line = tpl.format(**eq)
            lines.append(line)
        equations_table = '\n'.join(lines)

        cnt_equations = len(equations)

        errors1 = '''Ошибок: _____ /{cnt_equations}      Оценка: _______ '''.format(**locals())
        errors2 = errors1.replace('Ошибок', 'Ошибок2')

        html = '''
        <h1>Для: ___________   Дата: ______</h1>
            <table>
                {equations_table}
            </table>
        <h1>{errors1}</h1>
        <h1>{errors2}</h1>
        '''.format(**locals())
        return html

    def save_equations(self, html, want_display=0):
        f_to = 'temp/%s.html' % self.student
        f_to = 'temp/equations.html'
        with open(f_to, 'w+') as out:
            out.write(html)
        print('wrote to {f_to}'.format(**locals()))

        if want_display:
            display(HTML(html))

    def create_plan_for_answers(self):
        S = Pretty_sequence(size=self.cnt_equations)
        plan = S.create_sequence(mode=self.answers_mode, template=self.answers_template)
        return plan

    def create_plan_for_cnt_numbers(self):

        #print('plan: %s' % self.numbers_template)
        S = Pretty_sequence(size=self.cnt_equations)
        plan = S.create_sequence(mode='cycle', template=self.numbers_template)
        return plan

        #plan = []
        #one_cycle = itertools.cycle(self.numbers_template)
        #for i in range(self.cnt_equations):
        #    #print('    i%s/%s ' % (i, self.cnt_equations), end='')
        #    item = next(one_cycle)
        #    #print('item %s' % item)
        #    plan.append(item)
        #return plan

    def html_generate_table_with_equations(self):
        equations = []
        plan_numbers = self.create_plan_for_cnt_numbers()
        answers = self.create_plan_for_answers()
        i = 0
        for cnt_numbers in plan_numbers:
                answer = answers[i]
                equation = self.create_one_equation(cnt_numbers=cnt_numbers, number_low=self.number_low, number_high=self.number_high, answer_exact=answer)
                equations.append(equation)
                i += 1
        table = self.convert_equations_to_html_table(equations)
        return table

    def create_page_with_equations(
            self,
            want_save=0,
            ):

        table1 = self.html_generate_table_with_equations()
        table2 = self.html_generate_table_with_equations()

        style = """
        html0{
          background: url("../data/images/bg_jungle1.gif") no-repeat center center fixed;
          -webkit-background-size: cover;
          -moz-background-size: cover;
          -o-background-size: cover;
          background-size: cover;
        }

        html0{
          background: url("../data/images/bg_jungle1.gif") repeat;
        }

        body{
                padding: 5px;
        }

        table{
        background-color: white;
        }
        td{
            //border:1px solid gray;
			border-bottom: 1px solid gray;
			padding: 8px;
			text-align: right;
        }

        td.answer{
            border-left: 1px dotted gray;
            text-align: center;
        }

        h1{
        font-size:20px;
        }

		.number{
			border: 1px solid gray;
			padding: 5px;
            border-radius:5px;
		}

		.plus{
            background-color: white;

		}

		.minus{
    		background-color: #80808042;

		}

        .position{
            border:1px solid gray;
            border-radius: 10px;
            text-align:center;
            padding:5px;
        }

        tr.row_pair{
            background-color: #8080800d;
        }

        .image_6{
            background-image: url("../data/images/monkey1.png");
            background-repeat: no-repeat;
            background-size: 100% 100%;
        }
        .image_2{
            background-image: url("../data/images/bee3.png");
            background-repeat: no-repeat;
            background-size: 100% 100%;
        }
"""

        html = """<html><head>
        <style>
            {style}
        </style>
        </head>
        <body>

        <table>
        <tr>
            <td>{table1}</td>
            <td>{table2}</td>
            </tr>
        </table>
        </body>
        </html>""".format(**locals())

        if want_save:
            self.save_equations(html)
        return html


###############################################main code
if __name__ == '__main__':
    print('__main__')
    t = 0
    t = 1
    if t:
        student = 'dasha'
        student = 'dasha+-'

        student = 'unknown_student'
        cnt_equations = 20
        numbers_template = [2, 3]

        number_low = 0
        number_low = -10
        number_high = 10

        numbers_must_be = None
        numbers_must_be = [6, -6]

        E = Create_Equations(
                student=student,
                cnt_equations=cnt_equations,
                numbers_template=numbers_template,
                number_low=number_low,
                number_high=number_high,
                numbers_must_be=numbers_must_be,
                )

        ### тест - создание одного уравнения
        t = 0
        t = 1
        if t:
                cnt_numbers = 2
                equation = E.create_one_equation(cnt_numbers=cnt_numbers, answer_exact=0)
                print(equation)


        #тест - создание страницы с вопросами-ответами
        t = 0
        t = 1
        if t:
            E.create_page_with_equations()

#todo:
        """
        +вывести на 1 страничку 2 списка задач?
            Хотя это неважно, нужно ж зверей еще рисовать, место искать
                https://www.google.com/imgres?imgurl=https%3A%2F%2Fstatic.thenounproject.com%2Fpng%2F352929-200.png&imgrefurl=https%3A%2F%2Fthenounproject.com%2Fterm%2Fmonkey%2F&docid=vkKFX4x_t9QBtM&tbnid=egvqf-Ep2jaqaM%3A&vet=12ahUKEwj_sr-C4r7fAhWLy4UKHY3mANA4ZBAzKBAwEHoECAEQEQ..i&w=200&h=200&bih=668&biw=1364&q=image%20monkey&ved=2ahUKEwj_sr-C4r7fAhWLy4UKHY3mANA4ZBAzKBAwEHoECAEQEQ&iact=mrc&uact=8
                https://www.google.com/imgres?imgurl=https%3A%2F%2Fd184qs4ly5p9jl.cloudfront.net%2Fanimals%2Fdce2b5e8d0.svg&imgrefurl=https%3A%2F%2Fgreenscreenanimals.com%2Ffootage%2Fclips%2F64%2FSpider-Monkey&docid=OLNgDvystWUQdM&tbnid=FPmCUYRcWwdI8M%3A&vet=12ahUKEwj_sr-C4r7fAhWLy4UKHY3mANA4ZBAzKAYwBnoECAEQBw..i&w=800&h=800&bih=668&biw=1364&q=image%20monkey&ved=2ahUKEwj_sr-C4r7fAhWLy4UKHY3mANA4ZBAzKAYwBnoECAEQBw&iact=mrc&uact=8

            * выбор картинок:
                https://www.google.com/search?q=image+bee&tbs=ic:trans,itp:lineart&tbm=isch&source=lnt&sa=X&ved=0ahUKEwjiyuDt5L7fAhVFhRoKHWP_A5kQpwUIIA&biw=1364&bih=619&dpr=1#imgrc=_

            * выбор фона:
                c фоном было некрасиво
        """
