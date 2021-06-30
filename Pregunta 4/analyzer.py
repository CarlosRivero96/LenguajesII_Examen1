# GLOBAL VARIABLES
import sys

terminals = set("$")
nodes = {}
rules = {}
prec = {}
f = {}
g = {}
init = ''
op = {
    ">": "mayor",
    "<": "menor",
    "=": "igual"
}
wordMaxSize = 0

def checkValidRule(act):
    for i in range(len(act)-1):
        if ((act[i].isupper() and act[i+1].isupper()) or not act[i].isascii() or len(act[i]) > 1 or act[i] == "$" or act[i+1] == "$"):
                return False
    if(len(act) > 0):
        if(len(act[-1]) > 1 or not act[-1].isascii()):
            return False
    return True

def checkAllterminals(w):
    for i in w[1:-1]:
        if(i not in terminals or i == "$"):
            return False
    return True

def checkComparables(w):
    for i in range(len(w)-1):
        found = False
        if(w[i] in prec):
            for pr in prec[w[i]]:
                if(pr[1] == w[i+1]):
                    found = True
                    break
            if(not found):
                print("ERROR: " + w[i] + " is not comparable with " + w[i+1])
                return False
        else:
            print("ERROR: " + w[i] + " is not comparable with " + w[i+1])
            return False
    return True

def printAction(stack, w, si, action, rule):
    spaceStackCount = wordMaxSize + 2 - len(stack)
    spaceWCount = wordMaxSize + 2 - len(w)
    print("[" + " ".join(stack) + "]", end="")
    print("  "*spaceStackCount, end="")
    print(" ".join(w[:si]) + "\033[93m.\033[0m" + " ".join(w[si:]), end="")
    print("  "*spaceWCount, end="")
    if (rule != None):
        print(action + ": " + rules[rule] + " -> " + " ".join(rule))
    else:
        print(action)

def parse(w):
    global wordMaxSize
    wordMaxSize = len(w)
    print("\nStack" + "  "*(wordMaxSize) + "Input" + "  "*(wordMaxSize-1) + "Action\n")
    stack = ["$"]
    si = 1
    e = w[si]
    while(True):
        for i in stack:
            if (not i.isupper()):
                p = i
        if(p == "$" and e == "$"):
            if (len(stack) == 2 and stack[1] == init):
                printAction(stack, w, si, "Accept", None)
                return
            elif (''.join(stack[1:]) not in rules):
                printAction(stack, w, si, "Reject", None)
                return
            else:
                rule = ''.join(stack[1:])
                printAction(stack, w, si, "Reduce", rule)
                stack = [stack[0]] + [rules[rule]]
                continue

        if(f[p] <= g[e]):
            printAction(stack, w, si, "Read", None)
            stack.append(e)
            si += 1
            e = w[si]
        else:
            stack_temp = stack.copy()
            rule = ""
            while(stack[-1] not in terminals):
                rule = stack.pop() + rule
            
            x = stack.pop()
            delete = 1
            rule = x + rule
            
            while(stack[-1] not in terminals or f[stack[-1]] >= g[x]):
                rule = stack.pop() + rule
                if(rule[0] in terminals):
                    x = rule[0]
                    delete += 1

            if(rule in rules):
                printAction(stack_temp, w, si, "Reduce", rule)
                stack.append(rules[rule])
                w = w[:si-delete] + w[si:]
                si -= delete
                
            else:
                print(rule)
                printAction(stack_temp, w, si, "Reject", None)
                return


class precNode:

    def __init__(self, name):
        self.names = [name]
        self.children = []
        self.maxPath = -1

    def calcMaxPath(self, visited):
        if self in visited:
            cycle = "/".join(self.names)
            for node in reversed(visited):
                cycle = "/".join(node.names) + ' -> ' + cycle
                if(node.names == self.names):
                    break
            print("ERROR: Cycle present in graph: " + str(cycle))
            sys.exit()

        else:
            if(self.maxPath == -1):
                if self.children:
                    self.maxPath = max([child.calcMaxPath(visited + [self]) for child in self.children]) + 1
                else:
                    self.maxPath = 0
            return self.maxPath


if(len(sys.argv) > 1):
    fil = open(sys.argv[1], "r")

while(True):
    if(len(sys.argv) > 1):
        a = fil.readline()
        if (a == ""):
            sys.argv.pop(1)
    else:
        a = input("Action: ")
    action = a.split()
    if(len(action) < 1):
        print("Please enter a valid action")
    elif(action[0] == "RULE"):
        if(len(action[1]) == 1 and action[1].isupper() and checkValidRule(action[2:])):
            for i in action[2:]:
                if(i.isascii() and not i.isupper): terminals.add(i)

            if(''.join(action[2:]) in rules):
                print("Rule " + action[1] + " -> " + " ".join(action[2:]) + " already exists")
            else:
                rules[''.join(action[2:])] = action[1]
                print("Rule " + action[1] + " -> " + " ".join(action[2:]) + " added to grammar")

        else:
            print("ERROR: \"" + action[1] + " -> " + " ".join(action[2:]) + "\" is not a valid rule")


    elif(action[0] == "INIT"):
        if(len(action) == 2 and len(action[1]) == 1 and action[1].isupper()):
            init = action[1]
            print("\"" + action[1] + "\" is the new initial symbol")
        else:
            print("Error: Not a valid init")


    elif(action[0] == "PREC"):
        if(len(action) == 4 and action[2] in [">", "<", "="] and len(action[1]) == 1 and len(action[3]) == 1 and(action[1].isascii() and not action[1].isupper()) and (action[3].isascii() and not action[3].isupper()) ):
            terminals.add(action[1])
            terminals.add(action[3])
            if(action[1] in prec):
                if(action[2:] in prec[action[1]]):
                    print("Precedence " + " ".join(action[1:]) + " already exists")
                else:
                    prec[action[1]].append(action[2:])
                    print(action[1] + " tiene " + op[action[2]] + " precedencia que " + action[3])
            else:
                prec[action[1]] = []
                prec[action[1]].append(action[2:])
                print(action[1] + " tiene " + op[action[2]] + " precedencia que " + action[3])

        else:
            print("Error: Not a valid precedence")


    elif(action[0] == "BUILD"):
        # Restart nodes
        nodes.clear()

        # Create = nodes
        for key in prec.keys():
            n = precNode("f_" + key)
            nodes["f_" + key] = n
            for pr in prec[key]:
                if(pr[0] == "="):
                    n.names.append("g_" + pr[1])
                    nodes["g_" + pr[1]] = n
        
        # Connect nodes by precedence
        for key in prec.keys():
            n = nodes["f_"+key]
            for pr in prec[key]:
                if(pr[0] == ">"):
                    if(("g_"+pr[1]) in nodes.keys()):
                        n2 = nodes["g_" + pr[1]]
                        n.children.append(n2)
                    else:
                        n2 = precNode("g_" + pr[1])
                        nodes["g_" + pr[1]] = n2
                        n.children.append(n2)
                elif(pr[0] == "<"):
                    if(("g_"+pr[1]) in nodes.keys()):
                        n2 = nodes["g_" + pr[1]]
                        n2.children.append(n)
                    else:
                        n2 = precNode("g_" + pr[1])
                        nodes["g_" + pr[1]] = n2
                        n2.children.append(n)

        for key in terminals:
            if("g_" + key not in nodes.keys()):
                nodes["g_" + key] = precNode("g_" + key)
            if("f_" + key not in nodes.keys()):
                nodes["f_" + key] = precNode("f_" + key)

        for key in terminals:
            f[key] = nodes["f_" + key].calcMaxPath([])
            g[key] = nodes["g_" + key].calcMaxPath([])

        print("Syntax analizer constructed!")
        print("F values:")
        for key in f.keys():
            print("  " + key + ": " + str(f[key]))
        print("G values:")
        for key in g.keys():
            print("  " + key + ": " + str(g[key]))


    elif(action[0] == "PARSE"):
        if(f and g and init != ''):
            w = "$" + "".join(action[1:]) + "$"
            if(checkAllterminals(w)):
                if(checkComparables(w)):
                    parse(w)
                else:
                    print("ERROR: Input terminal symbols not comparable")
            else:
                print("ERROR: Input includes non terminal symbols")
            

        else:
            if(init == ''):
                print("ERROR: No initial symbol")
            elif(not f):
                print("ERROR: Syntax analizer not yet built")

    elif(action[0] == "EXIT"):
        break


    elif(action[0] == "debug"):
        print("rules: " + str(rules))
        print("prec: " + str(prec))
        print("nodes: " + str(nodes.keys()))
        print("terminals: " + str(terminals))
        print("f: " + str(f))
        print("g: " + str(g))

    else:
        print("Please enter a valid action")

