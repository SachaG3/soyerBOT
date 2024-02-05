
class profil:
    def profiles(self, author, id, ctx,z):
        with open('profile.txt', 'r') as f:
            lines = [line.strip('\n') for line in f.readlines()]
            a = 0
            while 0 == 0:
                if a > len(lines):
                    a = "Il te faut un profil fait ^^NP pour en crée un"
                    return a

                elif lines[a] == str(id):
                    q = lines[a + 2]
                    m=int(q)+z
                    if z==1:
                        return q

                    else:
                        with open("profile.txt", "r") as f:
                            lignes = [line.strip('\n') for line in f.readlines()]
                        lignes[a+2] = str(m)
                        with open("profile.txt", "w") as f:
                            f.write('\n'.join(lignes))
                        return

                else:
                    a = a + 4

    def modif(self, author, id, ctx):
        with open('profile.txt', 'a') as f:
            f.write('\n\n')
            f.write(str(id))
            f.write("\n", )
            f.write(str(author))
            f.write('\n0')