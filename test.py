from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle
import json
from unittest.mock import patch


app.config['TESTING'] = True

class FlaskTests(TestCase):
    def test_home(self):
        """ Tests the home page """
        with app.test_client() as client:
            res = client.get('/')
            html = res.get_data(as_text = True)
            self.assertEqual(res.status_code,200)
            self.assertIn("Boggle",html)


    def test_game(self):
        """ Tests that the board shows up properly """
        with app.test_client() as client:
            res = client.get('/board')
            html = res.get_data(as_text = True)
            self.assertEqual(res.status_code,200)
            item_on_board = session['game_board'][0][3]
            self.assertIn(item_on_board,html)



    def test_check_word(self):
        """ tests if you get 'ok' back when there is a word on the board and it is valid """
        with patch('app.session',dict()) as session:
            client = app.test_client()
            session['game_board'] = [['C','A','T','A','A'],
                                     ['A','A','A','A','A'],
                                     ['A','A','A','A','A'],
                                     ['A','A','A','A','A'],
                                     ['A','A','A','A','A']]

            res = client.post('/guess',data = json.dumps({"guess_word": "cat"}), content_type="application/json;charset=UTF-8")
            self.assertEqual(res.json['result'],'ok')



    def test_not_on_board(self):
        """ tests if you get 'not-on-board' back when the word is not on the board and it is valid """
        with patch('app.session',dict()) as session:
            client = app.test_client()
            session['game_board'] = [['C','A','T','A','A'],
                                     ['A','A','A','A','A'],
                                     ['A','A','A','A','A'],
                                     ['A','A','A','A','A'],
                                     ['A','A','A','A','A']]

            res = client.post('/guess',data = json.dumps({"guess_word": "mud"}), content_type="application/json;charset=UTF-8")
            self.assertEqual(res.json['result'],'not-on-board')


    def test_not_a_word(self):
        """ tests if you get 'not-word' back when the word is not valid """
        with patch('app.session',dict()) as session:
            client = app.test_client()
            session['game_board'] = [['C','A','T','A','A'],
                                     ['A','A','A','A','A'],
                                     ['A','A','A','A','A'],
                                     ['A','A','A','A','A'],
                                     ['A','A','A','A','A']]

            res = client.post('/guess',data = json.dumps({"guess_word": "wasd"}), content_type="application/json;charset=UTF-8")
            self.assertEqual(res.json['result'],'not-word')



    def test_score(self):
        """ tests if you get the right high_score and number of games back"""
        with patch('app.session',dict()) as session:
            client = app.test_client()
            session['high_score'] = 3
            session['num_of_games'] = 4
            res = client.post('/score',data = json.dumps({"score": 5}),content_type="application/json;charset=UTF-8")
            self.assertEqual(session['high_score'],5)
            self.assertEqual(session['num_of_games'],5)
            self.assertEqual(res.json['high_score'],3)
            self.assertEqual(res.json['game_num'],5)
