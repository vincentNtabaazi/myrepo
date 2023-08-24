// selectors
checkButtonList = document.querySelectorAll(".complete-btn");
listTotal = document.querySelectorAll(".outer-todo-item");
// listeners
if(window.location.href === 'https://web-production-c410.up.railway.app/new_todo/') {
  document.addEventListener('DOMContentLoaded', move())
}
document.addEventListener('DOMContentLoaded', function (e) {
  e.preventDefault
  checkButtonList.forEach(function (item) {
    const parentElement = item.parentElement.parentElement
    parentElement.classList.add('painted')
  });
})

function move() {
  let elem = document.getElementById("myBar2");
  let completed = checkButtonList.length;
  let total = listTotal.length;
  let percentage = completed/total * 100
  if (percentage === NaN){
    percentage = 0;
  } else {
    percentage = percentage;
  }
  var width = 0;
  var id = setInterval(frame, 15);
  function frame() {
    if (width >= 100) {
      clearInterval(id);
    } else {
      width = percentage.toFixed(0);
      elem.style.width = width + '%';
      elem.innerHTML = width + '%'
    }
  }
}



