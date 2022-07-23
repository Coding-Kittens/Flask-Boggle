const guessForm = $(".guessForm");
const startBtn = $("button[name='startBtn']");
const page = $("#page_stuff");
const timer = $("#timer");
const scoreTxt = $("#score");
const msgTxt = $("#msg");

let currentGame = null;

class BoggleGame {
  constructor(score, timeLimit) {
    this.isStartGame = true;
    this.score = score;
    this.timeLimit = timeLimit;
    this.wordsFound = new Set();
  }

  async checkAnswer() {
    let guessVal = $(".guessForm input").val();
    if (guessVal.length > 1) {
      const res = await axios.post(
        "http://127.0.0.1:5000/guess",
        { guess_word: guessVal },
        "application/json;charset=UTF-8"
      );

      switch (res.data.result) {
        case "ok":
          msgTxt.text("Good guess!");
          break;
        case "not-on-board":
          msgTxt.text("That word is not on this board.");
          break;
        case "not-word":
          msgTxt.text("That is not a word!");
          break;
        default:
          break;
      }
      if (!this.wordsFound.has(guessVal)) {
        if (res.data.result == "ok") {
          this.score += guessVal.length;
          this.wordsFound.add(guessVal);
          scoreTxt.text(`Score: ${this.score}`);
        }
      } else {
        msgTxt.text("You already got that word!");
      }
    } else {
      alert("Has to be a word with more than one letter!");
    }
    $(".guessForm input").val("");
  }

  async getScoreInfo() {
    const res = await axios.post(
      "http://127.0.0.1:5000/score",
      { score: this.score },
      "application/json;charset=UTF-8"
    );

    let highScore = res.data.high_score;
    let numOfGames = res.data.game_num;

    this.showScore(numOfGames, highScore);
  }

  showScore(numOfGames, highScore) {
    page.empty();
    if (this.score <= highScore) {
      page.append(`<h2>Your Score is ${this.score}!</h2>`);
      page.append(`<h2>Your High Score is ${highScore}!</h2>`);
    } else {
      page.append(`<h2> New High Score ${this.score}!</h2>`);
    }

    page.append(`<h2>You Have played ${numOfGames} games</h2>`);

    page.append(
      '<a href="/board"><button type="button" name="startBtn">Play Again</button></a>'
    );
  }

  startGameTimer() {
    console.log("timer started");
    let time = this.timeLimit;

    let timmerId = setInterval(function () {
      time--;

      timer.text(`Timer: ${Math.floor(time / 60)}:${(time % 60).toFixed(2)}`);
      if (time <= 0) {
        clearInterval(timmerId);
        if (currentGame.isStartGame) {
          console.log("game over");
          currentGame.isStartGame = false;
          currentGame.getScoreInfo();
        }
      }
    }, 1000);
  }
}

function startNewGame(timeLimit) {
  console.log("start");
  currentGame = new BoggleGame(0, timeLimit);
  if (timeLimit) {
    currentGame.startGameTimer();
  }
}

guessForm.on("submit", async function (evt) {
  evt.preventDefault();
  if (currentGame.isStartGame) {
    currentGame.checkAnswer();
  } else {
    alert("The game is over you can no longer make a guess.");
  }
});

startNewGame(60);
