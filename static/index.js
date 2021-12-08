const audioContext = new AudioContext();
let htmlAudioElement = document.getElementById("audio");
const source = audioContext.createMediaElementSource(htmlAudioElement);
source.connect(audioContext.destination);

let mic = document.getElementsByClassName('mic')[0];

const levelRangeElement = document.getElementById("levelRange");

function resume() {
    audioContext.resume();
}

const canvas = document.getElementById("output");
canvas.width = 400;
canvas.height = 400;
const ctx = canvas.getContext("2d");
let raf
if (raf) {
    cancelAnimationFrame(raf)
}

const numberOfSides = 512
const size = 100
const x = canvas.width / 2
const y = canvas.height / 2
const lineWidth = 10
const lineColor = '#fff'
const audioAmplifier = 100


function draw(buffer) {

    if (buffer === undefined || buffer === null) {
        ctx.arc(x, y, size, 0, 2 * Math.PI);
        ctx.strokeStyle = lineColor
        ctx.lineWidth = lineWidth
        ctx.stroke()

        return
    }

    ctx.beginPath();

    for (var i = 0; i < numberOfSides; i++) {

        const audioValue = buffer[i] * audioAmplifier
        const cos = Math.cos(i * 2 * Math.PI / numberOfSides)
        const sin = Math.sin(i * 2 * Math.PI / numberOfSides)
        const x1 = x + size * cos - audioValue
        const y1 = y + size * sin + (i % 2 === 1 ? audioValue : 0)

        if (i === 0) {
            ctx.moveTo(x1, y1);
        } else {
            ctx.lineTo(x1, y1);
        }
    }

    ctx.closePath()
    ctx.strokeStyle = lineColor
    ctx.lineWidth = lineWidth
    ctx.stroke()
}

(async function () {
    const analyzer = Meyda.createMeydaAnalyzer({
        "audioContext": audioContext,
        "source": source,
        "bufferSize": 512,
        "featureExtractors": ["rms"],
        "callback": features => {
            const buffer = analyzer.get('buffer');
            draw(buffer);
        }
    });
    analyzer.start();

    loop = delta => {
        raf = requestAnimationFrame(loop)

        ctx.fillRect(0, 0, canvas.width, canvas.height);
        const buffer = analyzer.get('buffer')
        draw(buffer)
    };

    raf = requestAnimationFrame(loop)
})();

function reset() {
    mic.style.color = '#0099CC';
    resume();
    console.warn('playing')
    setTimeout(() => { htmlAudioElement.play(); }, 100);
}

var SpeechRecognition = SpeechRecognition || webkitSpeechRecognition
var SpeechGrammarList = SpeechGrammarList || webkitSpeechGrammarList
var SpeechRecognitionEvent = SpeechRecognitionEvent || webkitSpeechRecognitionEvent

var colors = ['aqua', 'azure', 'beige', 'bisque', 'black', 'blue', 'brown', 'chocolate', 'coral', 'crimson', 'cyan', 'fuchsia', 'ghostwhite', 'gold', 'goldenrod', 'gray', 'green', 'indigo', 'ivory', 'khaki', 'lavender', 'lime', 'linen', 'magenta', 'maroon', 'moccasin', 'navy', 'olive', 'orange', 'orchid', 'peru', 'pink', 'plum', 'purple', 'red', 'salmon', 'sienna', 'silver', 'snow', 'tan', 'teal', 'thistle', 'tomato', 'turquoise', 'violet', 'white', 'yellow'];
var grammar = '#JSGF V1.0; grammar colors; public <color> = ' + colors.join(' | ') + ' ;'

var recognition = new SpeechRecognition();
var speechRecognitionList = new SpeechGrammarList();
speechRecognitionList.addFromString(grammar, 1);
recognition.grammars = speechRecognitionList;
recognition.continuous = false;
recognition.lang = 'en-US';
recognition.interimResults = false;
recognition.maxAlternatives = 1;

function startRecognition() {
    recognition.start();
}

recognition.onresult = function (event) {
    var req = new XMLHttpRequest();
    var speech = event.results[0][0].transcript;
    req.open('POST', "upload_static_file", true);
    req.setRequestHeader('content-type', 'application/x-www-form-urlencoded;charset=UTF-8');
    req.send("name=" + speech);
    //return xmlHttp.responseText;
    /*if(speech == 'where is my spoon' || speech == "where's my spoon"){
      htmlAudioElement.src = './spoon.m4a';
    }
    if(speech == "what's the weather like today"){
      htmlAudioElement.src = './rain.mp3';
      matrix();
    }
    if(speech == 'canedo' || speech == 'Canada'){
      htmlAudioElement.src = './kaneda.m4a';
    }
    if(speech == 'despacito'){
      htmlAudioElement.src = './despacito remix.mp3';
    }
  
    if(speech.includes('wake me up')){
      htmlAudioElement.src = './wakeup.m4a';
    }
    reset();
    setTimeout(() => {htmlAudioElement.src = './despacito.mp3';}, 10000);*/
}

function matrix() {
    body = document.getElementById('body');
    body.classList.add('matrix');
}