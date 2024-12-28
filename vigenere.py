alpha = 'abcdefghijklmnopqrstuvwxyz'
#alpha = 'KRYPTOSABCDEFGHIJLMNQUVWXZ'.lower()

def solve(message, key, encrypt=True, verbose=False):
    solution1 = ''
    i = 0
    for m in range(len(message)):
            if (message[m] == ' '):
                solution1 += ' '
            else:
                solution1 += alpha[(alpha.index(message[m])+alpha.index(key[0][i % len(key[0])]) )% 26] if encrypt else alpha[(alpha.index(message[m])-alpha.index(key[0][i % len(key[0])]) )% 26]
                i += 1
    if len(key) > 1:
        return solve(solution1, key[1:], encrypt=encrypt, verbose=verbose)
    else:
        if verbose:
            print('-------------------------------------')
            print(solution1)
        return solution1



#Exemple:
#On encrypte une phrase random en utilisant la clé d'enchiffrage 'patate'
encrypted = solve('bobo t bad', key=['patate'], encrypt=True, verbose=True)

solve(encrypted, key=['patate'], encrypt=False, verbose=True)
