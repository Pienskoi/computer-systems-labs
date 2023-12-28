class Parser:
    def __init__(self, expression):
        self.expression = expression.replace(' ', '')
        self.pos = -1
        self.ch = None
        self.prev = None
        self.parenthesis_state = 0
        self.function_state = 0
        self.node = None

    def next_char(self):
        self.pos += 1
        self.prev = self.ch
        if self.pos < len(self.expression):
            self.ch = self.expression[self.pos]
        else:
            self.ch = None

    def parse(self):
        errors = []
        self.next_char()
        if self.ch in ['*', '/']:
            errors.append(f'Вираз не може починатися з операції \'{self.ch}\'')
        if self.ch == ')':
            errors.append(f'Вираз не може починатися із закритої дужки; {self.pos}')
        while self.pos < len(self.expression):
            if self.ch in ['+', '-', '*', '/']:
                if self.prev in ['+', '-', '*', '/']:
                    errors.append(f'Подвійна операція \'{self.ch}\': {self.pos}')
                if self.ch in ['*', '/']:
                    if self.prev == '(':
                        errors.append(f'Вираз у дужках не може починатися з операції \'{self.ch}\': {self.pos}')
                    if self.prev == ',':
                        errors.append(f'Аргумент функції не може починатися з операції \'{self.ch}\': {self.pos}')
                self.next_char()
            elif self.ch == '(':
                self.parenthesis_state += 1
                if self.prev is not None and self.prev.isnumeric():
                    errors.append(f'Відсутня операція між дужкою і числом: {self.pos}')
                if self.prev is not None and self.prev.isalpha():
                    self.function_state = self.parenthesis_state
                self.next_char()
            elif self.ch == ')':
                self.parenthesis_state -= 1
                if self.prev == '(':
                    errors.append(f'Пусті дужки: {self.pos}')
                if self.parenthesis_state < 0:
                    errors.append(f'Неправильний порядок дужок {self.pos}')
                if self.prev in ['+', '-', '*', '/']:
                    errors.append(f'Вираз у дужках не може закінчуватися будь-якою алгебраїчною операцією: {self.pos}')
                if self.prev == ',':
                    errors.append(f'Відсутній аргумент у функції: {self.pos}')
                if self.function_state == self.parenthesis_state:
                    self.function_state = 0
                self.next_char()
            elif self.ch.isnumeric():
                if self.prev is not None and self.prev.isalpha():
                    errors.append(f'Відсутня операція між числом і змінною/функцією: {self.pos}')
                if self.prev == ')':
                    errors.append(f'Відсутня операція між дужками і числом {self.pos}')
                dot = False
                while self.ch is not None and self.ch.isnumeric() or (self.ch == '.' and not dot):
                    if self.ch == '.':
                        dot = True
                    self.next_char()
            elif self.ch == '.':
                errors.append(f'Крапка має знаходитись між двома числами: {self.pos}')
                self.next_char()
            elif self.ch.isalpha():
                if self.prev is not None and self.prev.isnumeric():
                    errors.append(f'Відсутня операція між числом і змінною/функцією {self.pos}')
                if self.prev == ')':
                    errors.append(f'Відсутня операція між дужками і змінною/функцією {self.pos}')
                while self.ch is not None and self.ch.isalpha():
                    self.next_char()
            elif self.ch == ',':
                if self.prev == '(' or self.prev == ',':
                    errors.append(f'Відсутній аргумент у функції: {self.pos}')
                if self.prev in ['+', '-', '*', '/']:
                    errors.append(
                        f'Аргумент функції не може закінчуватися будь-якою алгебраїчною операцією: {self.pos}')
                if self.function_state == 0:
                    errors.append(f'Кома може використовуватися лише для переліку аргументів функції: {self.pos}')
                self.next_char()
            else:
                errors.append(f'Невідома операція: \'{self.ch}\': {self.pos}')
                self.next_char()
        if self.parenthesis_state > 0:
            errors.append('Нерівна кількість відкритих та закритих дужок')
        if self.prev in ['+', '-', '*', '/']:
            errors.append('Вираз не може закінчуватися будь-якою алгебраїчною операцією')
        return errors
