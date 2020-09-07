// Dict of image objects
const HEIGHT = 124;
const WEIDTH = 150;

class Mahjong {
    constructor(sendMessage) {             
        // Callback for sending message
        this.sendMessage = sendMessage;
        
        this.p = new p5(this.getDraw());
    }

    processMessage(data) {
        console.log(data);
    }

    // Code to draw on canvas
    getDraw() {
        return (p) => {   
            let images;

            let getCardImages = function () {
                let ret = {};
            
                ret["BACK"] = p.loadImage("/static/images/MJhide.svg");
                ret["DONG"] = p.loadImage("/static/images/MJf1-.svg");
                ret["NAN"] = p.loadImage("/static/images/MJf2-.svg");
                ret["XI"] = p.loadImage("/static/images/MJf3-.svg");
                ret["BEI"] = p.loadImage("/static/images/MJf4-.svg");
                ret["BAN"] = p.loadImage("/static/images/MJd3-.svg");
                ret["FACAI"] = p.loadImage("/static/images/MJd2-.svg");
                ret["ZHONG"] = p.loadImage("/static/images/MJd1-.svg");
                
            
                for (let i = 1; i <= 9; i++) {
                    ret["TONG" + i] = new Image();
                    ret["TIAO" + i] = new Image();
                    ret["WAN" + i] = new Image();
            
                    ret["TONG" + i] = p.loadImage("/static/images/MJt" + i + "-.svg");
                    ret["TIAO" + i] = p.loadImage("/static/images/MJs" + i + "-.svg");
                    ret["WAN" + i] = p.loadImage("/static/images/MJw" + i + "-.svg");
                }
            
                return ret;
            }
            
            p.preload = function () {
                images = getCardImages();
            }
            
            p.setup = function() {
                let canvas = p.createCanvas(800, 800);
                canvas.parent('game');     
                let i = 0;
                for (const card in images) {
                    p.image(images[card], 112 * (i % 8), 150 * Math.floor(i / 8), 124, 150);
                    i++;
                }
            }
            
            p.mouseClicked = () => {
                this.sendMessage({
                    "x": p.mouseX,
                    "y": p.mouseY 
                });
            }
        }

    }

}

