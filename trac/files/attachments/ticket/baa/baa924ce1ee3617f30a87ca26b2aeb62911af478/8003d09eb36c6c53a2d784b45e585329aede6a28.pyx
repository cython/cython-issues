import sys

class FUSEError:
    pass

def run():
    try:
        raise RuntimeError("foo")
    except FUSEError as e:
        print("FUSEError")
    except BaseException as e:
        print("BaseException")
