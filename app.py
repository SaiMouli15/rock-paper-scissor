from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key in production

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'player_score' not in session:
        session['player_score'] = 0
        session['computer_score'] = 0
        session['tie_score'] = 0
        session['game_count'] = 0
        session['last_result'] = ''
        session['last_computer'] = ''
    if request.method == 'POST':
        player_choice = request.form.get('choice')
        if player_choice not in ['1', '2', '3']:
            session['last_result'] = '⚠️ Enter a valid input: Rock, Paper, or Scissors.'
            return redirect(url_for('index'))
        player = int(player_choice)
        computer = random.randint(1, 3)
        session['last_computer'] = computer
        if player == computer:
            session['tie_score'] += 1
            session['last_result'] = "It's a Tie!"
        elif (player == 1 and computer == 3) or \
             (player == 2 and computer == 1) or \
             (player == 3 and computer == 2):
            session['player_score'] += 1
            session['last_result'] = "You win!"
        else:
            session['computer_score'] += 1
            session['last_result'] = "Computer wins!"
        session['game_count'] += 1
        return redirect(url_for('index'))
    return render_template('index.html',
                           player_score=session['player_score'],
                           computer_score=session['computer_score'],
                           tie_score=session['tie_score'],
                           game_count=session['game_count'],
                           last_result=session['last_result'],
                           last_computer=session['last_computer'])

@app.route('/reset')
def reset():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True) 