def note_to_data(note):
    if note == "Je ne souhaite pas donner mon avis":
        return None
    else:
        for i in range(len(note)):
            print(note[i])
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

def update_moyenne(old_note, new_note):

    for (key, item) in new_note.items():
        if item != None:
            if old_note[key][0] !=None:
                old_note[key][0] = round((old_note[key][0]*old_note[key][1]+new_note[key])/(old_note[key][1]+1),2)
                old_note[key][1] += 1
            else:
                old_note[key][0] = new_note[key]
                old_note[key][1] += 1

    return old_note


