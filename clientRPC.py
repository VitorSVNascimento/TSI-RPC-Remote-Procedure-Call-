from rpc import client
from tkinter import *

client_rpc = client.Client('127.0.0.1',8888)

print(client_rpc.sum((1,1)))
print('ola')
def handle_result_two_inputs(result, input1, input2, input_window):
    print("Result:", result)
    if 'result_label' in input_window.__dict__:
        print('entrou')
        result_label = input_window.result_label
        result_label.config(text=f"Result: {result}")
    else:
        print('Else')
        result_label = Label(input_window, text=f"Result: {result}")
        result_label.pack()
    print('Saiu')
    input_window.result_label = result_label
    print('Aqui')
    input1.delete(0, END)  # Clear the first input field
    input2.delete(0, END)  # Clear the second input field

def sum_function():
    input_window = Toplevel(window)
    input_window.title('Input')
    input_window.geometry("250x150")
    Label(input_window, text="Enter first number:").pack()
    first_number = Entry(input_window)
    first_number.pack()
    Label(input_window, text="Enter second number:").pack()
    second_number = Entry(input_window)
    second_number.pack()
    Button(input_window, text="Submit",command=lambda: sum_submit(first_number, second_number, input_window)).pack()
    print('Entrou')

def sum_submit(first_number, second_number, input_window):
    result = client_rpc.sum((float(first_number.get()), float(second_number.get())))
    print('result')
    handle_result_two_inputs(result, first_number, second_number, input_window)


def subtraction_function():
    pass

def division_function():
    pass

def multiplication_function():
    pass

def is_prime_function():
    pass

def last_news_function():
    pass

def prime_in_range_function():
    pass

def cpf_validate_function():    
    pass

window = Tk()
window.title('RPC Client')
window.geometry("215x164+10+20")

sum_button = Button(window, text="Sum",
                    command=sum_function, width=14, height=2)
subtraction_button = Button(
    window, text="Subtraction", command=subtraction_function, width=14, height=2)
division_button = Button(window, text="Division",
                         command=division_function, width=14, height=2)
multiplication_button = Button(
    window, text="Multiplication", command=multiplication_function, width=14, height=2)
is_prime_button = Button(window, text="Is Prime",
                         command=is_prime_function, width=14, height=2)
last_news_button = Button(window, text="Last News",
                          command=last_news_function, width=14, height=2)
prime_in_range_button = Button(
    window, text="Prime In Range", command=prime_in_range_function, width=14, height=2)
cpf_validate_button = Button(
    window, text="CPF Validate", command=cpf_validate_function, width=14, height=2)

sum_button.grid(row=0, column=0)
subtraction_button.grid(row=0, column=1)
division_button.grid(row=1, column=0)
multiplication_button.grid(row=1, column=1)
is_prime_button.grid(row=2, column=0)
last_news_button.grid(row=2, column=1)
prime_in_range_button.grid(row=3, column=0)
cpf_validate_button.grid(row=3, column=1)

window.mainloop()