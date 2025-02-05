import model
donnees = [
        ['a', 'b', 'c', 'd', 'e'],
        [1, 2, 3, 4, 5, 6],
        [1, 3, 6],
        [6],
        [(1, 'a', 2), (1, 'a', 4),(2, 'a', 2), (2, 'c', 5), (2, 'd', 5),
         (3, 'b', 2), (3, 'b', 4), (4, 'b', 4), (4, 'c', 5), (4, 'd', 5), (5, 'e', 6)
         ]
    ]
automate = model.Automate()
automate.lire_automate(donnees)
try:
    while True:
        i = input("pour visionner automate taper 1\npour automate  cmpleter taper 2"
                  "\npour determiniser automate taper 3\npour minimiser automate taper 4\npour sortir taper 0 \n")
        if i == "1":
            automate.afficher_automate().render("automate", format='png', view=True)
            ## clear the terminal
            print("\033[H\033[J")
        elif i == "2":
            automate.rendre_complet()
            print("\033[H\033[J")
            print("votre automate a ete complete\n")
            
        elif i == "3":
            automate = automate.rendre_deterministe()
            print("\033[H\033[J")
            print("votre automate a ete determinise\n")
        elif i == "4":
            automate = automate.minimiser()
            print("\033[H\033[J")
            print("votre automate a ete minimise\n")
        elif i == "0":
            print("\033[H\033[J")
            break
        else:
            raise ValueError
except ValueError:
    print("\033[H\033[J")
    print("valeur invalid")
except KeyboardInterrupt:
    print("\033[H\033[J")
    print("oops")
