var leftBand = document.querySelector('.left-band');
var search = document.querySelector('.search');
var chevronLeft = document.querySelector('.left-band').querySelector('.chevron-left');
var mainPage = document.querySelector('#main-page');

chevronLeft.addEventListener('click', showMain)

document.addEventListener('DOMMouseScroll', showMain, false);

function showMain() {
    animate(leftBand, -leftBand.offsetWidth);
    animate(search, search.parentNode.offsetWidth, fadeIn(mainPage, 20));
}

function fadeIn(element, speed) {
    element.style.display = 'block';
    var speed = speed || 30;
    var num = 0;
    var st = setInterval(function () {
        num++;
        element.style.opacity = num / 100;
        if (num == 100) { clearInterval(st); }
    }, speed);
}

function animate(obj, target, callback) {
    clearInterval(obj.timer);
    obj.timer = setInterval(function () {
        // var step = Math.ceil((target - obj.offsetLeft) / 10);
        var step = (target - obj.offsetLeft) / 10;
        step = step > 0 ? Math.ceil(step) : Math.floor(step);
        if (obj.offsetLeft == target) {
            clearInterval(obj.timer);
            if (callback) {
                callback();
            }
        }
        obj.style.left = obj.offsetLeft + step + 'px';
    }, 15);
}