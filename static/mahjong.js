function getCardImages() {
    let images = {
        "BACK": new Image(),
        "DONG": new Image(),
        "NAN": new Image(),
        "XI": new Image(),
        "BEI": new Image(),
        "BAN": new Image(),
        "FACAI": new Image(),
        "ZHONG": new Image(),
    };
    
    images["BACK"].src = "/static/images/MJhide.svg";
    images["DONG"].src = "/static/images/MJf1-.svg";
    images["NAN"].src = "/static/images/MJf2-.svg";
    images["XI"].src = "/static/images/MJf3-.svg";
    images["BEI"].src = "/static/images/MJf4-.svg";
    images["BAN"].src = "/static/images/MJd3-.svg";
    images["FACAI"].src = "/static/images/MJd2-.svg";
    images["ZHONG"].src = "/static/images/MJd1-.svg";
    

    for (let i = 1; i <= 9; i++) {
        images["TONG" + i] = new Image();
        images["TIAO" + i] = new Image();
        images["WAN" + i] = new Image();

        images["TONG" + i].src = "/static/images/MJt" + i + "-.svg";
        images["TIAO" + i].src = "/static/images/MJs" + i + "-.svg";
        images["WAN" + i].src = "/static/images/MJw" + i + "-.svg";
    }

    return images;
}

function initMahjong() {
    let canvas = document.getElementById('gameCanvas');

    if (canvas.getContext) {
        let ctx = canvas.getContext('2d');
        let images = getCardImages();
        
        let interval = setInterval(function() {
            let i = 0;
            for (const card in images) {
                ctx.drawImage(images[card], 112 * (i % 8), 150 * Math.floor(i / 8), 124, 150);
                i++;
            }
        }, 2000);

    }
}