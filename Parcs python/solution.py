from Pyro4 import expose
import random

class Solver:
    def __init__(self, workers=None, input_file_name=None, output_file_name=None):
        self.input_file_name = input_file_name
        self.output_file_name = output_file_name
        self.workers = workers
        print("Inited")

    def solve(self):
        print("Job Started")
        k = len(self.workers)
        print("Workers %d" % k)

        # input
        N1,x1,x2,y1,y2 = self.read_input()

        # map
        mapped = []
        for i in xrange(0, k):
            print("map %d" % i)
            mapped.append(self.workers[i].mymap(N1//k +((N1%k)>i), x1,x2,y1,y2))

        # reduce
        num = self.myreduce(mapped)

        integral = 1.0*num*(x2-x1)*(y2-y1)/N1

        # output
        self.write_output(integral)

        print("Job Finished")

    @staticmethod
    @expose
    def mymap(N1, x1,x2,y1,y2):
        num = 0
        for _ in xrange(N1):
            x = random.uniform(x1, x2)
            y = random.uniform(y1, y2)
            fun = foo(x)
            if 0 <= y <= fun:
                num += 1
            elif 0 >= y >= fun:
                num -= 1
        return num

    @staticmethod
    @expose
    def myreduce(mapped):
        return sum(item.value for item in mapped)

    def read_input(self):
        with open(self.input_file_name, 'r') as f:
            lines = f.readlines()
            N = int(lines[0].strip())
            x1, x2, y1, y2 = map(float, lines[1].strip().split())
            return N, x1, x2, y1, y2

    def write_output(self, output):
        with open(self.output_file_name, 'w') as f:
            f.writelines(str(output))
        print("output done")
def foo(x):
    return 1 / (x ** 5 + 1)
