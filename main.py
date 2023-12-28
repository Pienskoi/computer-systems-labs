from parser import Parser
from tree import Tree, print_tree
from dynamic_pipeline import DynamicPipeline


if __name__ == '__main__':
    # expression = "/2.5-*(3-7)*() /2 + (7+b*)/(7+y-2) + e/dt*(f(bt+r)/(5*cos(bt)-it)) - fn(,5))(("
    # expression = "2.5-0*(3-7) /2 + (7+b)/(7+y-2) + e/dt*(f(bt+r)/(5*cos(bt)-it))"
    # expression = "/.1(2x-5x+7)-(-i)+ (j++)/0 - )(*f)(2, 7-x, )/q + send(-(2x+7)/A[j, i], 127.0.0.1 ) + )/"
    # expression = "0.1*(2*x-5*x+7)-(-i)+ (j+1)/0 - (f)(2, 7-x, )/q + send(-(2x+7)/A[j, i], 127.0.0.1 ) + )/"
    # expression = "0.1*(2*x-5*x+7)-(-i)+ (j+1)/0 - (f)-fun(2, 7-x, 5)/q + send(-(2*x+7)/A(j, i), 127 )"
    # expression = "a+b+c+d+f+g+1+2+3+4+5+6+7+8+9+10"
    # expression = "a/b/c/d/f/g/1/2"
    # expression = "a-b-c-d-f-g*h*1-0"
    # expression = "a*b*c*d*f*g*h*i"
    # expression = "(2*1+0)+(x+y)*0"
    # expression = "-(-5*x*((int*6)*exp(1+1))/t - 3.14*k/(2*x-5*x-1)*y - A(N*(i+1)+j))"
    # expression = "a-b*(k-t+(f-g)*(f*5.9-q)+(w-y*(m-1))/p)-(x-3)*(x+3)/(d+q-w)"
    # expression = "a*b*c/d + e*f*g/h + t*(a-q) - 5.0*i - 4*j + k + L + m*n*k*(p-1) + sin(pi*R)*log(q)/sin(3*pi/4 + x*pi/2)"
    expression = "a-b*(k-t+(f-g)*(f*5.9-q)+(w-y*(m-1))/p)-(x-3)*(x+3)/(d+q-w)"
    print(expression)
    errors = Parser(expression).parse()
    if not errors:
        print("Лексичний та синтаксичний аналіз виконано успішно")
        tree = Tree(expression).build()
        print_tree(tree)
        dynamic_pipeline = DynamicPipeline(4)
        dynamic_pipeline.immerse(tree)
        dynamic_pipeline.print()
        print("Оптимізований варіант:")
        optimized_tree = Tree(expression).build(optimize=True)
        print_tree(optimized_tree)
        dynamic_pipeline = DynamicPipeline(4)
        dynamic_pipeline.immerse(optimized_tree)
        dynamic_pipeline.print()
    else:
        print("Список помилок:")
        for error in errors:
            print(f"- {error}")
