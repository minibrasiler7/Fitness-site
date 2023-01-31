def note_to_data(note):
    if note == "Je ne souhaite pas donner mon avis":
        return None
    else:
        return len(note)

def is_there_note(note):
    if note !=None:
        return 1
    else:
        return 0

def moyenne(notes):
    number_note = 0
    sum = 0
    for note in notes:
        if note !=None:
            number_note += 1
            sum += note
    return round(sum/number_note,2)

def boolean_reponse(box):
    if box=="y":
        return True
    else:
        return False
