'use strict'
const demo = document.querySelector('#demo');
const imageUpload = document.getElementById('imageupload');
const dataAttributeEL = document.querySelectorAll(`div[data-type]`);
const displayAll = function () {
    dataAttributeEL.forEach(el => {
        el.classList.remove('hidden')
    })
}


imageUpload.addEventListener('change', (event) => {
    const fileList = event.target.files[0];

    //console.log(URL.createObjectURL(fileList));
    if (fileList) {
        demo.src =URL.createObjectURL(fileList);
    }
    displayAll();

});
  
const prediction = document.querySelector('#result')
dataAttributeEL.forEach(el => {
    if (el.dataset.type !== prediction.innerHTML.trim()) {
        el.classList.add('hidden')
    };
})