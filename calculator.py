import ast
from ast_transformer.python.ast_generator import PyASTGenerator
from ast_transformer.python.transform_visitor import PyTransformVisitor
from bigo_calculator.scope_separater import ScopeSeparater
from masterT import recursion_time_complexity_calculator

from bigo_calculator.time_complexity_scope_separater import TimeSeparater


def main():
    origin_ast = PyASTGenerator().generate('./examples/FiboTest.py')
    origin_ast = PyASTGenerator().generate('./examples/ForTest.py')
    bigo_ast = PyTransformVisitor().transform(origin_ast)
    RCV = ScopeSeparater(bigo_ast)
    RCV.check()
    for funcName, funcParameter, funcCall in zip(RCV.func_decl_name_list, RCV.func_decl_parameter_list, RCV.scope_list_final):
        print("funcName: %s%s, funcCall: %s" %(funcName, funcParameter, funcCall))
        print(recursion_time_complexity_calculator(funcParameter, funcCall))
        

    TCV = TimeSeparater(bigo_ast)
    TCV.calc()
    time_ast = TCV.root
    for f in time_ast.children:
        print(f.time_complexity)

if __name__ == '__main__' :
    main()

