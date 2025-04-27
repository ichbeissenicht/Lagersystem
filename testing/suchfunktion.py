import lagerLib as lib
import constants

def suchen(uuid):
    if len(uuid) < 15:
        if uuid in lib.storageData and len(lib.readAblagePlatz(uuid)) != 0:
            list = lib.readAblagePlatz(uuid)
            listToString = " ".join(list)
            einzelStrings = listToString.split(" ")
            for uuid in einzelStrings:

                lib.outPutFormatedEingelagert(uuid, 1)
        elif uuid in lib.storageData and len(lib.readAblagePlatz(uuid)) == 0:
            print(3 * "\n" + "Dieses Regal ist leer" + 2 * "\n")
        else:
            print(uuid)
            print(3 * "\n" + "Wie hast du denn das geschafft?" + 2 * "\n")
    elif len(uuid) == 32:

        return uuid
    else:
        print("Fehler")

