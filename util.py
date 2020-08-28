import time


# import os


def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            print('%r  %2.2f ms' % \
                  (method.__name__, (te - ts) * 1000))
        return result

    return timed


def safe(x, fn):
    try:
        return fn(x)
    except:
        pass


def spy(x):
    # from toolz import interpose
    # data_pipe = interpose(spy, [])
    print(x)
    return x

# @typechecked
# def load_size_from_dir(dir: str, size: int) -> List[str]:
#     iterator = os.listdir(dir)
#     filenames = [dir + "/" + filename for filename in iterator[:size]]
#     raw_texts = []
#     for fn in filenames:
#         with open(fn, "r") as file:
#             raw_text = file.read()
#             raw_texts.append(raw_text)
#     return raw_texts

# @overload
# @dispatch

# pytest fixtures
#

# class TextClean:
#   @staticmethod

# for idx, content in enumerate(contents):
#     print(idx, "---")
#     with open("stat_wiki/" + str(idx) + ".txt", "w+") as file:
#         file.write(content.encode('unicode-escape').decode('utf-8'))
