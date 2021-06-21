from ast_transformer.python.ast_generator import PyASTGenerator
from ast_transformer.python.transform_visitor import PyTransformVisitor
from bigo_calculator.bigo_calculator import TimeSeparater_main
from bigo_calculator.scope_separater_partialTC import TimeSeparater_partial
#from bigo_calculator.master_theorem import master_theorem

from master_theorem.master_theorem import master_theorem
import argparse
import os


def main():
    arg_parse = argparse.ArgumentParser()
    arg_parse.add_argument('filename', type=str)
    args = arg_parse.parse_args()
    source_file_name = args.filename
    if not os.path.isfile(source_file_name):
        raise FileNotFoundError

    origin_ast = PyASTGenerator().generate(source_file_name)

    #origin_ast = PyASTGenerator().generate('./examples/binarySearch_recursion.py')
    #origin_ast = PyASTGenerator().generate('./examples/fibo.py')
    #origin_ast = PyASTGenerator().generate('./examples/recursive_activity_selector.py')
    #origin_ast = PyASTGenerator().generate('./examples/bubblesort.py')
    #origin_ast = PyASTGenerator().generate('./examples/mergesort.py')

    bigo_ast = PyTransformVisitor().transform(origin_ast)
    RecTCC = TimeSeparater_main(bigo_ast)
    RecTCC.calc()
    #print(RecTCC.tc_list)
    
    bigo_ast = PyTransformVisitor().transform(origin_ast)
    restTCV = TimeSeparater_partial(bigo_ast)
    restTCV.calc()
    #print(restTCV.tc_list)

    master_theorem(RecTCC.tc_list, restTCV.tc_list)

if __name__ == '__main__' :
    main()
