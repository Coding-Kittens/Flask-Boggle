from boggle import Boggle
from flask import Flask, request, render_template, redirect, flash, session, jsonify
app=Flask(__name__)

app.config['SECRET_KEY'] = "catsarethebest24321837"
boggle_game = Boggle()


@app.route('/')
def home_page():
    """ Shows the home page """
    return render_template('home_page.html')


@app.route('/board')
def game_page():
    """ Gets the game board and shows it """
    session['game_board'] = boggle_game.make_board()

    return render_template('game_page.html')


@app.route('/guess',methods=["POST"])
def check_word():
    """ Checks if a word is a word and is on the current board"""
    word = request.json['guess_word']
    res = boggle_game.check_valid_word(session['game_board'],word)
    return jsonify(result=res)



@app.route('/score',methods=["POST"])
def score_page():
    """ Adds to the number of games played
     Checks what the high score should be based on what the score is
      and it returns the number of games played and the high score.
     """
    score = request.json['score']

    if session.get('num_of_games'):
        session['num_of_games'] += 1
    else:
        session['num_of_games'] = 1

    high_score = 0
    if session.get('high_score'):
        high_score = session.get('high_score')
        if session['high_score'] < score:
            session['high_score'] = score
    else:
        session['high_score'] = score

    game_num = session.get('num_of_games')


    return jsonify(high_score=high_score,game_num=game_num)
