

def parse_argument(argument:str):
    argument = argument.strip()
    if argument:
        if "=" in argument:
            return argument.split("=")[1]
    else:
        return argument