from flask import Flask, request, Response, render_template, flash
from datetime import datetime
from random import randrange
from collections import OrderedDict
from models import pyChart
import plivo, plivoxml
import sqlite3
import pandas as pd

app = Flask(__name__)
app.secret_key = 'iprompt12345'

oob_response = ["Let's be serious. Give me an answer from the available options...",
                "Pick a choice that is available por favor...",
                "Gimme a legit choice, mi amigo..."]

success_resp = ["Domo arigato! Your answer has been duly noted!",
                "Thank you for your response!",
                "Thank you for casting your answer!"]


@app.route('/in_sms', methods=['GET', 'POST'])
def inbound_sms():
    conn = sqlite3.connect('smsproto.db')
    c = conn.cursor()

    # Sender's phone number
    from_number = request.values.get('From')
    # Receiver's phone number - Plivo number
    to_number = request.values.get('To')
    # The text which was received
    text = request.values.get('Text')

    params = {
        "src": to_number,
        "dst": from_number,
    }
    body = ""

    answer = text.lower()

    # Admin check for polling privileges
    if from_number == '19045215155' and answer == 'open':
        c.execute("UPDATE question_pointer SET question=999 WHERE id=1")
        conn.commit()

        body = "Polling turned on"
    elif from_number == '19045215155' and answer == 'close':
        c.execute("UPDATE question_pointer SET question=0 WHERE id=1")
        conn.commit()

        body = "Polling turned off"
    elif from_number == '19045215155' and answer == 'flush':
        c.execute("DELETE FROM answers")
        conn.commit()

        body = "Poll answers flushed!"
    else:
        # Get the question pointer
        c.execute("SELECT question FROM question_pointer WHERE id=1")
        q = c.fetchone()[0]

        # Check if polling is active
        if q == 0:
            body = "Polling is now closed"
        elif q == 999:
            body = "Please wait while questions load..."
        else:
            # Get the question answer choices
            answers = []
            for row in c.execute("SELECT answer_choice FROM questions_meta WHERE question=?", (q,)):
                answers.append(row[0])

            # Test if answer is in the available choices
            if answer in answers:
                current_time = str(datetime.now())
                c.execute("INSERT INTO answers VALUES (?,?,?,?)", (q, from_number, answer, current_time))
                conn.commit()

                body = success_resp[randrange(len(success_resp))]
            else:
                body = oob_response[randrange(len(oob_response))]

    conn.close()

    # Generate a Message XML with the details of
    # the reply to be sent.
    r = plivoxml.Response()
    r.addMessage(body, **params)
    print r.to_xml()
    return Response(str(r), mimetype='text/xml')


@app.route('/question')
@app.route('/question/<int:question>')
def display_question(question=None):
    conn = sqlite3.connect('smsproto.db')
    c = conn.cursor()

    # Grab polling permission
    c.execute("SELECT question FROM question_pointer WHERE id=1")
    permission = c.fetchone()[0]

    # Grab question list
    q_dict = dict()
    for row in c.execute("SELECT question, prompt from question_text"):
        q_dict[row[0]] = row[1]
    oq_dict = OrderedDict(sorted(q_dict.items()))

    if question:
        if question in q_dict.keys():
            # Grab question prompt
            prompt = q_dict[question]

            if permission == 0:
                conn.close()
                return render_template('showquestion.html', title='Question {}'.format(question), question=question, prompt=prompt, choices=None, q_dict=oq_dict, allow=permission)
            else:
                # Set pointer
                c.execute("UPDATE question_pointer SET question=? WHERE id=1", (question,))
                conn.commit()

                # Grab answer choices
                c.execute("SELECT answer_choice, answer_text FROM questions_meta WHERE question=?", (question,))
                choices = c.fetchall()

                conn.close()
                return render_template('showquestion.html', title='Question {}'.format(question), question=question, prompt=prompt, choices=choices, q_dict=oq_dict, allow=permission)
        else:
            conn.close()
            flash('Question does not exist!', 'alert-info')
            return render_template('showquestion.html', title='Questions', question=None, prompt=None, choices=None, q_dict=oq_dict, allow=permission)

    conn.close()
    return render_template('showquestion.html', title='Questions', question=None, prompt=None, choices=None, q_dict=oq_dict, allow=permission)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='iPrompt')


@app.route('/results')
def results():
    conn = sqlite3.connect('smsproto.db')
    c = conn.cursor()

    # Make sure polling is closed
    c.execute("SELECT question FROM question_pointer WHERE id=1")
    pointer = c.fetchone()[0]

    if pointer != 0:
        conn.close()
        return render_template('results.html', title='Results', respondent_ct=None, score=None, result=None, q_dict=None, poll_open=True)
    else:
        # Get max score possible
        # TODO: Dynamically calculate
        max_score = 9.0

        # Grab question list
        q_dict = dict()
        for row in c.execute("SELECT question, prompt from question_text"):
            q_dict[row[0]] = row[1]
        oq_dict = OrderedDict(sorted(q_dict.items()))

        # Select most recent answers and values by question and phone
        df = pd.read_sql("""SELECT ans.question, p.prompt, ans.phone, meta.answer_text, meta.value, ans.dt
                            FROM answers ans
                            INNER JOIN questions_meta meta
                            ON ans.question = meta.question AND ans.answer = meta.answer_choice
                            INNER JOIN question_text p
                            ON ans.question = p.question
                            GROUP BY p.prompt, ans.phone
                            HAVING ans.dt = max(ans.dt)""", conn)

        respondent_ct = len(df['phone'].unique())  # Get respondent count
        total_score = df['value'].sum()  # Get total score

        charts = {}  # Init charts dictionary
        readiness_score = 0.0  # Init readiness score

        if respondent_ct > 0:
            # Calculate readiness score
            readiness_score = total_score * 1.0 / respondent_ct / max_score

            # Get counts of answers by question
            df_ct = df.groupby(['question', 'answer_text']).size().rename('count').reset_index().set_index('question')
            df_question_ct = df.groupby('question').size().rename('denom').reset_index().set_index('question')
            df_joined = df_ct.merge(df_question_ct, left_index=True, right_index=True)
            df_joined['percent'] = df_joined['count'] / df_joined['denom'] * 100
            df_final = df_joined.drop('denom', 1).reset_index()

            # Create chart objects
            charts = {}
            for q in oq_dict:
                df_query = df_final[df_final['question'] == q]
                if len(df_query.index) > 0:
                    charts[q] = pyChart('column', 'chart{}'.format(q), 'Percent', xLab=[str(ans) for ans in df_query['answer_text']], yLab="%")
                    charts[q].addToSeries('Percent', [value for value in df_query['percent']])
                    charts[q].formatPoint(r'{series.name}: <b>{point.y:.1f}%</b>')
                    charts[q].yAxisMax(100)
                    charts[q] = charts[q].generate()

            conn.close()
            return render_template('results.html', title='Results', respondent_ct=respondent_ct, score=readiness_score, result=charts, q_dict=oq_dict, poll_open=None)
        else:
            conn.close()
            return render_template('results.html', title='Results', respondent_ct=respondent_ct, score=readiness_score, result=charts, q_dict=oq_dict, poll_open=None)


if __name__ == "__main__":
    from waitress import serve
    serve(app, host='0.0.0.0', port=5000)
