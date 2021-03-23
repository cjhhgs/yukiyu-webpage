var leftBand = document.querySelector('.left-band');
var search = document.querySelector('.search');
var chevronLeft = document.querySelector('.left-band').querySelector('.chevron-left');
var mainPage = document.querySelector('#main-page');

chevronLeft.addEventListener('click', function () {
    animate(leftBand, -leftBand.offsetWidth);
    animate(search, search.parentNode.offsetWidth, showMain);
})

function showMain(){
    mainPage.style.display = 'block';
}

function animate(obj, target, callback) {
    clearInterval(obj.timer);
    obj.timer = setInterval(function () {
        // var step = Math.ceil((target - obj.offsetLeft) / 10);
        var step = (target - obj.offsetLeft) / 10;
        step = step > 0 ? Math.ceil(step):Math.floor(step);
        if (obj.offsetLeft == target) {
            clearInterval(obj.timer);
            if(callback){
                callback();
            }
        }
        obj.style.left = obj.offsetLeft + step + 'px';
    }, 15);
}