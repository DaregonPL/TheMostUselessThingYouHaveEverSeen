'''
Developed by VovLer

CalculatorApp.read()[0] values:
    -100 = Error: Invalid CalculatorApp.place value
    -1   = Back
    0    = Doesn't Match
    1-99 = ...
    100  = Help
    101  = Command executed propertly
    102  = Command not executed
'''


class Actions:  # FUCK THIS CLASS
    def sum(a: int, b: int):
        return a + b

    def sub(a: int, b: int):
        return a - b

    def mul(a: int, b: int):
        return a * b

    def div(a: int, b: int):
        return a / b

    def divmod(a: int, b: int):
        return a // b

    def exp(a: int, b: int):
        return a ** b


class CalculatorApp:
    intro = {
        'head': '\nCalculator App (function-based)\n',
        'prepared': 'CalculatorApp initialized propertly',
        'wrongcode': 'Wrong code returned from CalculatorApp.read',
        'N/P': 'Not programmed yet',
        '101': 'Command executed',
        '102': 'Command not executed'
    }  # System Messages (can be configured)
    programmed = {
        '+': Actions.sum,
        '-': Actions.sub,
        '*': Actions.mul,
        '/': Actions.div,
        '//': Actions.divmod,
        '**': Actions.exp
    }  # Programmed functions in Actions
    place = ''  # Var. to help self.read() to find our pos
    ans = ''  # Var. to share user's answer between methods
    stop = True  # Flag to stop self.mainloop()
    allow_float = True  # Flag to allow user enter float

    def help(self):
        print('======== Помощь для меню', self.place)
        if self.place == 'root':
            print('''
Допустимые вводимые типы данных: int, float, str(для команд и спец. действий)
Команды:
  quit - Выход из программы
  help - Меня помощи
Специальные Действия:

1. Выбор действия вручную:
  I.   Введите число типа int или float(только если включено allow_float)
  II.  Введите одно из действий, выведенных на экране
  III. Введите еще одно число в выражение, которое появится на экране
  IV.  Нажмите Enter после вывода ответа

  Пример:
  I  |10
     |Введите одно из действий: + - * / // **
  II |+
  III|10.0 + 5
  IV | = 15.0

2. Ввод математического выражения:
  I.  Введите верное математическое выражение
       *Математическим выражением является строка, каждый из символов
        которой можно найти в строке "+-/* ()0123456789".
  II. Нажмите Enter после вывода ответа

  Пример:
  I  |3 + 7
  II |3 + 7 = 10
  ''')
        else:
            print('Если вы смогли получить это сообщение,',
                  'используя только инструменты этой проги, то вы гигачад')
        input('Continue')

    def __init__(self, **introductions):
        for name, string in introductions.items():
            if name in self.intro:
                self.intro[name] = string
        self.out('prepared')  # Initialization finished propertly

    def start(self):
        self.stop = False
        self.mainloop()

    def mainloop(self):
        self.place = 'root'  # ------ ROOT
        self.out('head')
        print('''Напишите математическое выражение ниже или
  воспользуйтесь выбором действия (введите "help")
  Выход - "quit"''')
        code, ans = self.read()  # Reading answer
        # Replying to answer
        if code == -100:  # Error: Invalid Place
            pass
        elif code == -1:  # Stop mainloop
            self.stop = True
        elif code == 0:  # Continue
            print('Недопустимый ответ\n')
        elif code == 1:  # CalcByAction
            self.calcbyaction(ans)
        elif code == 2:  # Math
            corrcode, res = self.is_countable(ans)
            if corrcode:
                input(f'{ans.strip()} = {res}')
            else:
                print('Ошибка при выполнении математического выражения:')
                print(f'{res.__class__.__name__}: {res.args}', end='\n\n')
        elif code == 100:  # Help
            self.help()
        elif code == 101:
            self.out('101')
        elif code == 102:
            self.out('102')
        else:
            self.out('wrongcode')

        # End of Mainloop
        if not self.stop:
            self.mainloop()

    def calcbyaction(self, a):
        self.place = 'action'  # ------ Getting ACTION
        print('Введите одно из действий:', *self.programmed.keys())
        code, actn = self.read()
        if code == 1:  # >               Normal action
            self.place = 'get_b'  # > ------ Getting B
            code, b = self.read(f'{a} {actn} ')
            if code:  # Valid ans
                res = self.programmed[actn](a, b)
                input(f' = {res}')
            else:
                print('Недопустимый ответ')  # Get back to root
        elif code == 0:  # >     Wrong Action in input
            print('Недопустимый ответ')  # Get back to root
        elif code == -100:  # Error: Invalid Place
            pass
        else:
            self.out('wrongcode')

    def read(self, prompt='') -> (int, str | None):
        ans = input(prompt)
        place = self.place
        if self.command(ans, 0)[0]:
            return self.command(ans)
        elif place == 'root':
            # Testing for possible scenarios in root
            if self.is_float(ans):
                return 1, float(ans)  # Action Choose
            elif not [x for x in ans if not (x in '+-/* ()0123456789')]:
                return 2, ans  # Math Sentence
            elif ans.lower() == 'help':
                return 100, None  # Help
            elif ans.lower() == 'quit':
                return -1, None  # Exit mainloop
            else:
                return 0, None  # Doesn't Match

        elif place == 'action':
            # Testing for possible scenarios in "action"
            if ans in self.programmed:
                return 1, ans  # Found, key in CalculatorApp.programmed
            else:
                return 0, None  # Not Found, None

        elif place == 'get_b':
            if self.is_float(ans):
                return 1, float(ans)  # Valid (int)
            else:
                return 0, None  # Invalid (zdrastvuyte)

        else:
            print('Незапрограммированный сценарий (внутренняя ошибка)')
            print(f'PlaceNotProgrammedError: "{place}"')
            if not input('Продолжить работу программы? ' +
                         '(оставьте пустым для выхода)'):
                self.stop = True
            return -100, None  # Wrong place

    def command(self, ans, execute=1):
        if ans.startswith('run '):
            cmd = ans[4:].split(' ', 1)
            if cmd[0] == 'setplace':
                if len(cmd) == 2:
                    if execute:
                        self.place = cmd[1]
                        return 101, None
                    else:
                        return 1, None
                else:
                    print("Command 'setplace' takes 1 argument")
            elif cmd[0] == 'getplace':
                if len(cmd) == 1:
                    if execute:
                        print(self.place)
                        return 101, None
                    else:
                        return 1, None
                else:
                    print("Command 'getplace' doesn't take arguments")
            elif cmd[0] == 'return':
                if len(cmd) == 2:
                    if execute:
                        return eval(cmd[1])
                    else:
                        return 1, None
                else:
                    print("Command 'return' takes 1 argument")
            else:
                print(f"Command {cmd[0]} doesn't exist")
            if execute:
                return 102, None
            return 0, None
        else:
            return 0, None

    def out(self, key):
        print(self.intro[key], end='')

    def is_float(self, line):
        try:
            if self.allow_float:
                float(line)
            else:
                int(line)
            return True
        except ValueError:
            return False

    def is_countable(self, ans):
        try:
            eval(ans)
            return 1, eval(ans)
        except Exception as err:
            return 0, err


if __name__ == '__main__':
    app = CalculatorApp(prepared='''Welcome to Calculater
    made by VovLer''',
                        head='\n>>>Calculator App (function-based)\n')
    app.start()
