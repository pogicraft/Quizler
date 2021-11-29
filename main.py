import html
import urllib.request as urq
import json
import requests
import PySimpleGUI as sg
from PIL import Image, ImageTk


def run_image(directory):
    i = Image.open(directory)
    return ImageTk.PhotoImage(i)


def disp_question(current_question, offset):
    c_frame.delete('all')
    question_number = offset + 1
    t_string = f"Q{question_number}. {current_question['question']}"
    c_frame.create_text(40, 40, text=t_string, anchor='nw', font=('Book Antiqua', 24, 'normal'), width=900)
    if current_question['status'] == 1:
        c_frame.create_image(40, 20, image=i_correct, anchor='nw')
    elif current_question['status'] == 2:
        c_frame.create_image(40, 20, image=i_wrong, anchor='nw')

q_list = []
total_questions = 10
answered_questions = 0
correct_answers = 0
request_token = 'https://opentdb.com/api_token.php?command=request'
url = f"https://opentdb.com/api.php?amount={total_questions}&type=boolean"
request = urq.Request(url)
response = urq.urlopen(request).read()

data = json.loads(response)['results']
question_bank = []
offset = 0
for question in data:
    new_question = {'question': html.unescape(question['question']), 'answer': question['correct_answer'], 'offset': offset, 'status': 0}
    question_bank.append(new_question)
    offset += 1

FONT_TITLE = ('Franklin Gothic', 24, 'bold')
FONT_MAIN = ('Arial', 8, 'normal')
layout = [
    [sg.Frame("", [[sg.Canvas(size=(1000, 340), k='-display-')],
                   [sg.Button(image_filename="./images/false.png", k='b_false'), sg.Text("              "),
                    sg.Button(image_filename="./images/true.png", k='b_true')]], expand_x=True, expand_y=True,
              element_justification='c')],
    [sg.Text(f"Currently {correct_answers} correct out of {answered_questions} questions answered", background_color='#375362', font=FONT_MAIN, k='-score-')],
    [sg.Button("<       ", k='-prev-', expand_x=True, font=FONT_TITLE),
     sg.Text("          ", background_color='#375362'),
     sg.Button("       >", k='-next-', expand_x=True, font=FONT_TITLE)],
    [sg.Text("                  Images courtesy of SeekPng.com and PinClipart.com", expand_x=True,
             background_color='#375362', font=FONT_MAIN), sg.Button("Exit")]
]
window = sg.Window("", layout=layout, element_justification='center', finalize=True, size=(1200, 780),
                   background_color='#375362', margins=(20, 20))
c_frame = window['-display-'].tk_canvas
i_correct = run_image('./images/correct.png')
i_wrong = run_image('./images/wrong.png')
offset = 0
disp_question(question_bank[offset], offset)
while True:
    event, values = window.read()
    print(event, values)
    if event == sg.WINDOW_CLOSED or event == 'Exit':
        break
    if event == '-next-':
        if offset < len(question_bank) - 1:
            offset += 1
            disp_question(question_bank[offset], offset)
    if event == '-prev-':
        if offset > 0:
            offset -= 1
            disp_question(question_bank[offset], offset)
    if question_bank[offset]['status'] == 0:
        if event == 'b_true':
            if question_bank[offset]['answer'] == 'True':
                question_bank[offset]['status'] = 1
                correct_answers += 1
            else:
                question_bank[offset]['status'] = 2
            answered_questions += 1
            disp_question(question_bank[offset], offset)
            window['-score-'].update(value=f"Currently {correct_answers} correct out of {answered_questions} questions answered")
            if answered_questions == total_questions:
                sg.Popup(f"Game Over.\nCongratulations! You got {correct_answers} correct out of {answered_questions} questions answered.")
        if event == 'b_false':
            if question_bank[offset]['answer'] == 'False':
                question_bank[offset]['status'] = 1
                correct_answers += 1
            else:
                question_bank[offset]['status'] = 2
            answered_questions += 1
            disp_question(question_bank[offset], offset)
            window['-score-'].update(value=f"Currently {correct_answers} correct out of {answered_questions} questions answered")
            if answered_questions == total_questions:
                sg.Popup(f"Game Over.\nCongratulations! You got {correct_answers} correct out of {answered_questions} questions answered.")
window.close()
