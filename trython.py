import sys 
import os 
import re 
import subprocess

global active
active = []

global active_2 
active_2 = []

global active_3
active_3 = []

global import_list
import_list = []

class thread_simpifier:
    def seqq():
        
        mini_lib = '''
def seqq():
    try:
        for f in seq:
            x = threading.Thread(target=f, args=seq[f])
            x.start()
    except:
        pass
''' 
        return mini_lib
class data_marker:
    
    def function_storage(def_str:str):
# check if the input is valid        
        if type(def_str).__name__ != 'str':
            return 'syntax error, str is expected' 
        else:
            pass

        normalized_text = def_str.split('\n')

        func_list = []
# here we spot the functions using the keyword 'def'
        for i in normalized_text:
            if re.findall('def',i):
                func = i.split(' ')                
                for j in func :
                    if re.findall('def',j):
# once we have found the function we can extract the name of it and storage it 
                        indx = func.index(j)
                        func_name = func[indx+1].split('(')[0]
                        func_list.append(func_name)
        return func_list
    
# function :: x , y -> z
    def marker_parse(marker_str:str):
# check if the input is valid
        if type(marker_str).__name__ != 'str':
            return 'syntax error, str is expected' 
        else:
            pass 
        splitted = marker_str.split("::")
# first half , we get the name of the function to be typed 
        name = splitted[0].replace('|>','')
# second half , we get the parameter's types 
        parameters = splitted[1]
    # here we get the input and output types 
    # using the arrow as the splitter 
        io = parameters.split("->")

        output_type = io[1].split(',')
    # here we get all inputs , recursively
        input_type = io[0].split(',')
    # we then make a dict out of the information 
        type_list = {
            name:{
            'input':input_type,
            'output':output_type
            }
        }
        return type_list

class first_layer_parser:

    def semantic_checking(max_text:str):
        if type(max_text).__name__ != 'str':
            return 'syntax error, str is expected' 
        else:
            pass 
# here we check the linar structure 
# and start doing the filtering and the semantic analysis 

        function_relation = {
            'def':[
            ],
            'mark':[
            ]
        }

        type_list = {
            'mark':[ 
            ],
            'arg':{
            }
        }

# here we check if all function's types for input are well declared
        linear_text = max_text.split('\n')
        for sentence in linear_text:
            if re.findall('def',sentence):
                f = data_marker.function_storage(sentence)
                function_relation['def'].append(f[0])

            elif re.findall('::',sentence):
                f = data_marker.marker_parse(sentence)
                ff = list(f.keys())[0].replace(' ','')
                function_relation['mark'].append(ff)
                type_list['mark'].append(f)
                type_list['arg'][ff] = []

            elif re.findall('= do',sentence):
                b = 0 
                barrier = linear_text.index(sentence)
                counter = barrier 
                while counter < len(linear_text):
                    if re.findall('seq = {',linear_text[counter]):
                        import_list.append('import threading')
                        active_2.append('\n'+'global seq')
                        #active.append('\n'+str(linear_text[counter]))
                        active_2.append('\n'+str(thread_simpifier.seqq()))
                        if len(active_3) != 0:
                            pass 
                        else:
                            active_3.append('\n'+'    seqq()')
                    else:
                        pass 
                    if re.findall('= do',linear_text[counter]):
                        x = """\nif __name__ == '__main__': """
                        active.append(x)
                    else:
                        active.append('\n'+str(linear_text[counter]))
                    counter+=1
            elif re.findall('import',sentence):
                import_list.append('\n'+str(sentence))
                if import_list.index('\n'+str(sentence)) == 0:
                    import_list[0].replace('\n','')
                elif import_list.index('\n'+str(sentence)) == len(import_list)-1:
                    import_list[len(import_list)-1].replace('\n','')
                else:
                    pass

            elif re.findall('end',sentence):
                pass 
            else:
                try:
                    lk = list(type_list['arg'].keys())[len(list(type_list['arg'].keys()))-1]
                    if re.findall('return',sentence):
                        type_list['arg'][lk].append("\n"+sentence)
                    else:
                        type_list['arg'][lk].append("\n"+sentence)
                        if re.findall('return',type_list['arg'][lk][type_list['arg'][lk].index("\n"+sentence)-1])  :
                            type_list['arg'][lk].remove("\n"+sentence)
                except:
                    pass 
                pass
        if function_relation['mark'] != function_relation['def']:
            return 'semantic error'
        else:
            return type_list

class transpiler:

    def write_text(max_str:str,data_type:dict):
# check if the input is a string
        if type(data_type).__name__ != 'dict' and type(max_str).__name__ != 'str':
            return 'syntax error, str is expected' 
        else:
            pass 
        
        checker_list = {}

        counter = 0 
        while counter < len(data_type['mark']):
            info_esp = data_type['mark'][counter]
            name = list(info_esp.keys())[0]
            argument = data_type['arg'][name.replace(' ','')]
            for j in argument:
                if re.findall('return',j):
                    j_new = j.replace('return','r =')
                    argument[argument.index(j)] = j_new 
                                
            checker_skeleton = '''
    type_list  = {info_0}
             
    t = {l}

    function_name = inspect.currentframe().f_code.co_name

    possibles = globals().copy()
    possibles.update(locals())
    func_itself = possibles.get(str(function_name))

    i = inspect.getfullargspec(func_itself).args
    for v in i:
        t[eval(v)] = type_list['input'][i.index(v)]     
    
    for parameter in t :
        if type(parameter).__name__ not in t[parameter].split() :
            print('type error')
            return "type error on value {x} , expecting : {y} but recieved: {z}".format(
                x = parameter ,
                y = t[parameter] ,
                z = type(parameter).__name__
                )

    {argument}
    if type(r).__name__ not in type_list['output'][0].split() :
        return "type error on output {x} , expecting : {y} but recieved: {z}".format(
                    x = r ,
                    y = type_list['output'][0] ,
                    z = type(r).__name__
                )
    else:
        return r 
        '''.format(
                info_0=info_esp[name],
                x='{x}',
                y='{y}',
                z='{z}',
                argument=" ".join(argument),
                l="{}",
                name=name 
                )
            checker_list[name] = checker_skeleton
            counter+=1

        function_normalizer = max_str.split('|>')    
        
        py_func = []

        for j in function_normalizer:
            if re.findall('->',j) and re.findall('|>',j):
                nt = function_normalizer[function_normalizer.index(j)]+':'
                sub_nt = nt.split(" ")
                sub_nt_2 = [sub_nt[len(sub_nt)-2],sub_nt[len(sub_nt)-1]]
                nt = " ".join(sub_nt_2)
                dt = nt+checker_list[sub_nt[0]+' ']
                py_func.append(dt)
 
        imp = '''import sys\nimport re\nimport inspect\nimport configparser\n'''+''.join(active_2)+' '.join(import_list)    
        return imp+" ".join(py_func)+' '.join(active)+' '.join(active_3)

    def generate_file(title,plain_text):
        if type(title).__name__ != 'str':
            return 'syntax error, str is expected' 
        else:
            pass 
        try:
            title+='.py'
            text_file = open(title,'x')
            print('generating...')
            python_file = open(title,'w')
            python_file.write(plain_text)
            print('writing : {f}....'.format(f=title))
            python_file.close()
            return 'compiled...'
        except FileExistsError:
            print('warnning : checking an existing file...')
            python_file = open(title, 'w').close()
            print('writing : {f}....'.format(f=title))
            python_file = open(title,'w')
            python_file.write(plain_text)
            python_file.close()
            return 'compiled!'    

class command:
    def version():
        print('version 1.0')


commands = {
        '--exit':sys.exit,
        '--version':command.version
    }

if __name__ == '__main__':
    print('::Trython::')
    while True:
        active = []
        import_list = []
        a = str(input('|>  '))
        
        if a in commands:
            commands[a]()
        else: 
            try:
                f = open(a,'r')
                x = f.read()
                f = first_layer_parser.semantic_checking(x)
                t = transpiler.write_text(x,f)
                asp = a.split('.txt')
                c = transpiler.generate_file(asp[0],t)
                print(c)
                try:
                    if c == 'compiled!':
                        print('------output------')
                        subprocess.call(['py',asp[0]+'.py'])
                    else:
                        pass 
                except:
                    print('python is not in your path..\ncheck the source file at:{x}'.format(x=asp[0]+'.py'))
            except:
                print('compiling error, check again the syntax and the documentation')