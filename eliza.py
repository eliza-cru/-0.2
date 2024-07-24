# def sum(*args):       передает много аргументов 
#     print(args)
#     res = 0
#     for i in args:
#         res += i 
#     return res     

# print(sum(1, 2, 3, 4, 5, 6, 10, 54))


# def dict_print(**kwargs):       помещяется в переменную и потом передается 
#     print(kwargs)
#     for key, value in kwargs.items():
#         print(key, value)
# dict_print(a=1, b=2, c=3, e=4)

# def args_and_kwargs(*args, **kwargs):
#     print(args, kwargs)

# args_and_kwargs(1, 2, 3, 4, a=10, b=76)


# def decorate(function):                        
#     def wrapper(*args, **kwargs):
#         print('decorated function!')
#         return function(*args, **kwargs)
#     return wrapper

# @decorate
# def sum(a, b):
#     print(a + b)

# sum(20, 15)        


