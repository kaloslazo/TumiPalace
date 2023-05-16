const spinSound = document.getElementById("spin");
function playSpinSound() {
  spinSound.currentTime = 0;
  spinSound.play();
}
playSpinSound();