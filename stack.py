class Stack:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        if len(self.items) == 0:
            return 'True'
        else:
            return 'False'

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[len(self.items) - 1]

    def size(self):
        return len(self.items)

    def show_elements(self):
        return (self.items)


def balance_gaps(gaps):
    first_part = Stack()
    len_gaps = len(gaps)
    one_half = len(gaps) // 2
    second_part = gaps[one_half:len_gaps]
    if len_gaps % 2 == 0:
        for i in range(one_half):
            first_part.push(gaps[i])
        for i in range(len(second_part)):
            first_gap = first_part.peek()
            second_gap = second_part[i]
            if first_gap == '{' and second_gap == '}':
                first_part.pop()
                result = "Скобки сбалансированнны"
            elif first_gap == '(' and second_gap == ')':
                first_part.pop()
                result = "Скобки сбалансированнны"
            elif first_gap == '[' and second_gap == ']':
                first_part.pop()
                result = "Скобки сбалансированнны"
            elif first_part.isEmpty():
                result = "Скобки сбалансированнны"
                break
            else:
                result = "Скобки не сбалансированнны"
    else:
        result = "Скобки не сбалансированнны"
    return result


test_gaps = '(((([{}]))))'

print(balance_gaps(test_gaps))