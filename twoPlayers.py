import mylib as m
from datetime import datetime


# κώδικας για παιχνίδι με δύο παίκτες
def scrabble():
    print('\nΑρχή παιχνιδιού\n')
    name1 = input('Όνομα πρώτου παίκτη: ')
    name2 = input('Όνομα δεύτερου παίκτη: ')
    print()

    # παιχνίδι

    m.makeFile()

    sak = m.SakClass()
    player1 = m.Player(name1)
    player2 = m.Player(name2)

    # πρώτος παίζει ο human
    turn = 0

    # αρχικά το σακουλάκι δίνει γράμματα στους παίκτες
    new = sak.randomLetters(7 - len(player1.playerLetters))
    player1.playerLetters += new

    new = sak.randomLetters(7 - len(player2.playerLetters))
    player2.playerLetters += new

    # όσο υπάρχουν ακόμη γράμματα στο σακουλάκι
    while sak.letters > 0:
        # τις ζυγές σειρές παίζει ο player1
        if turn % 2 == 0:
            # αύξηση του turn για την επόμενη επανάληψη
            turn += 1
            # αν ο player1 έχει λιγότερα από 7 γράμματα παίρνει τυχαία όσα του λείπουν από το σακουλάκι
            if len(player1.playerLetters) < 7:
                new = sak.randomLetters(7 - len(player1.playerLetters))
                player1.playerLetters += new
            print('Στο σακουλάκι: ', sak.letters, ' γράμματα - Παίζει ο παίκτης ' + name1 + ': (p for pass, q for quit)')
            print('Διαθέσιμα Γράμματα: ', player1.playerLetters)
            # περιμένει λέξη από τον player1
            answer = input('Λέξη: ')
            # αν η λέξη είναι 'p' τότε επιστρέφει όλα τα γράμματα του παίκτη στο σακουλάκι και είναι η σειρά του player2
            if answer == 'p':
                sak.letters += len(player1.playerLetters)
                for i in player1.playerLetters:
                    # διορθωση error του list index out of range
                    if ord(list(i.keys())[0]) - ord('Α') > 17:
                        sak.lettersList[ord(list(i.keys())[0]) - ord('Α') - 1] += 1
                    else:
                        sak.lettersList[ord(list(i.keys())[0]) - ord('Α')] += 1
                player1.playerLetters = []
                print('--------------------------------------------------------------------------------------------')
                continue
            # αν η λέξη είναι 'q' τότε βγαίνει από την επανάληψη
            elif answer == 'q':
                break
            # διαφορετικά
            else:
                wordOk = True
                # αρχικοποιώ μια κενή λίστα με κάθε γράμμα του παίκτη
                temp = []
                for k in player1.playerLetters:
                    temp.append(list(k.keys())[0])
                # έλεγχος αν η λέξη αποτελείται από γράμματα που όντως διαθέτει ο player1
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
                        # οι πόντοι της λέξης προστίθενται στο σκορ του player1
                        player1.score += scoreLexis
                        # κάθε γράμμα που υπάρχει στη λέξη διαγράφεται απο τα διαθέσιμα γράμματα του player1
                        for i in answer:
                            for x in player1.playerLetters:
                                if i == list(x.keys())[0]:
                                    player1.playerLetters.remove(x)
                                    break
                        print('Αποδεκτή Λέξη - Βαθμοί: ', scoreLexis, ' - Σκορ: ', player1.score)
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
        # τις μονές σειρές παίζει ο player2
        else:
            # αύξηση του turn για την επόμενη επανάληψη
            turn += 1
            # αν ο player2 έχει λιγότερα από 7 γράμματα παίρνει τυχαία όσα του λείπουν από το σακουλάκι
            if len(player2.playerLetters) < 7:
                new = sak.randomLetters(7 - len(player2.playerLetters))
                player2.playerLetters += new
            print('Στο σακουλάκι: ', sak.letters, ' γράμματα - Παίζει ο παίκτης ' + name2 + ': (p for pass, q for quit)')
            print('Διαθέσιμα Γράμματα: ', player2.playerLetters)
            # περιμένει λέξη από τον player2
            answer = input('Λέξη: ')
            # αν η λέξη είναι 'p' τότε επιστρέφει όλα τα γράμματα του παίκτη στο σακουλάκι και είναι η σειρά του player1
            if answer == 'p':
                sak.letters += len(player2.playerLetters)
                for i in player2.playerLetters:
                    # διορθωση error του list index out of range
                    if ord(list(i.keys())[0]) - ord('Α') > 17:
                        sak.lettersList[ord(list(i.keys())[0]) - ord('Α') - 1] += 1
                    else:
                        sak.lettersList[ord(list(i.keys())[0]) - ord('Α')] += 1
                player2.playerLetters = []
                print('--------------------------------------------------------------------------------------------')
                continue
            # αν η λέξη είναι 'q' τότε βγαίνει από την επανάληψη
            elif answer == 'q':
                break
            # διαφορετικά
            else:
                wordOk = True
                # αρχικοποιώ μια κενή λίστα με κάθε γράμμα του παίκτη
                temp = []
                for k in player2.playerLetters:
                    temp.append(list(k.keys())[0])
                # έλεγχος αν η λέξη αποτελείται από γράμματα που όντως διαθέτει ο player2
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
                        # οι πόντοι της λέξης προστίθενται στο σκορ του player2
                        player2.score += scoreLexis
                        # κάθε γράμμα που υπάρχει στη λέξη διαγράφεται απο τα διαθέσιμα γράμματα του player2
                        for i in answer:
                            for x in player2.playerLetters:
                                if i == list(x.keys())[0]:
                                    player2.playerLetters.remove(x)
                                    break
                        print('Αποδεκτή Λέξη - Βαθμοί: ', scoreLexis, ' - Σκορ: ', player2.score)
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

    if player1.score > player2.score:
        winner = name1
    elif player2.score > player1.score:
        winner = name2
    else:
        winner = 'Ισοπαλία'

    scoreFile = open('score.txt', 'a', encoding='utf8')
    scoreFile.write('Παιχνίδι: ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\n')
    scoreFile.write('Νικητής: ' + winner + '\n')
    scoreFile.write('Σκορ παίκτη ' + name1 + ': ' + str(player1.score) + '\n')
    scoreFile.write('Σκορ παίκτη ' + name2 + ': ' + str(player2.score) + '\n')
    scoreFile.write('Συνολικές κινήσεις: ' + str(turn) + '\n')
    scoreFile.write('\n')
    scoreFile.close()

    print('--------------------------------------------------------------------------------------------')
    print('Τέλος παιχνιδιού\n')
    print('Νικητής: ' + winner)
    print('Σκορ παίκτη ' + name1 + ':', player1.score)
    print('Σκορ παίκτη ' + name2 + ':', player2.score)
    print('--------------------------------------------------------------------------------------------')
