function switchcolor(){
    if(!htmlAudioElement.paused){
      return;
    }
    startRecognition();
    mic.style.color = '#FF0000';
  }

