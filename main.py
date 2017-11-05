import mylib as m
import twoPlayers as two
from datetime import datetime


# αρχικοποιήσεις για το πιο απλό παιχνίδι
pcAlgorithm = 'min'
choice = ''
game = 'default'


while choice != 'q':
    # βασικό μενού
    print('***************************************** SCRABBLE *****************************************')
    print('--------------------------------------------------------------------------------------------')
    print('1: Σκορ')
    print('2: Ρυθμίσεις')
    print('3: Παιχνίδι')
    print('q: Έξοδος')
    choice = input('Πληκτρολογήστε επιλογή (1/ 2/ 3/ q): ')

    if choice == '1':
        print()
        try:
            with open('score.txt', 'r') as score:
                print(score.read())
        except FileNotFoundError:
            print('Δεν υπάρχουν παλαιότερα παιχνίδια\n')
    elif choice == '2':
        print('\n1: Επίπεδο Η/Υ')
        print('2: Επιλογή παικτών')
        setting = input('Πληκτρολογήστε επιλογή (1/ 2): ')
        if setting == '1':
            print('\n1: χαμηλό')
            print('2: μέτριο')
            print('3: υψηλό')
            level = input('Πληκτρολογήστε επιλογή (1/ 2/ 3): ')
            print()
            if level == '2':
                pcAlgorithm = 'max'
            elif level == '1':
                pcAlgorithm = 'min'
            elif level == '3':
                pcAlgorithm = 'smart'
        elif setting == '2':
            print('\n1: Παίκτης εναντίον Η/Υ')
            print('2: Παίκτης εναντίον παίκτη')
            players = input('Πληκτρολογήστε επιλογή (1/ 2): ')
            print()
            if players == '2':
                game = '2players'
            elif players == '1':
                game = 'default'
    elif choice == '3':
        if game == 'default':
            print('\nΑρχή παιχνιδιού\n')
            name = input('Όνομα παίκτη: ')
            # παιχνίδι

            m.makeFile()

            sak = m.SakClass()
            human = m.Player(name)
            pc = m.PcPlayer()

            # πρώτος παίζει ο human
            turn = 0

            # αρχικά το σακουλάκι δίνει γράμματα στους παίκτες
            new = sak.randomLetters(7 - len(human.playerLetters))
            human.playerLetters += new

            new = sak.randomLetters(7 - len(pc.playerLetters))
            pc.playerLetters += new

            # όσο υπάρχουν ακόμη γράμματα στο σακουλάκι
            while sak.letters > 0:
                # τις ζυγές σειρές παίζει ο human
                if turn % 2 == 0:
                    # αύξηση του turn για την επόμενη επανάληψη
                    turn += 1
                    # αν ο human έχει λιγότερα από 7 γράμματα παίρνει τυχαία όσα του λείπουν από το σακουλάκι
                    if len(human.playerLetters) < 7:
                        new = sak.randomLetters(7 - len(human.playerLetters))
                        human.playerLetters += new
                    print('Στο σακουλάκι: ', sak.letters, ' γράμματα - Παίζεις: (p for pass, q for quit)')
                    print('Διαθέσιμα Γράμματα: ', human.playerLetters)
                    # περιμένει λέξη από τον human
                    answer = input('Λέξη: ')
                    # αν η λέξη είναι 'p' τότε επιστρέφει όλα τα γράμματα του παίκτη στο σακουλάκι και είναι η σειρά του pc
                    if answer == 'p':
                        sak.letters += len(human.playerLetters)
                        for i in human.playerLetters:
                            # διορθωση error του list index out of range
                            if ord(list(i.keys())[0]) - ord('Α') > 17:
                                sak.lettersList[ord(list(i.keys())[0]) - ord('Α') - 1] += 1
                            else:
                                sak.lettersList[ord(list(i.keys())[0]) - ord('Α')] += 1
                        human.playerLetters = []
                        print(
                            '--------------------------------------------------------------------------------------------')
                        continue
                    # αν η λέξη είναι 'q' τότε βγαίνει από την επανάληψη
                    elif answer == 'q':
                        break
                    # διαφορετικά
                    else:
                        wordOk = True
                        # αρχικοποιώ μια κενή λίστα με κάθε γράμμα του παίκτη
                        temp = []
                        for k in human.playerLetters:
                            temp.append(list(k.keys())[0])
                        # έλεγχος αν η λέξη αποτελείται από γράμματα που όντως διαθέτει ο human
                        # χρήση temp, ώστε να μην επηρεαστεί η λίστα του παίκτη από διαγραφές
                        for i in answer:
                            exists = False
                            for j in temp:
                                if i == j:
                                    temp.remove(j)
                                    exists = True
                                    break
                            wordOk = wordOk and exists
                        # αν η λέξη πέρασε τον πρώτο έλεγχο, ελέγχεται αν ανήκει στις αποδεκτές λέξεις του λεξικού
                        if wordOk:
                            # αν η λέξη περιέχεται στο λεξικό
                            if answer in m.lexiko:
                                # οι πόντοι της λέξης είναι η τιμή value στο λεξικό
                                scoreLexis = m.lexiko.get(answer)
                                # οι πόντοι της λέξης προστίθενται στο σκορ του human
                                human.score += scoreLexis
                                # κάθε γράμμα που υπάρχει στη λέξη διαγράφεται απο τα διαθέσιμα γράμματα του human
                                for i in answer:
                                    for x in human.playerLetters:
                                        if i == list(x.keys())[0]:
                                            human.playerLetters.remove(x)
                                            break
                                print('Αποδεκτή Λέξη - Βαθμοί: ', scoreLexis, ' - Σκορ: ', human.score)
                                input('Enter για Συνέχεια')
                                print(
                                    '--------------------------------------------------------------------------------------------')
                            else:
                                turn -= 1
                                print('Πληκτρολόγησε λέξη που ανήκει στις αποδεκτές λέξεις του λεξικού')
                                continue
                        else:
                            turn -= 1
                            print('Πληκτρολόγησε λέξη που αποτελείται από τα διαθέσιμα γράμματα')
                            continue
                # τις μονές σειρές παίζει ο pc
                else:
                    # αύξηση του turn για την επόμενη επανάληψη
                    turn += 1
                    # αν ο pc έχει λιγότερα από 7 γράμματα παίρνει τυχαία όσα του λείπουν από το σακουλάκι
                    if len(pc.playerLetters) < 7:
                        new = sak.randomLetters(7 - len(pc.playerLetters))
                        pc.playerLetters += new
                    print('Στο σακουλάκι: ', sak.letters, ' γράμματα - Παίζει o H/Y:')
                    # temp
                    print('Διαθέσιμα Γράμματα: ', pc.playerLetters)
                    # ελεγχος επιπεδου αλγοριθμου
                    if pcAlgorithm == 'max':
                        answer = pc.maxLetters()
                    elif pcAlgorithm == 'smart':
                        answer = pc.smart()
                    else:
                        answer = pc.minLetters()
                    # αν ο pc δεν μπορεί να βρει λέξη με τα διαθέσιμα γράμματα, το παιχνίδι τελειώνει
                    if answer == 'q':
                        break
                    else:
                        # οι πόντοι της λέξης είναι η τιμή value στο λεξικό
                        scoreLexis = m.lexiko.get(answer)
                        # οι πόντοι της λέξης προστίθενται στο σκορ του pc
                        pc.score += scoreLexis
                        # κάθε γράμμα που υπάρχει στη λέξη διαγράφεται απο τα διαθέσιμα γράμματα του pc
                        for i in answer:
                            for j in pc.playerLetters:
                                if i == list(j.keys())[0]:
                                    pc.playerLetters.remove(j)
                        print('Λέξη Η/Υ: ', answer, ' Βαθμοί: ', scoreLexis, ' - Σκορ Η/Υ: ', pc.score)
                        print(
                            '--------------------------------------------------------------------------------------------')

            if human.score >= pc.score:
                winner = name
            else:
                winner = 'Η/Υ'

            scoreFile = open('score.txt', 'a', encoding='utf8')
            scoreFile.write('Παιχνίδι: ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\n')
            scoreFile.write('Νικητής: ' + winner + '\n')
            scoreFile.write('Σκορ Παίκτη: ' + str(human.score) + '\n')
            scoreFile.write('Σκορ Η/Υ: ' + str(pc.score) + '\n')
            scoreFile.write('Συνολικές κινήσεις: ' + str(turn) + '\n')
            scoreFile.write('\n')
            scoreFile.close()

            print('--------------------------------------------------------------------------------------------')
            print('Τέλος παιχνιδιού\n')
            print('Νικητής: ' + winner)
            print('Σκορ Παίκτη: ', human.score)
            print('Σκορ Η/Υ: ', pc.score)
            print('--------------------------------------------------------------------------------------------')
        elif game == '2players':
            two.scrabble()
