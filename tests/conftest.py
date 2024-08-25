simple_working_code = """
def main(input):
    print(input)
    return input * 2
"""

no_main_func_gateway_code1 = """
def hello(input):
    pass
"""

no_main_func_gateway_code2 = """
print("10")
"""

main_not_callable = """
main = 5
"""

code_runtime_error = """
def main(input):
    return 5 / 0
"""

code_syntax_error1 = """
def main(input
"""

code_syntax_error2 = """
deff main(input):
    pass
"""

code_syntax_error3 = """
deff main(input):
return 5
"""
