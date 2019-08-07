# import re

"""SYNTAX = {1: ("{%py", "%}"), 2: ("{!%py", "!%}"), 3: ("-#py", "#-"), 4: ("-!#py", "#!-"), 5: ("-%py", "%-"),
          6: ("!@py", "@!"), 7: ("~{py", "}~"), 8: ("{@py", "@}")}""" # Have to be from groups of 2 or 3 with the char between the two
SYNTAX = {1: ("(%py", "%)")}
ADD_FILE = {1: ("(!py", "!)")}
IFS = {1: {"if": ("{%pyif", "%}"), "elif": ("{%pyelif", "%}"), "else": "{%pyelse%}", "endif": "{%pyendif%}"}}

# Should be written as:     1:{%pyif variable %}


class DataConnection:
    """
    A python library by: Sean.T

    This library is built for the purpose of easy edit method of any file.
    It is copying the data into a temporary variable and then changes the wanted data to the given values by the user.
    Also, it is set by default to recognize only text formatted files - It can be changed by enabling 'binary_encoded'.
    * Warning: binary_encoded useful only for bytes that can be recognized as a text format

    Syntax - The file to edit ("number:" is separating the different types of formats): Not available at this point!
    You can specify the wanted syntax by their numbers - It is set to 1 by default.

    Writing in file format:
    Variables -> (%py var %)
    If statements ->
    -if-    id:{%pyif var %}
    -elif-  id:{%pyelif var %}
    -else-  id:{%pyelse%}
    -endif- id:{%endif%}
    * The id is the identifier of the specified if statement!
    * If the if, elif, else, endif are from the same statement they should have the same id!
    * -if- and -endif- statements has to exist in the code (if you have an if statement) in order for the function to work properly!
    """
    # The wanted syntax to use (formats: !1! 1  !2! 1,3,4  !3! 2-6)

    def __init__(self, edit_method: bool = False, binary_encoded: bool = False):
        """
        Initializing the class for future use.
        :param edit_method: The wanted method to edit the file.
        :param binary_encoded: If there is need to decode the file.
        :type edit_method: bool
        :type binary_encoded: bool
        """
        self.__syntax = [1]
        self.__max_c = 1
        self.__edit_method = edit_method
        self.binary_encoded = binary_encoded
    """
    def set_syntax(self, syntax: str):
        "The wanted syntax to use (formats: !1! 1  !2! 1,3,4  !3! 2-6) - Can't be mixed!"
        if len(syntax) == 1:
            if not syntax.isdigit():
                raise Exception("Invalid syntax Input!")
            self.__syntax = [int(syntax)]
        elif len(syntax.split(",")) > 1:
            list_syntax = syntax.split(",")
            for x in list_syntax:
                if not x.isdigit():
                    raise Exception("Invalid syntax input!")
            self.__syntax = list(map(int, list_syntax))
        elif len(syntax.split("-")) > 1:
            list_syntax = syntax.split("-")
            if len(list_syntax) > 2:
                raise Exception("Invalid syntax input!")
            for x in list_syntax:
                if not x.isdigit():
                    raise Exception("Invalid syntax input!")
            self.__syntax = list(range(int(list_syntax[0]), int(list_syntax[1]) + 1))
    """

    def change_max_c(self, num: int):
        """
        The function sets the max amount of digits for the id of the -for- loops.\
        NOTE! If you have for example: id of 2 digits and a number of one digit please write in the format of -> 05.
        :param num: The amount of digits
        :type num: int
        :return: Nothing
        """
        if 1 <= num <= 10:
            self.__max_c = num
        else:
            raise Exception("Invalid amount of digits for the max -for- number!")

    def edit_variables_data1(self, data: str, main_variables: dict = {}, side_variables: dict = {}):
        """
        The function rewrites the right variables and process if statements in the given code.
        :param data: The given code
        :param main_variables: The variables for the function to edit
        :param side_variables: The side part of variables to use
        :type data: str
        :type main_variables: dict
        :type side_variables: dict
        :return: The new processed code
        :rtype: str
        """

        if self.binary_encoded:
            data = data.decode()
        new_data = data

        # if statement checker
        for x in self.__syntax:
            while IFS.get(x).get("if")[0] in new_data:
                ifs = IFS.get(x).get("if")
                ifp = new_data.find(IFS.get(x).get("if")[0])
                num_chk = new_data[ifp - self.__max_c - 1: ifp]
                if num_chk[:self.__max_c].isdigit() and num_chk[-1] == ":":
                    worked = False
                    last_start = None
                    els_work = False
                    for k, v in IFS.get(x).items():
                        if k == "if":
                            if ifp - len(num_chk) >= 0:
                                ifp_cls = ifp + len(ifs[0]) + new_data[ifp + len(ifs[0]):].find(ifs[1])
                                # print("cls:", ifp_cls)
                                if ifp_cls != -1:
                                    new_str = "".join(new_data[ifp + len(ifs[0]): ifp_cls].split())
                                    if main_variables.get(new_str):
                                        worked = True
                                        new_data = new_data.replace(num_chk + new_data[ifp: ifp_cls + len(ifs[1])], "")
                                    else:
                                        last_start = ifp - len(num_chk)
                                else:
                                    raise Exception("Invalid closure of if statement!")
                            else:
                                raise Exception("Invalid numbering of if statements!")
                        elif k == "elif":
                            ifs = v
                            while (num_chk + ifs[0]) in new_data[ifp:]:
                                old_ifp = ifp
                                # print("OLD IFP", new_data[ifp:ifp+40])
                                ifp = new_data[old_ifp:].find(num_chk + ifs[0]) + len(num_chk) + len(new_data[:old_ifp])
                                if ifp - len(num_chk) - len(new_data[:old_ifp]) >= 0:
                                    if worked and last_start is None:
                                        last_start = ifp - len(num_chk)
                                    elif not worked:
                                        # old_ifp -= len(new_data[last_start:ifp - len(num_chk)])
                                        new_data = new_data.replace(new_data[last_start:ifp - len(num_chk)], "")
                                        ifp = new_data[old_ifp - len(num_chk):].find(num_chk + ifs[0]) + old_ifp
                                        if ifp - len(new_data[:old_ifp - len(num_chk)]) >= 0:
                                            ifp_cls = ifp + len(ifs[0]) + new_data[ifp + len(ifs[0]):].find(ifs[1])
                                            # print("DATA:", new_data[ifp:], ifs[1], new_data[ifp:])
                                            if ifp_cls != -1:
                                                new_str = "".join(new_data[ifp + len(ifs[0]): ifp_cls].split())
                                                # print("The new string is:", new_str, " or: ", new_data[ifp + len(ifs): ifp_cls])
                                                if main_variables.get(new_str):
                                                    worked = True
                                                    last_start = None
                                                    new_data = new_data.replace(num_chk + new_data[ifp: ifp_cls + len(ifs[1])], "")
                                                else:
                                                    last_start = ifp - len(num_chk)
                                            else:
                                                raise Exception("Invalid closure of if statement!")
                                        else:
                                            raise Exception("Invalid numbering of elif because of the cutting process!")
                                else:
                                    raise Exception("Invalid numbering of elif statements!")
                        elif k == "else":
                            ifs = v
                            ifp = new_data.find(num_chk + ifs) + len(num_chk)
                            if ifp - len(num_chk) >= 0:
                                if worked and last_start is None:
                                    last_start = ifp - len(num_chk)
                                elif not worked:
                                    els_work = True
                                    new_data = new_data.replace(new_data[last_start: ifp - len(num_chk)], "")
                                    new_data = new_data.replace(num_chk + ifs, "")
                        elif k == "endif":
                            ifs = v
                            ifp = new_data.find(num_chk + ifs) + len(num_chk)
                            if ifp - len(num_chk) >= 0:
                                if not els_work and last_start is not None:
                                    new_data = new_data.replace(new_data[last_start: ifp - len(num_chk)], "")
                                new_data = new_data.replace(num_chk + ifs, "")
                            else:
                                raise Exception("Invalid numbering of else statements!")
                else:
                    raise Exception("Invalid numbering of different if statements!")

        # Variables processor
        for x in self.__syntax:
            start_p, end_p = SYNTAX.get(x)
            if start_p in new_data and end_p in new_data:
                m_start, m_end = 0, 0
                while start_p in new_data[m_start:] and end_p in new_data[m_end:]:
                    old_m_start, old_m_end = m_start, m_end
                    m_start = new_data[old_m_start:].find(start_p) + old_m_start
                    m_end = new_data[old_m_end:].find(end_p) + old_m_end
                    new_str = "".join(new_data[m_start + len(start_p): m_end].split())
                    new_data = new_data.replace(new_data[m_start: m_end + len(end_p)], main_variables.get(new_str, ''))
                    m_start += 1
                    m_end += 1

        # Reading files into the data
        for x in self.__syntax:
            start_p, end_p = ADD_FILE.get(x)
            if start_p in data and end_p in new_data:
                m_start, m_end = 0, 0
                while start_p in new_data[m_start:] and end_p in new_data[m_end:]:
                    old_m_start, old_m_end = m_start, m_end
                    m_start = new_data[old_m_start:].find(start_p) + old_m_start
                    m_end = new_data[old_m_end:].find(end_p) + old_m_end
                    new_str = "".join(new_data[m_start + len(start_p): m_end].split())
                    try:
                        f = open(new_str, "r")
                        in_file_data = self.edit_variables_data1(f.read(), side_variables)
                        new_data = new_data.replace(new_data[m_start: m_end + len(end_p)], in_file_data)
                        f.close()
                    except IOError as e:
                        print("Invalid opening of the file -", new_str, ":", e)
                    m_start += 1
                    m_end += 1

        return new_data

    """def test(self, data: str, variables: dict = {}):
        for x in self.__syntax:
            worked = {}
            last_start = {}
            for k, v in IFS.get(x).items():
                print("Dic:", worked, " YAP ", last_start)
                if k == "if":
                    start_p, end_p = v
                    if start_p in data and end_p in data:
                        for m in re.finditer("(?<={})(.*?)(?={})".format(start_p, end_p), data):
                            num_chk = data[(m.start() - len(start_p)) - 2:(m.start() - len(start_p))]
                            if (m.start() - len(start_p)) - 2 >= 0 and num_chk[0].isdigit() and num_chk[1] == ":":
                                worked[num_chk[0]] = [False, False]
                                new_str = "".join(m.string[m.start():m.end()].split())
                                if variables.get(new_str):
                                    worked[num_chk[0]][0] = True
                                    new_data = new_data.replace(num_chk + data[m.start() - len(start_p):m.end() + len(end_p)], "")
                                else:
                                    last_start[num_chk[0]] = m.start() - len(start_p)
                            else:
                                raise Exception("Invalid numbering of if statements!")
                elif k == "elif":
                    start_p, end_p = v
                    if start_p in data and end_p in data:
                        for m in re.finditer("(?<={})(.*?)(?={})".format(start_p, end_p), data):
                            num_chk = data[(m.start() - len(start_p)) - 2:(m.start() - len(start_p))]
                            if m.start() - len(start_p) - 2 >= 0 and num_chk[0].isdigit() and num_chk[1] == ":":
                                if worked.get(num_chk[0])[0] and not worked.get(num_chk[0])[1]:
                                    worked[num_chk[0]][1] = True
                                    last_start[num_chk[0]] = m.start() - len(start_p)
                                elif not worked.get(num_chk[0])[0]:
                                    new_data = new_data.replace(num_chk + data[last_start.get(num_chk[0]):m.start() - len(num_chk) - len(start_p)], "")
                                    new_str = "".join(m.string[m.start():m.end()].split())
                                    if variables.get(new_str):
                                        worked[num_chk[0]][0] = True
                                        new_data = new_data.replace(num_chk + data[m.start() - len(start_p):m.end() + len(end_p)], "")
                                    else:
                                        last_start[num_chk[0]] = m.start() - len(start_p)
                            else:
                                raise Exception("Invalid numbering of elif statements!")
                elif k == "else":
                    start_p = v
                    if start_p in data:
                        for m in re.finditer("{}".format(start_p), data):
                            num_chk = data[m.start() - 2:m.start()]
                            if m.start() - 2 >= 0 and num_chk[0].isdigit() and num_chk[1] == ":":
                                if worked.get(num_chk[0])[0] and not worked.get(num_chk[0])[1]:
                                    worked[num_chk[0]][1] = True
                                    last_start[num_chk[0]] = m.start()
                                elif not worked.get(num_chk[0])[0]:
                                    new_data = new_data.replace(num_chk + data[last_start.get(num_chk[0]):m.start() - len(num_chk)], "")
                                    new_data = new_data.replace(num_chk + start_p, "")
                            else:
                                raise Exception("Invalid numbering of else statements!")
                elif k == "endif":
                    start_p = v
                    if start_p in data:
                        for m in re.finditer("{}".format(start_p), data):
                            num_chk = data[m.start() - 2:m.start()]
                            if m.start() - 2 >= 0 and num_chk[0].isdigit() and num_chk[1] == ":":
                                new_data = new_data.replace(num_chk + data[last_start.get(num_chk[0]):m.start()], "")
                                new_data = new_data.replace(num_chk + start_p, "")
                            else:
                                raise Exception("Invalid numbering of endif statements!")"""
