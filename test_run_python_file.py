from functions.run_python_file import run_python_file

def test():
    result = run_python_file("calculator", "main.py")
    print("******")
    print(result)
    print("****")

    result = run_python_file("calculator", "main.py", ["3 + 5"])
    print("******")
    print(result)
    print("****")

    result = run_python_file("calculator", "tests.py")
    print("******")
    print(result)
    print("****")

    result = run_python_file("calculator", "../main.py")
    print("******")
    print(result)
    print("****")

    result = run_python_file("calculator", "nonexistent.py")
    print("******")
    print(result)
    print("****")

    result = run_python_file("calculator", "lorem.txt")
    print("******")
    print(result)
    print("****")


if __name__ == "__main__":
    test()