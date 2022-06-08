var canvas = document.getElementById('Canvas');
var context = canvas.getContext("2d");

pointMap = new Map();

var mapSprite = new Image();
mapSprite.src = "../static/SeeroseSample.JPG";
points=["Left Acetabular", "Left Femoral Head", "Right Femoral Head", "Right Acetabular"]

var unsetPoints = function () {
    let pointsUnused = [];
    for (var i = 0; i<points.length; i++) {
        if(!pointMap.has(points[i])){
            pointsUnused.push(points[i])
        }
    }
    return pointsUnused;
}

function drawLines() {
    context.strokeStyle = 'red';
    context.lineWidth = 2;

    let leftAcetabular = pointMap.get("Left Acetabular");
    let leftFemoral = pointMap.get("Left Femoral Head");
    let rightFemoral = pointMap.get("Right Femoral Head");
    let rightAcetabular = pointMap.get("Right Acetabular");

    context.beginPath();
    context.moveTo(leftAcetabular.XPos, leftAcetabular.YPos);
    context.lineTo(leftFemoral.XPos, leftFemoral.YPos);
    context.stroke();

    context.beginPath();
    context.moveTo(leftFemoral.XPos, leftFemoral.YPos);
    context.lineTo(rightFemoral.XPos, rightFemoral.YPos);
    context.stroke();

    context.beginPath();
    context.moveTo(rightFemoral.XPos, rightFemoral.YPos);
    context.lineTo(rightAcetabular.XPos, rightAcetabular.YPos);
    context.stroke();
}

function drawArcs() {
    let leftAcetabular = pointMap.get("Left Acetabular");
    let leftFemoral = pointMap.get("Left Femoral Head");
    let rightFemoral = pointMap.get("Right Femoral Head");
    let rightAcetabular = pointMap.get("Right Acetabular");
    var angle1=calculateAngle(pointMap.get("Left Femoral Head"), pointMap.get("Left Acetabular"), pointMap.get("Right Femoral Head"))
    var angle2=calculateAngle(pointMap.get("Right Femoral Head"), pointMap.get("Right Acetabular"), pointMap.get("Left Femoral Head"))

    context.beginPath();

    let distX= Math.abs(leftFemoral.XPos-leftAcetabular.XPos)
    let distY= Math.abs(leftFemoral.YPos-leftAcetabular.YPos)
    let xStart= leftFemoral.XPos-distX/2
    let yStart= leftFemoral.YPos-distY/2
    let startAngle=0;
    context.arc(xStart, yStart, 10, startAngle, angle1, false);
    context.stroke()
    context.beginPath();

    distX= Math.abs(rightFemoral.XPos-rightAcetabular.XPos)
    distY= Math.abs(rightFemoral.YPos-rightAcetabular.YPos)
    xStart= rightFemoral.XPos+distX/2
    yStart= rightFemoral.YPos+distY/2
    startAngle=0;
    context.arc(xStart, yStart, 10, startAngle, angle2, false);
    context.stroke()

}

var calculateAll = function (){
    let pointsLeftToSet = unsetPoints();
    if(pointsLeftToSet.length!==0){
        let message="Cannot calculate angles, points left unset:"
        for (i=0; i<pointsLeftToSet.length;i++){
            message+=pointsLeftToSet[i]+", ";
        }
        message = message.substr(0, message.length-2);
        document.getElementById("missing-points").innerHTML=message;
    } else {
        //drawLines();
        document.getElementById("missing-points").innerHTML="";
        var angle1=calculateAngle(pointMap.get("Left Femoral Head"), pointMap.get("Left Acetabular"), pointMap.get("Right Femoral Head"))
        var angle2=calculateAngle(pointMap.get("Right Femoral Head"), pointMap.get("Left Femoral Head"), pointMap.get("Right Acetabular"))
        //drawArcs()
        document.getElementById("Angle Left").innerHTML="Norberg angle for left hip is "+convertRadiansToDegrees(angle1) +" degrees";
        document.getElementById("Angle Right").innerHTML="Norberg angle for right hip is "+convertRadiansToDegrees(angle2) + " degrees";


    }
}

var Marker = function () {
    this.Sprite = new Image();
    this.Sprite.src = "../static/marker.png"
    this.Width = 12;
    this.Height = 20;
    this.XPos = 0;
    this.YPos = 0;
}

var mouseClicked = function (mouse) {
    // Get corrent mouse coords
    var rect = canvas.getBoundingClientRect();
    var mouseXPos = (mouse.x - rect.left);
    var mouseYPos = (mouse.y - rect.top);


    let currentMarker = document.querySelector('input[name="Current Marker"]:checked').value;
    var marker = new Marker();
    marker.XPos = mouseXPos
    marker.YPos = mouseYPos
    pointMap.set(currentMarker, marker);
}

canvas.addEventListener("mousedown", mouseClicked, false);

var firstLoad = function () {
    context.font = "15px Georgia";
    context.textAlign = "center";
}

firstLoad();

var main = function () {
    draw();
    if(unsetPoints().length===0){
        drawLines()
        drawArcs();
    }
};

var draw = function () {
    context.fillStyle = "#000";
    context.fillRect(0, 0, canvas.width, canvas.height);

    context.drawImage(mapSprite, 0, 0, 756, 755);

    for(let tempMarker of pointMap.values()){

        context.drawImage(tempMarker.Sprite, tempMarker.XPos-6, tempMarker.YPos-20, tempMarker.Width, tempMarker.Height);

        context.fillStyle = "#666";
        context.globalAlpha = 0.7;
        context.globalAlpha = 1;

        context.fillStyle = "#000";
    }
};

setInterval(main, (1000 / 60)); // Refresh 60 times a second

var calculateAngle = function (p1,p2,p3) {
    aX=p1.XPos-p2.XPos;
    aY=p1.YPos-p2.YPos;
    modA=Math.sqrt(aX*aX+aY*aY)

    bX=p1.XPos-p3.XPos;
    bY=p1.YPos-p3.YPos;
    modB=Math.sqrt(bX*bX+bY*bY)

    ratio=(aX*bX+aY*bY)/(modA*modB);

    angle=Math.acos(ratio);
    return angle;
}

var convertRadiansToDegrees = function (radians) {
    return 180/Math.PI *radians
}